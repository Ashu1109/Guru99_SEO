import mysql.connector
# Function to refresh the access token
def refresh_token(conn, cursor, new_access_token, row_result):
    try:
        update_query = "UPDATE `access_token` SET `access_token` = %s WHERE id = %s"
        cursor.execute(update_query, (new_access_token, row_result["id"]))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        return None