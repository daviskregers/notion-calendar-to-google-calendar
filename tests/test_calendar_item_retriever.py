from .testcase import TestCase
from src.comparison_item import ComparisonItem
from unittest import mock
import sys
import json

mock_builder = mock.Mock()
sys.modules['googleapiclient.discovery'] = mock_builder
from src.calendar_item_retriever import CalendarItemRetriever

class MockService:
    pass


class TestCalendarItemRetrieveer(TestCase):

    def setUp(self):
        self.mock_builder = mock_builder
        self.mock_events_service = mock.Mock()
        self.mock_events_list = mock.Mock()
        self.mock_events_collection = mock.Mock()
        self.mock_builder.reset_mock()
        self.mock_events_service.reset_mock()
        self.mock_events_list.reset_mock()
        self.mock_events_collection.reset_mock()

        self.mock_builder.build.return_value = self.mock_events_service
        self.mock_events_service.events.return_value = self.mock_events_list
        self.mock_events_list.list.return_value = self.mock_events_collection
        self.mock_events_collection.execute.return_value = self.mock_events_collection

    def test_accepts_credentials_and_calendar_id_in_constructor(self):
        credentials = 'some-credentials'
        calendar_id = 'some-calendar-id'

        retriever = CalendarItemRetriever(credentials, calendar_id)
        self.assertEqual(retriever.credentials, credentials)
        self.assertEqual(retriever.calendar_id, calendar_id)

    def test_returns_a_list_of_calendar_items(self):
        expected_response = [
            {
                "id": "dummy_id",
                "created": "2022-02-16T17:24:47.000Z",
                "updated": "2022-02-16T17:30:28.391Z",
                "summary": "dummy_title",
                "location": "dummy_link",
                "start": {"date": "2022-03-31"},
                "end": {"date": "2022-04-01"}
            },
            {
                "id": "other_id",
                "created": "2022-02-16T17:25:47.000Z",
                "updated": "2022-02-16T17:31:28.391Z",
                "summary": "other_title",
                "start": {"dateTime": "2022-03-31 05:06:07"},
                "end": {"dateTime": "2022-04-01 12:34:56"}
            }
        ]

        expected_items = [
                ComparisonItem(
                    'dummy_id',
                    '2022-02-16T17:24:47.000Z',
                    '2022-02-16T17:30:28.391Z',
                    'dummy_title',
                    'dummy_link',
                    '2022-03-31',
                    '2022-04-01'
                ),
                ComparisonItem(
                    'other_id',
                    '2022-02-16T17:25:47.000Z',
                    '2022-02-16T17:31:28.391Z',
                    'other_title',
                    None,
                    '2022-03-31 05:06:07',
                    '2022-04-01 12:34:56'
                )
        ]
        self.mock_events_collection.get.return_value = expected_response

        retriever = CalendarItemRetriever('creds', 'calendar_id')
        items = retriever.retrieve_items()

        self.mock_builder.build.assert_called_once_with('calendar', 'v3', credentials='creds')
        self.mock_events_service.events.assert_called_once()
        self.mock_events_list.list.assert_called_once_with(calendarId='calendar_id', singleEvents=True, orderBy='startTime')
        self.mock_events_collection.execute.assert_called_once_with()
        self.mock_events_collection.get.assert_called_once_with('items', [])

        def obj_to_dict(item):
            return item.__dict__

        self.assertEqual(list(map(obj_to_dict, items)), list(map(obj_to_dict, expected_items)))
