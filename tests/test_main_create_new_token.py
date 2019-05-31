import pytest
from unittest import mock

import requests
import json
from src.rotate_codepipeline_tokens.main import create_new_token

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

@mock.patch('requests.post')
def test_create_new_token_status_code_201(
    mock_post,
    username,
    password,
    otp,
    token
):

    mock_post.return_value = MockResponse(201, {
        'id': 123456789,
        'url': 'https://api.github.com/authorizations/123456789',
        'app': {
            'name': 'qux_token',
            'url': 'https://developer.github.com/v3/oauth_authorizations/',
            'client_id': '00000000000000000000'
        },
        'token': 'foobar',
        'hashed_token': \
            '12ab34cd56ef78gh90ij12lm34no56pq78rs90tu12vw34xy56za78bc90de12fg',
        'token_last_eight': '90de12fg',
        'note': 'qux_token',
        'note_url': None,
        'created_at': '2019-05-31T17:41:09Z',
        'updated_at': '2019-05-31T17:41:09Z',
        'scopes': ['repo', 'admin:repo_hook'],
        'fingerprint': None
    })

    new_token = create_new_token(username, password, otp, token)
    assert mock_post.called
    assert new_token == 'foobar'

@mock.patch('requests.post')
def test_delete_token_status_code_401(
    mock_post,
    username,
    password,
    otp,
    token
):

    mock_post.return_value = MockResponse(401, {
        'message': 'Must specify two-factor authentication OTP code.',
        'documentation_url': \
            'https://developer.github.com' \
            '/v3/auth#working-with-two-factor-authentication'
    })

    with pytest.raises(
        Exception,
        match="Unable to create new Token. Check user credentials!"
    ):
        assert create_new_token(username, password, otp, token)
        assert mock_post.called

@mock.patch('requests.post')
def test_delete_token_status_code_422(
    mock_post,
    username,
    password,
    otp,
    token
):

    mock_post.return_value = MockResponse(422, {
        'message': 'Validation Failed',
        'errors': [{
            'resource': 'OauthAccess',
            'code': 'already_exists',
            'field': 'note'
        }],
        'documentation_url': 'https://developer.github.com' \
            '/v3/oauth_authorizations/#create-a-new-authorization'
    })

    with pytest.raises(
        Exception,
        match="Unable to create new Token. Token already exists!"
    ):
        assert create_new_token(username, password, otp, token)
        assert mock_post.called

@mock.patch('requests.post')
def test_delete_token_status_code_404(
    mock_post,
    username,
    password,
    otp,
    token
):

    mock_post.return_value = MockResponse(404, {})

    with pytest.raises(
        Exception,
        match="Could not create a new GitHub Authorization token!"
    ):
        assert create_new_token(username, password, otp, token)
        assert mock_post.called
