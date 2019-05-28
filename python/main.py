import requests
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass

def get_current_tokens(username, password, otp, token):
    # Search for "test" Token
    authorizations = requests.get(
        'https://api.github.com/authorizations',
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp}
    )
    print("GitHub List of Authorizations:")
    print(authorizations.json())

    # Print current ID that matches desired App Name
    response = authorizations.json()
    token_id = None
    for i in response:
        if i['app']['name'] == token:
            token_id = i['id']
    print("Token ID: " + str(token_id))
    return token_id

def delete_token(username, password, otp, token):
    # Delete "test" Token
    token_id = get_current_tokens(username, password, otp, token)
    delete_authorization = requests.delete(
        'https://api.github.com/authorizations/' + str(token_id),
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp}
    )
    print("Delete Response:")
    print(delete_authorization)

def create_new_token(username, password, otp, token):
    # Create new "test" Token
    new_authorization = requests.post(
        'https://api.github.com/authorizations',
        auth=HTTPBasicAuth(username, password),
        headers={'x-github-otp': otp},
        data='{"scopes":["repo", "admin:repo_hook"], "note": "%s"}' % token
    )
    print("New GitHub Token:")
    print(new_authorization.json())
    print(new_authorization.json()['token'])

def main():
    # User prompts
    gh_token_name = input("Enter the name of the GitHub Token to be rotated: ")
    gh_username = input("Enter your GitHub username: ")
    gh_pw = getpass(prompt="Enter your GitHub Password: ")
    gh_otp = input("Enter your GitHub One-Time-Password: ")
    
    # Collect all current Tokens
    get_current_tokens(gh_username, gh_pw, gh_otp, gh_token_name)

    # Delete defined Token
    delete_token(gh_username, gh_pw, gh_otp, gh_token_name)

    # Create new Token
    create_new_token(gh_username, gh_pw, gh_otp, gh_token_name)

if __name__ == "__main__":
    main()