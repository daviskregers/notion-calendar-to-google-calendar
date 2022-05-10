import datetime
from dateutil.parser import parse

class ComparisonItem:

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, id, created_at, updated_at, title, link, start_date, end_date) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.title = title
        self.link = link
        self.start_date = parse(start_date)
        self.same_day_event = False
        self.end_date = parse(end_date if end_date else start_date)
        self.type = 'date' if ':' not in start_date else 'dateTime' # TODO: this should be const as well as date
        if self.type == 'date' and start_date == end_date:
            self.same_day_event = True

        if self.type == 'dateTime':
            if (self.start_date == self.end_date):
                self.end_date = self.end_date + datetime.timedelta(hours=1)

            self.start_date = self.start_date.isoformat()
            self.end_date = self.end_date.isoformat()
        else:
            if not self.same_day_event:
                self.end_date += datetime.timedelta(days=1)
            self.start_date = self.start_date.strftime(self.DATE_FORMAT)
            self.end_date = self.end_date.strftime(self.DATE_FORMAT)

    def get_id(self):
        return self.id.encode('utf-8').hex()

    def __eq__(self, other):
        return (
                    (
                        self.id == other.id or
                        self.id == other.get_id() or
                        self.get_id() == other.id
                    ) and
                    self.title == other.title and
                    self.link == other.link and
                    self.start_date == other.start_date and
                    self.end_date == other.end_date
                )

    def to_google_calendar_item(self):
        return {
            'id': self.id.encode('utf-8').hex(),
            'summary': self.title,
            'location': self.link,
            'start': {
                self.type: self.start_date,
                'timeZone': 'Europe/Riga'
            },
            'end': {
                self.type: self.end_date,
                'timeZone': 'Europe/Riga'
            }
        }
