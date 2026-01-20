import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from weasyprint import HTML
from io import BytesIO
from base64 import b64encode
from .base_reporter import BaseReporter
from database.queries import connect_to_database
from datetime import datetime

class StatisticalReport(BaseReporter):
    def generate_statistical_report(self):
        """
        Генерирует статистический отчёт с общей информацией о сотрудниках, задачах и проектах,
        а также круговой диаграммой и рейтингом лучших сотрудников.
        """
        
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
    
        # Запрашиваем общую статистику
        cursor.execute("SELECT COUNT(*) AS count FROM Employees")
        total_employees = cursor.fetchone()['count']
    
        cursor.execute("SELECT COUNT(*) AS count FROM Tasks")
        total_tasks = cursor.fetchone()['count']
    
        cursor.execute("SELECT COUNT(*) AS count FROM Project")
        total_projects = cursor.fetchone()['count']
    
        # Получаем распределение задач по статусам
        cursor.execute("""
            SELECT ts.name AS status_name, COUNT(*) AS task_count
            FROM Employee_Tasks et
            JOIN Task_status ts ON et.status_id = ts.id
            GROUP BY ts.name
        """)
        task_statuses = cursor.fetchall()
    
        # Получаем топ-5 сотрудников с наибольшим количеством выполненных задач
        cursor.execute("""
            SELECT e.Fcs, COUNT(et.task_id) AS completed_tasks
            FROM Employees e
            JOIN Productivity_Report pr ON e.id = pr.employee_id AND pr.status = 2
            JOIN Employee_Tasks et ON pr.task_id = et.task_id
            GROUP BY e.id
            ORDER BY completed_tasks DESC LIMIT 5
        """)
        top_employees = cursor.fetchall()
    
        # Закрываем подключение
        cursor.close()
        connection.close()
    
        # Готовим данные для круговой диаграммы
        df = pd.DataFrame(task_statuses)
        labels = df['status_name']
        sizes = df['task_count']
        colors = ['#FFC0CB', '#ADD8E6', '#BADA55']  # Цвета секторов
    
        # Рисуем круговую диаграмму
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Распределение задач по статусам')
        plt.tight_layout()
    
        # Сохраняем диаграмму в память
        pie_chart_buffer = BytesIO()
        plt.savefig(pie_chart_buffer, format="png")
        plt.close()
        pie_chart_base64 = b64encode(pie_chart_buffer.getvalue()).decode('utf-8')
    
        # Формирование HTML-кода отчета
        html_content = f"""
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Статистический отчет</title>
            <style>
                body {{
                    font-family: Arial, Helvetica, sans-serif;
                    line-height: 1.6;
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                }}
                .title-page {{
                    page-break-after: always;
                }}
                img {{
                    display: block;
                    margin: auto;
                    max-width: 100%;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                thead {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <!-- Титульная страница -->
            <section class="title-page">
                <h1>Статистический отчет</h1>
                <h1>Управление распределенной командой</h1>
                <p>Автор: Система отчетности</p>
                <p>Дата формирования отчета: {datetime.now().strftime('%d.%m.%Y')}</p>
            </section>
        
            <!-- Основная статистика -->
            <section>
                <h2>Общая статистика</h2>
                <ul>
                    <li>Количество сотрудников: {total_employees}</li>
                    <li>Количество задач: {total_tasks}</li>
                    <li>Количество проектов: {total_projects}</li>
                </ul>
                
                <!-- Круговая диаграмма -->
                <img src="data:image/png;base64,{pie_chart_base64}" alt="Круговая диаграмма задач"/>
            
                <!-- Топ сотрудников -->
                <h2>Топ сотрудников по количеству выполненых задач:</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ФИО</th>
                            <th>Кол-во задач</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for emp in top_employees:
            html_content += f"""
                <tr>
                    <td>{emp['Fcs']}</td>
                    <td>{emp['completed_tasks']}</td>
                </tr>
            """
        html_content += """
                    </tbody>
                </table>
            </section>
        </body>
        </html>
        """
    
        # Конвертация HTML в PDF
        HTML(string=html_content).write_pdf("statistical_report.pdf")
        print("Отчет успешно создан: statistical_report.pdf")
