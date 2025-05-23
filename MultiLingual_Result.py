from action.connect_to_db import connect_to_db
import streamlit as st
import pandas as pd
import io
import json
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


def download_excel(data, sheet_name, button_label="Download Summary Excel Sheet"):
    # Check if data is None
    if data is None:
        st.warning(f"No data available for {sheet_name}")
        return
    
    # Remove empty dicts/rows
    if isinstance(data, dict):
        data = [data]
    # Filter out empty dicts
    filtered_data = [row for row in data if any(row.values())]
    df = pd.DataFrame(filtered_data)
    
    # Check if filtered data is empty
    if filtered_data:
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
    else:
        st.warning(f"No data available for {sheet_name} after filtering")
        return







def download_excel_seo(data, query_data, sheet_name, button_label="Download Summary Excel Sheet"):
    # Check if data is None
    if data is None:
        st.warning(f"No data available for {sheet_name}")
        return
    
    # Remove empty dicts/rows
    if isinstance(data, dict):
        data = [data]
    # Filter out empty dicts
    filtered_data = [row for row in data if any(row.values())]
    
    # Create Excel file with multiple sheets
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Get workbook for formatting
        workbook = writer.book
        
        # Write main data to Sheet1
        df = pd.DataFrame(filtered_data)
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # Format Sheet1
        worksheet1 = writer.sheets['Sheet1']
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'border': 1,
            'bg_color': '#D7E4BC'
        })
        
        # Apply header format to Sheet1
        for col_num, value in enumerate(df.columns.values):
            worksheet1.write(0, col_num, value, header_format)
        
        # Handle query_data for Sheet2 - specifically for the format with 'rows' structure
        try:
            # Parse query_data if it's a string
            if isinstance(query_data, str):
                try:
                    query_data = json.loads(query_data)
                except json.JSONDecodeError:
                    pass
            
            # Handle the specific structure with 'rows' key
            if isinstance(query_data, dict) and 'rows' in query_data:
                rows_data = query_data['rows']
                query_df = pd.DataFrame(rows_data)
                
                # Write to Sheet2 with formatting
                query_df.to_excel(writer, index=False, sheet_name='Query Data')
                worksheet2 = writer.sheets['Query Data']
                
                # Apply header format to Query Data sheet
                for col_num, value in enumerate(query_df.columns.values):
                    worksheet2.write(0, col_num, value, header_format)
                
                # Set column widths based on content
                worksheet2.set_column('A:A', 30)  # keys column
                worksheet2.set_column('B:E', 15)  # other numeric columns
                
                # Add conditional formatting for high CTR values (above 0.5)
                good_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
                worksheet2.conditional_format('C2:C1000', {'type': 'cell',
                                                         'criteria': '>', 
                                                         'value': 0.5,
                                                         'format': good_format})
                
                # Add conditional formatting for good positions (below 3)
                good_pos_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
                worksheet2.conditional_format('E2:E1000', {'type': 'cell',
                                                         'criteria': '<', 
                                                         'value': 3,
                                                         'format': good_pos_format})
            else:
                # Fallback for other formats
                if isinstance(query_data, dict):
                    query_df = pd.DataFrame([query_data])
                elif isinstance(query_data, list):
                    query_df = pd.DataFrame(query_data)
                else:
                    query_df = pd.DataFrame({'data': [str(query_data)]})
                
                query_df.to_excel(writer, index=False, sheet_name='Sheet2')
        except Exception as e:
            # If there's any error processing query_data, create an error sheet
            error_df = pd.DataFrame({'Error': [f"Could not process query data: {str(e)}"]})
            error_df.to_excel(writer, index=False, sheet_name='Error')

        
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
        # Handle both tuple and dictionary formats
        if isinstance(backlink, tuple):
            link_text = backlink[1]
            backlink_id = backlink[0]  # Assuming ID is at index 0
        else:
            link_text = backlink.get('backlink', 'Unknown')
            backlink_id = backlink.get('id')
        
        truncated_text = link_text[:30] + "..." if len(link_text) > 30 else link_text
        if st.sidebar.button(f"{i+1}: {truncated_text}", key=f"backlink_{i}", use_container_width=True):
            st.write(f"Data of backlink: {link_text}")
            seo = get_seo_data(backlink_id)
            seo_master = get_seo_master_data(backlink_id)
            
            # Only call download_excel if data is available
            download_excel(seo_master, f"SEO_Master_Data_{backlink_id}", button_label="Download SEO Master Excel")
            
            st.title("Response:🤖")
            if seo_master and len(seo_master) > 0:
                st.write(seo_master[0]["response"])
            else:
                st.warning("No response data found")
    with st.expander(f"List of Backlinks"):
            # Get the first backlink ID safely
            if backlinks and len(backlinks) > 0:
                first_backlink = backlinks[0]
                first_backlink_id = first_backlink[0] if isinstance(first_backlink, tuple) else first_backlink.get('id')
                
                if first_backlink_id:
                    seo = get_seo_data(first_backlink_id)
                    if not seo:
                        st.warning("No SEO data found for the selected backlink.")
                    else:
                        for i, seo_data in enumerate(seo):
                            try:
                                link = seo_data['link'] if isinstance(seo_data, dict) else seo_data[2]  # Adjust index as needed based on data structure
                                seo_id = seo_data['id'] if isinstance(seo_data, dict) else seo_data[0]
                                st.write(f"Link {i+1}: {link}")
                                # Safely access query_data if it exists
                                query_data = None
                                if isinstance(seo_data, dict) and "query_data" in seo_data:
                                    query_data = seo_data["query_data"]
                                download_excel_seo(seo_data, query_data, f"SEO_Data_{seo_id}", button_label="Download Excel Data")
                            except (KeyError, IndexError, TypeError) as e:
                                st.warning(f"Error displaying data for item {i+1}: {e}")
                else:
                    st.warning("Could not determine ID for the first backlink")
            else:
                st.warning("No backlinks available")
                




