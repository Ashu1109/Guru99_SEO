from model.model import model
import streamlit as st
def get_only_title(response_content):
    prompt = """
        Extract only the optimized titles from the following response content. 
        Provide the titles as plain text, separated by a newline.

        Response Content:
        {response_content}
        
        Title1:
        Title2:
    """
    response = model().invoke(prompt.format(response_content=response_content))
    lines = response.content.strip().splitlines()
    return lines