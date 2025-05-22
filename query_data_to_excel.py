import pandas as pd
import json
import io
import streamlit as st

# Sample query data (replace with your actual data)
query_data_str = """{"rows": [{"keys": "contains in xpath", "clicks": 202, "impressions": 325, "ctr": 0.6215384615384615, "position": 1.32}, {"keys": "contains xpath", "clicks": 138, "impressions": 322, "ctr": 0.42857142857142855, "position": 2.596273291925466}]}"""

def convert_query_data_to_excel(query_data_str):
    try:
        # Parse the JSON string if it's a string
        if isinstance(query_data_str, str):
            query_data = json.loads(query_data_str)
        else:
            query_data = query_data_str
            
        # Check if the data has the expected 'rows' structure
        if 'rows' in query_data and isinstance(query_data['rows'], list):
            # Extract the rows data
            rows = query_data['rows']
            
            # Create a DataFrame from the rows
            df = pd.DataFrame(rows)
            
            # Create an Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Query Data')
                
                # Get the workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Query Data']
                
                # Add some formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'border': 1
                })
                
                # Write the column headers with the defined format
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    
                # Set column widths
                worksheet.set_column('A:A', 30)  # keys column
                worksheet.set_column('B:E', 15)  # other columns
            
            # Get the Excel data
            excel_data = output.getvalue()
            
            # For Streamlit, provide a download button
            st.download_button(
                label="Download Query Data Excel",
                data=excel_data,
                file_name="query_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            return excel_data
            
    except Exception as e:
        st.error(f"Error converting query data to Excel: {e}")
        return None

# For testing
if __name__ == "__main__":
    st.title("Query Data to Excel Converter")
    
    # Text area for pasting JSON data
    input_data = st.text_area("Paste your query data JSON here:", value=query_data_str, height=300)
    
    if st.button("Convert to Excel"):
        convert_query_data_to_excel(input_data)
