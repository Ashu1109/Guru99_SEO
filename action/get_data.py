from action.get_click_of_words import get_click_of_words
from action.top_15_KW import top_15_KW
from action.fetch_data_from_link import fetch_data_from_link
# TODO: Add the function to fetch data from Google Search Console and formate the data according to it...
def get_data(input_link, input_title):

    # TODO:
    if input_link:
        fetched_data = fetch_data_from_link(
            input_link,
            "ya29.a0AZYkNZg3wqbNveOG2EgUwGE4YzxDvrf8LerhRaOC4fpJpdA2mbYK0uXbJII6jdEY-xjzYjdMltZkjM4mkmcMs-w3Z9l-AsenC38s976es6y6O-RfXuyku2jYqJI49QP5VofX6zJBY1PKlx3nDRFHSo5vrfOxzjyqpRgU4A6BaCgYKASASARASFQHGX2MitXxDmTlyXKhXr5InAGE1Qg0175",
        )
        return fetched_data

    # current_title = input_link

    # sorted_gsc_clicks = getGscClick(current_title)

    current_title = input_title
    sorted_gsc_clicks = top_15_KW()
    result_df, full_results = sorted_gsc_clicks
    clicks_in_title = get_click_of_words(current_title)
    return current_title, sorted_gsc_clicks, clicks_in_title
