import pytest
from unittest import mock

import requests
import json
from src.rotate_codepipeline_tokens.main import get_current_tokens

@pytest.fixture
def username():
    return 'test_username'

@pytest.fixture
def password():
    return 'test_password'

@pytest.fixture
def otp():
    return 123456

@pytest.fixture
def token():
    return 'test_token'

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
def test_get_current_tokens_status_code_200(mock_api, username, password, otp, token):

    mock_api.return_value = MockResponse(200, [{
        'id': 'foobar',
        'url': 'https://api.github.com/authorizations/123456789'
    }])

    authorizations = get_current_tokens(username, password, otp, token)
    assert mock_api.called
    assert authorizations[0]['id'] == 'foobar'

@mock.patch('requests.get')
def test_get_current_tokens_status_code_401(mock_api, username, password, otp, token):

    mock_api.return_value = MockResponse(401, [])
    with pytest.raises(Exception) as e:
        get_current_tokens(username, password, otp, token)
        assert mock_api.called
        assert str(e) == 'Could not get current list of GitHub tokens!'

