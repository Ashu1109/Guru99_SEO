import streamlit as st
import pandas as pd
import asyncio
from action.get_processed_array import access_token
from action.get_filtered_links  import get_filtered_links 
from action.create_title_for_links import get_title_for_links
from action.fetch_data_from_link import fetch_data_from_link
from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
from deep_translator import GoogleTranslator
from action.connect_to_db import connect_to_db
from action.create_seo_table import create_seo_data_table,create_backlink_table,save_backlink,create_table_master_seo_link,save_seo_data
from action.fetch_api_key import fetch_api_key, clear_api_key_db
from action.run_SEO_llm import run_SEO_llm
from action.redis_queue import RedisQueue
import time
import pandas as pd
from io import StringIO



seo_tasks_queue = RedisQueue("seo_tasks")
# # Create SEO data table if it doesn't exist
# backlink = create_backlink_table()
# master_seo = create_table_master_seo_link()
# if master_seo:
#     st.success("Master SEO link table created successfully!")
# table_created = create_seo_data_table()
# if table_created:
#     st.success("SEO data table created successfully!")
# else:
#     st.error("Failed to create SEO data table")



def try_parse_dataframe(value):
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, str):
        # Try to detect the format from the string structure
        try:
            # If the string is already a formatted table, parse it
            if "\n" in value and (value.count("\t") > 0 or value.count("  ") > 0):
                df = pd.read_csv(StringIO(value), sep=None, engine='python')
                return df
            else:
                # Try as JSON or other formats
                return pd.read_json(StringIO(value))
        except Exception:
            pass
    return None

def collect_tables(processed_array):
    tables = {
        "clicks_of_words": [],
        "top15": [],
        "GSC_top_KW": []
    }
    
    for item in processed_array:
        if isinstance(item, dict):
            for key in tables.keys():
                if key in item and item[key] is not None:
                    df = try_parse_dataframe(item[key])
                    if df is not None and not df.empty:
                        tables[key].append(df)
    
    return tables

def combine_and_aggregate_tables(tables):
    combined_tables = {}
    
    # Process clicks_of_words tables
    if tables["clicks_of_words"]:
        dfs_with_columns = []
        for df in tables["clicks_of_words"]:
            if len(df.columns) >= 2:  # Ensure there are at least 2 columns
                # Check column names and create a standardized DataFrame
                if "word" in df.columns and "clicks" in df.columns:
                    dfs_with_columns.append(df[["word", "clicks"]])
                else:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df.iloc[:, 0] if df.shape[1] > 0 else [],
                        "clicks": df.iloc[:, 1] if df.shape[1] > 1 else []
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping (in case of mixed types)
            combined_df["word"] = combined_df["word"].astype(str)
            aggregated_df = combined_df.groupby("word", as_index=False)["clicks"].sum()
            combined_tables["clicks_of_words"] = aggregated_df.sort_values("clicks", ascending=False)
    
    # Process top15 tables
    if tables["top15"]:
        dfs_with_columns = []
        for df in tables["top15"]:
            if df.shape[1] >= 2:  # Ensure DataFrame has at least 2 columns
                # Check if column names exist or are numeric
                if 0 in df.columns and 1 in df.columns:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df[0],
                        "freq": df[1]
                    }))
                elif "word" in df.columns and "freq" in df.columns:
                    dfs_with_columns.append(df[["word", "freq"]])
                else:
                    # Use the first two columns whatever they're called
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df.iloc[:, 0],
                        "freq": df.iloc[:, 1]
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping
            combined_df["word"] = combined_df["word"].astype(str)
            aggregated_df = combined_df.groupby("word", as_index=False)["freq"].sum()
            combined_tables["top15"] = aggregated_df.sort_values("freq", ascending=False)
    
    # Process GSC_top_KW tables
    if tables["GSC_top_KW"]:
        dfs_with_columns = []
        for df in tables["GSC_top_KW"]:
            if df.shape[1] >= 2:  # Ensure DataFrame has at least 2 columns
                if "keyword" in df.columns and "clicks" in df.columns:
                    dfs_with_columns.append(df[["keyword", "clicks"]])
                else:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "keyword": df.iloc[:, 0],
                        "clicks": df.iloc[:, 1]
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping
            combined_df["keyword"] = combined_df["keyword"].astype(str)
            aggregated_df = combined_df.groupby("keyword", as_index=False)["clicks"].sum()
            combined_tables["GSC_top_KW"] = aggregated_df.sort_values("clicks", ascending=False)
    
    return combined_tables


def get_total_calculation(processed_array):
    # Collect all tables by type
    print(f"Processing array: {processed_array}")
    tables = collect_tables(processed_array)
    print(f"Tables collected: {tables}")
    # Combine and aggregate tables
    combined_tables = combine_and_aggregate_tables(tables)
    print(f"Combined tables: {combined_tables}")
    
    return combined_tables


