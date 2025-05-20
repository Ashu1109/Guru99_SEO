import streamlit as st
import requests
from bs4 import BeautifulSoup
def get_title_for_links(urls):
    try:    
        processed_array = []
        for i in urls:
            response = requests.get(i)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                title_tag = soup.title.string if soup.title else "No title found"
                processed_array.append({
                        "link": i,
                        "title": title_tag
                    })
    except Exception as e:
        st.error(f"Error fetching {i}: {e}")
    return processed_array