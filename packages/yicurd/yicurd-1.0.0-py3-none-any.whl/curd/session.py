import json
from functools import partial
from collections import OrderedDict

from .connections import CURD_FUNCTIONS

from .errors import ProgrammingError


DB_CONNECTION_POOL = {}

try:
    from .connections.mysql import MysqlConnectionPool
except Exception:
    pass
else:
    DB_CONNECTION_POOL['mysql'] = MysqlConnectionPool

try:
    from .connections.cassandra import CassandraConnectionPool
except Exception:
    pass
else:
    DB_CONNECTION_POOL['cassandra'] = CassandraConnectionPool

try:
    from .connections.hbase import HbaseConnectionPool
except Exception:
    pass
else:
    DB_CONNECTION_POOL['hbase'] = HbaseConnectionPool


class Session(object):
    """
    mysql db conf
    {
        'type': 'mysql',
        'conf': {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'user',
            'password': 'password',
            'max_op_fail_retry': 3,
            'timeout': 60
        }
    }
    tidb conf
    {
        'type': 'mysql',
        'conf': {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'user',
            'password': 'password',
            'tidb_patch': True,
            'max_op_fail_retry': 3,
            'timeout': 60
        }
    }
    cassandra db conf
    {
        'type': 'cassandra',
        'conf': {
            'hosts': ['127.0.0.1'],
            'username': 'username',
            'password': 'password',
            'max_op_fail_retry': 3,
            'timeout': 60
        }
    }
    hbase db conf
    {
        'type': 'hbase',
        'conf': {
            'urls': ['http://127.0.0.1:8765/'],
            'username': '',
            'password': '',
        }
    }
    """
    
    def __init__(self, dbs=None):
        self._connection_cache = OrderedDict()
        self._default_connection = None
        
        if dbs:
            for db in dbs:
                self._get_connection(db)
        
    def _create_connection(self, db):
        class_conn_pool = DB_CONNECTION_POOL.get(db['type'], None)
        if class_conn_pool:
            return class_conn_pool(db['conf'])
        else:
            if db['type'] in ['mysql', 'cassandra', 'hbase']:
                raise ProgrammingError('no database driver')
            else:
                raise ProgrammingError('not supported database')
        
    def set_default_connection(self, db):
        key = json.dumps(db)
        conn = self._connection_cache.get(key, None)
        if not conn:
            conn = self._create_connection(db)
            self._connection_cache[key] = conn
        self._default_connection = conn
        
    def _get_connection(self, db):
        key = json.dumps(db)
        conn = self._connection_cache.get(key, None)
        if conn:
            return conn
        else:
            conn = self._create_connection(db)
            self._connection_cache[key] = conn
            
            if not self._default_connection:
                self._default_connection = conn
            
            return conn
        
    def using(self, db=None):
        if db:
            return self._get_connection(db)
        else:
            return self._default_connection
        
    def __getattr__(self, item):
        if item in CURD_FUNCTIONS:
            if self._default_connection:
                return getattr(self._default_connection, item)
            else:
                raise ProgrammingError('no database conf')
        else:
            raise AttributeError
            
    def close(self):
        for k, v in self._connection_cache.items():
            v.close()
        self._connection_cache = OrderedDict()
        self._default_connection = None


class F(object):
    def __init__(self, value):
        self._value = value
    
    def __eq__(self, other):
        return '=', self._value, other
    
    def __ne__(self, other):
        return '!=', self._value, other
    
    def __lt__(self, other):
        return '<', self._value, other
    
    def __le__(self, other):
        return '<=', self._value, other
    
    def __gt__(self, other):
        return '>', self._value, other
    
    def __ge__(self, other):
        return '>=', self._value, other
    
    def __lshift__(self, other):
        return 'IN', self._value, other


class SimpleCollection(object):
    def __init__(self, session, path, timeout=None, retry=None):
        self.s = session
        self.path = path
        self.timeout = timeout
        self.retry = retry
        
        for func in CURD_FUNCTIONS:
            setattr(
                self,
                func,
                partial(
                    getattr(self.s, func),
                    collection=self.path,
                    timeout=timeout,
                    retry=retry
                )
            )
