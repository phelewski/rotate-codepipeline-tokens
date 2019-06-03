import pytest
from unittest import mock

import boto3
import requests
import json
from src.rotate_codepipeline_tokens.main import codepipeline_get_pipeline

@pytest.fixture
def pipeline_name():
    return 'foo_pipeline_name'

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
def test_codepipeline_get_pipeline_type_is_dict(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': 'arn:aws:iam::123456789012:role/bar_project_CodePipelineServiceRo-ABC123DEF456',
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

    response = codepipeline_get_pipeline(boto3.client('codepipeline'), pipeline_name)
    assert mock_boto.called
    assert isinstance(response, dict)

@mock.patch('botocore.client.BaseClient._make_request')
def test_codepipeline_get_pipeline_name_type_is_str(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': 'arn:aws:iam::123456789012:role/bar_project_CodePipelineServiceRo-ABC123DEF456',
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

    response = codepipeline_get_pipeline(boto3.client('codepipeline'), pipeline_name)
    assert mock_boto.called
    assert isinstance(response['name'], str)

@mock.patch('botocore.client.BaseClient._make_request')
def test_codepipeline_get_pipeline_name_matches(
    mock_boto,
    pipeline_name
):

    mock_boto.return_value = MockResponse(200, {'pipeline': {
        'name': 'foo_pipeline_name',
        'roleArn': 'arn:aws:iam::123456789012:role/bar_project_CodePipelineServiceRo-ABC123DEF456',
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

    response = codepipeline_get_pipeline(boto3.client('codepipeline'), pipeline_name)
    assert mock_boto.called
    assert response['name'] == 'foo_pipeline_name'
