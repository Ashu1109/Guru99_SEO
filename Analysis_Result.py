import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from action.get_excel_sheet import get_excel_sheet  
from action.get_all_link import get_all_link
import pandas as pd
import io

st.title("Analysis Result")


st.markdown("""
    <style>
    div.stButton > button {
        background-color: grey;
        color: white;
        border-radius: 8px;
        height: 1em;
        width: 100%;
        font-size: 18px;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
    div.stButton > button:active {
        background-color: #388e3c;
        color: white;
        border-color: #388e3c;
    }
    div.stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #4CAF50;
    }
    div.stButton > button:disabled {
        background-color: #ccc;
        color: #666;
        border-color: #ccc;
    }
    div.stButton > button:disabled:hover {
        background-color: #ccc;
        color: #666;
        border-color: #ccc;
    }
    div.stButton > button:disabled:active {
        background-color: #ccc;
        color: #666;
        border-color: #ccc;
    }
    div.stButton > button:disabled:focus {
        outline: none;
        box-shadow: none;
    }
    div.stButton > button:disabled {
        cursor: not-allowed;
    }
    div.stButton > button:disabled:hover {
        cursor: not-allowed;
    }
    div.stButton > button:disabled:active {
        cursor: not-allowed;
    }
    </style>
""", unsafe_allow_html=True)

def download_excel(data, sheet_name,button_label="Download Summary Excel Sheet"):
    # Remove empty dicts/rows
    if isinstance(data, dict):
        data = [data]
    # Filter out empty dicts
    filtered_data = [row for row in data if any(row.values())]
    df = pd.DataFrame(filtered_data)
    # Create Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    excel_data = output.getvalue()
    st.download_button(
        label=button_label,
        data=excel_data,
        file_name=f"{sheet_name}_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

excel_sheets = get_excel_sheet()
st.sidebar.write("Excel Sheets")

# Use session state to store selected sheet
if 'selected_sheet' not in st.session_state:
    st.session_state.selected_sheet = None

if excel_sheets:
    for idx, sheet in enumerate(excel_sheets):
        if st.sidebar.button(f"{idx+1} {sheet['name']}", key=sheet["id"]):
            st.session_state.selected_sheet = sheet
else:
    st.sidebar.write("No Excel sheets available.")
    
selected_sheet = st.session_state.selected_sheet
if selected_sheet:
    st.write(f"Selected sheet: {selected_sheet['name']}")
    data = get_all_link(selected_sheet["id"])
    if data:
        download_excel(data, selected_sheet["name"])
        for item in data:
            with st.expander(item["link"]):
                st.write(item)
                download_excel(item, item["link"],button_label="Download Link Excel Sheet")
                st.subheader("Suggested Title 1:")
                st.write(item["suggested_title_1"])
                st.subheader("Suggested Title 2:")
                st.write(item["suggested_title_2"])
                st.write(item["response"])
    else:
        st.write("No data found for the selected sheet.")

