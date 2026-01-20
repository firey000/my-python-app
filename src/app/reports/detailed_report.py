# detailed_report.py
from .base_reporter import BaseReporter
from database.queries import connect_to_database
from datetime import datetime, date


class DetailedReport(BaseReporter):
    def generate_detailed_report(self):
        """Генерирует красивый подробный PDF-отчёт с актуальными данными"""
        
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # 1. Сотрудники
        cursor.execute("SELECT Fcs AS full_name, Post AS position FROM Employees ORDER BY Fcs")
        employees = cursor.fetchall()

        # 2. Задачи сотрудников — берём из Productivity_Report (там есть данные!)
        cursor.execute("""
            SELECT 
                e.Fcs AS employee_name,
                t.purpose AS task_purpose,
                ts.name AS status_name
            FROM Productivity_Report pr
            JOIN Employees e ON pr.employee_id = e.id
            JOIN Tasks t ON pr.task_id = t.id
            JOIN Task_status ts ON pr.status = ts.id
            ORDER BY e.Fcs, t.purpose
        """)
        tasks = cursor.fetchall()

        # 3. Проекты
        cursor.execute("SELECT Name AS project_name, Purpose AS purpose, Deadline AS deadline FROM Project ORDER BY Deadline")
        projects = cursor.fetchall()

        cursor.close()
        connection.close()

        # Функция разбивки на страницы
        def paginate(data, size=10):
            return [data[i:i + size] for i in range(0, len(data), size)]

        employee_pages = paginate(employees)
        task_pages = paginate(tasks)
        project_pages = paginate(projects)

        today = datetime.now().strftime("%d.%m.%Y в %H:%M")

        # Вспомогательная функция для красивого статуса
        def format_status(status_name):
            if status_name == "Готова":
                return f'<span style="color:#27ae60; font-weight:bold;">{status_name}</span>'
            elif status_name == "Отменена":
                return f'<span style="color:#c0392b; font-weight:bold;">{status_name}</span>'
            else:
                return status_name

        # === HTML ===
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Подробный отчёт по компании</title>
    <style>
        body {{ font-family: "DejaVu Sans", "Segoe UI", Arial, sans-serif; margin:40px; line-height:1.6; color:#333; }}
        h1 {{ color:#2c3e50; text-align:center; }}
        h2 {{ color:#2980b9; border-bottom:3px solid #3498db; padding-bottom:8px; margin-top:60px; }}
        table {{ width:100%; border-collapse:collapse; margin:25px 0; font-size:15px; }}
        th {{ background:#3498db; color:white; padding:12px; text-align:left; }}
        td {{ padding:10px 12px; border-bottom:1px solid #ddd; }}
        tr:nth-child(even) {{ background:#f9f9f9; }}
        tr:hover {{ background:#f0f8ff; }}
        .pagination {{ text-align:center; margin:40px 0; }}
        .page-btn {{ display:inline-block; width:44px; height:44px; line-height:44px; margin:0 6px;
                     background:#3498db; color:white; text-decoration:none; border-radius:10px;
                     font-weight:bold; }}
        .page-btn:hover {{ background:#2980b9; }}
        .page-btn.active {{ background:#e74c3c; }}
        .cover, .toc {{ page-break-after:always; text-align:center; padding-top:100px; }}
        .date {{ font-size:19px; color:#7f8c8d; margin:30px 0; }}
    </style>
</head>
<body>

<div class="cover">
    <h1>Подробный отчёт по компании</h1>
    <p class="date">Сформирован {today}</p>
</div>

<div class="toc">
    <h2>Содержание</h2>
    <ol style="font-size:20px; line-height:2.5;">
        <li><a href="#employees">Сотрудники</a></li>
        <li><a href="#tasks">Задачи сотрудников</a></li>
        <li><a href="#projects">Проекты</a></li>
    </ol>
</div>

<!-- СОТРУДНИКИ -->
<section id="employees">
    <h2>Сотрудники компании</h2>
    {self._make_table(
        headers=["ФИО", "Должность"],
        rows=[[e["full_name"], e["position"]] for page in employee_pages for e in page],
        section="employees"
    )}
</section>

<!-- ЗАДАЧИ -->
<section id="tasks">
    <h2>Задачи сотрудников</h2>
    {self._make_table(
        headers=["Сотрудник", "Задача", "Статус", "Проект"],
        rows=[[t["employee_name"], t["task_purpose"], format_status(t["status_name"]), "—"] 
              for page in task_pages for t in page],
        section="tasks"
    )}
</section>

<!-- ПРОЕКТЫ -->
<section id="projects">
    <h2>Текущие проекты</h2>
    {self._make_table(
        headers=["Название", "Цель (кратко)", "Дедлайн"],
        rows=[[p["project_name"],
               (p["purpose"][:140] + "..." if len(p["purpose"]) > 140 else p["purpose"]),
               p["deadline"].strftime("%d.%m.%Y") if isinstance(p["deadline"], date) else p["deadline"]]
              for page in project_pages for p in page],
        section="projects"
    )}
</section>

<script>
function showPage(section, n) {{
    const rows = document.querySelectorAll('#' + section + '-table tbody tr');
    const size = 10;
    rows.forEach((r, i) => r.style.display = (i >= n*size && i < (n+1)*size) ? '' : 'none');
    document.querySelectorAll('#' + section + '-pagination .page-btn')
            .forEach((b, i) => b.className = 'page-btn' + (i===n ? ' active' : ''));
}}
document.addEventListener('DOMContentLoaded', () => {{
    ['employees','tasks','projects'].forEach(s => showPage(s, 0));
}});
</script>

</body>
</html>"""

        self.generate_pdf(html_content, "detailed_report.pdf")
        print("Отчёт успешно создан: detailed_report.pdf")

    def _make_table(self, headers, rows, section, page_size=10):
        if not rows:
            return '<p style="text-align:center; color:#95a5a6; font-style:italic;">Нет данных</p>'

        total_pages = (len(rows) + page_size - 1) // page_size

        table = f'''
        <table id="{section}-table">
            <thead><tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr></thead>
            <tbody>
                {''.join(f"<tr>{"".join(f"<td>{c}</td>" for c in row)}</tr>" for row in rows)}
            </tbody>
        </table>'''

        if total_pages > 1:
            buttons = ''.join(
                f'<a href="#" class="page-btn" onclick="showPage(\'{section}\',{i});return false;">{i+1}</a>'
                for i in range(total_pages)
            )
            table += f'<div id="{section}-pagination" class="pagination">{buttons}</div>'

        return table
