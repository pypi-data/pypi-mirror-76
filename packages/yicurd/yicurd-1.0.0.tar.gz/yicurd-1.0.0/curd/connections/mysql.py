import os
import copy
import queue
from functools import partial

import pymysql

from ..errors import (
    UnexpectedError, OperationFailure, ProgrammingError,
    ConnectError,
    DuplicateKeyError
)
from . import logger
from .utils.sql import (
    query_parameters_from_create,
    query_parameters_from_update,
    query_parameters_from_delete,
    query_parameters_from_filter,
    query_parameters_from_create_many)
from . import (
    BaseConnection, DEFAULT_FILTER_LIMIT, DEFAULT_TIMEOUT, OP_RETRY_WARNING,
    CURD_FUNCTIONS
)

# https://www.briandunning.com/error-codes/?source=MySQL

PE_MYSQL_ERROR_CODE_LIST = [
                               1265,  # Data truncated, tidb error
                           ] + list(range(1046, 1076))

PE_DUPLICATE_ENTRY_KEY_ERROR_CODE = 1062

OF_MYSQL_ERROR_CODE_LIST = [0, 1040, 2006, 2013]
OF_MYSQL_RETRY_ERROR_CODE_LIST = [
    0,  # mysql interface error
    1040,  # mysql too many connections
    2006,  # mysql gone away
    2013,  # mysql connection timeout
]

TIDB_ADDITION_ERROR_CODE_LIST = [
    1105,  # Information schema is out of date or backoffer.maxSleep is exceeded
    9002,  # TiKV server timeout[try again later]
]
OF_TIDB_ERROR_CODE_LIST = OF_MYSQL_ERROR_CODE_LIST + \
                          TIDB_ADDITION_ERROR_CODE_LIST
OF_TIDB_RETRY_ERROR_CODE_LIST = OF_MYSQL_RETRY_ERROR_CODE_LIST + \
                                TIDB_ADDITION_ERROR_CODE_LIST


