mysql_conf = {
    'type': 'mysql',
    'conf': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
    }
}

cassandra_conf = {
    'type': 'cassandra',
    'conf': {
        'hosts': ['127.0.0.1'],
    }
}

hbase_conf = {
    'type': 'hbase',
    'conf': {
        'urls': ['http://127.0.0.1:8765/'],
    }
}
