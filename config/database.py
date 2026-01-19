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
