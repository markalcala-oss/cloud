import os
import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db_cursor():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),       # Aquí irá la IP Privada de EC2-DB
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor(dictionary=True)
        yield connection, cursor
        connection.commit()
    except mysql.connector.Error as err:
        if connection:
            connection.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()