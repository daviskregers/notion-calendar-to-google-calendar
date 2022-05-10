from .testcase import TestCase
from src.notion_item_retriever import NotionItemRetriever
from src.comparison_item import ComparisonItem
from unittest import mock

global first_response, next_response_second
first_response = True
next_response_second = True

EXPECTED = [{'id': '123', 'title': 'Title 1'}, {'id': '456', 'title': 'Title 2'}]
expected_response = [
    {
        "id": "dummy_id",
        "created_time": "2022-02-16T17:24:47.000Z",
        "last_edited_time": "2022-02-16T17:30:28.391Z",
        "url": "dummy_link",
        "properties": {
            'Name': {'id': 'title',
                      'title': [{'plain_text': 'dummy_title'}],
                      'type': 'title'},
            'Work Time': {'date': {'end': None,
                            'start': '2022-02-24',
                            'time_zone': None},
                   'type': 'date'}
        }
    },
    {
        "id": "other_id",
        "created_time": "2022-02-16T17:24:47.000Z",
        "last_edited_time": "2022-02-16T17:30:28.391Z",
        "url": "https://asdasd",
        "properties": {
            'Name': {'id': 'title',
                      'title': [{'plain_text': 'other_title'}],
                      'type': 'title'},
            'Work Time': {'date': {'end': '2022-02-24',
                            'start': '2022-02-22',
                            'time_zone': None},
                   'type': 'date'}
        }
    },
    {
        "id": "different_id",
        "created_time": "2022-02-16T17:24:47.000Z",
        "last_edited_time": "2022-02-16T17:30:28.391Z",
        "url": "https://asdasd",
        "properties": {
            'Name': {'id': 'title',
                      'title': [{'plain_text': 'yet another title'}],
                      'type': 'title'},
            'Work Time': {'date': {'end': '2022-02-24T13:00:00.000+02:00',
                            'start': '2022-02-24T00:00:00.000+02:00',
                            'time_zone': None},
                   'type': 'date'}
        }
    }
]
expected_second_response = [
    {
        "id": "dummy_id_",
        "created_time": "2022-02-16T17:24:47.000Z",
        "last_edited_time": "2022-02-16T17:30:28.391Z",
        "url": "dummy_link",
        "properties": {
            'Name': {'id': 'title',
                      'title': [{'plain_text': 'dummy_title'}],
                      'type': 'title'},
            'Work Time': {'date': {'end': None,
                            'start': '2022-02-24',
                            'time_zone': None},
                   'type': 'date'}
        }
    },
    {
        "id": "dummy_id__",
        "created_time": "2022-02-16T17:24:47.000Z",
        "last_edited_time": "2022-02-16T17:30:28.391Z",
        "url": "dummy_link",
        "properties": {
            'Name': {'id': 'title',
                      'title': [{'plain_text': 'dummy_title'}],
                      'type': 'title'},
            'Work Time': {'date': {'end': None,
                            'start': '2022-02-24',
                            'time_zone': None},
                   'type': 'date'}
        }
    },
]

expected_items = [
        ComparisonItem(
            'dummy_id',
            '2022-02-16T17:24:47.000Z',
            '2022-02-16T17:30:28.391Z',
            'dummy_title',
            'dummy_link',
            '2022-02-24',
            ''
        ),
        ComparisonItem(
            'other_id',
            '2022-02-16T17:24:47.000Z',
            '2022-02-16T17:30:28.391Z',
            'other_title',
            'https://asdasd',
            '2022-02-22',
            '2022-02-24'
        ),
        ComparisonItem(
            'different_id',
            '2022-02-16T17:24:47.000Z',
            '2022-02-16T17:30:28.391Z',
            'yet another title',
            'https://asdasd',
            '2022-02-24T00:00:00.000+02:00',
            '2022-02-24T13:00:00.000+02:00'
        ),
]

