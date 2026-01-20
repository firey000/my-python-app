import wx
import wx.adv
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, registry
import configparser

from run import StatisticalReport
from run import DetailedReport


config = configparser.ConfigParser()
config.read('config.ini')

if 'database' not in config:
    raise ValueError("Файл config.ini не содержит секции [database]")

DB_USER = config['database']['user']
DB_PASSWORD = config['database']['password']
DB_HOST = config['database']['host']
DB_NAME = config['database']['name']

# Создание движка базы данных
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

# Базовый класс моделей
Base = declarative_base()

# Модели баз данных
class Employees(Base):
    __tablename__ = 'Employees'
    id = Column(Integer, primary_key=True)
    Fcs = Column(String(255))
    Post = Column(String(255))
    Timezone = Column(String(50))

class Project(Base):
    __tablename__ = 'Projects'
    id = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Purpose = Column(String(255))
    Deadline = Column(String(50))

# Класс диалогового окна для добавления проекта
class ProjectDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 400))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Название проекта
        name_label = wx.StaticText(self, label="Название проекта:")
        self.name_input = wx.TextCtrl(self)
        main_sizer.Add(name_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        main_sizer.Add(self.name_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Цель проекта
        goal_label = wx.StaticText(self, label="Цель проекта:")
        self.goal_input = wx.TextCtrl(self)
        main_sizer.Add(goal_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        main_sizer.Add(self.goal_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Дедлайн
        deadline_label = wx.StaticText(self, label="Дедлайн:")
        self.deadline_input = wx.TextCtrl(self)
        main_sizer.Add(deadline_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        main_sizer.Add(self.deadline_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Кнопки
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.Layout()
    
    def GetData(self):
        return {
            "Название проекта": self.name_input.GetValue(),
            "Цель проекта": self.goal_input.GetValue(),
            "Дедлайн": self.deadline_input.GetValue()
        }

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title="Управление распределенной командой", size=(1200, 800))
        self.create_menu()
        self.CreateStatusBar()
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Загрузка данных из базы данных
        self.load_data_from_db()

        self._init_ui()
        self.Centre()
        self.Show()

    def load_data_from_db(self):
        # Получаем данные из базы данных
        self.personnel_data = session.query(Employees).all()
        self.projects_data = session.query(Project).all()

    def save_to_database(self, obj):
        session.add(obj)
        session.commit()

    def _init_ui(self):
        # Левая часть UI
        left_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        # 3 блока с информацией
        squares_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_square = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        data_squares = [
            {"label": "Активных проектов:", "value": len(self.projects_data), "color": "#E0FFFF"},
            {"label": "Кол сотрудников:", "value": len(self.personnel_data), "color": "#F0FFF0"},
            {"label": "Задач на сегодня:", "value": "7", "color": "#FFFACD"}
        ]

        for item in data_squares:
            square_panel = wx.Panel(self.panel, size=(150, 100))
            square_panel.SetBackgroundColour(item["color"])
            square_sizer = wx.BoxSizer(wx.VERTICAL)

            label_text = wx.StaticText(square_panel, label=item["label"])
            label_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            value_text = wx.StaticText(square_panel, label=str(item["value"]))
            value_text.SetFont(font_square)

            square_sizer.Add(label_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)
            square_sizer.Add(value_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
            square_panel.SetSizer(square_sizer)
            squares_sizer.Add(square_panel, 0, wx.ALL | wx.EXPAND, 5)

        left_panel_sizer.Add(squares_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Фильтры для проектов
        projects_filter_box = wx.StaticBox(self.panel, label="Фильтры проектов")
        projects_filter_sizer = wx.StaticBoxSizer(projects_filter_box, wx.VERTICAL)

        self.projects_filters = {}
        project_cols = ['Название проекта', 'Цель проекта', 'Дедлайн']
        grid_filter_projects = wx.FlexGridSizer(rows=len(project_cols), cols=2, vgap=5, hgap=5)

        for col_name in project_cols:
            grid_filter_projects.Add(wx.StaticText(self.panel, label=f"{col_name}:"), 0, wx.ALIGN_CENTER_VERTICAL)
            text_ctrl = wx.TextCtrl(self.panel, size=(200, -1))
            self.projects_filters[col_name] = text_ctrl
            text_ctrl.Bind(wx.EVT_TEXT, self._on_filter_projects)
            grid_filter_projects.Add(text_ctrl, 0, wx.EXPAND)

        projects_filter_sizer.Add(grid_filter_projects, 0, wx.EXPAND | wx.ALL, 5)
        left_panel_sizer.Add(projects_filter_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Таблица проектов
        self.projects_list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES)
        for i, col_name in enumerate(project_cols):
            self.projects_list_ctrl.InsertColumn(i, col_name, width=150)
        self._update_projects_table()
        left_panel_sizer.Add(self.projects_list_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Календарь
        calendar_panel = wx.StaticBox(self.panel, label="Календарь")
        calendar_sizer = wx.StaticBoxSizer(calendar_panel, wx.VERTICAL)
        self.calendar = wx.adv.CalendarCtrl(self.panel, wx.ID_ANY, wx.DateTime.Now(), style=wx.adv.CAL_SHOW_HOLIDAYS)
        calendar_sizer.Add(self.calendar, 1, wx.EXPAND | wx.ALL, 5)
        left_panel_sizer.Add(calendar_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # Правая часть UI
        right_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        # Текущая дата
        date_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.today_date_label = wx.StaticText(self.panel, label=datetime.now().strftime("Сегодня: %d.%m.%Y"))
        self.today_date_label.SetFont(date_font)
        right_panel_sizer.Add(self.today_date_label, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        # Фильтры для персонала
        personnel_filter_box = wx.StaticBox(self.panel, label="Фильтры персонала")
        personnel_filter_sizer = wx.StaticBoxSizer(personnel_filter_box, wx.VERTICAL)

        self.personnel_filters = {}
        personnel_cols = ['ФИО', 'Должность', 'Часовой пояс']
        grid_filter_personnel = wx.FlexGridSizer(rows=len(personnel_cols), cols=2, vgap=5, hgap=5)

        for col_name in personnel_cols:
            grid_filter_personnel.Add(wx.StaticText(self.panel, label=f"{col_name}:"), 0, wx.ALIGN_CENTER_VERTICAL)
            text_ctrl = wx.TextCtrl(self.panel, size=(200, -1))
            self.personnel_filters[col_name] = text_ctrl
            text_ctrl.Bind(wx.EVT_TEXT, self._on_filter_personnel)
            grid_filter_personnel.Add(text_ctrl, 0, wx.EXPAND)

        personnel_filter_sizer.Add(grid_filter_personnel, 0, wx.EXPAND | wx.ALL, 5)
        right_panel_sizer.Add(personnel_filter_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Таблица персонала
        self.personnel_list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES)
        for i, col_name in enumerate(personnel_cols):
            self.personnel_list_ctrl.InsertColumn(i, col_name, width=150)
        self._update_personnel_table()
        right_panel_sizer.Add(self.personnel_list_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        self.main_sizer.Add(left_panel_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.main_sizer.Add(right_panel_sizer, 1, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Layout()

    def _update_personnel_table(self):
        self.personnel_list_ctrl.DeleteAllItems()
    
        filtered_personnel_data = []

        for item in self.personnel_data:
            match = True
            for col_name, filter_ctrl in self.personnel_filters.items():
                filter_text = filter_ctrl.GetValue().lower()
                    
                # Проверяем каждое поле объекта по соответствию фильтру
                field_value = getattr(item, {
                    'ФИО': 'Fcs',
                    'Должность': 'Post',
                    'Часовой пояс': 'Timezone'
                }[col_name])
                if filter_text and filter_text not in field_value.lower():
                    match = False
                    break
                
            if match:
                filtered_personnel_data.append(item)

        # Заполняем ListCtrl правильными значениями
        for i, employee in enumerate(filtered_personnel_data):
            index = self.personnel_list_ctrl.InsertItem(i, employee.Fcs)
            self.personnel_list_ctrl.SetItem(index, 1, employee.Post)
            self.personnel_list_ctrl.SetItem(index, 2, str(employee.Timezone))

    def _on_filter_personnel(self, event):
        self._update_personnel_table()

    def _update_projects_table(self):
        self.projects_list_ctrl.DeleteAllItems()
        filtered_projects_data = []

        for item in self.projects_data:
            match = True
            for col_name, filter_ctrl in self.projects_filters.items():
                filter_text = filter_ctrl.GetValue().lower()
                if filter_text and filter_text not in getattr(item, col_name.lower()).lower():
                    match = False
                    break
            if match:
                filtered_projects_data.append(item)

        for i, project in enumerate(filtered_projects_data):
            index = self.projects_list_ctrl.InsertItem(i, project.Name)
            self.projects_list_ctrl.SetItem(index, 1, project.Purpose)
            self.projects_list_ctrl.SetItem(index, 2, str(project.Deadline))

    def _on_filter_projects(self, event):
        self._update_projects_table()

    def create_menu(self):
        menubar = wx.MenuBar()
        
        # Меню "Сотрудники"
        sotr_menu = wx.Menu()
        sotr_add = sotr_menu.Append(wx.ID_ANY, "&Добавить сотрудника\tCtrl+A", "Добавить сотрудника")
        sotr_edit = sotr_menu.Append(wx.ID_ANY, "&Редактировать инф. о сотруднике\tCtrl+E", "Редактировать информацию о сотруднике")
        sotr_view = sotr_menu.Append(wx.ID_ANY, "Посмотреть список сотрудников\tCtrl+V", "Посмотреть список сотрудников")
        sotr_del = sotr_menu.Append(wx.ID_ANY, "Удалить записи сотрудника\tCtrl+D", "Удалить запись сотрудника")
        menubar.Append(sotr_menu, "Сотрудники")

        # Меню "Администрирование"
        admin_menu = wx.Menu()
        # Подменю "Резервное копирование"
        rezerv_menu = wx.Menu()
        rezerv_full = rezerv_menu.Append(wx.ID_ANY, "Полное резервное копирование", "Сделать резервное копирование всего")
        rezerv_short = rezerv_menu.Append(wx.ID_ANY, "Выборочное резервное копирование", "Сделать резервное копирование того что нужно")
        admin_menu.AppendSubMenu(rezerv_menu, "Резервное копирование", "Сделать резервное копирование")
        
        # Подменю "Проекты"
        project_menu = wx.Menu()
        project_add = project_menu.Append(wx.ID_ANY, "Добавить проект", "Добавить проект")
        project_view = project_menu.Append(wx.ID_ANY, "Посмотреть список проектов", "Посмотреть список проектов")
        project_del = project_menu.Append(wx.ID_ANY, "Удалить проект", "Удалить проект")
        admin_menu.AppendSubMenu(project_menu,"Проекты", "Информация о проектах")

        # Подменю "Задачи"
        task_menu = wx.Menu()
        task_add = task_menu.Append(wx.ID_ANY, "Добавить задачу", "Добавить задачу команде")
        task_view = task_menu.Append(wx.ID_ANY, "Посмотреть задачи", "Посмотреть список задач команды")
        task_del = task_menu.Append(wx.ID_ANY, "Удалить задачу", "Удалить задачу")
        admin_menu.AppendSubMenu(task_menu,"Задачи","Информация о задачах")

        menubar.Append(admin_menu, "Администрирование")

        # Меню "Отчёт"
        otch_menu = wx.Menu()
        otch_exp = otch_menu.Append(wx.ID_ANY, "Экспорт отчётов", "Экспорт отчётов")
        otch_otch = otch_menu.Append(wx.ID_ANY, "Отчёт продуктивности сотрудника", "Посмотреть отчёт продуктивности сотрудника")
        menubar.Append(otch_menu, "Отчёт")

        # Меню "Справка"
        help_menu = wx.Menu()
        help_about = help_menu.Append(wx.ID_ABOUT, "&О программе", "Информация о программе")
        help_exit = help_menu.Append(wx.ID_EXIT, "&Выход\tCtrl+Q", "Выход из программы")
        menubar.Append(help_menu, "&Справка")

        self.SetMenuBar(menubar)
        
        # Привязываем события
        self.Bind(wx.EVT_MENU, self.on_exit, help_exit)
        self.Bind(wx.EVT_MENU, self.on_about, help_about)
        
        self.Bind(wx.EVT_MENU, self.on_add_employee, sotr_add)
        self.Bind(wx.EVT_MENU, self.on_edit_employee, sotr_edit)
        self.Bind(wx.EVT_MENU, self.on_view, sotr_view)
        self.Bind(wx.EVT_MENU, self.on_delete_employee, sotr_del)
        
        self.Bind(wx.EVT_MENU, self.on_export_reports, otch_exp)
        

        # Новое событие для добавления проекта
        self.Bind(wx.EVT_MENU, self.on_add_project, project_add)

    def on_export_reports(self, event):
        """Обработчик события экспорта отчётов."""
        # Генерируем статистический отчёт
        stat_report_generator = StatisticalReport()
        stat_report_generator.generate_statistical_report()
        
        # Генерируем детальный отчёт
        detail_report_generator = DetailedReport()
        detail_report_generator.generate_detailed_report()
        
        # Сообщаем пользователю о завершении процесса
        wx.MessageBox("Отчёты успешно экспортированы.", "Экспорт завершён", wx.OK | wx.ICON_INFORMATION)

    def on_add_project(self, event):
        # Открываем окно добавления проекта
        add_dialog = ProjectDialog(self, title="Добавление нового проекта")
        if add_dialog.ShowModal() == wx.ID_OK:
            new_project = add_dialog.GetData()
            project_obj = Project(
                Name=new_project["Название проекта"],
                Purpose=new_project["Цель проекта"],
                Deadline=new_project["Дедлайн"]
            )
            self.save_to_database(project_obj)  # Сохраняем новый проект в базу данных
            self.load_data_from_db()  # Обновляем данные
            self._update_projects_table()  # Обновляем интерфейс
        add_dialog.Destroy()

    def on_add_employee(self, event):
        add_dialog = AddEmployeeDialog(self)
        if add_dialog.ShowModal() == wx.ID_OK:
            new_employee = add_dialog.GetData()
            employee_obj = Employees(Fcs=new_employee["ФИО"], Post=new_employee["Должность"], Timezone=new_employee["Часовой пояс"])
            self.save_to_database(employee_obj)  # Сохраняем нового сотрудника в базу данных
            self.load_data_from_db()  # Обновляем данные
            self._update_personnel_table()  # Обновляем интерфейс
        add_dialog.Destroy()

    def on_edit_employee(self, event):
        select_dialog = SelectEmployeeDialog(self, self.personnel_data)
        if select_dialog.ShowModal() == wx.ID_OK:
            selected_employee = select_dialog.GetSelectedEmployee()
            if selected_employee is not None:
                edit_dialog = EditEmployeeDialog(self, selected_employee)
                if edit_dialog.ShowModal() == wx.ID_OK:
                    edited_data = edit_dialog.GetEditedData()

                    # Обновляем данные в базе
                    selected_employee.Fcs = edited_data["ФИО"]
                    selected_employee.Post = edited_data["Должность"]
                    selected_employee.Timezone = edited_data["Часовой пояс"]

                    self.save_to_database(selected_employee)  # Сохраняем изменения
                    self.load_data_from_db()  # Обновляем данные
                    self._update_personnel_table()  # Обновляем интерфейс
                edit_dialog.Destroy()
        select_dialog.Destroy()

    def on_delete_employee(self, event):
        del_dialog = DeleteEmployeeDialog(self, self.personnel_data)
        if del_dialog.ShowModal() == wx.ID_DELETE:
            selected_employee = del_dialog.GetSelectedEmployee()
            if selected_employee is not None:
                session.delete(selected_employee)
                session.commit()
                self.load_data_from_db()
                self._update_personnel_table()
        del_dialog.Destroy()
        

    def on_view(self, event):
        print("Список сотрудников открыт.")

    def on_del(self, event):
        print("Запрошено удаление сотрудника.")

    def on_exit(self, event):
        self.Close()

    def on_about(self, event):
        wx.MessageBox("Программа создана Михайловым Данилом.", "О программе")

        

class AddEmployeeDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Добавление нового сотрудника", size=(800, 300))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ФИО
        first_last_middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        first_label = wx.StaticText(self, label="Имя:")
        last_label = wx.StaticText(self, label="Фамилия:")
        middle_label = wx.StaticText(self, label="Отчество:")
        
        self.first_input = wx.TextCtrl(self)
        self.last_input = wx.TextCtrl(self)
        self.middle_input = wx.TextCtrl(self)
        
        first_last_middle_sizer.Add(first_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.first_input, 1, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(last_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.last_input, 1, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(middle_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.middle_input, 1, wx.RIGHT|wx.LEFT, 5)
        
        main_sizer.Add(first_last_middle_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        # Должность
        position_label = wx.StaticText(self, label="Должность:")
        self.position_input = wx.TextCtrl(self)
        main_sizer.Add(position_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        main_sizer.Add(self.position_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Часовой пояс
        timezone_label = wx.StaticText(self, label="Часовой пояс:")
        self.timezone_input = wx.TextCtrl(self)
        main_sizer.Add(timezone_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        main_sizer.Add(self.timezone_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Кнопки
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()
        
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.Layout()
    
    def GetData(self):
        return {
            "ФИО": f"{self.first_input.GetValue()} {self.last_input.GetValue()} {self.middle_input.GetValue()}",
            "Должность": self.position_input.GetValue(),
            "Часовой пояс": self.timezone_input.GetValue()
        }

class SelectEmployeeDialog(wx.Dialog):
    def __init__(self, parent, employees):
        super().__init__(parent, title="Выберите сотрудника для редактирования")
        self.employees = employees
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Выбор сотрудника
        self.listbox = wx.ListBox(self, choices=[employee.Fcs for employee in employees], size=(300, 200))
        sizer.Add(self.listbox, 1, wx.EXPAND|wx.ALL, 5)
        
        # Кнопки
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
    
    def GetSelectedEmployee(self):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            return self.employees[selection]
        else:
            return None




class EditEmployeeDialog(wx.Dialog):
    def __init__(self, parent, employee):
        """
        Инициализирует диалоговое окно для редактирования сотрудника.
        :param parent: Родительский фрейм.
        :param employee: Объект сотрудника, который будем редактировать.
        """
        super().__init__(parent, title="Редактирование сотрудника", size=(700, 400))
        self.employee = employee
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ФИО
        first_last_middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        first_label = wx.StaticText(self, label="Имя:")
        last_label = wx.StaticText(self, label="Фамилия:")
        middle_label = wx.StaticText(self, label="Отчество:")
        
        # Парсим ФИО на отдельные компоненты
        names = employee.Fcs.split()
        self.first_input = wx.TextCtrl(self, value=names[0])
        self.last_input = wx.TextCtrl(self, value=names[1])
        self.middle_input = wx.TextCtrl(self, value=names[2])
        
        first_last_middle_sizer.Add(first_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.first_input, 1, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(last_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.last_input, 1, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(middle_label, 0, wx.RIGHT|wx.LEFT, 5)
        first_last_middle_sizer.Add(self.middle_input, 1, wx.RIGHT|wx.LEFT, 5)
        
        sizer.Add(first_last_middle_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        # Должность
        position_label = wx.StaticText(self, label="Должность:")
        self.position_input = wx.TextCtrl(self, value=employee.Post)
        sizer.Add(position_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer.Add(self.position_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Часовой пояс
        timezone_label = wx.StaticText(self, label="Часовой пояс:")
        self.timezone_input = wx.TextCtrl(self, value=str(employee.Timezone))
        sizer.Add(timezone_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer.Add(self.timezone_input, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Кнопки
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
    
    def GetEditedData(self):
        """Возвращает измененные данные сотрудника."""
        return {
            "ФИО": f"{self.first_input.GetValue()} {self.last_input.GetValue()} {self.middle_input.GetValue()}",
            "Должность": self.position_input.GetValue(),
            "Часовой пояс": self.timezone_input.GetValue()
        }

class DeleteEmployeeDialog(wx.Dialog):
    def __init__(self, parent, employees):
        super().__init__(parent, title="Удаление сотрудника")
        self.parent = parent  # Хранит ссылку на родительский экземпляр (MyFrame)
        self.employees = employees
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Список сотрудников
        listbox_label = wx.StaticText(self, label="Выберите сотрудника для удаления:")
        self.listbox = wx.ListBox(self, choices=[emp.Fcs for emp in employees])
        main_sizer.Add(listbox_label, 0, wx.ALL, 5)
        main_sizer.Add(self.listbox, 1, wx.EXPAND|wx.ALL, 5)
        
        # Кнопки
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        delete_button = wx.Button(self, wx.ID_DELETE, label="Удалить")
        cancel_button = wx.Button(self, wx.ID_CANCEL, label="Отмена")
        buttons_sizer.Add(delete_button, 0, wx.RIGHT, 5)
        buttons_sizer.Add(cancel_button, 0, wx.LEFT, 5)
        main_sizer.Add(buttons_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.Layout()
        
        # Обработчик нажатия на кнопку "Удалить"
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_employee)
    
    def GetSelectedEmployee(self):
        idx = self.listbox.GetSelection()
        if idx != wx.NOT_FOUND:
            return self.employees[idx]
        return None
    
    def on_delete_employee(self, event):
        selected_employee = self.GetSelectedEmployee()
        if selected_employee is not None:
            confirm_msg = f"Вы уверены, что хотите удалить сотрудника '{selected_employee.Fcs}'?"
            answer = wx.MessageBox(confirm_msg, "Подтверждение удаления", wx.YES_NO|wx.ICON_WARNING)
            
            if answer == wx.YES:
                try:
                    session.delete(selected_employee)
                    session.commit()
                    
                    # Обновляем данные в родительском окне
                    self.parent.load_data_from_db()
                    self.parent.update_personnel_table()
                    
                    # Сообщаем пользователю
                    wx.MessageBox("Сотрудник успешно удалён.", "Удалено", wx.OK|wx.ICON_INFORMATION)
                    
                    # Закрываем диалог
                    self.EndModal(wx.ID_DELETE)
                except Exception as e:
                    wx.MessageBox(f"Произошла ошибка при удалении: {str(e)}", "Ошибка", wx.OK|wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, "Панель управления")
    app.MainLoop()
