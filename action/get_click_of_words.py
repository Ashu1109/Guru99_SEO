import pandas as pd
import re
import streamlit as st



def get_click_of_words(query, title):
    tokens = re.findall(r"\b\w+\b", title.lower())
    results = []
    for tok in tokens:
        total_clicks = 0
        if not query or "rows" not in query or not query["rows"]:
            return pd.DataFrame()
        # Check if the token is in the query
        if not any(tok in row["keys"][0].lower() for row in query["rows"]):
            continue
        for row in query["rows"]:
            if tok in row["keys"][0].lower():
                total_clicks += row["clicks"]
        results.append({"word": tok, "clicks": total_clicks})
    return pd.DataFrame(results)