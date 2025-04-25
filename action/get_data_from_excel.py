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