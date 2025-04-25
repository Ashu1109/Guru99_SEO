import streamlit as st
import requests
from bs4 import BeautifulSoup
def get_title_for_links(df):
    link_title = []
    for index, row in df.iterrows():
        link_array = row.to_dict().values()
        for link in link_array:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    title_tag = soup.title.string if soup.title else "No title found"
                    link_title.append({
                        "link": link,
                        "title": title_tag
                    })
                else:
                    st.warning(f"Failed to fetch {link}: Status code {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching {link}: {e}")
    return link_title