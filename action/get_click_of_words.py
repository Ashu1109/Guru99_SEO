import pandas as pd
import re
import streamlit as st
# Clicks of words in Title
def get_click_of_words(query, title):
    tokens = re.findall(r"\b\w+\b", title.lower())
    results = []
    for tok in tokens:
        total_clicks = 0
        for row in query["rows"]:
            if tok in row["keys"][0].lower():
                total_clicks += row["clicks"]
        results.append({"word": tok, "clicks": total_clicks})
    return pd.DataFrame(results)