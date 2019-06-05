import pytest
from unittest import mock

import boto3
import requests
import json
from src.rotate_codepipeline_tokens.main import codepipeline_update_pipeline

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

@mock.patch('src.rotate_codepipeline_tokens.main.update_response_token_info')
@mock.patch('botocore.client.BaseClient._make_request')
def test_codepipeline_update_pipeline_httpstatuscode_is_200(
    mock_boto,
    mock_update,
    pipeline_name
):

    mock_boto.return_value = MockResponse(
        200,
        {
            'pipeline': {
                'name': 'foo_pipeline_name',
                'roleArn': \
                    'arn:aws:iam::123456789012:role/' \
                    'bar_project_CodePipelineServiceRo-ABC123DEF456',
                'artifactStore': {
                    'type': 'S3',
                    'location': 'bar_project_artifactstorebucket-abc123def456'
                },
                'stages': [
                    {
                        'name': 'Source',
                        'actions': [
                            {
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
                                    'OAuthToken': 'foobar_token',
                                    'Owner': 'bar_owner',
                                    'PollForSourceChanges': 'false',
                                    'Repo': 'baz_repo'
                                },
                                'outputArtifacts': [
                                    {
                                        'name': 'SourceOutput'
                                    }
                                ],
                                'inputArtifacts': []
                            }
                        ]
                    },
                    {
                        'name': 'Build',
                        'actions': [
                            {
                                'name': 'BuildAction',
                                'actionTypeId': {
                                    'category': 'Build',
                                    'owner': 'AWS',
                                    'provider': 'CodeBuild',
                                    'version': '1'
                                },
                                'runOrder': 1,
                                'configuration': {
                                    'ProjectName': \
                                        'FooCodeBuildProject-aBc123DeF456'
                                },
                                'outputArtifacts': [],
                                'inputArtifacts': [
                                    {
                                        'name': 'SourceOutput'
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'version': 1
            },
            'ResponseMetadata': {
                'RequestId': 'abcd1234-12ab-34cd-56ef-abcdef123456',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'abcd1234-12ab-34cd-56ef-abcdef123456',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '986'
                },
                'RetryAttempts': 0
            }
        }
    )

    mock_update.return_value = dict(
        {
            'name': 'foo_pipeline_name',
            'roleArn': \
                'arn:aws:iam::123456789012:role/' \
                'bar_project_CodePipelineServiceRo-ABC123DEF456',
            'artifactStore': {
                'type': 'S3',
                'location': 'bar_project_artifactstorebucket-abc123def456'
            },
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
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
                            'outputArtifacts': [
                                {
                                    'name': 'SourceOutput'
                                }
                            ],
                            'inputArtifacts': []
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'runOrder': 1,
                            'configuration': {
                                'ProjectName': \
                                    'FooCodeBuildProject-aBc123DeF456'
                            },
                            'outputArtifacts': [],
                            'inputArtifacts': [
                                {
                                    'name': 'SourceOutput'
                                }
                            ]
                        }
                    ]
                }
            ],
            'version': 1
        }
    )

    response = codepipeline_update_pipeline(
        boto3.client('codepipeline'),
        username,
        pipeline_name,
        new_token
    )

    assert mock_boto.called
    assert mock_update.called
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

@mock.patch('src.rotate_codepipeline_tokens.main.update_response_token_info')
@mock.patch('botocore.client.BaseClient._make_request')
def test_codepipeline_update_pipeline_httpstatuscode_is_400(
    mock_boto,
    mock_update,
    pipeline_name
):

    mock_boto.return_value = MockResponse(
        200,
        {
            'pipeline': {
                'name': 'foo_pipeline_name',
                'roleArn': \
                    'arn:aws:iam::123456789012:role/' \
                    'bar_project_CodePipelineServiceRo-ABC123DEF456',
                'artifactStore': {
                    'type': 'S3',
                    'location': 'bar_project_artifactstorebucket-abc123def456'
                },
                'stages': [
                    {
                        'name': 'Source',
                        'actions': [
                            {
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
                                    'OAuthToken': 'foobar_token',
                                    'Owner': 'bar_owner',
                                    'PollForSourceChanges': 'false',
                                    'Repo': 'baz_repo'
                                },
                                'outputArtifacts': [
                                    {
                                        'name': 'SourceOutput'
                                    }
                                ],
                                'inputArtifacts': []
                            }
                        ]
                    },
                    {
                        'name': 'Build',
                        'actions': [
                            {
                                'name': 'BuildAction',
                                'actionTypeId': {
                                    'category': 'Build',
                                    'owner': 'AWS',
                                    'provider': 'CodeBuild',
                                    'version': '1'
                                },
                                'runOrder': 1,
                                'configuration': {
                                    'ProjectName': \
                                        'FooCodeBuildProject-aBc123DeF456'
                                },
                                'outputArtifacts': [],
                                'inputArtifacts': [
                                    {
                                        'name': 'SourceOutput'
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'version': 1
            },
            'ResponseMetadata': {
                'RequestId': 'abcd1234-12ab-34cd-56ef-abcdef123456',
                'HTTPStatusCode': 400,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'abcd1234-12ab-34cd-56ef-abcdef123456',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '986'
                },
                'RetryAttempts': 0
            }
        }
    )

    mock_update.return_value = dict(
        {
            'name': 'foo_pipeline_name',
            'roleArn': \
                'arn:aws:iam::123456789012:role/' \
                'bar_project_CodePipelineServiceRo-ABC123DEF456',
            'artifactStore': {
                'type': 'S3',
                'location': 'bar_project_artifactstorebucket-abc123def456'
            },
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
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
                            'outputArtifacts': [
                                {
                                    'name': 'SourceOutput'
                                }
                            ],
                            'inputArtifacts': []
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'runOrder': 1,
                            'configuration': {
                                'ProjectName': \
                                    'FooCodeBuildProject-aBc123DeF456'
                            },
                            'outputArtifacts': [],
                            'inputArtifacts': [
                                {
                                    'name': 'SourceOutput'
                                }
                            ]
                        }
                    ]
                }
            ],
            'version': 1
        }
    )

    with pytest.raises(
        Exception,
        match="Unable to update CodePipeline with the new Token!"
    ):
        assert codepipeline_update_pipeline(
            boto3.client('codepipeline'),
            username,
            pipeline_name,
            new_token
        )
        assert mock_boto.called
        assert mock_update.called
