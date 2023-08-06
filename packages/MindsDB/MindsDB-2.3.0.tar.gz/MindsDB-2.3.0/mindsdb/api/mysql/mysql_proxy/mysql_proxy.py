"""
*******************************************************
 * Copyright (C) 2017 MindsDB Inc. <copyright@mindsdb.com>
 *
 * This file is part of MindsDB Server.
 *
 * MindsDB Server can not be copied and/or distributed without the express
 * permission of MindsDB Inc
 *******************************************************
"""


import os
import random
import socketserver as SocketServer
import ssl
import re
import traceback
import json
import atexit
import tempfile
import datetime

import moz_sql_parser as sql_parser

from mindsdb.utilities.wizards import make_ssl_cert

from mindsdb.api.mysql.mysql_proxy.data_types.mysql_packet import Packet
from mindsdb.api.mysql.mysql_proxy.controllers.session_controller import SessionController
from mindsdb.api.mysql.mysql_proxy.controllers.log import init_logger, log
from mindsdb.api.mysql.mysql_proxy.datahub import init_datahub
from mindsdb.api.mysql.mysql_proxy.classes.client_capabilities import ClentCapabilities

from mindsdb.api.mysql.mysql_proxy.classes.sql_query import (
    SQLQuery,
    NotImplementedError,
    SqlError
)

from mindsdb.api.mysql.mysql_proxy.libs.constants.mysql import (
    getConstName,
    CHARSET_NUMBERS,
    ERR,
    COMMANDS,
    TYPES,
    SERVER_VARIABLES,
    DEFAULT_AUTH_METHOD,
    SERVER_STATUS,
    FIELD_FLAG
)

from mindsdb.api.mysql.mysql_proxy.data_types.mysql_packets import (
    ErrPacket,
    HandshakePacket,
    FastAuthFail,
    PasswordAnswer,
    HandshakeResponsePacket,
    OkPacket,
    SwitchOutPacket,
    SwitchOutResponse,
    CommandPacket,
    ColumnCountPacket,
    ColumnDefenitionPacket,
    ResultsetRowPacket,
    EofPacket,
    STMTPrepareHeaderPacket,
    BinaryResultsetRowPacket
)

from mindsdb.interfaces.datastore.datastore import DataStore
from mindsdb.interfaces.native.mindsdb import MindsdbNative


connection_id = 0

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

HARDCODED_USER = None
HARDCODED_PASSWORD = None
CERT_PATH = None
default_store = None
mdb = None
datahub = None
config = None


