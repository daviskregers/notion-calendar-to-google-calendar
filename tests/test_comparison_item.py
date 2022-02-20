from .testcase import TestCase
from src.comparison_item import ComparisonItem

class TestComparisonItemRetrieval(TestCase):

    id = 'dummy-id'
    created_at = 'some-created-at'
    updated_at = 'some-updated-at'
    title = 'dummy-title'
    link = 'dummy-link'
    start_date = '2022-02-17'
    end_date = '2022-02-18'

    def test_constructs_notion_item(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, self.start_date, self.end_date)

        self.assertEqual(notion_item.id, self.id)
        self.assertEqual(notion_item.created_at, self.created_at)
        self.assertEqual(notion_item.updated_at, self.updated_at)
        self.assertEqual(notion_item.title, self.title)
        self.assertEqual(notion_item.link, self.link)
        self.assertEqual(notion_item.start_date, self.start_date)
        self.assertEqual(notion_item.end_date, self.end_date)

    def test_end_date_matches_start_date_if_none(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, self.start_date, None)

        self.assertEqual(notion_item.end_date, self.start_date)

    def test_type_param_set_as_date(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17', None)

        self.assertEqual(notion_item.type, 'date')

    def test_type_param_set_as_datetime(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17 00:00:00', None)

        self.assertEqual(notion_item.type, 'dateTime')

    def test_if_type_is_datetime_and_end_date_is_none_then_increment_it_by_hour(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17 00:00:00', None)

        self.assertEqual(notion_item.start_date, '2022-02-17T00:00:00')
        self.assertEqual(notion_item.end_date, '2022-02-17T01:00:00')

    def test_if_type_is_datetime_its_iso_format(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17 05:00:00', '2022-02-19 01:23:00')

        self.assertEqual(notion_item.start_date, '2022-02-17T05:00:00')
        self.assertEqual(notion_item.end_date, '2022-02-19T01:23:00')

    def test_throws_if_invalid_string_start_date(self):
        with self.assertRaises(ValueError):
            ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, 'dummy', None)

    def test_throws_if_none_start_date(self):
        with self.assertRaises(TypeError):
            ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, None, None)

    def test_converts_to_google_calendar_item_datetime(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17 05:00:00', '2022-02-19 01:23:00')

        self.assertEqual(notion_item.to_google_calendar_item(), {
            'id': self.id.encode('utf-8').hex(),
            'summary': self.title,
            'location': self.link,
            'start': {
                'dateTime': '2022-02-17T05:00:00',
                'timeZone': 'Europe/Riga'
            },
            'end': {
                'dateTime': '2022-02-19T01:23:00',
                'timeZone': 'Europe/Riga'
            }
        })

    def test_get_id_converts_to_hex(self):
        notion_item = ComparisonItem(self.id, self.created_at, self.updated_at, self.title, self.link, '2022-02-17 05:00:00', '2022-02-19 01:23:00')
        self.assertEqual(notion_item.get_id(), self.id.encode('utf-8').hex())

    def test_equality_returns_true_if_id_title_link_start_end_match(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(True, left == right)

    def test_equality_returns_true_if_id_differ_but_right_is_hex(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id'.encode('utf-8').hex(),
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(True, left == right)

    def test_equality_returns_true_if_id_differ_but_left_is_hex(self):
        left = ComparisonItem(
                'some-id'.encode('utf-8').hex(),
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(True, left == right)

    def test_returns_false_if_ids_differ(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-other-id',
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(False, left == right)

    def test_returns_false_if_titles_differ(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title 2',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(False, left == right)

    def test_returns_false_if_links_differ(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title',
                'link 2',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(False, left == right)

    def test_returns_false_if_start_differ(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:01',
                '2022-02-19T01:23:00'
            )
        self.assertEqual(False, left == right)

    def test_returns_false_if_end_differ(self):
        left = ComparisonItem(
                'some-id',
                'created time',
                'updated time',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:00'
            )
        right = ComparisonItem(
                'some-id',
                'created time 2',
                'updated time 2',
                'title',
                'link',
                '2022-02-19T01:23:00',
                '2022-02-19T01:23:01'
            )
        self.assertEqual(False, left == right)
