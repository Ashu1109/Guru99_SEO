import mysql.connector
def fetch_access_token(cursor):
    get_accesstoken = "SELECT * FROM `access_token`"
    try:
        cursor.execute(get_accesstoken)
        row_result = cursor.fetchone()
        if not row_result:
            return None
        return row_result
    except mysql.connector.Error as err:
        return None
    except Exception as e:
        return None