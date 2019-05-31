import pytest
from unittest import mock

import requests
import json
from src.rotate_codepipeline_tokens.main import get_token_id

@pytest.fixture
def username():
    return 'foo_username'

@pytest.fixture
def password():
    return 'bar_password'

@pytest.fixture
def otp():
    return 'baz_otp'

@pytest.fixture
def token():
    return 'qux_token'

class MockResponse(object):
    '''
    Class to Mock urllib3 response
    '''
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def json(self):
        return self.body

@mock.patch('requests.get')
def test_get_token_id_exists(
    mock_api,
    username,
    password,
    otp,
    token
):

    mock_api.return_value = MockResponse(200, [{
        'id': 123456789,
        'url': 'https://api.github.com/authorizations/123456789',
        'app': {
            'name': 'qux_token',
            'url': 'https://developer.github.com/v3/oauth_authorizations/',
            'client_id': '00000000000000000000'
        },
        'token': '',
        'hashed_token': \
            '12ab34cd56ef78gh90ij12lm34no56pq78rs90tu12vw34xy56za78bc90de12fg',
        'token_last_eight': '90de12fg',
        'note': 'qux_token',
        'note_url': None,
        'created_at': '2019-05-30T15:21:24Z',
        'updated_at': '2019-05-30T15:21:24Z',
        'scopes': ['repo', 'admin:repo_hook'],
        'fingerprint': None
    }])

    response = get_token_id(username, password, otp, token)
    assert mock_api.called
    assert response == 123456789

@mock.patch('requests.get')
def test_get_token_id_does_not_exist(
    mock_api,
    username,
    password,
    otp,
    token
):

    mock_api.return_value = MockResponse(200, [{
        'id': 123456789,
        'url': 'https://api.github.com/authorizations/123456789',
        'app': {
            'name': 'foobar',
            'url': 'https://developer.github.com/v3/oauth_authorizations/',
            'client_id': '00000000000000000000'
        },
        'token': '',
        'hashed_token': \
            '12ab34cd56ef78gh90ij12lm34no56pq78rs90tu12vw34xy56za78bc90de12fg',
        'token_last_eight': '90de12fg',
        'note': 'foobar',
        'note_url': None,
        'created_at': '2019-05-30T15:21:24Z',
        'updated_at': '2019-05-30T15:21:24Z',
        'scopes': ['repo', 'admin:repo_hook'],
        'fingerprint': None
    }])

    with pytest.raises(
        Exception,
        match="GitHub token name does not exist!"
    ):
        assert get_token_id(username, password, otp, token)
        assert mock_api.called
