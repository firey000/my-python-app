import mysql.connector
from config import DATABASE_CONFIG

def execute_sql_query(query):
    """
    Выполняет SQL-запрос и возвращает результат.
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")
        return []
    finally:
        if connection:
            connection.close()
