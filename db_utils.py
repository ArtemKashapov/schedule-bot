import psycopg2
from psycopg2 import OperationalError
import config


class Database:
    def __init__(self):
        self.connection = self.create_connection(
            config.DB_NAME,
            config.DB_USER,
            config.DB_PASSWORD,
            config.DB_HOST,
            "5432"
        )

        self.cursor = self.connection.cursor()


    def create_connection(self, db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        return connection


    def execute_query(self, query):
        self.connection.autocommit = True
        try:
            self.cursor.execute(query)
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def execute_read_query(self, query):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def create_subscribers_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, 
            telegram_id TEXT NOT NULL UNIQUE 
            )
            """
        self.execute_query(create_table_query)


    def delete_subscribers_table(self):
        delete_table_query = """
        DROP TABLE users
        """
        self.execute_query(delete_table_query)


    def insert_user(self, user_id):
        insert_user_query = (
            f"INSERT INTO users (telegram_id) VALUES ({user_id})"
        )
        self.execute_query(insert_user_query)


    def delete_user(self, user_id):
        delete_user_query = (
            f"DELETE FROM users WHERE telegram_id = '{user_id}'"
        )
        self.execute_query(delete_user_query)


    def get_all(self):
        create_table_query = """
            SELECT telegram_id FROM users
            """
        return self.execute_read_query(create_table_query)


    def close_all(self):
        self.connection.close()
        self.cursor.close()
        print('DB connetion has been closed')
