
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

database =mysql.connector.connect(
        host='bvlts1sjujv3nvfvmtv6-mysql.services.clever-cloud.com',
        port='3306',
        user='u8ibzlg4rsrl8tqc',
        password='cL5h8aX7EJEsu6TpBhvs',
        database='bvlts1sjujv3nvfvmtv6'
    )
