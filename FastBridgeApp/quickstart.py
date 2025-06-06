from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
Bridge_sheet_id = '1jA7KbTKS8UUZ_E_gu4Tr5IpQWntQu16wxixTDm45bM0' #not a secret thing
SAMPLE_RANGE_NAME = 'Bridge Texts!A1:H'
#important: the final column should have values for all texts, otherwise we end up with non existent cells, which are even worse than empty cells

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=Bridge_sheet_id,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))

    if not values:
        print('No data found.')
    return values

if __name__ == '__main__':
    main()
