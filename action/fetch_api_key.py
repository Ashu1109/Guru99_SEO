from action.connect_to_db import connect_to_db
import pandas as pd
def fetch_api_key():
    try:
        conn,cursor = connect_to_db()
        cursor.execute("SELECT * FROM API;")
        data = cursor.fetchall()
        if data:
            api_key = data[0]["api_key"]
            return api_key
        else:
            print("No API key found in the database.")
        return None
    except Exception as e:
        print(f"Error fetching API key: {e}")
        return None
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()


def clear_api_key_db():
    try:
        
        conn,cursor = connect_to_db()
        cursor.execute("DELETE FROM API;")
        conn.commit()
        print("API key cleared from the database.")
    except Exception as e:
        print(f"Error clearing API key: {e}")
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
            
def set_api_key_db(openai_api_key):
    try:
        conn,cursor = connect_to_db()
        cursor.execute("INSERT INTO API (api_key) VALUES (%s);", (openai_api_key,))
        conn.commit()
        print("API key set in the database.", openai_api_key)
    except Exception as e:
        print(f"Error setting API key: {e}")
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()