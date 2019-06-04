import requests
import json
import sys
import boto3
from requests.auth import HTTPBasicAuth
from getpass import getpass

def get_current_tokens(username, password, otp, token):
    """
    Use the GitHub API to return a current list of all the associated Tokens
    for the given user.
    """
    authorizations = requests.get(
        'https://api.github.com/authorizations',
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp}
    )
    if authorizations.status_code == 200:
        print("")
        print("GitHub List of Authorizations:")
        print(authorizations.json())
        return authorizations.json()

    print("")
    print("Could not get current list of GitHub tokens!")
    print(authorizations.json())
    raise Exception("Could not get current list of GitHub tokens!")


def get_token_id(username, password, otp, token):
    """
    Return the ID for the desired Token defined by user input.
    """
    response = get_current_tokens(username, password, otp, token)
    token_id = None
    for i in response:
        if i['app']['name'] == token:
            token_id = i['id']

    if token_id != None:
        print("")
        print(f"Token ID: {token_id}")
        return token_id

    print("")
    print("GitHub token name does not exist!")
    raise Exception("GitHub token name does not exist!")

def delete_token(username, password, otp, token):
    """
    Delete the defined Token ID from the GitHub users Token list.
    """
    token_id = get_token_id(username, password, otp, token)
    delete_authorization = requests.delete(
        'https://api.github.com/authorizations/' + str(token_id),
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp}
    )

    if delete_authorization.status_code == 204:
        print("")
        print(f"Successfully Deleted the GitHub Authorization {token_id}")
        print(delete_authorization)
        return delete_authorization

    print("")
    print(f"Could not delete the GitHub Authorization token: {token_id}!")
    print(delete_authorization)
    raise Exception(f"Could not delete the GitHub Authorization token: {token_id}!")

def create_new_token(username, password, otp, token):
    """
    Creates a new Token with "repo" & "admin:repo_hook" permissions and returns
    the new Token value.
    """
    new_authorization = requests.post(
        'https://api.github.com/authorizations',
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp},
        data='{"scopes":["repo", "admin:repo_hook"], "note": "%s"}' % token
    )

    if new_authorization.status_code == 201:
        new_token = new_authorization.json()['token']
        print("")
        print(f"Successfully Created a new the GitHub Authorization Token")
        print(f"New GitHub Token: {new_token}")
        print(new_authorization.json())
        return new_token
    elif new_authorization.status_code == 401:
        print("")
        print("Unable to create new Token. Check user credentials!")
        print(new_authorization.json())
        print(new_authorization.status_code)
        raise Exception("Unable to create new Token. Check user credentials!")
    elif new_authorization.status_code == 422:
        print("")
        print("Unable to create new Token. Token already exists!")
        print(new_authorization.json())
        print(new_authorization.status_code)
        raise Exception("Unable to create new Token. Token already exists!")

    print("")
    print("Could not create a new GitHub Authorization token!")
    print(new_authorization.json())
    print(new_authorization.status_code)
    raise Exception("Could not create a new GitHub Authorization token!")

def codepipeline_get_pipeline(client, pipeline_name):
    response = client.get_pipeline(
        name=pipeline_name
    )

    # Remove 'metadata' & 'ResponseMetadata'
    response = response.pop('pipeline')

    if isinstance(response, dict):
        print("")
        print("Get CodePipeline:")
        print(response)
        print("codepipeline_get_pipeline - client")
        print(client)
        return response

    print("")
    print("Get CodePipeline is not a dict!")
    print(response)
    raise Exception("Get CodePipeline is not a dict!")

def update_response_token_info(client, username, pipeline_name, new_token):
    response = codepipeline_get_pipeline(client, pipeline_name)

    # Update the OAuthToken
    for stage in response['stages']:
        for action in stage['actions']:
            if action['configuration'].get('OAuthToken', None) \
                and action['configuration'].get('Owner', None):
                    action['configuration']['OAuthToken'] = new_token
                    action['configuration']['Owner'] = username
                    print("")
                    print("Adjusted pipeline template with new Token")
                    print(response)
                    return response

    print("")
    print("Not able to adjust pipeline template with new Token!")
    print(response)
    raise Exception("Not able to adjust pipeline template with new Token!")

def codepipeline_update_pipeline(client, username, pipeline_name, new_token):
    updated_pipeline = update_response_token_info(
        client,
        username,
        pipeline_name,
        new_token
    )
    response = client.update_pipeline(
        pipeline=updated_pipeline
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("Successfully updated CodePipeline with the new Token")
        print(response)
        return response

    print("")
    print("Unable to update CodePipeline with the new Token!")
    print(response)
    raise Exception("Unable to update CodePipeline with the new Token!")

def main():
    """
    This script assumes that the defined GitHub user is utilizing Multi-Factor
    Authentication, therefore you will also need to define a One-Time-Password
    to pass along with the username and password.

    This script grab a current list of the current available tokens listed by
    the defined GitHub user.

    It will then search through this list and grab the ID for the matching
    token name as defined by the user input.

    The matching Token ID will then be deleted from the users account and a
    new Token will be created with permissions needed for AWS CodePipeline.

    Afterwards the defined CodePipeline will be updated to utilize the new
    GitHub Token and associated username.
    """

    # User prompts
    codepipeline_name = input("Enter the name of the CodePipeline to update: ")
    gh_token_name = input("Enter the name of the GitHub Token to be rotated: ")
    gh_username = input("Enter your GitHub username: ")
    gh_pw = getpass(prompt="Enter your GitHub Password: ")
    gh_otp = input("Enter your GitHub One-Time-Password: ")
    
    # GitHub Actions
    delete_token(gh_username, gh_pw, gh_otp, gh_token_name)

    # CodePipeline Actions
    client = boto3.client('codepipeline')
    codepipeline_update_pipeline(
        client,
        gh_username,
        codepipeline_name,
        create_new_token(
            gh_username,
            gh_pw,
            gh_otp,
            gh_token_name
        ))

if __name__ == "__main__":
    main()
