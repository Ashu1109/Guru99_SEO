import urllib.parse
import requests
from datetime import datetime, timedelta
def fetch_data_from_link(url,webmaster_access_token):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=29)
    start_date = start_date.isoformat()
    end_date = end_date.isoformat()
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