class MysqlConnection(BaseConnection):
    pe_mysql_error_code_list = PE_MYSQL_ERROR_CODE_LIST
    pe_duplicate_entry_key_error_code = PE_DUPLICATE_ENTRY_KEY_ERROR_CODE

    of_mysql_error_code_list = OF_MYSQL_ERROR_CODE_LIST
    of_mysql_retry_error_code_list = OF_MYSQL_RETRY_ERROR_CODE_LIST

    def __init__(self, conf):
        self._conf = conf
        self.pid = os.getpid()
        self.conn, self.cursor = None, None

        self.max_op_fail_retry = conf.get('max_op_fail_retry', 0)
        self.default_timeout = conf.get('timeout', DEFAULT_TIMEOUT)

    def _connect(self, conf):
        conf = copy.deepcopy(conf)

        self.max_op_fail_retry = conf.pop('max_op_fail_retry', 0)
        self.default_timeout = conf.pop('timeout', DEFAULT_TIMEOUT)

        conf['use_unicode'] = True
        conf['charset'] = 'utf8mb4'
        conf['autocommit'] = True

        conf['read_timeout'] = self.default_timeout
        conf['write_timeout'] = self.default_timeout

        if conf.pop('tidb_patch', False):
            self.patch_execute_as_tidb()

        conn = pymysql.connect(**conf)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # disable, _show_warnings func will cause mem leak where there are lots of different Dup key warnings
        cursor._defer_warnings = True
        return conn, cursor

    def connect(self, conf):
        try:
            self.conn, self.cursor = self._connect(conf)
        except Exception as e:
            raise ConnectError(origin_error=e)

    def close(self):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                logger.warning(str(e))
        if self.conn:

            try:
                self.conn.close()
            except Exception as e:
                logger.warning(str(e))

        self.conn, self.cursor = None, None

    def _execute(self, query, params, timeout, cursor_func='execute'):
        if not self.cursor:
            self.connect(self._conf)

        self.conn._read_timeout = timeout
        self.conn._write_timeout = timeout

        try:
            func = getattr(self.cursor, cursor_func)
            func(query, params)
        except pymysql.err.ProgrammingError as e:
            raise ProgrammingError(origin_error=e)
        except Exception as e:
            if isinstance(e.args, tuple) and len(e.args) >= 1:
                if e.args[0] in self.pe_mysql_error_code_list:
                    raise ProgrammingError(origin_error=e)
                elif e.args[0] in self.of_mysql_error_code_list:
                    raise OperationFailure(origin_error=e)
                else:
                    raise UnexpectedError(origin_error=e)
            else:
                raise UnexpectedError(origin_error=e)
        else:
            return list(self.cursor.fetchall())

    def execute(self, query, params=None, retry=None, timeout=None, cursor_func='execute'):
        if os.getpid() != self.pid:
            self.close()
            self.pid = os.getpid()

        if retry is None:
            retry = self.max_op_fail_retry

        if timeout is None:
            timeout = self.default_timeout

        retry_no = 0
        while True:
            try:
                rows = self._execute(query, params, timeout, cursor_func)
            except OperationFailure as e:
                self.close()
                if retry_no < retry:
                    logger.warning(OP_RETRY_WARNING.format(str(e)))
                    retry_no += 1
                else:
                    raise
            except ProgrammingError:
                raise
            except (UnexpectedError, Exception, KeyboardInterrupt):
                self.close()
                raise
            else:
                return rows

    def executemany(self, query, params=None, retry=None, timeout=None, cursor_func='executemany'):
        return self.execute(query, params, retry, timeout, cursor_func=cursor_func)

    def create(self, collection, data, mode='INSERT', compress_fields=None, **kwargs):
        query, params = query_parameters_from_create(
            collection, data, mode.upper(), compress_fields
        )
        try:
            self.execute(query, params, **kwargs)
        except ProgrammingError as e:
            if e._origin_error.args[0] == self.pe_duplicate_entry_key_error_code:
                raise DuplicateKeyError(str(e._origin_error))
            else:
                raise

    def create_many(self, collection, data, mode='INSERT', compress_fields=None, **kwargs):
        if not isinstance(data, list):
            data = [data, ]

        query, params = query_parameters_from_create_many(
            collection, data, mode.upper(), compress_fields
        )
        try:
            self.execute(query, params, cursor_func='executemany', **kwargs)
        except ProgrammingError as e:
            if e._origin_error.args[0] == self.pe_duplicate_entry_key_error_code:
                raise DuplicateKeyError(str(e._origin_error))
            else:
                raise

    def update(self, collection, data, filters, **kwargs):
        filters = self._check_filters(filters)
        query, params = query_parameters_from_update(collection, filters, data)
        self.execute(query, params, **kwargs)

    def delete(self, collection, filters, **kwargs):
        filters = self._check_filters(filters)
        query, params = query_parameters_from_delete(collection, filters)
        self.execute(query, params, **kwargs)

    def filter(self, collection, filters=None, fields=None,
               order_by=None, limit=DEFAULT_FILTER_LIMIT, **kwargs):
        filters = self._check_filters(filters)
        query, params = query_parameters_from_filter(
            collection, filters, fields, order_by, limit)
        rows = self.execute(query, params, **kwargs)
        return rows

    def patch_execute_as_tidb(self):
        self.of_mysql_error_code_list = OF_TIDB_ERROR_CODE_LIST
        self.of_mysql_retry_error_code_list = OF_TIDB_RETRY_ERROR_CODE_LIST


class MysqlConnectionPool(object):
    def __init__(self, *args, **kwargs):
        self.conn_queue = queue.Queue()
        self._args = args
        self._kwargs = kwargs

        for func in CURD_FUNCTIONS:
            setattr(self, func, partial(self._wrap_func, func))

    def get_connection(self):
        return MysqlConnection(*self._args, **self._kwargs)

    def _wrap_func(self, func, *args, **kwargs):
        try:
            conn = self.conn_queue.get_nowait()
        except queue.Empty:
            conn = self.get_connection()

        try:
            return getattr(conn, func)(*args, **kwargs)
        except:
            raise
        finally:
            self.conn_queue.put_nowait(conn)

    def close(self):
        while True:
            try:
                conn = self.conn_queue.get_nowait()
            except queue.Empty:
                break
            else:
                conn.close()
