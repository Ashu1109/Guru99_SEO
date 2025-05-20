from action.connect_to_db import connect_to_db
from action.refresh_access_token import refresh_access_token
import streamlit as st
from action.fetch_access_token import fetch_access_token
from action.fetch_data_from_link import fetch_data_from_link

def access_token():
    webmaster_access_token = None 
    conn, cursor = connect_to_db()
    if conn and cursor:
        row_result = fetch_access_token(cursor)
        try:
            token_response = refresh_access_token(row_result["refresh_token"])
            if "access_token" in token_response:
                new_access_token = token_response["access_token"]
                webmaster_access_token = new_access_token
            else:
                webmaster_access_token = row_result["access_token"]
        except Exception as e:
            st.error(f"Error refreshing token: {e}")
            webmaster_access_token = row_result["access_token"]
    return webmaster_access_token


def get_processed_array(link_title):
    """
    Process the link_title array to create a new array with the desired format.
    """
    token = access_token()
    data = fetch_data_from_link(link_title["link"],webmaster_access_token=token)
    if data:
        processed_item = {
            "link": link_title["link"],
            "title": link_title["title"],
            "query_data": data
        }
    return processed_item
