import streamlit as st
import pandas as pd
from action.get_processed_array import access_token
from test import get_filtered_links 
from action.connect_to_db import connect_to_db
st.write("create table")




def get_data():
    st.write(get_filtered_links())
    
st.button("info Table", on_click=get_data)
# def info_table():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         cursor.execute("SHOW TABLES;")
#         tables = cursor.fetchall()
#         if tables:
#             st.write("Tables in the database:")
#             for table in tables:
#                 # Handle dict or tuple row format
#                 if isinstance(table, dict):
#                     table_name = list(table.values())[0]
#                 elif isinstance(table, (list, tuple)) and len(table) > 0:
#                     table_name = table[0]
#                 else:
#                     st.write("Unexpected table format: ", table)
#                     continue
#                 st.subheader(f"Table: {table_name}")
#                 cursor.execute(f"DESCRIBE `{table_name}`;")
#                 schema = cursor.fetchall()
#                 columns = [desc[0] for desc in cursor.description]
#                 df = pd.DataFrame(schema, columns=columns)
#                 st.dataframe(df)
#         else:
#             st.write("No tables found in the database.")
#     else:
#         st.error("Failed to connect to the database")


# def create_table():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         table_name = "excel_sheet"
#         if table_name:
#             try:
#                 create_query = f"""
#                 CREATE TABLE IF NOT EXISTS `{table_name}` (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     name VARCHAR(255) NOT NULL,
#                     created_date DATETIME DEFAULT CURRENT_TIMESTAMP
#                 );
#                 """
#                 cursor.execute(create_query)
#                 conn.commit()
#                 st.success(f"Table `{table_name}` created successfully.")

#                 # Create link_analysis table if not exists, with foreign key to the above table
#                 link_analysis_query = f"""
#                 CREATE TABLE IF NOT EXISTS link_analysis (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     {table_name}_id INT,
#                     link VARCHAR(500),
#                     title VARCHAR(500),
#                     query_data TEXT,
#                     clicks_of_words INT,
#                     top15 TEXT,
#                     GSC_top_KW TEXT,
#                     suggested_title_1 VARCHAR(500),
#                     suggested_title_2 VARCHAR(500),
#                     response TEXT,
#                     FOREIGN KEY ({table_name}_id) REFERENCES `{table_name}`(id)
#                 );
#                 """
#                 cursor.execute(link_analysis_query)
#                 conn.commit()
#                 st.success("Table `link_analysis` created/updated successfully.")
#             except Exception as e:
#                 st.error(f"Error creating tables: {e}")
#         else:
#             st.warning("Please enter a table name.")
#     else:
#         st.error("Failed to connect to the database")


# def update_schema():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         table_name = "excel_sheet"
#         try:
#             # Check if created_date exists
#             cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'created_date';")
#             result = cursor.fetchone()
#             if not result:
#                 alter_query = f"ALTER TABLE `{table_name}` ADD COLUMN created_date DATETIME DEFAULT CURRENT_TIMESTAMP;"
#                 cursor.execute(alter_query)
#                 conn.commit()
#                 st.success("'created_date' column added to excel_sheet table.")
#             else:
#                 st.info("'created_date' column already exists.")
#         except Exception as e:
#             st.error(f"Error updating schema: {e}")
#     else:
#         st.error("Failed to connect to the database")


# def fetch_data():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         table_name = "excel_sheet"
#         try:
#             fetch_query = f"SELECT * FROM `{table_name}`;"
#             cursor.execute(fetch_query)
#             data = cursor.fetchall()
#             columns = [desc[0] for desc in cursor.description]
#             df = pd.DataFrame(data, columns=columns)
#             # Fetch link_analysis table as well
#             try:
#                 link_analysis_query = "SELECT * FROM link_analysis;"
#                 cursor.execute(link_analysis_query)
#                 link_analysis_data = cursor.fetchall()
#                 link_analysis_columns = [desc[0] for desc in cursor.description]
#                 link_analysis_df = pd.DataFrame(link_analysis_data, columns=link_analysis_columns)
#                 st.subheader("link_analysis Table")
#                 st.dataframe(link_analysis_df)
#             except Exception as e:
#                 st.error(f"Error fetching link_analysis data: {e}")
#             st.dataframe(df)
#         except Exception as e:
#             st.error(f"Error fetching data: {e}")
#     else:
#         st.error("Failed to connect to the database")
#     st.write("Connected to database successfully")


