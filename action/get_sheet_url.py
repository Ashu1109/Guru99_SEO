from oauth2client.service_account import ServiceAccountCredentials
import gspread
from action.get_only_title import get_only_title

def get_sheet_url(current_title, response_content, sorted_gsc_clicks, clicks_in_title):

    # Install required packages if not already installed
    # !pip install gspread oauth2client

    # Define the scope and credentials
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # You need to have a credentials JSON file from Google Cloud Console
    # If you have a JSON string instead of a file, you can use this approach:
    # credentials_dict = json.loads(credentials_json_string)
    # credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    # If you have a JSON file:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "cred.json", scope
    )

    # Authorize the client
    client = gspread.authorize(credentials)

    # Create a new Google Sheet or open an existing one
    # To create a new sheet:
    new_sheet = client.create("SEO Title Analysis")
    # To open existing sheet:
    # new_sheet = client.open('SEO Title Analysis')

    # Share the sheet with your email (optional)
    # new_sheet.share('2022ugcs008@nitjsr.ac.in', perm_type='user', role='writer')
    # Make the sheet public (anyone with the link can view)
    new_sheet.share(None, perm_type="anyone", role="reader")

    # Select the first sheet
    worksheet = new_sheet.get_worksheet(0)

    # Add data from our dataframe and analysis
    # Headers
    worksheet.update(
        "A1:E1",
        [
            [
                "Current Title",
                "Optimized Title 1",
                "Optimized Title 2",
                "Top GSC Keywords",
                "Title Clicks",
            ]
        ],
    )

    # Data
    worksheet.update("A2", [[current_title]])

    # Extract the optimized titles from the response content
    # Look for the specific title lines in the response
    title1 = None
    title2 = None
    # Parse the response content for the titles
    # Using regex to find the titles more reliably
    titles = get_only_title(response_content)
    title1 = titles[0]
    title2 = titles[1]

    # Check if titles were found
    if title1 and title2:
        worksheet.update("B2", [[title1]])
        worksheet.update("C2", [[title2]])
        print(f"Optimized titles added to spreadsheet:")
        print(f"Title 1: {title1}")
        print(f"Title 2: {title2}")
    else:
        print("Error: Could not extract titles from response content")
        print("Response content format may have changed")

    # Convert dictionaries to strings for Google Sheets
    gsc_keywords_str = ", ".join([f"{k}={v}" for k, v in sorted_gsc_clicks])
    title_clicks_str = ", ".join([f"{k}={v}" for k, v in clicks_in_title.items()])

    # Wrap string values in a list of lists for the update method
    worksheet.update("D2", [[gsc_keywords_str]])
    worksheet.update("E2", [[title_clicks_str]])

    return new_sheet.url