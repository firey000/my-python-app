from .base_report import BaseReport
from utils.db_utils import execute_sql_query

class TableReport(BaseReport):
    def __init__(self):
        super().__init__('Детальная информация')
        self.data = self.fetch_details()

    def fetch_details(self):
        # Получаем подробную информацию из базы данных
        results = execute_sql_query("""
            SELECT u.username, o.amount, o.order_id
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            LIMIT 10
        """)
        return results

    def render_html(self):
        from jinja2 import Template
        template_path = Path(__file__).parent.parent.joinpath('templates', 'details.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        return super().render_html(template)
