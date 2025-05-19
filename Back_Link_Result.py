from action.connect_to_db import connect_to_db
import streamlit as st
import pandas as pd
import io
def get_backlinks_table():
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            st.error("Failed to connect to the database")
            return
        try:
            # Drop the table if it exists
            cursor.execute("SELECT * FROM backlinks ORDER BY id DESC;")
            rows = cursor.fetchall()
            if not rows:
                st.warning("No backlinks found")
                return
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
            # st.dataframe(df)
            conn.commit()
            # st.success("Backlinks table fetched successfully!")
            return rows
        except Exception as e:
            st.error(f"Error fetching backlinks table: {e}")
        finally:
            if conn:
                conn.close()

def get_seo_data(id):
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            st.error("Failed to connect to the database")
            return
        try:
            # Fetch data from the database
            cursor.execute("SELECT * FROM seo_data WHERE backlink_id = %s", (id,))
            rows = cursor.fetchall()
            if not rows:
                st.warning("No SEO data found")
                return
            
            return rows
        except Exception as e:
            st.error(f"Error fetching SEO data: {e}")
        finally:
            if conn:
                conn.close()

def get_seo_master_data(id):
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            st.error("Failed to connect to the database")
            return
        try:
            # Fetch data from the database
            cursor.execute("SELECT * FROM master_seo_link WHERE backlink_id = %s", (id,))
            rows = cursor.fetchall()
            if not rows:
                st.warning("No SEO master data found")
                return
            
            return rows
        except Exception as e:
            st.error(f"Error fetching SEO master data: {e}")
        finally:
            if conn:
                conn.close()


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





st.sidebar.title("Results")
backlinks = get_backlinks_table()
    
    
if not backlinks:
    st.sidebar.warning("No backlinks found. Please run the backlink processing first.")
else:
    for i, backlink in enumerate(backlinks):
        link_text = backlink[1] if isinstance(backlink, tuple) else backlink['backlink']
        truncated_text = link_text[:30] + "..." if len(link_text) > 30 else link_text
        if st.sidebar.button(f"{i+1}: {truncated_text}", key=f"backlink_{i}", use_container_width=True):
            st.write(f"Data of backlink: {link_text}")
            seo = get_seo_data(backlink["id"])
            seo_master = get_seo_master_data(backlink["id"])
            download_excel(seo, f"SEO_Data_{backlink['id']}", button_label="Download SEO Excel")
            download_excel(seo_master, f"SEO_Master_Data_{backlink['id']}", button_label="Download SEO Master Excel")
            st.title("Response:🤖")
            if seo_master and len(seo_master) > 0:
                st.write(seo_master[0]["response"])
            else:
                st.warning("No response data found")
    with st.expander(f"List of Backlinks"):
            seo = get_seo_data(backlinks[0]["id"])
            if not seo:
                st.warning("No SEO data found for the selected backlink.")
            else:
                for i, seo_data in enumerate(seo):
                    st.write(f"Link {i+1}: {seo_data['link']}")
                    download_excel(seo_data, f"SEO_Data_{seo_data['id']}", button_label="Download Excel Data")
                


