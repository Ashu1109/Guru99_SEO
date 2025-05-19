from action.get_data import get_data
from model.model import model
from action.get_only_title import get_only_title
import streamlit as st
from pandas import DataFrame

def run_SEO_llm(
    backlink_id,
    conn,
    cursor,
    input_link: str,
    query_data: str,
    current_title: DataFrame,
    clicks_in_title: DataFrame,
    top_15_KW: DataFrame,
    GSC_Top_KW_Clicks: str,
):
    # Create the prompt
    prompt = f"""
        Act as an SEO expert.
        Check my current page title '{current_title}' and {clicks_in_title}.
        Also compare data with Google Search Console: {top_15_KW},{GSC_Top_KW_Clicks}.
        Based on this analysis and incorporating the following top-performing keywords from Google Search Console: {top_15_KW},{GSC_Top_KW_Clicks}, generate two distinct and compelling title tags, each no longer than 60-65 characters, aimed at improving search engine visibility and click-through rates.

        Instructions:
        - Use no more than 60-65 characters.
        - Help drive clicks and improve ranking in search engines.
        - Create meaningful titles based on top-clicked words.
        - In the provided data, the number after "=" indicates the number of clicks for a particular word.
        - Compare data of {clicks_in_title} & {top_15_KW},{GSC_Top_KW_Clicks} in table format. When comparing, add a column explaining why you selected the keyword for the title.
        - Create new titles based on the clicks we received in data {top_15_KW},{GSC_Top_KW_Clicks}.
        - Output must contain my existing {current_title} with optimized titles.
        - Provide a bulleted list for both titles separately that highlights included keywords with a green emoji and removed keywords with a red emoji compared to the current {current_title}.

        Link: {input_link}
        Title: {current_title}

        current_title:{current_title}
        clicks_in_title:{clicks_in_title}
        top_15_KW:{top_15_KW}
        GSC_Top_KW_Clicks:{GSC_Top_KW_Clicks}
        """
    st.write("LLM working on it...")
    response = model().invoke(prompt)
    st.write("LLM finished working on it.")
    st.write("Response from LLM:", response)
    response_content = response.content
    suggested_titles = get_only_title(response_content)
    title_1 = str(suggested_titles[0]) if len(suggested_titles) > 0 else ""
    title_2 = str(suggested_titles[1]) if len(suggested_titles) > 1 else ""

    create_query = """
        INSERT INTO master_seo_link ( backlink_id, link, title, query_data, clicks_of_words, top15, GSC_top_KW, suggested_title_1, suggested_title_2, response)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
    if isinstance(clicks_in_title, DataFrame):
        clicks_in_title = clicks_in_title.to_string(index=True, header=False)
    else:
        clicks_in_title = str(clicks_in_title)

    if isinstance(top_15_KW, DataFrame):
        top_15_KW = top_15_KW.to_string(index=True, header=False)
    else:
        top_15_KW = str(top_15_KW)

    if isinstance(GSC_Top_KW_Clicks, DataFrame):
        GSC_Top_KW_Clicks = GSC_Top_KW_Clicks.to_string(index=True, header=False)
    else:
        GSC_Top_KW_Clicks = str(GSC_Top_KW_Clicks)
        
        
    # Ensure all values are strings before inserting into the database
    def to_str(val):
        if isinstance(val, list):
            return ','.join(map(str, val))
        return str(val)
    

    
    values = (
        backlink_id,
        input_link,
        to_str(current_title),
        to_str(query_data),
        to_str(clicks_in_title),
        to_str(top_15_KW),
        to_str(GSC_Top_KW_Clicks),
        to_str(title_1),
        to_str(title_2),
        to_str(response_content)
    )
    cursor.execute(create_query, values)
    conn.commit()

