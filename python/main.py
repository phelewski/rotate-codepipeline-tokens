import requests
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass

# Search for "test" Token
first_otp = input("OTP1: ")
authorizations = requests.get(
    'https://api.github.com/authorizations',
    auth=HTTPBasicAuth('phelewski', getpass()),
    headers={'x-github-otp': first_otp}
)
# print(authorizations.json())
response = authorizations.json()

token_id = None
for i in response:
    if i['app']['name'] == 'test':
        token_id = i['id']

print(token_id) # TODO: prettier

# Delete "test" Token
second_otp = input("OTP2: ")
delete_authorization = requests.delete(
    'https://api.github.com/authorizations/' + str(token_id),
    auth=HTTPBasicAuth('phelewski', getpass()),
    headers={'x-github-otp': second_otp}
) #TODO: spit out something useful

# Create new "test" Token
third_otp = input("OTP3: ")
new_authorization = requests.post(
    'https://api.github.com/authorizations',
    auth=HTTPBasicAuth('phelewski', getpass()),
    headers={'x-github-otp': third_otp},
    data='{"scopes":["public_repo"], "note": "test"}'
)
print(new_authorization.json())
print(new_authorization.json()['token'])
