import os
# import logging
import urllib
from urllib.parse import unquote

import colorlog

from clickhouse_driver import Client


# os.system('clear')
# logger = colorlog.getLogger()
#
# logger.setLevel(logging.INFO)
# handler = colorlog.StreamHandler()
# handler.setFormatter(colorlog.ColoredFormatter(
#     '%(log_color)s%(levelname)s:%(message)s "LINE":%(lineno)d\n'
#     '------------------------------------------------------------'
# ))

# logger.addHandler(handler)


class ClickHouse:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self._connect_to_server(host=self.host, port=self.port)
        self.database = Database(self.client)

    def _connect_to_server(self, host: str, port: int) -> None:
        """
            Establishes a connection to the ClickHouse server running at the specified `host` and `port`.

            Args:
                host (str): The IP address or hostname of the ClickHouse server.
                port (int): The port number on which the ClickHouse server is listening.

            Returns:
                None

            Raises:
                Any exceptions raised by the `Client` constructor.

        """

        try:
            self.client = Client(host=host, port=port)
            # logging.info('Connected to ClickHouse')

        except Exception as e:
            pass
            # logging.error(f'Failed to connect to ClickHouse: {e}')


class Database:
    def __init__(self, client):
        self.client = client
        self.active_database = None

    def optimize_table(self, table_name, pk_field):
        self.manual_query(f"optimize {table_name} DEDUPLICATE BY {pk_field}")

    def create(self, database_name: str, using=True):
        try:
            self.client.execute(f'CREATE DATABASE IF NOT EXISTS {database_name};')

        except Exception as e:
            print(e)

        if using:
            self.use(database_name)

    def drop(self, database_name: str):
        try:
            self.client.execute(f'DROP DATABASE IF EXISTS {database_name}')

        except Exception as e:
            print(e)

    def use(self, database_name: str):
        try:
            self.client.execute(f'USE {database_name};')
            self.active_database = database_name

        except Exception as e:
            print(e)

    def create_table(self, table_name: str, fields: dict, engine='MergeTree', duplicate=True) -> None:
        if 'PRIMARY KEY' not in fields:
            raise Exception('Missing required fields:PRIMARY KEY')

        field, setting = '', ''
        for key, value in fields.items():
            if key.upper() in ['PRIMARY KEY', 'ORDER BY']:
                setting += f'{key} ({value}) '

            else:
                field += f'{key} {value},'
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({field}) ENGINE={engine} {setting};"""
        self.client.execute(query)

        if not duplicate:
            self.optimize_table(table_name=table_name, pk_field=fields.get('PRIMARY KEY'))

    def insert(self, table_name: str, fields: dict):
        column_value: list = []
        for i in fields.values():
            column_value.append(self._check_encoded(i))

        self.client.execute(
            f"""INSERT INTO {table_name} ({','.join(fields.keys())}) values ({','.join(column_value)})"""
        )

    def manual_query(self, query):
        return self.client.execute(query)

    @staticmethod
    def _check_encoded(value: str = 'None') -> str:
        if value == 'None' or value == None:
            return 'NULL'
        elif value != 'NULL' and type(value) == type(str()):
            value = unquote(value)
            return f"'{value}'"
        else:
            return str(value)
