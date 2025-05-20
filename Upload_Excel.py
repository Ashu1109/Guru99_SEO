import streamlit as st
import pandas as pd
import uuid
from action.get_data_from_excel import get_data_from_excel
from action.create_title_for_links import get_title_for_links
from action.get_processed_array import get_processed_array
from action.make_script_data import make_script_data
from action.get_analysis import get_analysis
from action.set_api_key import set_api_key
from action.set_api_key import clear_api_key
from action.fetch_api_key import fetch_api_key,clear_api_key_db,set_api_key_db
from action.connect_to_db import connect_to_db
from action.redis_queue import RedisQueue
import time

seo_tasks_queue = RedisQueue("upload_excel")

form_key = f"Run_The_LLM_Form"

fetch_api = fetch_api_key()

if fetch_api is not None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=fetch_api)
    st.sidebar.button("Clear API Key", on_click=clear_api_key_db, key="clear_api_key")
else:
    with st.sidebar.form("insert_api_form"):
        api_key = st.text_input("API Key", type="password", placeholder="Enter your API Key")
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
            st.rerun()


with st.form(form_key):
    st.write("Upload link of Excel")
    excel_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx"],
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("RUN LLM")
    if submitted:
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            set_api_key(openai_api_key)
            # Save API key to database if it's not already there
            set_api_key_db(openai_api_key)
            if not excel_file:
                st.warning("Both link and title are required. Please fill out the fields.")
            else:
                with st.spinner("Running LLM..."):
                    df,file_name = get_data_from_excel(excel_file)
                    conn,cursor = connect_to_db()
                    sql = "INSERT INTO excel_sheet (name) VALUES (%s)"
                    cursor.execute(sql, (file_name,))
                    conn.commit()
                    inserted_id = cursor.lastrowid
                    for index,row in df.iterrows():
                        print(f"Processing row {row['Links']}")
                        success = seo_tasks_queue.enqueue({"url":row['Links'],"inserted_id":inserted_id})
                        if success:
                            st.success(f"Backlink URL {row['Links']} added to the queue successfully!")



def process_upload_link(url,inserted_id):
    link_title =  get_title_for_links(url)
    processed_item = get_processed_array(link_title)
    processed_item = make_script_data(processed_item)
    res = get_analysis(processed_item,inserted_id)
    print(f"Analysis completed for {url}")
    
def process_seo_task(task_data):
    """Process an SEO task (example function)"""
    print(f"Processing SEO analysis for {task_data['url']}")
    process_upload_link(task_data["url"],task_data["inserted_id"])
    return {"status": "completed", "url": task_data["url"]}




def run_worker():
    """Run a worker process that processes tasks from the queue"""
    print("Starting SEO analysis worker...")
    while True:
        # Block until a task is available
        task = seo_tasks_queue.dequeue(timeout=0)  # 0 means block indefinitely
        
        if task:
            print(f"Received task: {task}")
            try:
                result = process_seo_task(task)
                print(f"Task completed: {result}")
            except Exception as e:
                print(f"Error processing task: {e}")
        else:
            print("No task available or error occurred")
            time.sleep(1)  # Prevent CPU spinning

run_worker()