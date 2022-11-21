from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/contacts.readonly']

CREDENTIALS_FILE = './credentials.json'

class Calendar():

    def login(self):
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
                try:
                    creds.refresh(Request())
                except Exception:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(
                        port=0, 
                        success_message="Successfully authorized Chatbot! You can close this window.", 
                        open_browser=True, 
                        redirect_uri_trailing_slash=True
                    ) 
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(
                    port=0, 
                    success_message="Successfully authorized Chatbot! You can close this window.", 
                    open_browser=True, 
                    redirect_uri_trailing_slash=True
                )

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)
        self.peopleservice = build('people', 'v1', credentials=creds)

    def get_calendar_list(self):
        # Call the Calendar API
        print('Getting list of calendars')
        calendars_result = self.service.calendarList().list().execute()

        calendars = calendars_result.get('items', [])
        cal_list = []

        if not calendars:
            print('No calendars found.')
        for calendar in calendars:
            summary = calendar['summary']
            cal_list.append({"name":calendar['summary'],"id":calendar['id']})
        return cal_list

    def get_events(self, num=10):
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print(f'Getting List of {num} events')
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=num, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        event_list = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_list.append({"start":start,"summary":event['summary']})
        return event_list

    def create_event(self,
        title="Automated Event",
        desc='This is a tutorial example of automating google calendar with python',
        start=None,
        end=None,
        tz='Australia/Perth'
    ):
        d = datetime.now().date()
        tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
        if start is None: start = tomorrow.isoformat()
        if end is None: end = (tomorrow + timedelta(hours=1)).isoformat()

        event_result = self.service.events().insert(calendarId='primary',
            body={
                "summary": title,
                "description": desc,
                "start": {"dateTime": start, "timeZone": tz},
                "end": {"dateTime": end, "timeZone": tz},
            }
        ).execute()

        print("Created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    def get_contacts(self):
        results = self.peopleservice.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses').execute()
        return results
    
    def get_contact(self, query):
        search_results = self.peopleservice.people().searchContacts(
            query = "",
            readMask = "names"
        )
        sleep(1)
        search_results = self.peopleservice.people().searchContacts(
            query = query,
            readMask = "names"
        ).execute()
        if search_results.get("results") == None: return None
        resourcesname = search_results["results"][0]["person"]["resourceName"]
        person = self.peopleservice.people().get(
            resourceName = resourcesname,
            personFields = "names,phoneNumbers,emailAddresses"
        ).execute()

        personInfo = {
            "name" : person.get('names')[0].get("displayName") if person.get('names') else None,
            "email" : person.get("emailAddresses")[0].get("value") if person.get('emailAddresses') else None,
            "phone" : person.get("phoneNumbers")[0].get("canonicalForm") if person.get('phoneNumbers') else None,
        }
        return personInfo


if __name__ == '__main__':
    cal = Calendar()
    cal.login()
    from pprint import pprint
    pprint(cal.get_calendar_list())
    pprint(cal.get_events())

    contact = cal.get_contact("zo")
    print("Search")
    pprint(contact)
    # if input("Create calendar event (y/n)")=="y":
        # cal.create_event()
