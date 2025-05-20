import streamlit as st
import requests
from bs4 import BeautifulSoup
def get_title_for_links(link):
    try:    
        response = requests.get(link)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.title.string if soup.title else "No title found"
            return {
                        "link": link,
                        "title": title_tag
                    }
    except Exception as e:
        st.error(f"Error fetching {link}: {e}")
    return None