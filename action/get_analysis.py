from action.run_llm import run_llm
from action.connect_to_db import connect_to_db
def get_analysis(processed_array,file_name):
    conn,cursor = connect_to_db()
    sql = "INSERT INTO excel_sheet (name) VALUES (%s)"
    cursor.execute(sql, (file_name,))
    conn.commit()
    inserted_id = cursor.lastrowid
    for item in processed_array:
        link = item["link"]
        title = item["title"]
        query_data = item["query_data"]
        clicks_of_words = item["clicks_of_words"]
        top15 = item["top15"]
        GSC_top_KW = item["GSC_top_KW"]
        run_llm(
            inserted_id=inserted_id,
            conn=conn,
            cursor=cursor,
            query_data=query_data,
            input_link=link,
            current_title=title,
            clicks_in_title=clicks_of_words,
            top_15_KW=top15,
            GSC_Top_KW_Clicks=GSC_top_KW
        )