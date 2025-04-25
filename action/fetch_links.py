import mysql.connector
# Function to fetch links from database
def fetch_links(cursor):
    get_link = "SELECT * FROM `links`"
    try:
        cursor.execute(get_link)
        row_result = cursor.fetchall()
        if not row_result:
            return None
        return row_result
    except mysql.connector.Error as err:
        
        return None
    except Exception as e:
        return None