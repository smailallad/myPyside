# import mysql.connector
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def get_connection(create_db=False):
#     cnx = mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD")
#     )

#     cursor = cnx.cursor()
#     if create_db:
#         cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
#     cursor.execute(f"USE {os.getenv('DB_NAME')}")

#     return cnx, cursor
#==========
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "stock.db")

# print("📁 Database path:", DB_PATH)

def get_connection():
    # ✅ créer le dossier data/ si absent
    os.makedirs(DATA_DIR, exist_ok=True)

    # ✅ crée stock.db automatiquement s'il n'existe pas
    cnx = sqlite3.connect(DB_PATH)
    cnx.row_factory = sqlite3.Row  # accès par nom
    cnx.execute("PRAGMA foreign_keys = ON")
    cursor = cnx.cursor()

    return cnx,cursor