expected_second_items = [
        ComparisonItem(
            'dummy_id_',
            '2022-02-16T17:24:47.000Z',
            '2022-02-16T17:30:28.391Z',
            'dummy_title',
            'dummy_link',
            '2022-02-24',
            ''
        ),
        ComparisonItem(
            'dummy_id__',
            '2022-02-16T17:24:47.000Z',
            '2022-02-16T17:30:28.391Z',
            'dummy_title',
            'dummy_link',
            '2022-02-24',
            ''
        ),
]

class MockResponse:
    def __init__(self, json_data, status_code, paged = False):
        global first_response, next_response_second
        if first_response:
            first_response = False
            next_response_second = True
        else:
            paged = False
            next_response_second = False
        self.json_data = {'results': json_data, 'has_more': paged}
        if paged:
            self.json_data['next_cursor'] = 'some-cursor'
        self.status_code = status_code

    def json(self):
        return self.json_data

def mock_request(*args, **kwargs):
    return MockResponse(expected_response, 200)

def mock_request_paged(*args, **kwargs):
    global next_response_second
    response = expected_second_response if next_response_second else expected_response
    return MockResponse(response, 200, True)

class TestNotionItemRetriever(TestCase):

    def test_sets_token_id(self):
        tokens = ['123', '345', '678']
        for token in tokens:
            retriever = NotionItemRetriever(token, 'asdad')
            self.assertEqual(retriever.get_token(), token)

    def test_sets_database_id(self):
        database_ids = ['123', '345', '678']
        for database_id in database_ids:
            retriever = NotionItemRetriever('token', database_id)
            self.assertEqual(retriever.get_database_id(), database_id)

    @mock.patch('requests.post', side_effect=mock_request)
    def test_notion_item_retrieval(self, mock_get):
        service = NotionItemRetriever('dummy_token', 'dummy_database_id')

        for token in ['dummy_token', 'even_dummer_token']:
            for database_id in ['dummy_database_id', 'even_dummer_database_id']:
                service = NotionItemRetriever(token, database_id)
                items = service.get_notion_items()

                self.assertEqual(mock.call(
                    f'https://api.notion.com/v1/databases/{database_id}/query',
                    headers={
                        "Authorization": f'Bearer {token}',
                        "Notion-Version": "2021-08-16"
                    },
                    json={
                        "filter": {
                            "and": [
                                {
                                    "property": "Archive",
                                    "checkbox": {
                                        "equals": False
                                    }
                                },
                                {
                                    "property": "Work Time",
                                    "date": {
                                        "is_not_empty": True
                                    }
                                },
                            ]
                        },
                    }
                ), mock_get.call_args)

                def obj_to_dict(item):
                    return item.__dict__

                self.assertEqual(list(map(obj_to_dict, items)), list(map(obj_to_dict, expected_items)))

    @mock.patch('requests.post', side_effect=mock_request_paged)
    def test_throws_not_implemented_if_not_all_records_are_on_the_first_page(self, mock_get):
        global first_response, next_response_second
        first_response = True
        next_response_second = False
        token = 'some_token'
        database_id = 'some_id'
        service = NotionItemRetriever(token, database_id)
        items = service.get_notion_items()

        self.assertEqual(mock.call(
            f'https://api.notion.com/v1/databases/{database_id}/query',
            headers={
                "Authorization": f'Bearer {token}',
                "Notion-Version": "2021-08-16"
            },
            json={
                "filter": {
                    "and": [
                        {
                            "property": "Archive",
                            "checkbox": {
                                "equals": False
                            }
                        },
                        {
                            "property": "Work Time",
                            "date": {
                                "is_not_empty": True
                            }
                        },
                    ]
                },
                'start_cursor': 'some-cursor'
            }
        ), mock_get.call_args)

        def obj_to_dict(item):
            return item.__dict__

        actual = list(map(obj_to_dict, items))
        expected = \
            list(map(obj_to_dict, expected_items)) + \
            list(map(obj_to_dict, expected_second_items))

        self.assertEqual(actual, expected)
