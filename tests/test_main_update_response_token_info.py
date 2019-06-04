import pytest
from unittest import mock

import boto3
import requests
import json
from src.rotate_codepipeline_tokens.main import update_response_token_info

@pytest.fixture
def username():
    return 'foo_username'

@pytest.fixture
def pipeline_name():
    return 'bar_pipeline_name'

@pytest.fixture
def new_token():
    return 'baz_new_token'

class MockResponse:
    '''
    Class to Mock urllib3 response
    '''
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __iter__(self) -> any:
        '''
        Need to implement iterable in order to be representable
        '''
        for value in [self, self.body]:
            yield value

    def __repr__(self) -> (any, str):
        '''
        Overload the representation of the object for
        assigning values from this class when destructuring
        '''
        return repr([self, self.body])

@mock.patch('botocore.client.BaseClient._make_request')
def test_update_response_token_info_type_is_dict(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': \
            'arn:aws:iam::123456789012:role/' \
            'bar_project_CodePipelineServiceRo-ABC123DEF456',
        'artifactStore': {
            'type': 'S3',
            'location': 'bar_project_artifactstorebucket-abc123def456'
        },
        'stages': [{
            'name': 'Source',
            'actions': [{
                'name': 'SourceAction',
                'actionTypeId': {
                    'category': 'Source',
                    'owner': 'ThirdParty',
                    'provider': 'GitHub',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'Branch': 'foo_branch',
                    'OAuthToken': '****',
                    'Owner': 'bar_owner',
                    'PollForSourceChanges': 'false',
                    'Repo': 'baz_repo'
                },
                'outputArtifacts': [{
                    'name': 'SourceOutput'
                }],
                'inputArtifacts': []
            }]
        },
        {
            'name': 'Build',
            'actions': [{
                'name': 'BuildAction',
                'actionTypeId': {
                    'category': 'Build',
                    'owner': 'AWS',
                    'provider': 'CodeBuild',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'ProjectName': 'FooCodeBuildProject-aBc123DeF456'
                },
                'outputArtifacts': [],
                'inputArtifacts': [{
                    'name': 'SourceOutput'
                }]
            }]
        }],
        'version': 1
    }})

    response = update_response_token_info(
        boto3.client('codepipeline'),
        username,
        pipeline_name,
        new_token
    )
    assert mock_boto.called
    assert isinstance(response, dict)

@mock.patch('botocore.client.BaseClient._make_request')
def test_update_response_token_info_no_update(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': \
            'arn:aws:iam::123456789012:role/' \
            'bar_project_CodePipelineServiceRo-ABC123DEF456',
        'artifactStore': {
            'type': 'S3',
            'location': 'bar_project_artifactstorebucket-abc123def456'
        },
        'stages': [{
            'name': 'Source',
            'actions': [{
                'name': 'SourceAction',
                'actionTypeId': {
                    'category': 'Source',
                    'owner': 'AWS',
                    'provider': 'CodeCommit',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'BranchName': 'foo_branch',
                    'RepositoryName': 'bar_repo'
                },
                'outputArtifacts': [{
                    'name': 'SourceOutput'
                }],
                'inputArtifacts': []
            }]
        },
        {
            'name': 'Build',
            'actions': [{
                'name': 'BuildAction',
                'actionTypeId': {
                    'category': 'Build',
                    'owner': 'AWS',
                    'provider': 'CodeBuild',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'ProjectName': 'FooCodeBuildProject-aBc123DeF456'
                },
                'outputArtifacts': [],
                'inputArtifacts': [{
                    'name': 'SourceOutput'
                }]
            }]
        }],
        'version': 1
    }})

    with pytest.raises(
        Exception,
        match="Not able to adjust pipeline template with new Token!"
    ):
        assert update_response_token_info(boto3.client('codepipeline'), username, pipeline_name, new_token)
        assert mock_boto.called

@mock.patch('botocore.client.BaseClient._make_request')
def test_update_response_token_info_oauth_token_updated_token_name(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': \
            'arn:aws:iam::123456789012:role/' \
            'bar_project_CodePipelineServiceRo-ABC123DEF456',
        'artifactStore': {
            'type': 'S3',
            'location': 'bar_project_artifactstorebucket-abc123def456'
        },
        'stages': [{
            'name': 'Source',
            'actions': [{
                'name': 'SourceAction',
                'actionTypeId': {
                    'category': 'Source',
                    'owner': 'ThirdParty',
                    'provider': 'GitHub',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'Branch': 'foo_branch',
                    'OAuthToken': '****',
                    'Owner': 'bar_owner',
                    'PollForSourceChanges': 'false',
                    'Repo': 'baz_repo'
                },
                'outputArtifacts': [{
                    'name': 'SourceOutput'
                }],
                'inputArtifacts': []
            }]
        },
        {
            'name': 'Build',
            'actions': [{
                'name': 'BuildAction',
                'actionTypeId': {
                    'category': 'Build',
                    'owner': 'AWS',
                    'provider': 'CodeBuild',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'ProjectName': 'FooCodeBuildProject-aBc123DeF456'
                },
                'outputArtifacts': [],
                'inputArtifacts': [{
                    'name': 'SourceOutput'
                }]
            }]
        }],
        'version': 1
    }})

    response = update_response_token_info(
        boto3.client('codepipeline'),
        username,
        pipeline_name,
        new_token
    )
    assert mock_boto.called
    assert response['stages'][0]['actions'][0]['configuration'] \
        ['OAuthToken'] == new_token

@mock.patch('botocore.client.BaseClient._make_request')
def test_update_response_token_info_oauth_token_updated_username(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': \
            'arn:aws:iam::123456789012:role/' \
            'bar_project_CodePipelineServiceRo-ABC123DEF456',
        'artifactStore': {
            'type': 'S3',
            'location': 'bar_project_artifactstorebucket-abc123def456'
        },
        'stages': [{
            'name': 'Source',
            'actions': [{
                'name': 'SourceAction',
                'actionTypeId': {
                    'category': 'Source',
                    'owner': 'ThirdParty',
                    'provider': 'GitHub',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'Branch': 'foo_branch',
                    'OAuthToken': '****',
                    'Owner': 'bar_owner',
                    'PollForSourceChanges': 'false',
                    'Repo': 'baz_repo'
                },
                'outputArtifacts': [{
                    'name': 'SourceOutput'
                }],
                'inputArtifacts': []
            }]
        },
        {
            'name': 'Build',
            'actions': [{
                'name': 'BuildAction',
                'actionTypeId': {
                    'category': 'Build',
                    'owner': 'AWS',
                    'provider': 'CodeBuild',
                    'version': '1'
                },
                'runOrder': 1,
                'configuration': {
                    'ProjectName': 'FooCodeBuildProject-aBc123DeF456'
                },
                'outputArtifacts': [],
                'inputArtifacts': [{
                    'name': 'SourceOutput'
                }]
            }]
        }],
        'version': 1
    }})

    response = update_response_token_info(
        boto3.client('codepipeline'),
        username,
        pipeline_name,
        new_token
    )
    assert mock_boto.called
    assert response['stages'][0]['actions'][0]['configuration'] \
        ['Owner'] == username