# def remove_query_data_column():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         try:
#             alter_query = "ALTER TABLE link_analysis DROP COLUMN query_data;"
#             cursor.execute(alter_query)
#             conn.commit()
#             st.success("'query_data' column removed from link_analysis table.")
#         except Exception as e:
#             st.error(f"Error removing column: {e}")
#     else:
#         st.error("Failed to connect to the database")


# st.button("info Table", on_click=info_table)

# st.button("Create Table", on_click=create_table)

# st.button("Update Schema", on_click=update_schema)

# st.button("Fetch Data", on_click=fetch_data)

# st.button("Remove query_data column", on_click=remove_query_data_column)

# def update_clicks_of_words_to_text():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         try:
#             alter_query = "ALTER TABLE link_analysis MODIFY COLUMN clicks_of_words TEXT;"
#             cursor.execute(alter_query)
#             conn.commit()
#             st.success("'clicks_of_words' column type updated to TEXT in link_analysis table.")
#         except Exception as e:
#             st.error(f"Error updating column type: {e}")
#     else:
#         st.error("Failed to connect to the database")

# st.button("Update clicks_of_words to TEXT", on_click=update_clicks_of_words_to_text)



# def empty_tables():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         try:
#             cursor.execute("DELETE FROM link_analysis;")
#             cursor.execute("DELETE FROM excel_sheet;")
#             conn.commit()
#             st.success("'link_analysis' and 'excel_sheet' tables have been emptied.")
#         except Exception as e:
#             st.error(f"Error emptying tables: {e}")
#     else:
#         st.error("Failed to connect to the database")

# st.button("Empty link_analysis & excel_sheet", on_click=empty_tables)



# def create_password_table():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     if conn and cursor:
#         try:
#             create_query = """
#             CREATE TABLE IF NOT EXISTS password_table (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 password VARCHAR(255) NOT NULL,
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#             );
#             """
#             cursor.execute(create_query)
#             conn.commit()
#             st.success("Table `password_table` created successfully.")
#         except Exception as e:
#             st.error(f"Error creating password_table: {e}")
#     else:
#         st.error("Failed to connect to the database")

# st.button("Create Password Table", on_click=create_password_table)




# def insert_password():
#     conn, cursor = connect_to_db()
#     st.write("Connected to database successfully")
#     password = "user123"
#     cursor.execute("INSERT INTO password_table (password) VALUES (%s);", (password,))
#     conn.commit()
#     st.write("Password inserted successfully.")

# st.button("insert password", on_click=insert_password)



def create_table():
    conn, cursor = connect_to_db()
    st.write("Connected to database successfully")
    if conn and cursor:
        table_name = "API"
        if table_name:
            try:
                create_query = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    api_key VARCHAR(255) NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(create_query)
                conn.commit()
                st.success(f"Table `{table_name}` created successfully.")
            except Exception as e:
                st.error(f"Error creating tables: {e}")
        else:
            st.warning("Please enter a table name.")


st.button("Create Table", on_click=create_table)
with st.form("insert_api_form"):
    api_key = st.text_input("API Key")
    submitted = st.form_submit_button("Insert API Key")
    if submitted:
        if api_key:
            conn, cursor = connect_to_db()
            if conn and cursor:
                try:
                    cursor.execute("INSERT INTO API (api_key) VALUES (%s);", (api_key,))
                    conn.commit()
                    st.success("API Key inserted successfully.")
                except Exception as e:
                    st.error(f"Error inserting API Key: {e}")
            else:
                st.error("Failed to connect to the database")
        else:
            st.warning("Please enter an API Key.")


def fetch_api_key():
                # Display the API table after insertion
            try:
                conn,cursor = connect_to_db()
                cursor.execute("SELECT * FROM API;")
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(data, columns=columns)
                st.subheader("API Table")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error fetching API table: {e}")

st.button("Fetch API Key", on_click=fetch_api_key)

