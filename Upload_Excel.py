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

form_key = f"Run_The_LLM_Form"
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
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