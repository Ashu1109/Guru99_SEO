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
            if not excel_file:
                st.warning("Both link and title are required. Please fill out the fields.")
            else:
                with st.spinner("Running LLM..."):
                    st.write("Running LLM...")
                    df,file_name = get_data_from_excel(excel_file)
                    link_title =  get_title_for_links(df)
                    processed_array = get_processed_array(link_title)
                    processed_array = make_script_data(processed_array)
                    res = get_analysis(processed_array,file_name)
                    clear_api_key()
                    openai_api_key = ""
                    excel_file = ""
                    st.header("Analysis Completed")