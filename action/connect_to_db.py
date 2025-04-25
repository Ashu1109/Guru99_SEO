import mysql.connector
from config.db_config import db_config
def connect_to_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    except mysql.connector.Error as err:
        return None, None
    except Exception as e:
        return None, None