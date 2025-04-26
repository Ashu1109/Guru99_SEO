import streamlit as st
from action.connect_to_db import connect_to_db
import pandas as pd

conn, cursor = connect_to_db()

# Add form to create a new password
st.subheader("Add New Password")
with st.form("create_password_form"):
        new_password = st.text_input("Enter new password", type="password")
        submitted = st.form_submit_button("Create Password")
        if submitted:
            if new_password:
                try:
                    cursor.execute("INSERT INTO password_table (password) VALUES (%s)", (new_password,))
                    conn.commit()
                    st.success("Password created successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating password: {e}")
            else:
                st.warning("Password cannot be empty.")

def get_passwords():
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM password_table;")
            passwords = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            if passwords:
                df = pd.DataFrame(passwords, columns=columns)
                st.subheader("All Passwords:")
                # Add column headers
                header1, header2, header3, header4 = st.columns([2, 4, 4, 2])
                with header1:
                    st.markdown("**S.No**")
                with header2:
                    st.markdown("**Password**")
                with header3:
                    st.markdown("**Created At**")
                with header4:
                    st.markdown("**Action**")
                for idx, row in df.iterrows():
                    col1, col2, col3, col4 = st.columns([2, 4, 4, 2])
                    with col1:
                        st.write(idx + 1)
                    with col2:
                        st.write(row['password'])
                    with col3:
                        st.write(row['created_at'].strftime('%Y-%m-%d %I:%M %p') if pd.notnull(row['created_at']) else "")
                    with col4:
                        if st.button("Delete", key=f"delete_{row['id']}"):
                            try:
                                cursor.execute("DELETE FROM password_table WHERE id = %s", (row['id'],))
                                conn.commit()
                                st.success(f"Password with id {row['id']} removed.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error removing password: {e}")
            else:
                st.write("No passwords found in password_table.")
        except Exception as e:
            st.error(f"Error fetching passwords: {str(e)}")
    else:
        st.error("Failed to connect to the database")
        
get_passwords()