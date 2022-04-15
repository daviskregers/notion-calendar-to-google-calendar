# Notion Calendar - Google Calendar sync

[![codecov](https://codecov.io/gh/daviskregers/notion-calendar-to-google-calendar/branch/main/graph/badge.svg?token=YJ27Q8HISR)](https://codecov.io/gh/daviskregers/notion-calendar-to-google-calendar)

This will take a notion database and sync changes to a google calendar.

- Create a notion integration at: https://www.notion.so/my-integrations
- Share the database with the integration: https://developers.notion.com/docs/getting-started
- Create a google api key with google calendar integration enabled, download the credentials.json and place them into the root directory.
- Copy .env.example to .env file and fill in the secrets
- python main.py

## Note on the Notion properties

I'm using the the second brain notion template https://www.notion.so/Second-Brain-87220ae827774816aa7328a131f1fd2f
and the properties match the project properties there.

## Development

- Tests: `make test`
- Coverage `make coverage`
