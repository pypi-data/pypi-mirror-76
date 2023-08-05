# dnxsso

[![Pull Request Build Status](https://github.com/DNXLabs/dnxsso/workflows/Pull%20Request%20Build/badge.svg)](https://github.com/DNXLabs/dnxsso/actions) [![codecov.io](https://codecov.io/gh/DNXLabs/dnxsso/coverage.svg?branch=master)](https://codecov.io/gh/DNXLabs/dnxsso?branch=master) [![Build Status](https://travis-ci.org/DNXLabs/dnxsso.svg?branch=master)](https://travis-ci.org/DNXLabs/dnxsso) [![Coverage Status](https://coveralls.io/repos/github/DNXLabs/dnxsso/badge.svg?branch=master)](https://coveralls.io/github/DNXLabs/dnxsso?branch=master)

Yet Another AWS SSO - sync up AWS CLI v2 SSO login session to legacy CLI v1 credentials.

## Do I need it?

- See https://github.com/DNXLabs/dnxsso/wiki

## Prerequisite

- Required [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- Assume you have already setup [AWS SSO](https://aws.amazon.com/single-sign-on/) for your organization

## TL;DR

- Install [latest from PyPI](https://pypi.org/project/dnxsso/) like so:
```commandline
pip install dnxsso
```

- Do your per normal SSO login and, have at least one org-level SSO login session cache:
```commandline
aws sso login --profile=dev
```

- To sync for all named profiles (e.g. dev, prod, stag, ...), then just:
```commandline
dnxsso
```

- To sync default profile and all named profiles, do:
```commandline
dnxsso --default
```

- To sync default profile only, do:
```commandline
dnxsso --default-only
```

- To sync for selected named profile, do:
```commandline
dnxsso -p dev
```

- To sync for multiple selected named profiles, do:
```commandline
dnxsso -p dev prod
```

- To sync for default profile as well as multiple selected named profiles, do:
```commandline
dnxsso --default -p dev prod
```

- To sync for all named profiles start with prefix pattern `lab*`, do:
```
(zsh)
dnxsso -p 'lab*'

(bash)
dnxsso -p lab*
```

- To sync for all named profiles start with prefix pattern `lab*` as well as `dev` and `prod`, do:
```
dnxsso -p 'lab*' dev prod
```

- Use `-e` flag if you want a temporary copy-paste-able time-gated access token for an instance or external machine. It use `default` profile if no additional arguments pass. The main use case is for those who use `default` profile, and would like to PIPE like this `aws sso login && dnxsso -e | pbcopy`. Otherwise for named profile, do `dnxsso -e -p dev`.

    > PLEASE USE THIS FEATURE WITH CARE SINCE **ENVIRONMENT VARIABLES USED ON SHARED SYSTEMS CAN GIVE UNAUTHORIZED ACCESS TO PRIVATE RESOURCES**:

```
dnxsso -e
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_SESSION_TOKEN=xxx
```

- You can also use `dnxsso` subcommand `login` to SSO login then sync all in one go:
```commandline
dnxsso login -h
dnxsso login
dnxsso login -e
dnxsso login --this
dnxsso login --profile dev
dnxsso login --profile dev --this
```

- Print help to see other options:
```commandline
dnxsso -h
```

- Then, continue per normal with your daily tools. i.e.
    - `cdk deploy ...`
    - `terraform ...`
    - `cw ls -p dev groups`
    - `awsbw -L -P dev`

## Develop

- Create virtual environment, activate it and then:

```
make install
make test
python -m dnxsso --trace version
```

- Create issue or pull request welcome

## License

MIT License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