async def translate_text(text, target_language='en'):
    """
    Asynchronously translate text to the target language with automatic source language detection.
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (default: 'en' for English)
        show_detection (bool): Whether to show detected language (default: False)
        
    Returns:
        str: Translated text
    """
    try:
        # Skip translation if text is empty
        if not text or text.strip() == "":
            return text
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(text)
        return translation
        
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text in case of error

def get_data(backlink_url):
    print(f"Fetching data for {backlink_url}")
    data = get_filtered_links(backlink_url)
    print(f"Data fetched for {backlink_url}")
    urls = []
    
    # Check if data is None or doesn't have 'rows' key
    if data is None or 'rows' not in data:
        print(f"Error: No data or 'rows' found for {backlink_url}")
        return None
        
    for i in data["rows"]:
        if "keys" in i and len(i["keys"]) > 0:
            urls.append(i["keys"][0])
    # Check if urls list is empty
    if not urls:
        print(f"Error: No valid URLs found for {backlink_url}")
        return None
        
    processed_array = get_title_for_links(urls)
    
    # Check if processed_array is None or empty
    if not processed_array:
        print(f"Error: No processed array data for {backlink_url}")
        return None
        
    for i in processed_array:
        if "link" not in i:
            print(f"Error: Missing 'link' in processed item")
            continue
            
        data = fetch_data_from_link(i["link"], webmaster_access_token=access_token())
        if data:
            i["data"] = data
        else:
            print(f"Failed to fetch data for link: {i['link']}")
    print(f"Data fetched successfully...{backlink_url}")
    print(f"Translating data...{backlink_url}")
    async def translate_all_data():
        for i in processed_array:
            if "title" in i:
                i["title"] = await translate_text(i["title"])
            if "data" in i and "rows" in i["data"]:
                for j in i["data"]["rows"]:
                    if "keys" in j:
                        for k in range(len(j["keys"])):
                            j["keys"][k] = await translate_text(j["keys"][k])
    # Run the async function
    asyncio.run(translate_all_data())
    print(f"Translating data done...{backlink_url}")
    conn, cursor = connect_to_db()
    # Process data after translation
    print(f"Processing data...{backlink_url}")
    backlink_id = save_backlink(backlink_url)
    for i in processed_array:
        link = i["link"]
        title = i["title"]
        query_data = i["data"]
        clicks_of_words = get_click_of_words(query_data, title)
        top15, GSC_top_KW = top_15_KW(data=query_data)
        i["clicks_of_words"] = clicks_of_words
        i["top15"] = top15
        i["GSC_top_KW"] = GSC_top_KW
        # Save the processed data to the database
        print(f"Saving data to database...{backlink_url}")
        save_seo_data(
            backlink_id=backlink_id,
            link=link,
            title=title,
            query_data=query_data,
            clicks_of_words=clicks_of_words,
            top15=top15,
            gsc_top_kw=GSC_top_KW
        )
        print(f"Data saved to database...{backlink_url}")
    print(f"Data processing done...{backlink_url}")
    print(f"Calculating total data...{backlink_url}")
    final_data = get_total_calculation(processed_array)
    print(f"Total data calculated...{final_data}")
    print(f"Final data calculation done...{backlink_url}")
    
    # Check if final_data is None or missing required keys
    if not final_data:
        print(f"Error: No final data calculated for {backlink_url}")
        return None
        
    # Check if processed_array has at least one item with required keys
    if not processed_array or len(processed_array) == 0:
        print(f"Error: No processed array data for {backlink_url}")
        return None
        
    # Check if the first item in processed_array has the required keys
    if "data" not in processed_array[0] or "title" not in processed_array[0]:
        print(f"Error: Missing required keys in processed_array for {backlink_url}")
        return None
        
    # Check if final_data has all required keys
    required_keys = ["clicks_of_words", "top15", "GSC_top_KW"]
    for key in required_keys:
        if key not in final_data:
            print(f"Error: Missing {key} in final_data for {backlink_url}")
            final_data[key] = pd.DataFrame()  # Provide an empty DataFrame as fallback
    
    try:
        run_SEO_llm(
            backlink_id=backlink_id,
            conn=conn,
            cursor=cursor,
            input_link=backlink_url,
            current_title=processed_array[0]["title"],  # Removed print() call that was causing issues
            clicks_in_title=final_data["clicks_of_words"],
            top_15_KW=final_data["top15"],
            GSC_Top_KW_Clicks=final_data["GSC_top_KW"],
        )
    except Exception as e:
        print(f"Error running SEO LLM: {e}")
        return None
    print(f"Total calculation done...{backlink_url}")




import pandas as pd
import streamlit as st
from action.connect_to_db import connect_to_db
def get_data_from_excel(excel_file):
    conn, cursor = connect_to_db()
    # Read the uploaded Excel file
    try:
        df = pd.read_excel(excel_file)
        file_name = excel_file.name
        return df,file_name
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred while reading the Excel file: {e}")



