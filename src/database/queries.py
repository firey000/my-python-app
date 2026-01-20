import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host="pma.mikhailov.info",
        user="phpmyadmin",
        password="0907",
        database="phpmyadmin"
    )
    return connection

# Пример запросов
def fetch_employees(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    cursor.close()
    return employees

def fetch_projects(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Project")
    projects = cursor.fetchall()
    cursor.close()
    return projects

# database/queries.py

def fetch_tasks(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Employee_Tasks;")
    return cursor.fetchall()

def fetch_tasks_with_details(connection):
    try:
        with connection.cursor() as cursor:
            # Используем JOIN для соединения трех таблиц
            sql_query = """
                SELECT 
                    E.Fcs AS Employee_Name,
                    TS.name AS Task_Status,
                    T.Goal AS Task_Goal
                FROM Tasks T
                INNER JOIN Employees E ON T.employee_id = E.id
                INNER JOIN Task_status TS ON T.status_id = TS.id;
            """
            cursor.execute(sql_query)
            
            # Возвращаем список объектов
            tasks = cursor.fetchall()
            
            return tasks
    
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
