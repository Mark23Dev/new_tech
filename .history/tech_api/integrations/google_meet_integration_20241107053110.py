import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.conf import settings

# SCOPES specify the permissions your application will need
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path to your OAuth2 credentials file
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'path/to/credentials.json')

def get_authenticated_service():
    """Authenticate and return the Google Calendar service instance."""
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_google_meet_event(summary, description, start_time, end_time, attendees_emails):
    """
    Create a Google Meet event using the Google Calendar API.
    
    Args:
    - summary: The event title
    - description: Event description
    - start_time: Event start time (datetime object)
    - end_time: Event end time (datetime object)
    - attendees_emails: List of attendees' email addresses
    
    Returns:
    - The created event data including the Meet link
    """
    service = get_authenticated_service()
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',  # unique request ID for creating conference links
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            }
        },
        'attendees': [{'email': email} for email in attendees_emails],
    }
    
    try:
        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        return {
            "meet_link": created_event.get('hangoutLink'),
            "event_id": created_event.get('id'),
            "html_link": created_event.get('htmlLink')
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