# if st.button("Clear ALL Tables"):
#     def clear_all_tables():
#         conn, cursor = connect_to_db()
#         if not conn or not cursor:
#             st.error("Failed to connect to the database")
#             return
#         try:
#             # Clear all tables
#             cursor.execute("DELETE FROM seo_data")
#             cursor.execute("DELETE FROM master_seo_link")
#             cursor.execute("DELETE FROM backlinks")
#             conn.commit()
#             st.success("All tables cleared successfully!")
#         except Exception as e:
#             st.error(f"Error clearing tables: {e}")
#         finally:
#             if conn:
#                 conn.close()
    
#     clear_all_tables()
#     st.success("All tables cleared successfully!")


# def fetch_all_tables():
#     conn, cursor = connect_to_db()
#     if not conn or not cursor:
#         st.error("Failed to connect to the database")
#         return
#     try:
#         # Fetch all tables
#         cursor.execute("SHOW TABLES;")
#         tables = cursor.fetchall()
#         if tables:
#             st.write("Tables in the database:")
#             for table in tables:
#                 table_name = list(table.values())[0]
#                 st.subheader(f"Table: {table_name}")
#                 cursor.execute(f"SELECT * FROM {table_name};")
#                 data = cursor.fetchall()
#                 columns = [desc[0] for desc in cursor.description]
#                 df = pd.DataFrame(data, columns=columns)
#                 st.dataframe(df)
#         else:
#             st.write("No tables found in the database.")
#     except Exception as e:
#         st.error(f"Error fetching tables: {e}")
#     finally:
#         if conn:
#             conn.close()
    
# if st.button("Fetch All Tables"):
#     fetch_all_tables()








def backlink_form():
        st.header("Backlink Input Form")
        
        with st.form("backlink_form"):
            st.write("Upload link of Excel")
            excel_file = st.file_uploader(
                "Upload Excel file",
                type=["xlsx"],
                label_visibility="collapsed",
            )
            # backlink_url = st.text_input("Enter backlink URL")
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                df,file_name = get_data_from_excel(excel_file)
                st.write("Excel file uploaded successfully!")
                st.write("File Name:", file_name)
                st.write(df)
                if  df.empty:
                    st.error("Please enter a backlink URL")
                else:
                    for index, row in df.iterrows():
                        backlink_url = row[0]
                        st.write(f"Processing backlink URL: {backlink_url}")
                        start_time = time.time()
                        with st.spinner('Processing data... This may take a while'):
                            # get_data(backlink_url)
                            success = seo_tasks_queue.enqueue({"url":backlink_url})
                            if success:
                                st.success(f"Backlink URL {backlink_url} added to the queue successfully!")
                            execution_time = time.time() - start_time
                            st.success(f"Processing completed in {execution_time:.2f} seconds")

backlink_form()






# def process_seo_task(task_data):
#     """Process an SEO task (example function)"""
#     print(f"Processing SEO analysis for {task_data['url']}")
#     get_data(task_data["url"])
#     return {"status": "completed", "url": task_data["url"]}




# def run_worker():
#     """Run a worker process that processes tasks from the queue"""
#     print("Starting SEO analysis worker...")
#     while True:
#         # Block until a task is available
#         task = seo_tasks_queue.dequeue(timeout=0)  # 0 means block indefinitely
        
#         if task:
#             print(f"Received task: {task}")
#             try:
#                 result = process_seo_task(task)
#                 print(f"Task completed: {result}")
#             except Exception as e:
#                 print(f"Error processing task: {e}")
#         else:
#             print("No task available or error occurred")
#             time.sleep(1)  # Prevent CPU spinning

# run_worker()

# if st.button("getSEOdata"):
#     def get_seo_data():
#         # Fetch and display SEO data
#         st.write("Fetching SEO data...")
#         conn, cursor = connect_to_db()
#         if not conn or not cursor:
#             st.error("Failed to connect to the database")
#             return
#         try:
#             # Fetch data from the database
#             cursor.execute("SELECT * FROM seo_data")
#             rows = cursor.fetchall()
#             if not rows:
#                 st.warning("No SEO data found")
#                 return
            
#             # Convert to DataFrame for better display
#             df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
#             st.dataframe(df)
#         except Exception as e:
#             st.error(f"Error fetching SEO data: {e}")
#         finally:
#             if conn:
#                 conn.close()
    
#     get_seo_data()
    
    
    
    
    





# if st.button("Delete row"):
#     def delete_row():
#         conn, cursor = connect_to_db()
#         if not conn or not cursor:
#             st.error("Failed to connect to the database")
#             return
#         try:
#             # Delete a specific row from the backlinks table
#             backlink_id = 12
#             cursor.execute("DELETE FROM seo_data WHERE backlink_id = %s", (backlink_id,))
#             conn.commit()
#             cursor.execute("DELETE FROM backlinks WHERE id = %s", (backlink_id,))
#             conn.commit()

#             st.success(f"Row with ID {backlink_id} deleted successfully!")
#         except Exception as e:
#             st.error(f"Error deleting row: {e}")
#         finally:
#             if conn:
#                 conn.close()
    
#     delete_row()



