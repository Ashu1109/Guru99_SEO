from action.run_llm import run_llm
from action.connect_to_db import connect_to_db
def get_analysis(processed_item,inserted_id):
    conn,cursor = connect_to_db()
    if conn and cursor:
        link = processed_item["link"]
        title = processed_item["title"]
        query_data = processed_item["query_data"]
        clicks_of_words = processed_item["clicks_of_words"]
        top15 = processed_item["top15"]
        GSC_top_KW = processed_item["GSC_top_KW"]
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