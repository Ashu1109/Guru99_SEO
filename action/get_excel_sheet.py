from action.connect_to_db import connect_to_db
import pandas as pd
def get_excel_sheet():
    conn, cursor = connect_to_db()
    if conn and cursor:
        # Fetch the data from the excel_sheet table
        query = "SELECT * FROM excel_sheet ORDER BY id DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        
        # Check if data is empty
        if not data:
            return None
        
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return data
    else:
        return None