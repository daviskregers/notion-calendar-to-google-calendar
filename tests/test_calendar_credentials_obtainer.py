from .testcase import TestCase
from google.oauth2.credentials import Credentials
from src.calendar_credentials_obtainer import CalendarCredentialsObtainer
from unittest import mock

def mock_path_does_exist(path) -> bool:
    return True

def mock_path_doesnt_exist(path) -> bool:
    return False

class CredentialRefresh(Exception):
    pass

class MockCredentials(object):
    def __init__(self, response, valid = True, expired = False, refresh_token = True):
        self.response = response
        self.valid = valid
        self.expired = expired
        self.refresh_token = refresh_token

    def refresh(self, request):
        raise CredentialRefresh(request)

    def to_json(self):
        return self.response


class TestCalendarCredentialsObtainer(TestCase):

    @mock.patch.object(Credentials, 'from_authorized_user_file')
    @mock.patch('os.path.exists', side_effect=mock_path_does_exist)
    def test_get_credentials_when_token_file_exists(self, mock_path_exists, mock_token_read):
        expected = MockCredentials('very-legit-credentials-yes')
        mock_token_read.return_value = expected

        credentials_obtainer = CalendarCredentialsObtainer()
        credentials = credentials_obtainer.get_credentials()

        self.assertEqual(credentials, expected)
        mock_path_exists.assert_called_once_with('token.json')
        self.assert_called_path_with_scopes(mock_token_read)

    def assert_called_path_with_scopes(self, mock, file = 'token.json') -> None:
        mock.assert_called_once_with(
            file,
            [
                'https://www.googleapis.com/auth/calendar'
            ]
        )

    @mock.patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file')
    @mock.patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    @mock.patch('os.path.exists', side_effect=mock_path_doesnt_exist)
    def test_get_credentials_when_token_file_doesnt_exist(self, mock_path_exists, mock_token_read, mock_flow):
        expected = MockCredentials('very-legit-secret-credentials-yes')
        instance = mock_flow.return_value
        instance.run_local_server.return_value = expected

        with mock.patch('builtins.open', mock.mock_open()) as m:
            credentials_obtainer = CalendarCredentialsObtainer()
            credentials = credentials_obtainer.get_credentials()

            self.assertEqual(credentials, expected)
            mock_path_exists.assert_called_once_with('token.json')
            mock_token_read.assert_not_called()
            self.assert_called_path_with_scopes(mock_flow, 'credentials.json')

            m.assert_called_once_with('token.json', 'w')
            handle = m()
            handle.write.assert_called_once_with(expected.to_json())

    def test_token_file_found_not_valid_not_expired(self):
        combinations = [
                {'expired': False, 'refresh_token': False},
                {'expired': False, 'refresh_token': True },
                {'expired': True,  'refresh_token': False},
            ]

        for conf in combinations:
            with mock.patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
                with mock.patch('google.oauth2.credentials.Credentials.from_authorized_user_file') as mock_token_read:
                    with mock.patch('os.path.exists', side_effect=mock_path_does_exist) as mock_path_exists:
                        # print(conf)
                        expected = MockCredentials('very-legit-credentials-yes', False, conf['expired'], conf['refresh_token'])
                        mock_token_read.return_value = expected
                        instance = mock_flow.return_value
                        instance.run_local_server.return_value = expected

                        with mock.patch('builtins.open', mock.mock_open()) as m:
                            credentials_obtainer = CalendarCredentialsObtainer()
                            credentials = credentials_obtainer.get_credentials()

                            self.assertEqual(credentials, expected)
                            mock_path_exists.assert_called_once_with('token.json')
                            self.assert_called_path_with_scopes(mock_token_read)
                            self.assert_called_path_with_scopes(mock_flow, 'credentials.json')

                            m.assert_called_once_with('token.json', 'w')
                            handle = m()
                            handle.write.assert_called_once_with(expected.to_json())

    @mock.patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    @mock.patch('os.path.exists', side_effect=mock_path_does_exist)
    def test_token_file_found_expired_with_refresh_token(self, mock_path_exists, mock_token_read):
        expected = MockCredentials('very-legit-credentials-yes', False, True, True)
        mock_token_read.return_value = expected

        credentials_obtainer = CalendarCredentialsObtainer()

        self.assertRaises(CredentialRefresh, credentials_obtainer.get_credentials)
