from action.connect_to_db import connect_to_db
import pandas as pd
def fetch_api_key():
    try:
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            print("Failed to connect to database")
            return None
            
        cursor.execute("SELECT * FROM API;")
        data = cursor.fetchall()
        if data:
            api_key = data[0]["api_key"]
            # Set the API key in memory and environment
            from action.set_api_key import set_api_key
            set_api_key(api_key)
            print(f"API key successfully loaded from database")
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
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            print("Failed to connect to database")
            return
            
        # First, check if this API key already exists
        cursor.execute("SELECT * FROM API WHERE api_key = %s;", (openai_api_key,))
        existing_key = cursor.fetchone()
        
        if existing_key:
            print("API key already exists in the database")
            return
            
        # Clear any existing API keys to avoid multiple keys
        clear_api_key_db()
        
        # Insert the new API key
        cursor.execute("INSERT INTO API (api_key) VALUES (%s);", (openai_api_key,))
        conn.commit()
        print("API key set in the database.")
    except Exception as e:
        print(f"Error setting API key: {e}")
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()