import requests
import json
import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'your_spreadsheet_id_here'
RANGE_NAME = 'Sheet1!A1'

# Fetch data from Pico API
def fetch_data_from_pico():
    pico_url = "http://your-pico-ip/data"  # Replace with your Pico's URL
    try:
        response = requests.get(pico_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from Pico.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

# Authenticate Google Sheets API
def authenticate_google_sheets():
    creds, project = google.auth.default(scopes=SCOPES)
    if not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds)
    return service

# Upload data to Google Sheets
def upload_to_sheets(data):
    service = authenticate_google_sheets()

    # Convert the data to a 2D list format for Google Sheets
    values = []
    for entry in data:
        values.append([entry])  # For simple single column data, adjust as needed

    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updates').get('updatedCells')} cells updated.")

# Main entry point for Cloud Function
def fetch_and_upload(request):
    data = fetch_data_from_pico()
    if data:
        upload_to_sheets(data)
        return "Data uploaded successfully!", 200
    else:
        return "Failed to fetch data from Pico.", 500
