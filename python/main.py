import requests
import json
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
    print("")
    print("GitHub List of Authorizations:")
    print(authorizations.json())
    return authorizations.json()

def get_token_id(username, password, otp, token):
    """
    Return the ID for the desired Token defined by user input.
    """
    response = get_current_tokens(username, password, otp, token)
    token_id = None
    for i in response:
        if i['app']['name'] == token:
            token_id = i['id']
    print("")
    print("Token ID: " + str(token_id))
    return token_id

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
    print("")
    print("Delete Response:")
    print(delete_authorization)
    return delete_authorization

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

    new_token = new_authorization.json()['token']

    print("")
    print("New GitHub Token:")
    print(new_authorization.json())
    print(new_authorization.json()['token'])
    print(new_token)
    # return new_authorization.json()['token']
    return new_token

def codepipeline_get_pipeline(client):
    response = client.get_pipeline(
        name='peter-demo-sam-pipeline' # TODO:
    )

    # Remove 'metadata' & 'ResponseMetadata'
    response = response.pop('pipeline')

    print("")
    print("Get CodePipeline:")
    print(response)
    return response

def update_response_token_info(client, username, new_token):
    print("")
    print("update_response_token_info client")
    print(client)
    print("update_response_token_info username")
    print(username)
    print("update_response_token_info new_token")
    print(new_token)

    response = codepipeline_get_pipeline(client)

    # Update the OAuthToken
    for stage in response['stages']:
        for action in stage['actions']:
            if action['configuration'].get('OAuthToken', None):
                action['configuration']['OAuthToken'] = new_token
    
    # Update the GitHub username
    for stage in response['stages']:
        for action in stage['actions']:
            if action['configuration'].get('Owner', None):
                action['configuration']['Owner'] = username

    print("Updated CodePipeline with New Token")
    print(response)
    return response

def codepipeline_update_pipeline(client, username, new_token):
    updated_pipeline = update_response_token_info(client, username, new_token)
    response = client.update_pipeline(
        pipeline=updated_pipeline
    )
    print("")
    print("Update CodePipeline:")
    print(response)
    return response

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
    GitHub Token.
    """

    # User prompts
    gh_token_name = input("Enter the name of the GitHub Token to be rotated: ")
    gh_username = input("Enter your GitHub username: ")
    gh_pw = getpass(prompt="Enter your GitHub Password: ")
    gh_otp = input("Enter your GitHub One-Time-Password: ")
    
    # GitHub Actions
    # get_current_tokens(gh_username, gh_pw, gh_otp, gh_token_name)
    # get_token_id(gh_username, gh_pw, gh_otp, gh_token_name)
    delete_token(gh_username, gh_pw, gh_otp, gh_token_name)
    # create_new_token(gh_username, gh_pw, gh_otp, gh_token_name)

    # CodePipeline Actions
    client = boto3.client('codepipeline')
    # new_token = create_new_token(gh_username, gh_pw, gh_otp, gh_token_name)
    # codepipeline_get_pipeline(client)
    # update_response_token_info(client, gh_username, new_token)
    codepipeline_update_pipeline(client, gh_username, create_new_token(gh_username, gh_pw, gh_otp, gh_token_name))

if __name__ == "__main__":
    main()