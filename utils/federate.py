import gspread
from oauth2client.service_account import ServiceAccountCredentials


def sync():
    try:
        print("Authorizing credentials...")
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        print("Accessing worksheet...")
        sheets = client.open_by_key("1RRx2XM7fhFoYxeGlEeKog1xHeU06eAUXLm1zOXfO5nk").worksheet("MM Registration Form Responses")
        print(sheets.col_values(1))
        return True
    except Exception as e:
        print("ERROR: " + str(e))
        print(">> Worksheet not found.")

        return False