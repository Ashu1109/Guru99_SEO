import streamlit as st
import pandas as pd
import asyncio
from action.get_processed_array import access_token
from action.get_filtered_links  import get_filtered_links 
from action.create_title_for_links import get_title_for_links
from action.fetch_data_from_link import fetch_data_from_link
from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
from action.get_total_calculation import get_total_calculation
from deep_translator import GoogleTranslator
from action.connect_to_db import connect_to_db
from action.create_seo_table import create_seo_data_table,create_backlink_table,save_backlink,create_table_master_seo_link,save_seo_data
from action.fetch_api_key import fetch_api_key, clear_api_key_db
from action.run_SEO_llm import run_SEO_llm
import time

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
    data = get_filtered_links(backlink_url)
    urls = []
    for i in data["rows"]:
        urls.append(i["keys"][0])
    processed_array = get_title_for_links(pd.DataFrame(urls))
    for i in processed_array:
        data = fetch_data_from_link(i["link"],webmaster_access_token=access_token())
        if data:
            i["data"] = data
        else:
            st.error(f"Failed to fetch data for link: {i['link']}")
    st.write("Data fetched successfully...")
    st.write("Translating data...")
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
    st.write("Translating data done...")
    conn, cursor = connect_to_db()
    # Process data after translation
    st.write("Processing data...")
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
        save_seo_data(
            backlink_id=backlink_id,
            link=link,
            title=title,
            query_data=query_data,
            clicks_of_words=clicks_of_words,
            top15=top15,
            gsc_top_kw=GSC_top_KW
        )
    st.write("Data processing done...")
    st.write("Translating done...")
    final_data =  get_total_calculation(processed_array)
    run_SEO_llm(
        backlink_id,
        conn,
        cursor,
        input_link=backlink_url,
        query_data=processed_array[0]["data"],
        current_title=print(processed_array[0]["title"]),
        clicks_in_title=final_data["clicks_of_words"],
        top_15_KW=final_data["top15"],
        GSC_Top_KW_Clicks=final_data["GSC_top_KW"],
    )
    st.write("Total calculation done...")




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
                            get_data(backlink_url)
                            execution_time = time.time() - start_time
                            st.success(f"Processing completed in {execution_time:.2f} seconds")

backlink_form()




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