rotate-codepipeline-tokens
========

Project to help automate the rotation of GitHub Tokens for CodePipeline.

This package will take an existing GitHub Token, deletes it, then will recreate it with permissions needed for CodePipeline integreation. Then it will take that newly created token and updated your CodePipeline pipeline with the new token passphrase. This package performs these actions by making API calls to GitHub and AWS.

For the GitHub API calls you will need to have Multi-Factor-Authentication enabled for you user account. You will need to supply the script with your password and a one-time-password.

For the AWS API calls you will need to already be authenticated with the awscli.

## Usage

Pass in a CodePipeline name along with a GitHub Token name, username, password, & one-time-password.

Example:

```
$ rotate-codepipeline-tokens
  Enter the name of the CodePipeline to update: <example-pipeline>
  Enter the name of the GitHub Token to be rotated: <example-token>
  Enter your GitHub username: <example-username>
  Enter your GitHub Password: < >
  Enter your GitHub One-Time-Password: <example-otp>
```

## Installation From Source

To install the package after you've cloned the repository, you'll want to run the following command from within the project directory:

```
$ pip install --user -e .
```

## Preparing for Development

Follow these steps to start developing with this project:

1. Ensure `pip` and `pipenv` are installed
2. Clone repository: `git clone git@github.com:phelewski/rotate-codepipeline-tokens.git`
3. `cd` into the repository
4. Activate virtualenv: `pipenv shell`
5. Install dependencies: `pipenv install`

### Unit Testing

PyTest is used for unit testing.

From the `pipenv shell`:

```
python -m pytest
```

To show the coverage:
```
python -m pytest --cov=src
```

To hide those `urllib3` `DeprecationWarning:` lines:
```
python -m pytest --cov=src tests  -W ignore::DeprecationWarning
```
