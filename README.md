# Python приложения для управления распределенной командой

Проект демонстрирует интеграцию Python с MySQL, обеспечивает простое управление данными и аутентификацию.


## О проекте

Проект позволяет управлять распределенной командой, а точнее создавать и изменять проекты, задачи для сотрудников и сами записи сотрудников


## Оглавление

 

- [Особенности](#особенности)

- [Требования](#требования)

- [Установка](#установка)

- [Конфигурация](#конфигурация)

- [Использование](#использование)

- [Структура проекта](#структура-проекта)

- [Разработка и тестирование](#Разработка-и-тестирование)

 

## Особенности

 

- Поддержка Python 3.8+

- Интеграция с MySQL 8.0

- Асинхронные операции

- Логирование

- Конфигурация через переменные окружения

 

## Требования

 

### Системные требования

- **OS**: Debian 10/11/12, Ubuntu 20.04+

- **Python**: 3.8 или выше

- **MySQL**: 8.0 или выше

 

### Зависимости Python

Смотрите `requirements.txt`


### Установка:

#### 1. Клонируйте репозиторий:

 bash

 git clone https://github.com/ВАШ_USERNAME/my-python-app.git

#### 2. Активируйте виртуальное окружение:

 bash

 python3 -m venv env

 source env/bin/activate

#### 3. Установите зависимости:

 bash

 pip install -r requirements.txt

#### 4. Настройте базу данных:
 bash

 sudo apt-get install mysql-server mysql-client



### Создайте базу данных и пользователя MySQL вручную либо автоматически с помощью скрипта миграции.

#### Вручную:

 sudo apt update

 sudo apt install mysql-server mysql-client -y

 sudo systemctl start mysql

 sudo systemctl enable mysql

 

### Создание базы данных и пользователя

 sudo mysql -u root -p

 

#### В MySQL CLI:

 CREATE DATABASE myapp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

 CREATE USER 'myapp_user'@'localhost' IDENTIFIED BY 'secure_password';

 GRANT ALL PRIVILEGES ON myapp_db.* TO 'myapp_user'@'localhost';

 FLUSH PRIVILEGES;

 EXIT;


#### 5. Используйте `.env.example`, чтобы создать `.env` с параметрами доступа к базе данных.


#### 6.Инициализируйте базу данных:
 
 python src/database/init_db.py



### Конфигурация

#### Файл .env:

 env

##### Database

 DB_HOST=localhost

 DB_PORT=3306

 DB_NAME=myapp_db

 DB_USER=myapp_user

 DB_PASSWORD=secure_password

 DB_CHARSET=utf8mb4

 

##### App

 DEBUG=False

 SECRET_KEY=your-secret-key-here

 LOG_LEVEL=INFO

 

##### API

 API_HOST=0.0.0.0
 
 API_PORT=8000

 
### Конфигурационный файл

#### python:

 config/database.py

 import os

 from dotenv import load_dotenv

 

 load_dotenv()

 

 DATABASE_CONFIG = {

    'host': os.getenv('DB_HOST', 'localhost'),

    'port': int(os.getenv('DB_PORT', 3306)),

    'database': os.getenv('DB_NAME'),

    'user': os.getenv('DB_USER'),

    'password': os.getenv('DB_PASSWORD'),

    'charset': os.getenv('DB_CHARSET', 'utf8mb4')

 }


## Использование


Начните работу:

 bash

 python src/main.py



## Структура проекта


my-python-app/

├── src/                    # Исходный код

│   ├── __init__.py

│   ├── main.py            # Точка входа

│   ├── models/            # Модели данных

│   ├── database/          # Работа с БД

│   │   ├── __init__.py

│   │   ├── connection.py  # Подключение к MySQL

│   │   └── queries.py     # SQL запросы

│   ├── api/               # API endpoints

│   └── utils/             # Вспомогательные функции

├── config/                # Конфигурация

│   ├── __init__.py

│   └── database.py

├── database/

│   └── migrations/        # Миграции БД

├── docs/                  # Документация

├── requirements.txt       # Зависимости Python

├── .env.example          # Шаблон переменных окружения

├── .gitignore

└── README.md




Используйте файл `requirements.txt` для управления зависимостями:

 bash

 mysql-connector-python==8.0.33

 SQLAlchemy==2.0.19

 python-dotenv==1.0.0

 Flask==3.0.0

 Flask-SQLAlchemy==3.1.1

 pytest==7.4.3


## Разработка и тестирование

pytest==7.4.3

pytest-cov==4.1.0

black==23.11.0

flake8==6.1.0

isort==5.12.0

mypy==1.7.0

