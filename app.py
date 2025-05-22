import streamlit as st
from action.connect_to_db import connect_to_db

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = True
if 'admin' not in st.session_state:
    st.session_state['admin'] = True
    
if not st.session_state['authenticated']:
    st.title("Login Required")
    password = st.text_input("Enter password to continue", type="password")
    if st.button("Login"):
        conn,cursor = connect_to_db()
        cursor.execute("SELECT 1 FROM password_table WHERE password = %s LIMIT 1", (password,))
        result = cursor.fetchone()
        
        if password=="GuruSEO123":
            st.session_state['admin'] = True
            st.session_state['authenticated'] = True
            st.rerun()
        elif result:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Incorrect password. Access denied.")
else:
    if st.session_state["admin"]:
        pg = st.navigation(["Upload_Excel.py","Analysis_Result.py","Back_Link.py","Back_Link_Result.py","Admin.py"])
    else:
        pg = st.navigation(["Upload_Excel.py","Analysis_Result.py","Back_Link.py","Back_Link_Result.py"])
    pg.run()