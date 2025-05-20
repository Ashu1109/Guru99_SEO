from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
import streamlit as st
def make_script_data(processed_item):
    link = processed_item["link"]
    title = processed_item["title"]
    query_data = processed_item["query_data"]
    clicks_of_words = get_click_of_words(query_data, title)
    top15,GSC_top_KW =top_15_KW(data=query_data)
    processed_item["clicks_of_words"] = clicks_of_words
    processed_item["top15"] = top15
    processed_item["GSC_top_KW"] = GSC_top_KW
    return processed_item
