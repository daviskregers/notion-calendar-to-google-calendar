import requests
from src.comparison_item import ComparisonItem

class NotionItemRetriever:
    def __init__(self, token, database_id) -> None:
        self.token = token
        self.database_id = database_id

    def get_token(self) -> str:
        return self.token

    def get_database_id(self) -> str:
        return self.database_id

    def get_notion_items(self, start_cursor = None) -> list:
        body = {
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
        if start_cursor:
            body['start_cursor'] = start_cursor

        results = requests.post(
            f'https://api.notion.com/v1/databases/{self.get_database_id()}/query',
            headers={
                "Authorization": f"Bearer {self.get_token()}",
                "Notion-Version": "2021-08-16"
            },
            json=body,
        ).json()

        items = list(map(self.map_notion_items, results['results']))

        if results['has_more']:
            items += self.get_notion_items(results['next_cursor'])

        return items

    def map_notion_items(self, item):
        return ComparisonItem(
                item['id'],
                item['created_time'],
                item['last_edited_time'],
                item['properties']['Name']['title'][0]['plain_text'],
                item['url'],
                item['properties']['Work Time']['date']['start'],
                item['properties']['Work Time']['date']['end']
            )
