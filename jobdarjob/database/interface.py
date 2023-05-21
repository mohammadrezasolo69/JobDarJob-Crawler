from urllib.parse import unquote
from clickhouse_driver import Client
from jobdarjob.database.meta_class import ClickHouseMetaClass


class ClickHouseModel(metaclass=ClickHouseMetaClass):
    """
        Base class for ClickHouse models.

        This class inherits from ClickHouseMetaClass metaclass, which ensures that only one instance
        of the class is created and returned when called. It provides a convenient way to connect to
        a ClickHouse server and interact with the database.

        Attributes:
            host (str): The hostname or IP address of the ClickHouse server. Default is 'localhost'.
            port (int): The port number of the ClickHouse server. Default is 9000.
            client (Client): The ClickHouse client instance used for database operations.
            database (Database): The ClickHouse database instance associated with the create_table.

        Methods:
            __init__(self, host: str = 'localhost', port: int = 9000): Initializes the ClickHouseModel instance.
                Connects to the ClickHouse server using the provided host and port, and initializes the client
                and database attributes.

        """

    def __init__(self, host: str = 'localhost', port: int = 9000):
        """
                Initializes the ClickHouseModel instance.

                Connects to the ClickHouse server using the provided host and port, and initializes
                the client and database attributes.

                Args:
                    host (str): The hostname or IP address of the ClickHouse server. Default is 'localhost'.
                    port (int): The port number of the ClickHouse server. Default is 9000.
        """

        self.host = host
        self.port = port
        self.client = Client(host=self.host, port=self.port)
        self.database = Database(client=self.client)


class Database:
    """
        Wrapper class for interacting with a ClickHouse database.

        This class provides methods to execute queries and perform database operations such as
        creating a database, creating a table, dropping a database, dropping a table, inserting
        data into a table, setting the active database, and optimizing a table.

        Attributes:
            client (Client): The ClickHouse client instance used for executing queries.
            active_database (str): The name of the active database.

        Methods:
            __init__(self, client): Initializes the Database instance.
                Sets the client attribute with the provided ClickHouse client instance.

            _execute_query(self, query): Executes a query using the client and returns the result.

            create_db(self, database_name, using=True): Creates a database with the given name.
                If 'using' is True, sets the created database as the active database.

            create_table(self, table_name, fields, primary_key, engine='MergeTree'): Creates a table
                with the given name, fields, primary key, and engine.

            drop_db(self, database_name): Drops a database with the given name.

            drop_table(self, table_name): Drops a table with the given name.

            insert(self, table_name, data): Inserts data into the specified table.

            active_database(self, database_name): Sets the active database.

            use(self, database_name): Sets the active database for use in queries.

            _check_encoded(value): Helper method to check and format the value for insertion into a query.

            optimize_table(self, table_name, pk_field): Optimizes a table by deduplicating rows based on a primary key.

            select(self, table_name, columns=('*',), order_by=None): Executes a SELECT query on the specified table.

        """

    def __init__(self, client):
        """
                Initializes the Database instance.

                Args:
                    client (Client): The ClickHouse client instance used for executing queries.
        """
        self.client = client
        self.active_database = None

    def _execute_query(self, query):
        """
                Executes a query using the client and returns the result.

                Args:
                    query (str): The query to be executed.

                Returns:
                    The result of the query execution.
        """
        result = self.client.execute(query)
        return result

    def create_db(self, database_name, using=True):
        """
                Creates a database with the given name.

                If 'using' is True, sets the created database as the active database.

                Args:
                    database_name (str): The name of the database to be created.
                    using (bool): Whether to set the created database as the active database.
                        Defaults to True.
        """
        query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        self._execute_query(query)
        if using:
            self.active_database = database_name
        print(f'*** database {database_name} created . ***')

    def create_tabel(self, table_name: str, fields: dict, primary_key: tuple, engine: str = 'MergeTree'):
        """
           Creates a table with the given name, fields, primary key, and engine.

           Args:
               table_name (str): The name of the table to be created.
               fields (dict): A dictionary mapping field names to their corresponding types.
               primary_key (tuple): The primary key fields of the table.
               engine (str): The engine to be used for the table. Defaults to 'MergeTree'.
        """
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
        """
            Drops a database with the given name.

            Args:
                database_name (str): The name of the database to be dropped.
        """
        query = f"DROP DATABASE IF EXISTS {database_name};"
        self._execute_query(query)
        print(f'*** database {database_name} dropped. ***')

    def drop_tabel(self, table_name):
        """
           Drops a table with the given name.

           Args:
               table_name (str): The name of the table to be dropped.
        """
        if self.active_database in None:
            raise Exception('First, please USE the database')
        query = f'DROP TABLE IF EXISTS {table_name};'
        self._execute_query(query)
        print(f"*** table {table_name} dropped ***")

    def insert(self, table_name: str, data: dict):
        """
           Inserts data into the specified table.

           Args:
               table_name (str): The name of the table to insert data into.
               data (dict): A dictionary mapping column names to their corresponding values.
        """
        column_value: list = []
        for i in data.values():
            column_value.append(self._check_encoded(i))

        query = f"""INSERT INTO {table_name} ({','.join(data.keys())}) values ({','.join(column_value)});"""
        self._execute_query(query)

    def active_database(self, database_name):
        """
        Sets the active database.

        Args:
            database_name (str): The name of the database to set as active.
        """
        self.active_database = database_name

    def use(self, database_name):
        """
            Sets the active database for use in queries.

            Args:
                database_name (str): The name of the database to set as active.
        """
        query = f"USE {database_name};"
        self._execute_query(query)
        print(f'*** database {database_name} using . ***')

    @staticmethod
    def _check_encoded(value: str = 'None') -> str:
        """
            Helper method to check and format the value for insertion into a query.

            Args:
                value: The value to be checked and encoded.

            Returns:
                str: The encoded value.
        """
        if value == 'None' or value == None:
            return 'NULL'
        elif value != 'NULL' and type(value) == type(str()):
            value = unquote(value)
            return f"'{value}'"
        else:
            return str(value)

    def optimize_table(self, table_name: str, pk_field: str):
        """
                Optimizes a table by deduplicating rows based on a primary key.

                Args:
                    table_name (str): The name of the table to optimize.
                    pk_field (str): The primary key field used for deduplication.
        """
        query = f"OPTIMIZE TABLE {table_name} FINAL DEDUPLICATE BY COLUMNS ({pk_field});"
        self._execute_query(query)
        print(f'*** table {table_name} optimized ***')

    def select(self, table_name: str, columns: tuple = ('*',), order_by=None) -> list:
        """
                Executes a SELECT query on the specified table.

                Args:
                    table_name (str): The name of the table to select from.
                    columns (tuple): The columns to select. Defaults to ('*',) to select all columns.
                    order_by (dict): The columns and order to use for ordering the result. Defaults to None.

                Returns:
                    list: The result of the SELECT query.
                """
        if order_by is None:
            order_by = {'date_last_crawl': 'DESC'}

        columns_str = ','.join(map(str, columns))
        order_by_str = ', '.join([f'{colum} {value}' for colum, value in order_by.items()])

        query = f'SELECT {columns_str} FROM {table_name} ORDER BY {order_by_str}'
        print("&"*100)
        print(query)
        return self._execute_query(query)
