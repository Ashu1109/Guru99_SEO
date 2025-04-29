from action.connect_to_db import connect_to_db
def get_all_link(id):
    conn, cursor = connect_to_db()
    if conn and cursor:
        # Fetch the data from the excel_sheet table
        query = f"SELECT * FROM link_analysis WHERE excel_sheet_id = {id} "
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
