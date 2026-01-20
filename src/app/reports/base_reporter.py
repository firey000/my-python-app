from abc import ABC, abstractmethod
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML
from pathlib import Path

class BaseReporter(ABC):
    def __init__(self, title='отчет', data=None):
        self.title = title
        self.data = data or {}

    @abstractmethod
    def render_html(self):
        pass

    def generate_pdf(self, html_content, filename):
        pdf_path = Path(filename).with_suffix('.pdf')
        HTML(string=html_content).write_pdf(str(pdf_path))
        print(f"PDF report generated at {pdf_path}")

    def render_html(self, template):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = template.render(title=self.title, data=self.data, current_time=now)
        return content
