from urllib.parse import unquote
from clickhouse_driver import Client


class ClickHouseModel:
    def __init__(self, host: str = 'localhost', port: int = 9000):
        self.host = host
        self.port = port
        self.client = Client(host=self.host, port=self.port)
        self.database = Database(client=self.client)


class Database:
    def __init__(self, client):
        self.client = client

    def _execute_query(self, query):
        return self.client.execute(query)

    def create_db(self, database_name, using=True):
        query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        self._execute_query(query)
        if using:
            self.active_database(database_name=database_name)
        print(f'*** database {database_name} created . ***')

    def create_tabel(self, table_name: str, fields: dict, primary_key: tuple, engine: str = 'MergeTree'):
        if not primary_key:
            raise Exception('Missing required fields:PRIMARY KEY .')
        if not isinstance(primary_key, tuple):
            raise Exception('PRIMARY KEY must be a tuple .')

        data, pk = '', ''
        for colum, value in fields.items():
            if colum in primary_key:
                pk += f'{colum},'
            data += f'{colum} {value},'

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({data}) ENGINE={engine} PRIMARY KEY ({pk});"
        self._execute_query(query)
        print(query)
        print(f'*** table {table_name} created ***')

    def drop_db(self, database_name):
        query = f"DROP DATABASE IF EXISTS {database_name};"
        self._execute_query(query)
        print(f'*** database {database_name} dropped. ***')

    def drop_tabel(self, table_name):
        if self.active_database in None:
            raise Exception('First, please USE the database')
        query = f'DROP TABLE IF EXISTS {table_name};'
        self._execute_query(query)
        print(f"*** table {table_name} dropped ***")

    def insert(self, table_name: str, data: dict):
        column_value: list = []
        for i in data.values():
            column_value.append(self._check_encoded(i))

        self._execute_query(
            f"""INSERT INTO {table_name} ({','.join(data.keys())}) values ({','.join(column_value)});"""
        )

    def active_database(self, database_name):
        self.active_database = database_name

    def use(self, database_name):
        query = f"USE {database_name};"
        self._execute_query(query)
        print(f'*** database {database_name} using . ***')

    @staticmethod
    def _check_encoded(value: str = 'None') -> str:
        if value == 'None' or value == None:
            return 'NULL'
        elif value != 'NULL' and type(value) == type(str()):
            value = unquote(value)
            return f"'{value}'"
        else:
            return str(value)

    def optimize_table(self, table_name: str, pk_field: str):
        query = f"OPTIMIZE TABLE {table_name} FINAL DEDUPLICATE BY COLUMNS ({pk_field});"
        self._execute_query(query)
        print(f'*** table {table_name} optimized ***')

# class ClickHouse:
#     def __init__(self, host='localhost', port=9000):
#         self.host = host
#         self.port = port
#         self._connect_to_server(host=self.host, port=self.port)
#         self.database = Database(self.client)
#
#     def _connect_to_server(self, host: str, port: int) -> None:
#         """
#             Establishes a connection to the ClickHouse server running at the specified `host` and `port`.
#
#             Args:
#                 host (str): The IP address or hostname of the ClickHouse server.
#                 port (int): The port number on which the ClickHouse server is listening.
#
#             Returns:
#                 None
#
#             Raises:
#                 Any exceptions raised by the `Client` constructor.
#
#         """
#
#         try:
#             self.client = Client(host=host, port=port)
#             # logging.info('Connected to ClickHouse')
#
#         except Exception as e:
#             pass
#             # logging.error(f'Failed to connect to ClickHouse: {e}')
#
#
# class Database:
#     def __init__(self, client):
#         self.client = client
#         self.active_database = None
#
#     def optimize_table(self, table_name, pk_field):
#         query = f"OPTIMIZE TABLE {table_name} DEDUPLICATE BY {pk_field};"
#         self.manual_query(query)
#
#     def create(self, database_name: str, using=True):
#         try:
#             self.client.execute(f'CREATE DATABASE IF NOT EXISTS {database_name};')
#
#         except Exception as e:
#             print(e)
#
#         if using:
#             self.use(database_name)
#
#     def drop(self, database_name: str):
#         try:
#             self.client.execute(f'DROP DATABASE IF EXISTS {database_name}')
#
#         except Exception as e:
#             print(e)
#
#     def use(self, database_name: str):
#         try:
#             self.client.execute(f'USE {database_name};')
#             self.active_database = database_name
#
#         except Exception as e:
#             print(e)
#
#     def create_table(self, table_name: str, fields: dict, engine='MergeTree',extra_setting=None) -> None:
#         if ('PRIMARY KEY' not in fields) or ('PRIMARY KEY' not in extra_setting):
#             raise Exception('Missing required fields:PRIMARY KEY')
#
#         field, setting = '', ''
#         for key, value in fields.items():
#             if extra_setting is None:
#                 if key.upper() in ['PRIMARY KEY', 'ORDER BY']:
#                     setting += f'{key} ({value})'
#                 else:
#                     setting += setting
#
#             else:
#                 field += f'{key} {value},'
#         query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({field}) ENGINE={engine} {setting};"""
#         self.client.execute(query)
#
#     def insert(self, table_name: str, fields: dict):
#         column_value: list = []
#         for i in fields.values():
#             column_value.append(self._check_encoded(i))
#
#         self.client.execute(
#             f"""INSERT INTO {table_name} ({','.join(fields.keys())}) values ({','.join(column_value)})"""
#         )
#
#     def manual_query(self, query):
#         return self.client.execute(query)
#
#     @staticmethod
#     def _check_encoded(value: str = 'None') -> str:
#         if value == 'None' or value == None:
#             return 'NULL'
#         elif value != 'NULL' and type(value) == type(str()):
#             value = unquote(value)
#             return f"'{value}'"
#         else:
#             return str(value)
