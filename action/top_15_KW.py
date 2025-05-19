import pandas as pd
from collections import Counter
import re
import streamlit as st
def top_15_KW(data):
    # Top 15 KW Frequency
    # Load the 'Queries' and 'Script Data' sheets
    # file_path =  "./https___www.guru99.com_best-iptv-services.html.xlsx"
    # queries_df = pd.read_excel(file_path, sheet_name="Queries")
    # script_df = pd.read_excel(file_path, sheet_name="Script Data")

    # # Extract the top 15 keywords from the first row of Script Data
    # kw_str = script_df.loc[0, "Top 15 KW Frequency"]
    # keywords = [line.split("=")[0] for line in kw_str.split("\n")]

    # # Calculate frequency using substring match across all rows
    # results = []
    # for kw in keywords:
    #     freq = int(
    #         queries_df["Top queries"].str.contains(kw, case=False, na=False).sum()
    #     )
    #     results.append({"keyword": kw, "frequency": freq})
    # # Display the recalculated frequencies
    # result_df = pd.DataFrame(results)
    # ########################################
    # # GSC Top KW Clicks
    # # Append missing keywords for full list
    # additional_keywords = keywords[5:]  # remaining after provider
    # results_add = []
    # for kw in additional_keywords:
    #     mask = queries_df["Top queries"].str.contains(kw, case=False, na=False)
    #     total_clicks = int(queries_df.loc[mask, "Clicks"].sum())
    #     results_add.append({"keyword": kw, "clicks": total_clicks})

    # # Combine and display all
    # full_results = pd.concat([result_df, pd.DataFrame(results_add)], ignore_index=True)
    # return result_df, full_results
    
    
    
    
    
    # queries_df = pd.read_excel(file_path, sheet_name='Queries')

    # Format the data["rows"] to have "keys" as a string instead of an array
    if "rows" not in data or not isinstance(data["rows"], list):
        st.warning("No data available")
        return pd.DataFrame(), pd.DataFrame()
    for row in data["rows"]:
        if "keys" in row and isinstance(row["keys"], list) and len(row["keys"]) > 0:
            row["keys"] = row["keys"][0]
            
    queries_df = pd.DataFrame(data["rows"])
    # Count the frequency of each unique word across queries
    counter = Counter()
    for query in queries_df['keys'].dropna().astype(str):
        tokens = set(re.findall(r'\b\w+\b', query.lower()))
        for token in tokens:
            counter[token] += 1

    # Extract the top 15 most common keywords
    top15 = counter.most_common(15)
    
    #  GSC Top KW Clicks
    additional_keywords = [kw for kw, _ in top15[:10]]
    results_add = []
    
    for kw in additional_keywords:
        mask = queries_df["keys"].str.contains(kw, case=False, na=False)
        total_clicks = int(queries_df.loc[mask, "clicks"].sum())
        results_add.append({"keyword": kw, "clicks": total_clicks})
    # Display results
    return  pd.DataFrame(top15),pd.DataFrame(results_add)