class MysqlProxy(SocketServer.BaseRequestHandler):
    """
    The Main Server controller class
    """

    charset = 'utf8'

    charset_text_type = CHARSET_NUMBERS['utf8_general_ci']

    session = None

    client_capabilities = None

    @staticmethod
    def server_close(srv):
        srv.server_close()

    def initSession(self):
        global connection_id, ALPHABET
        log.info('New connection [{ip}:{port}]'.format(
            ip=self.client_address[0], port=self.client_address[1]))
        log.debug(self.__dict__)

        connection_id += 1

        self.session = SessionController()
        self.salt = ''.join([random.choice(ALPHABET) for i in range(20)])
        self.socket = self.request
        self.count = 0  # next packet number
        self.connection_id = connection_id
        self.logging = log

        self.current_transaction = None

        log.debug('session salt: {salt}'.format(salt=self.salt))

    def isAuthOk(self, user, orig_user, password, orig_password):
        try:
            if user != orig_user:
                log.warning(f'Check auth, user={user}: user mismatch')
                return False
            if password != orig_password:
                log.warning(f'check auth, user={user}: password mismatch')
                return False

            self.session.username = user
            self.session.auth = True
            log.info(f'Check auth, user={user}: Ok')
            return True
        except Exception:
            log.error(f'Check auth, user={user}: ERROR')
            log.error(traceback.format_exc())

    def handshake(self):
        global HARDCODED_PASSWORD, HARDCODED_USER, CERT_PATH, config

        def switch_auth(method='mysql_native_password'):
            self.packet(SwitchOutPacket, seed=self.salt, method=method).send()
            switch_out_answer = self.packet(SwitchOutResponse)
            switch_out_answer.get()
            password = switch_out_answer.password
            if method == 'mysql_native_password' and len(password) == 0:
                password = handshake_resp.scramble_func('', self.salt)
            return password

        def get_fast_auth_password():
            log.info('Asking for fast auth password')
            self.packet(FastAuthFail).send()
            password_answer = self.packet(PasswordAnswer)
            password_answer.get()
            try:
                password = password_answer.password.value.decode()
            except Exception:
                log.info('error: no password in Fast Auth answer')
                self.packet(ErrPacket, err_code=ERR.ER_PASSWORD_NO_MATCH, msg='Is not password in connection query.').send()
                return None
            return password

        if self.session is None:
            self.initSession()
        log.info('send HandshakePacket')
        self.packet(HandshakePacket).send()

        handshake_resp = self.packet(HandshakeResponsePacket)
        handshake_resp.get()
        if handshake_resp.length == 0:
            log.warning('HandshakeResponsePacket empty')
            self.packet(OkPacket).send()
            return False
        self.client_capabilities = ClentCapabilities(handshake_resp.capabilities.value)

        client_auth_plugin = handshake_resp.client_auth_plugin.value.decode()

        orig_username = HARDCODED_USER
        orig_password = HARDCODED_PASSWORD
        orig_password_hash = handshake_resp.scramble_func(HARDCODED_PASSWORD, self.salt)
        username = None
        password = None

        self.session.is_ssl = False

        if handshake_resp.type == 'SSLRequest':
            log.info('switch to SSL')
            self.session.is_ssl = True

            ssl_socket = ssl.wrap_socket(
                self.socket,
                server_side=True,
                certfile=CERT_PATH,
                do_handshake_on_connect=True
            )

            self.socket = ssl_socket
            handshake_resp = self.packet(HandshakeResponsePacket)
            handshake_resp.get()
            client_auth_plugin = handshake_resp.client_auth_plugin.value.decode()

        username = handshake_resp.username.value.decode()
        # if connect come from 'integration', then username will be like username_dbname
        integration = ''
        prefix = orig_username + '_'
        if username.startswith(prefix):
            integration = username[len(prefix):]
        if len(integration) > 0 and integration in config['integrations']:
            self.session.integration = integration
            username = orig_username

        if client_auth_plugin != DEFAULT_AUTH_METHOD:
            if client_auth_plugin == 'mysql_native_password' and \
                    orig_password == '' and len(handshake_resp.enc_password.value) == 0:
                switch_auth('mysql_native_password')
                password = ''
            else:
                new_method = 'caching_sha2_password' if client_auth_plugin == 'caching_sha2_password' else 'mysql_native_password'

                if new_method == 'caching_sha2_password' and self.session.is_ssl is False:
                    log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                             'error: cant switch to caching_sha2_password without SSL')
                    self.packet(ErrPacket, err_code=ERR.ER_PASSWORD_NO_MATCH, msg='caching_sha2_password without SSL not supported').send()
                    return False

                log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                         f'switch auth method to {new_method}')
                password = switch_auth(new_method)

                if new_method == 'caching_sha2_password':
                    password = get_fast_auth_password()
                else:
                    orig_password = orig_password_hash
        elif orig_username == username and HARDCODED_PASSWORD == '':
            log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                     'empty password')
            password = ''
        elif 'caching_sha2_password' in client_auth_plugin:
            log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                     'check auth using caching_sha2_password')
            password = get_fast_auth_password()
            orig_password = HARDCODED_PASSWORD
        elif 'mysql_native_password' in client_auth_plugin:
            log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                     'check auth using mysql_native_password')
            password = handshake_resp.enc_password.value
            orig_password = orig_password_hash
        else:
            log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                     'unknown method, possible ERROR. Try to switch to mysql_native_password')
            password = switch_auth('mysql_native_password')
            orig_password = orig_password_hash

        try:
            self.session.database = handshake_resp.database.value.decode()
        except Exception:
            self.session.database = None
        log.info(f'Check auth, user={username}, ssl={self.session.is_ssl}, auth_method={client_auth_plugin}: '
                 f'connecting to database {self.session.database}')

        if self.isAuthOk(username, orig_username, password, orig_password):
            self.packet(OkPacket).send()
            return True
        else:
            self.packet(ErrPacket, err_code=ERR.ER_PASSWORD_NO_MATCH, msg=f'Access denied for user {username}').send()
            log.warning('AUTH FAIL')
            return False

    def sendPackageGroup(self, packages):
        string = b''.join([x.accum() for x in packages])
        self.socket.sendall(string)

    def answerVersionComment(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'table_name': '',
                'name': '@@version_comment',
                'type': TYPES.MYSQL_TYPE_VAR_STRING
            }],
            data=[{'@@version_comment': '(MindsDB)'}]
        )
        if self.client_capabilities.DEPRECATE_EOF is True:
            packages.append(self.packet(OkPacket, eof=True))
        else:
            packages.append(self.packet(EofPacket))
        self.sendPackageGroup(packages)

    def answerVersion(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'table_name': '',
                'name': '@@version',
                'type': TYPES.MYSQL_TYPE_VAR_STRING
            }],
            data=[{'@@version': '0.1'}]
        )
        packages.append(self.packet(OkPacket, eof=True))
        self.sendPackageGroup(packages)

    def answerTableQuery(self, query):
        packages = []
        packages += self.getTabelPackets(
            columns=query.columns,
            data=query.result
        )
        packages.append(self.packet(OkPacket, eof=True))
        self.sendPackageGroup(packages)

    def insert_predictor_answer(self, insert):
        global mdb, default_store, config

        is_external_datasource = isinstance(insert.get('external_datasource'), str) and len(insert['external_datasource']) > 0
        is_select_data_query = isinstance(insert.get('select_data_query'), str) and len(insert['select_data_query']) > 0

        if is_external_datasource and is_select_data_query:
            self.packet(
                ErrPacket,
                err_code=ERR.ER_WRONG_ARGUMENTS,
                msg="'external_datasource' and 'select_data_query' should not be used in one query"
            ).send()
            return
        elif is_external_datasource is False and is_select_data_query is False:
            self.packet(
                ErrPacket,
                err_code=ERR.ER_WRONG_ARGUMENTS,
                msg="in query should be 'external_datasource' or 'select_data_query'"
            ).send()
            return

        models = mdb.get_models()
        if insert['name'] in [x['name'] for x in models]:
            self.packet(
                ErrPacket,
                err_code=ERR.ER_WRONG_ARGUMENTS,
                msg=f"predictor with name '{insert['name']}'' already exists"
            ).send()
            return

        kwargs = {}
        if isinstance(insert.get('training_options'), str) \
                and len(insert['training_options']) > 0:
            try:
                kwargs = json.loads(insert['training_options'])
            except Exception:
                self.packet(
                    ErrPacket,
                    err_code=ERR.ER_WRONG_ARGUMENTS,
                    msg='training_options should be in valid JSON string'
                ).send()
                return

        if is_select_data_query:
            integration = self.session.integration
            if isinstance(integration, str) is False or len(integration) == 0:
                self.packet(
                    ErrPacket,
                    err_code=ERR.ER_WRONG_ARGUMENTS,
                    msg='select_data_query can be used only in query from database'
                ).send()
                return
            insert['select_data_query'] = insert['select_data_query'].replace(r"\'", "'")
            ds = default_store.save_datasource(insert['name'], integration, insert['select_data_query'])
        elif is_external_datasource:
            ds = default_store.get_datasource_obj(insert['external_datasource'], raw=True)

        insert['predict'] = [x.strip() for x in insert['predict'].split(',')]

        mdb.learn(insert['name'], ds, insert['predict'], kwargs)

        self.packet(OkPacket).send()

    def delete_predictor_sql(self, sql):
        global datahub

        fake_sql = sql.strip(' ')
        fake_sql = 'select name ' + fake_sql[len('delete '):]
        query = SQLQuery(fake_sql, integration=self.session.integration, database=self.session.database)

        result = query.fetch(datahub)

        if result['success'] is False:
            self.packet(
                ErrPacket,
                err_code=result['error_code'],
                msg=result['msg']
            ).send()
            return

        predictors_names = [x[0] for x in result['result']]

        if len(predictors_names) == 0:
            raise NotImplementedError('nothing to delete')

        for predictor_name in predictors_names:
            datahub['mindsdb'].delete_predictor(predictor_name)

    def handle_custom_command(self, sql):
        insert = SQLQuery.parse_insert(sql)

        if 'command' not in insert:
            self.packet(ErrPacket, err_code=ERR.ER_WRONG_ARGUMENTS, msg="command should be inserted").send()
            return
        if len(insert) > 1:
            self.packet(ErrPacket, err_code=ERR.ER_WRONG_ARGUMENTS, msg="only command should be inserted").send()
            return

        command = insert['command'].strip(' ;').split()

        if command[0].lower() == 'delete' and command[1].lower() == 'predictor':
            if len(command) != 3:
                self.packet(
                    ErrPacket,
                    err_code=ERR.ER_SYNTAX_ERROR,
                    msg="wrong syntax of 'DELETE PREDICTOR {NAME}' command"
                ).send()
                return
            predictor_name = command[2]
            self.delete_predictor_sql(f"delete from mindsdb.predictors where name = '{predictor_name}'")
            self.packet(OkPacket).send()
            return

        self.packet(
            ErrPacket,
            err_code=ERR.ER_SYNTAX_ERROR,
            msg="at this moment only 'delete predictor' command supported"
        ).send()

    def get_binary_resultset(self, columns, row):
        return self.packet(BinaryResultsetRowPacket, data=row, columns=columns)

    def answer_stmt_prepare(self, sql):
        statement_id = self.session.register_statement(sql)
        statement = self.session.statements[statement_id]

        sql_lower = sql.lower()
        if sql_lower.startswith('insert into'):
            insert = SQLQuery.parse_insert(sql)
            statement['type'] = 'insert'
            statement['insert'] = insert

            columns_str = ','.join(list(insert.keys()))
            query = SQLQuery(
                f'select {columns_str} from mindsdb.predictors',
                integration=self.session.integration,
                database=self.session.database
            )
            num_columns = 0
            num_params = len(query.columns)

            columns_def = []
            for col in query.columns:
                columns_def.append(dict(
                    database='',
                    table_alias='',
                    table_name='',
                    alias='',
                    name='?',
                    type=TYPES.MYSQL_TYPE_VAR_STRING,
                    charset=CHARSET_NUMBERS['binary']
                ))
        elif sql_lower.startswith('select') and sql_lower.endswith('for update'):
            # postgres when execute "delete from mindsdb.predictors where name = 'x'" sends for it prepare statement:
            # 'select name from mindsdb.predictors where name = 'x' FOR UPDATE;'
            # and after it send prepare for delete query.
            statement['type'] = 'lock'
            sql = sql[:sql.rfind('FOR UPDATE')]
            statement['prepared_sql'] = sql
            query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)
            num_columns = len(query.columns)
            num_params = 0
            columns_def = query.columns
            for col in columns_def:
                col['charset'] = CHARSET_NUMBERS['utf8_general_ci']

        elif sql_lower.startswith('delete'):
            statement['type'] = 'delete'

            fake_sql = sql.strip(' ')
            fake_sql = fake_sql.replace('?', '"?"')
            fake_sql = 'select name ' + fake_sql[len('delete '):]
            statement['prepared_sql'] = fake_sql
            query = SQLQuery(fake_sql, integration=self.session.integration, database=self.session.database)
            num_columns = 0
            num_params = len(query.columns)
            columns_def = []
            for col in query.columns:
                columns_def.append(dict(
                    database='',
                    table_alias='',
                    table_name='',
                    alias='?',
                    name='',
                    type=TYPES.MYSQL_TYPE_VAR_STRING,
                    charset=CHARSET_NUMBERS['binary'],
                    flags=sum([FIELD_FLAG.BINARY_COLLATION])
                ))
            for col in columns_def:
                col['charset'] = CHARSET_NUMBERS['utf8_general_ci']

        elif sql_lower.startswith('select'):
            statement['type'] = 'select'
            query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)
            num_columns = len(query.columns)
            num_params = 0
            columns_def = query.columns
        else:
            raise SqlError(f"Only 'SELECT' and 'INSERT' statements supported. Got: {sql}")

        packages = [
            self.packet(
                STMTPrepareHeaderPacket,
                statement_id=statement_id,
                num_columns=num_columns,
                num_params=num_params
            )
        ]

        packages.extend(
            self._get_column_defenition_packets(columns_def)
        )

        if self.client_capabilities.DEPRECATE_EOF is False:
            status = sum([SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT])
            packages.append(self.packet(EofPacket, status=status))

        self.sendPackageGroup(packages)

    def answer_stmt_execute(self, statement_id, parameters):
        statement = self.session.statements[statement_id]
        if statement['type'] == 'select':
            sql = statement['sql']
            query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)

            columns = query.columns
            packages = [self.packet(ColumnCountPacket, count=len(columns))]
            packages.extend(self._get_column_defenition_packets(columns))

            if self.client_capabilities.DEPRECATE_EOF is True:
                packages.append(self.packet(OkPacket, eof=True, status=0x0062))
            else:
                packages.append(self.packet(EofPacket, status=0x0062))
            self.sendPackageGroup(packages)
        elif statement['type'] == 'insert':
            insert = statement['insert']
            if len(parameters) != len(insert):
                raise SqlError(f"For INSERT statement got {len(parameters)} parameters, but should be {len(insert)}")

            for i, col in enumerate(insert.keys()):
                insert[col] = parameters[i]

            sql = statement['sql'].lower().replace('`', '')
            if 'commands' in sql or 'mindsdb.commands' in sql:
                sql = sql.replace('?', f"'{insert['command']}'")
                self.handle_custom_command(sql)
            elif 'predictors' in sql or 'mindsdb.predictors' in sql:
                self.insert_predictor_answer(insert)
            else:
                raise NotImplementedError("Only 'insert into predictors' and 'insert into commands' implemented")
        elif statement['type'] == 'lock':
            sql = statement['prepared_sql']
            query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)

            columns = query.columns
            packages = [self.packet(ColumnCountPacket, count=len(columns))]
            packages.extend(self._get_column_defenition_packets(columns))

            status = sum([
                SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT,
                SERVER_STATUS.SERVER_STATUS_CURSOR_EXISTS,
            ])

            if self.client_capabilities.DEPRECATE_EOF is True:
                packages.append(self.packet(OkPacket, eof=True, status=status))
            else:
                packages.append(self.packet(EofPacket, status=status))
            self.sendPackageGroup(packages)
        elif statement['type'] == 'delete':
            if len(parameters) != 1:
                raise SqlError("Delete statement must content 'where' filter")
            self.delete_predictor_sql(statement['sql'].replace('?', f"'{parameters[0]}'"))
            self.packet(OkPacket).send()
        else:
            raise NotImplementedError(f"Unknown statement type: {statement['type']}")

    def answer_stmt_fetch(self, statement_id, limit=100000):
        global datahub
        statement = self.session.statements[statement_id]
        sql = statement.get('prepared_sql', statement['sql'])
        fetched = statement['fetched']
        query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)

        result = query.fetch(datahub)

        if result['success'] is False:
            self.packet(
                ErrPacket,
                err_code=result['error_code'],
                msg=result['msg']
            ).send()
            return

        packages = []
        columns = query.columns
        for row in query.result[fetched:limit]:
            packages.append(self.get_binary_resultset(columns, row))

        statement['fetched'] += len(query.result[fetched:limit])

        if len(query.result) <= limit:
            status = sum([
                SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT,
                SERVER_STATUS.SERVER_STATUS_LAST_ROW_SENT,
            ])
        else:
            status = sum([
                SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT,
                SERVER_STATUS.SERVER_STATUS_CURSOR_EXISTS,
            ])
        packages.append(self.packet(EofPacket, status=status))  # what should be if CLIENT_DEPRECATE_EOF?

        self.sendPackageGroup(packages)

    def answer_stmt_close(self, statement_id):
        self.session.unregister_statement(statement_id)

    def answer_explain_table(self, sql):
        parts = sql.split(' ')
        table = parts[1].lower()
        if table == 'predictors' or table == 'mindsdb.predictors':
            self.answer_explain_predictors()
        elif table == 'commands' or table == 'mindsdb.commands':
            self.answer_explain_commands()
        else:
            raise NotImplementedError("Only 'EXPLAIN predictors' and 'EXPLAIN commands' supported")

    def _get_explain_columns(self):
        return [{
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'COLUMN_NAME',
            'alias': 'Field',
            'type': TYPES.MYSQL_TYPE_VAR_STRING,
            'charset': self.charset_text_type,
            'flags': sum([FIELD_FLAG.NOT_NULL])
        }, {
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'COLUMN_TYPE',
            'alias': 'Type',
            'type': TYPES.MYSQL_TYPE_BLOB,
            'charset': self.charset_text_type,
            'flags': sum([
                FIELD_FLAG.NOT_NULL,
                FIELD_FLAG.BLOB
            ])
        }, {
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'IS_NULLABLE',
            'alias': 'Null',
            'type': TYPES.MYSQL_TYPE_VAR_STRING,
            'charset': self.charset_text_type,
            'flags': sum([FIELD_FLAG.NOT_NULL])
        }, {
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'COLUMN_KEY',
            'alias': 'Key',
            'type': TYPES.MYSQL_TYPE_VAR_STRING,
            'charset': self.charset_text_type,
            'flags': sum([FIELD_FLAG.NOT_NULL])
        }, {
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'COLUMN_DEFAULT',
            'alias': 'Default',
            'type': TYPES.MYSQL_TYPE_BLOB,
            'charset': self.charset_text_type,
            'flags': sum([FIELD_FLAG.BLOB])
        }, {
            'database': 'information_schema',
            'table_name': 'COLUMNS',
            'name': 'EXTRA',
            'alias': 'Extra',
            'type': TYPES.MYSQL_TYPE_VAR_STRING,
            'charset': self.charset_text_type,
            'flags': sum([FIELD_FLAG.NOT_NULL])
        }]

    def answer_explain_predictors(self):
        status = sum([
            SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT,
            SERVER_STATUS.SERVER_QUERY_NO_INDEX_USED,
        ])

        packages = self.getTabelPackets(
            columns=self._get_explain_columns(),
            # [Field, Type, Null, Key, Default, Extra]
            data=[
                ['name', 'varchar(255)', 'NO', 'PRI', None, ''],
                ['status', 'varchar(255)', 'YES', '', None, ''],
                ['accuracy', 'varchar(255)', 'YES', '', None, ''],
                ['predict', 'varchar(255)', 'YES', '', None, ''],
                ['select_data_query', 'varchar(255)', 'YES', '', None, ''],
                ['external_datasource', 'varchar(255)', 'YES', '', None, ''],
                ['training_options', 'varchar(255)', 'YES', '', None, ''],
            ],
            status=status
        )

        if self.client_capabilities.DEPRECATE_EOF is False:
            packages.append(self.packet(EofPacket, status=status))
        else:
            packages.append(self.packet(OkPacket, eof=True, status=status))

        self.sendPackageGroup(packages)

    def answer_explain_commands(self):
        status = sum([
            SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT,
            SERVER_STATUS.SERVER_QUERY_NO_INDEX_USED,
        ])

        packages = self.getTabelPackets(
            columns=self._get_explain_columns(),
            data=[
                # [Field, Type, Null, Key, Default, Extra]
                ['command', 'varchar(255)', 'NO', 'PRI', None, '']
            ],
            status=status
        )

        if self.client_capabilities.DEPRECATE_EOF is False:
            packages.append(self.packet(EofPacket, status=status))
        else:
            packages.append(self.packet(OkPacket, eof=True, status=status))

        self.sendPackageGroup(packages)

    def queryAnswer(self, sql):
        sql_lower = sql.lower()
        sql_lower = sql_lower.replace('`', '')

        if 'show databases' in sql_lower:
            sql = 'select schema_name as Database from information_schema.SCHEMATA;'
            sql_lower = sql.lower()
        if 'show full tables from' in sql_lower:
            schema = re.findall(r'show\s+full\s+tables\s+from\s+(\S*)', sql_lower)[0]
            sql = f"select table_name as Tables_in_{schema} from INFORMATION_SCHEMA.TABLES WHERE table_schema = '{schema.upper()}' and table_type = 'BASE TABLE'"
            sql_lower = sql.lower()

        keyword = sql_lower.split(' ')[0]

        # TODO show tables from {name}
        if keyword == 'start':
            # start transaction
            self.packet(OkPacket).send()
        elif keyword == 'set':
            if 'autocommit' in sql_lower:
                self.packet(OkPacket).send()
            elif 'set names' in sql_lower:
                # it can be "set names utf8"
                self.charset = re.findall(r"set\s+names\s+(\S*)", sql_lower)[0]
                self.charset_text_type = CHARSET_NUMBERS['utf8_general_ci']
                if self.charset == 'utf8mb4':
                    self.charset_text_type = CHARSET_NUMBERS['utf8mb4_general_ci']
                self.packet(
                    OkPacket,
                    state_track=[
                        ['character_set_client', self.charset],
                        ['character_set_connection', self.charset],
                        ['character_set_results', self.charset]
                    ]
                ).send()
            else:
                self.packet(OkPacket).send()
        elif keyword == 'use':
            self.session.database = sql_lower.split()[1].trim(' ;')
            self.packet(OkPacket).send()
        elif 'show warnings' in sql_lower:
            self.answerShowWarnings()
        elif 'show engines' in sql_lower:
            self.answerShowEngines()
        elif 'show charset' in sql_lower:
            self.answerShowCharset()
        elif 'show collation' in sql_lower:
            self.answerShowCollation()
        elif 'show table status' in sql_lower:
            self.answer_show_table_status(sql)
        elif keyword == 'delete' and \
                ('mindsdb.predictors' in sql_lower or self.session.database == 'mindsdb' and 'predictors' in sql_lower):
            self.delete_predictor_sql(sql)
            self.packet(OkPacket).send()
        elif keyword == 'insert' and \
                ('mindsdb.commands' in sql_lower or self.session.database == 'mindsdb' and 'commands' in sql_lower):
            self.handle_custom_command(sql)
        elif keyword == 'insert' and \
                ('mindsdb.predictors' in sql_lower or self.session.database == 'mindsdb' and 'predictors' in sql_lower):
            insert = SQLQuery.parse_insert(sql)
            self.insert_predictor_answer(insert)
        elif keyword in ('update', 'insert'):
            raise NotImplementedError('Update and Insert not implemented')
        elif keyword == 'alter' and ('disable keys' in sql_lower) or ('enable keys' in sql_lower):
            self.packet(OkPacket).send()
        elif keyword == 'select':
            if '@@' in sql_lower:
                self.answerVariables(sql)
                return
            if 'select 1' in sql_lower:
                self.answerSelect1(sql)
                return
            if 'database()' in sql_lower:
                self.answerSelectDatabase()
                return
            query = SQLQuery(sql, integration=self.session.integration, database=self.session.database)
            self.selectAnswer(query)
        elif keyword == 'rollback':
            self.packet(OkPacket).send()
        elif keyword == 'commit':
            self.packet(OkPacket).send()
        elif keyword == 'explain':
            self.answer_explain_table(sql)
        else:
            raise NotImplementedError('Action not implemented')

    def answer_show_table_status(self, sql):
        # NOTE at this moment parsed statement only like `SHOW TABLE STATUS LIKE 'table'`.
        # NOTE some columns has {'database': 'mysql'}, other not. That correct. This is how real DB sends messages.
        parts = sql.split(' ')
        if parts[3].lower() != 'like':
            raise NotImplementedError('Action not implemented')
        table = parts[4].strip("'")

        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': 'mysql',
                'table_name': 'tables',
                'name': 'Name',
                'alias': 'Name',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Engine',
                'alias': 'Engine',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Version',
                'alias': 'Version',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': 'mysql',
                'table_name': 'tables',
                'name': 'Row_format',
                'alias': 'Row_format',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Rows',
                'alias': 'Rows',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Avg_row_length',
                'alias': 'Avg_row_length',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Data_length',
                'alias': 'Data_length',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Max_data_length',
                'alias': 'Max_data_length',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Index_length',
                'alias': 'Index_length',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Data_free',
                'alias': 'Data_free',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Auto_increment',
                'alias': 'Auto_increment',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Create_time',
                'alias': 'Create_time',
                'type': TYPES.MYSQL_TYPE_TIMESTAMP,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Update_time',
                'alias': 'Update_time',
                'type': TYPES.MYSQL_TYPE_TIMESTAMP,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Check_time',
                'alias': 'Check_time',
                'type': TYPES.MYSQL_TYPE_TIMESTAMP,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': 'mysql',
                'table_name': 'tables',
                'name': 'Collation',
                'alias': 'Collation',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Checksum',
                'alias': 'Checksum',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Create_options',
                'alias': 'Create_options',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': 'tables',
                'name': 'Comment',
                'alias': 'Comment',
                'type': TYPES.MYSQL_TYPE_BLOB,
                'charset': self.charset_text_type
            }],
            data=[[
                table,          # Name
                'InnoDB',       # Engine
                10,             # Version
                'Dynamic',      # Row_format
                1,              # Rows
                16384,          # Avg_row_length
                16384,          # Data_length
                0,              # Max_data_length
                0,              # Index_length
                0,              # Data_free
                None,           # Auto_increment
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Create_time
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Update_time
                None,           # Check_time
                'utf8mb4_0900_ai_ci',   # Collation
                None,           # Checksum
                '',             # Create_options
                ''              # Comment
            ]]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerShowWarnings(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': '',
                'table_name': '',
                'name': 'Level',
                'alias': 'Level',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': '',
                'table_name': '',
                'name': 'Code',
                'alias': 'Code',
                'type': TYPES.MYSQL_TYPE_LONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': '',
                'table_name': '',
                'name': 'Message',
                'alias': 'Message',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }],
            data=[]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerSelectDatabase(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': '',
                'table_name': '',
                'name': 'database()',
                'alias': 'database()',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }],
            data=[
                [None]
            ]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0000))
        self.sendPackageGroup(packages)

    def answerShowCollation(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'COLLATION_NAME',
                'alias': 'Collation',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'CHARACTER_SET_NAME',
                'alias': 'Charset',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'ID',
                'alias': 'Id',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }, {
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'IS_DEFAULT',
                'alias': 'Default',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'IS_COMPILED',
                'alias': 'Compiled',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'COLLATIONS',
                'name': 'SORTLEN',
                'alias': 'Sortlen',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }],
            data=[
                ['utf8_general_ci', 'utf8', 33, 'Yes', 'Yes', 1],
                ['latin1_swedish_ci', 'latin1', 8, 'Yes', 'Yes', 1]
            ]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerShowCharset(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': 'information_schema',
                'table_name': 'CHARACTER_SETS',
                'name': 'CHARACTER_SET_NAME',
                'alias': 'Charset',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'CHARACTER_SETS',
                'name': 'DESCRIPTION',
                'alias': 'Description',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'CHARACTER_SETS',
                'name': 'DEFAULT_COLLATE_NAME',
                'alias': 'Default collation',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'CHARACTER_SETS',
                'name': 'MAXLEN',
                'alias': 'Maxlen',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }],
            data=[
                ['utf8', 'UTF-8 Unicode', 'utf8_general_ci', 3],
                ['latin1', 'cp1252 West European', 'latin1_swedish_ci', 1]
            ]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerShowEngines(self):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'Engine',
                'alias': 'Engine',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'Support',
                'alias': 'Support',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'Comment',
                'alias': 'Comment',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'Transactions',
                'alias': 'Transactions',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'XA',
                'alias': 'XA',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }, {
                'database': 'information_schema',
                'table_name': 'ENGINES',
                'name': 'Savepoints',
                'alias': 'Savepoints',
                'type': TYPES.MYSQL_TYPE_VAR_STRING,
                'charset': self.charset_text_type
            }],
            data=[['InnoDB', 'DEFAULT', 'Supports transactions, row-level locking, and foreign keys', 'YES', 'YES', 'YES']]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerSelect1(self, sql):
        packages = []
        packages += self.getTabelPackets(
            columns=[{
                'table_name': '',
                'name': '',
                'alias': '1',
                'type': TYPES.MYSQL_TYPE_LONGLONG,
                'charset': CHARSET_NUMBERS['binary']
            }],
            data=[[1]]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def answerVariables(self, sql):
        if '@@version_comment' in sql.lower():
            self.answerVersionComment()
            return
        elif '@@version' in sql.lower():
            self.answerVersion()
            return
        p = sql_parser.parse(sql)
        select = p.get('select')
        if isinstance(select, dict):
            select = [select]
        columns = []
        row = []
        for s in select:
            fill_name = s.get('value')
            alias = s.get('name', fill_name)
            variable = SERVER_VARIABLES.get(fill_name)
            columns.append({
                'table_name': '',
                'name': '',
                'alias': alias,
                'type': variable[1],
                'charset': variable[2]
            })
            row.append(variable[0])

        packages = []
        packages += self.getTabelPackets(
            columns=columns,
            data=[row]
        )
        packages.append(self.packet(OkPacket, eof=True, status=0x0002))
        self.sendPackageGroup(packages)

    def selectAnswer(self, query):
        global datahub
        result = query.fetch(datahub)

        if result['success'] is False:
            self.packet(
                ErrPacket,
                err_code=result['error_code'],
                msg=result['msg']
            ).send()
            return

        self.answerTableQuery(query)

    def _get_column_defenition_packets(self, columns, data=[]):
        packets = []
        for i, column in enumerate(columns):
            table_name = column.get('table_name', 'table_name')
            column_name = column.get('name', 'column_name')
            column_alias = column.get('alias', column_name)
            flags = column.get('flags', 0)
            length = 1
            for row in data:
                if isinstance(row, dict):
                    length = max(len(str(row[column_alias])), length)
                else:
                    length = max(len(str(row[i])), length)
            packets.append(
                self.packet(
                    ColumnDefenitionPacket,
                    schema=column.get('database', 'mindsdb_schema'),
                    table_alias=column.get('table_alias', table_name),
                    table_name=table_name,
                    column_alias=column_alias,
                    column_name=column_name,
                    column_type=column['type'],
                    charset=column.get('charset', CHARSET_NUMBERS["utf8_unicode_ci"]),
                    max_length=length,
                    flags=flags
                )
            )
        return packets

    def getTabelPackets(self, columns, data, status=0):
        # TODO remove columns order
        packets = [self.packet(ColumnCountPacket, count=len(columns))]
        packets.extend(self._get_column_defenition_packets(columns, data))

        if self.client_capabilities.DEPRECATE_EOF is False:
            packets.append(self.packet(EofPacket, status=status))

        packets += [self.packet(ResultsetRowPacket, data=x) for x in data]
        return packets

    def _prepare_sql(self, sql):
        try:
            prepared_sql = sql.decode('utf-8')
            # NOTE dbeaver can insert in start of query comment with connector version, for example
            # /* mysql-connector-java-8.0.11 (Revision: 6d4eaa273bc181b4cf1c8ad0821a2227f116fedf) */SELECT @@session.auto_increment_increment
            prepared_sql = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", prepared_sql)
            prepared_sql = prepared_sql.strip(' ;')
            return prepared_sql
        except Exception:

            log.error('SQL contains non utf-8 values: {sql}'.format(sql=sql))
            self.packet(OkPacket).send()

    def handle(self):
        """
        Handle new incoming connections
        :return:
        """
        log.info('handle new incoming connection')
        if self.handshake() is False:
            return

        while True:
            log.debug('Got a new packet')
            p = self.packet(CommandPacket)

            try:
                success = p.get()
            except Exception:
                log.warning('Session closed, on packet read error')
                log.debug(traceback.format_exc())
                # self.server.shutdown()
                return

            if success is False:
                log.info('Session closed by client')
                # self.server.shutdown()
                return

            log.info('Command TYPE: {type}'.format(
                type=getConstName(COMMANDS, p.type.value)))

            if p.type.value == COMMANDS.COM_QUERY:
                try:
                    sql = self._prepare_sql(p.sql.value)
                except Exception:
                    log.error('SQL contains non utf-8 values: {sql}'.format(sql=p.sql.value))
                    self.packet(OkPacket).send()
                    continue
                log.info(f'COM_QUERY: {sql}')

                try:
                    self.queryAnswer(sql)
                except Exception as e:
                    log.error(
                        f'ERROR while executing query: {sql}\n'
                        f'{traceback.format_exc()}\n'
                        f'{e}'
                    )
                    self.packet(
                        ErrPacket,
                        err_code=ERR.ER_SYNTAX_ERROR,
                        msg=str(e)
                    ).send()
            elif p.type.value == COMMANDS.COM_STMT_PREPARE:
                # https://dev.mysql.com/doc/internals/en/com-stmt-prepare.html
                try:
                    sql = self._prepare_sql(p.sql.value)
                except Exception:
                    log.error('SQL contains non utf-8 values: {sql}'.format(sql=p.sql.value))
                    self.packet(OkPacket).send()
                    continue
                log.info(f'COM_STMT_PREPARE: {sql}')

                try:
                    self.answer_stmt_prepare(sql)
                except Exception as e:
                    log.error(
                        f'ERROR while preparing query: {sql}\n'
                        f'{traceback.format_exc()}\n'
                        f'{e}'
                    )
                    self.packet(
                        ErrPacket,
                        err_code=ERR.ER_SYNTAX_ERROR,
                        msg=str(e)
                    ).send()
            elif p.type.value == COMMANDS.COM_STMT_EXECUTE:
                self.answer_stmt_execute(p.stmt_id.value, p.parameters)
            elif p.type.value == COMMANDS.COM_STMT_FETCH:
                self.answer_stmt_fetch(p.stmt_id.value, p.limit.value)
            elif p.type.value == COMMANDS.COM_STMT_CLOSE:
                self.answer_stmt_close(p.stmt_id.value)
            elif p.type.value == COMMANDS.COM_QUIT:
                log.info('Session closed, on client disconnect')
                self.session = None
                break
            else:
                log.info('Command has no specific handler, return OK msg')
                log.debug(str(p))
                # p.pprintPacket() TODO: Make a version of print packet
                # that sends it to debug isntead
                self.packet(OkPacket).send()

    def packet(self, packetClass=Packet, **kwargs):
        """
        Factory method for packets

        :param packetClass:
        :param kwargs:
        :return:
        """
        p = packetClass(socket=self.socket, seq=self.count, session=self.session, proxy=self, **kwargs)
        self.count = (self.count + 1) % 256
        return p

    @staticmethod
    def startProxy(_config):
        global HARDCODED_USER
        global HARDCODED_PASSWORD
        global CERT_PATH
        global default_store
        global mdb
        global datahub
        global config
        """
        Create a server and wait for incoming connections until Ctrl-C
        """
        config = _config
        init_logger(config)

        HARDCODED_USER = config['api']['mysql']['user']
        HARDCODED_PASSWORD = config['api']['mysql']['password']
        CERT_PATH = config['api']['mysql'].get('certificate_path')
        if CERT_PATH is None or CERT_PATH == '':
            CERT_PATH = tempfile.mkstemp(prefix='mindsdb_cert_', text=True)[1]
            make_ssl_cert(CERT_PATH)
            atexit.register(lambda: os.remove(CERT_PATH))

        default_store = DataStore(config)
        mdb = MindsdbNative(config)
        datahub = init_datahub(config)

        host = config['api']['mysql']['host']
        port = int(config['api']['mysql']['port'])

        log.info(f'Starting MindsDB Mysql proxy server on tcp://{host}:{port}')

        # Create the server
        if config['debug'] is True:
            SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.ThreadingTCPServer((host, port), MysqlProxy)

        atexit.register(MysqlProxy.server_close, srv=server)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        log.info('Waiting for incoming connections...')
        server.serve_forever()
