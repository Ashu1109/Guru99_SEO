import urllib.parse
import requests
def fetch_data_from_link(url,webmaster_access_token):
    start_date = "2025-03-01"
    end_date = "2025-03-31"
    request_data = {
    "startDate": start_date,
    "endDate": end_date,
    "dimensions": ["query"],
    "dimensionFilterGroups": [
        {
            "filters": [
                {
                    "dimension": "page",
                    "expression": url,
                }
            ]
        }
    ],
    "rowLimit": 10000,
    "searchType": "web",
    }
    parsed_url = urllib.parse.urlparse(url)
    site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    encoded_site_url = urllib.parse.quote(site_url, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/searchAnalytics/query"
    headers = {
        "Authorization": f"Bearer {webmaster_access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(api_url, headers=headers, json=request_data)
        response.raise_for_status()  # Raise exception for non-2xx responses
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None