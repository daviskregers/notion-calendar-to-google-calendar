from googleapiclient.discovery import build
from src.comparison_item import ComparisonItem

class CalendarItemRetriever:
    def __init__(self, credentials, calendar_id):
        self.credentials = credentials
        self.calendar_id = calendar_id

    def retrieve_items(self):
        service = build('calendar', 'v3', credentials=self.credentials)
        events_result = service.events().list(calendarId=self.calendar_id,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        return list(map(self.map_to_comparison_item, events))

    def map_to_comparison_item(self, item):
        return ComparisonItem(
                item['id'],
                item['created'],
                item['updated'],
                item['summary'],
                item.get('location'),
                item['start']['date'] if 'date' in item['start'].keys() else item['start']['dateTime'],
                item['end']['date'] if 'date' in item['end'].keys() else item['end']['dateTime'],
            )
