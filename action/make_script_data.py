from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
import streamlit as st
def make_script_data(processed_array):
    for item in processed_array:
        # item = processed_array[0]
        link = item["link"]
        title = item["title"]
        query_data = item["query_data"]
        clicks_of_words = get_click_of_words(query_data, title)
        top15,GSC_top_KW =top_15_KW(data=query_data)
        st.write("Top 15 Keywords:", top15)
        st.write("GSC Top Keywords Clicks:", GSC_top_KW)
        st.write("Clicks of Words in Title:", clicks_of_words)
        item["clicks_of_words"] = clicks_of_words
        item["top15"] = top15
        item["GSC_top_KW"] = GSC_top_KW
        st.write("Processed Item:", item)
    return processed_array
