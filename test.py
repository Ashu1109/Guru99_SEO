import requests
from action.get_processed_array import access_token
def get_filtered_links():
    access_token_ = access_token()
    site_url = 'https://www.guru99.com/'  # Use the exact property URL
    api_url = f'https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(site_url, safe="")}/searchAnalytics/query'

    body = {
        "startDate": "2025-04-01",
        "endDate": "2025-04-29",
        "dimensions": ["page"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "contains",
                "expression": "/best-private-twitter-viewer-apps.html"
            }]
        }],
        "rowLimit": 1000
    }

    headers = {
        'Authorization': f'Bearer {access_token_}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=body, headers=headers)
    return response.json()

