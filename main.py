from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.calendar_credentials_obtainer import CalendarCredentialsObtainer
from src.calendar_item_retriever import CalendarItemRetriever
from src.notion_item_retriever import NotionItemRetriever
import os

def main():
    credentials    = CalendarCredentialsObtainer().get_credentials()
    calendar_id    = os.getenv('CALENDAR_ID')
    token          = os.getenv('NOTION_TOKEN')
    database_id    = os.getenv('NOTION_DATABASE_ID')
    calendar_items = CalendarItemRetriever(credentials, calendar_id).retrieve_items()
    notion_items   = NotionItemRetriever(token, database_id).get_notion_items()

    service = build('calendar', 'v3', credentials=credentials)
    def callback_s(id, res, exc):
        print(id, res, exc)

    br = service.new_batch_http_request(callback=callback_s)
    for item in notion_items:
        found = False
        for event in calendar_items:
            if event.id == item.get_id():
                found = True
                matches = event == item
                if not matches:
                    sr = service.events().update(
                            calendarId=calendar_id,
                            eventId=event.id,
                            body=item.to_google_calendar_item()
                        )
                    br.add(sr, request_id=event.id)

        if not found:
            sr = service.events().insert(
                    calendarId=calendar_id,
                    body=item.to_google_calendar_item()
                )
            br.add(sr, request_id=item.id)
    br.execute()

def obj_to_dict(item):
    return item.__dict__

if __name__ == '__main__':
    load_dotenv()
    main()
