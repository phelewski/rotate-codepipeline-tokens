rotate-codepipeline-tokens
========

Project to help automate the rotation of GitHub Tokens for CodePipeline.

## Usage

Pass in a CodePipeline name along with a GitHub Token name, username, password, & one-time-password.

Example:

```
$ rotate-codepipeline-tokens
  Enter the name of the CodePipeline to update: example-pipeline
  Enter the name of the GitHub Token to be rotated: example-token
  Enter your GitHub username: example-username
  Enter your GitHub Password: 
  Enter your GitHub One-Time-Password: example-otp
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