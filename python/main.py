import requests
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass

# User prompts
# Ask the user for the Token name
gh_token_name = input("Enter the name of the GitHub Token to be rotated: ")

# Ask the user for their GitHub username
gh_username = input("Enter your GitHub username: ")

# Ask the user for their GitHub password
gh_pw = getpass(prompt="Enter your GitHub Password: ")

# Ask the user for their GitHub OTP
gh_otp = input("Enter your GitHub One-Time-Password: ")


# Search for "test" Token
authorizations = requests.get(
    'https://api.github.com/authorizations',
    auth=HTTPBasicAuth(gh_username, gh_pw),
    headers={'x-github-otp': gh_otp}
)
print("GitHub List of Authorizations:")
print(authorizations.json())

# Print current ID that matches desired App Name
response = authorizations.json()
token_id = None
for i in response:
    if i['app']['name'] == gh_token_name:
        token_id = i['id']
print("Token ID: " + str(token_id))


# Delete "test" Token
delete_authorization = requests.delete(
    'https://api.github.com/authorizations/' + str(token_id),
    auth=HTTPBasicAuth(gh_username, gh_pw),
    headers={'x-github-otp': gh_otp}
)
print("Delete Response:")
print(delete_authorization)


# Create new "test" Token
new_authorization = requests.post(
    'https://api.github.com/authorizations',
    auth=HTTPBasicAuth(gh_username, gh_pw),
    headers={'x-github-otp': gh_otp},
    data='{"scopes":["repo", "admin:repo_hook"], "note": "%s"}' % gh_token_name
)
print("New GitHub Token:")
print(new_authorization.json())
print(new_authorization.json()['token'])
