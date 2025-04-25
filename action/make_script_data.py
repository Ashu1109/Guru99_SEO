from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
def make_script_data(processed_array):
    for item in processed_array:
        link = item["link"]
        title = item["title"]
        query_data = item["query_data"]
        clicks_of_words = get_click_of_words(query_data, title)
        top15,GSC_top_KW =top_15_KW(data=query_data)
        item["clicks_of_words"] = clicks_of_words
        item["top15"] = top15
        item["GSC_top_KW"] = GSC_top_KW
    return processed_array
