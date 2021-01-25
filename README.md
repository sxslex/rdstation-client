# RDStation-client

[![Current version at PyPI](https://img.shields.io/badge/pypi-v0.0.10-yellowgreen.svg)](https://pypi.org/project/rdstation-client/)
[![Downloads current version](https://img.shields.io/badge/download-v0.0.10-lightgrey.svg)](https://github.com/sxslex/rdstation-client/archive/v0.0.10.tar.gz)
[![Supported Python Versions](https://img.shields.io/badge/pyhton-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://github.com/sxslex/rdstation-client/)
[![Build Status](https://travis-ci.org/sxslex/rdstation-client.svg?branch=master)](https://travis-ci.org/sxslex/rdstation-client)
[![codecov](https://codecov.io/gh/sxslex/rdstation-client/branch/master/graph/badge.svg)](https://codecov.io/gh/sxslex/rdstation-client)
[![License: LGPLv3](https://img.shields.io/badge/license-LGPLv3+-red.svg)](https://github.com/sxslex/rdstation-client/blob/master/LICENSE)

Client for access API rdstation.


## Installation

The easiest way to getting the hands dirty is install rdstation-client, using 
pip.

### [PyPI][pypi-rdstation-client]

## Usage

Install

```bash
pip install rdstation-client
```

Create file auth rdstation_client.json

Vide: [https://developers.rdstation.com/en/overview](https://developers.rdstation.com/en/overview)

```json
{
  "client_id": "049bf777-bbbb-0000-9e09-7ebe2972b8b0",
  "client_secret": "952e14d9dbad9c28d2247da9a19645d8",
  "redirect_url": "https://appname.org/auth/callback"
}
```

Python code example:

```python
from rdstation_client import RDStationClient
rdsc = RDStationClient('/home/var/rdstation_client.json')
rdsc.account_info_get()
# Visite link
# Enter CODE in url param
print(rdsc.contacts_patch(
    {
        "name": "RD Station Developer",
        "email": "contact@example.com",
        "job_title": "Developer",
        "bio": "This documentation explains the RD Station API.",
        "website": "https://developers.rdstation.com/",
        "linkedin": "rd_station",
        "personal_phone": "+55 48 3037-3600",
        "city": "Florianópolis",
        "state": "SC",
        "country": "Brasil",
        "tags": ["developer", "rdstation", "api"]
    }
))
```

## Contribution start guide

The preferred way to start contributing for the project is creating a virtualenv (you can do by using virtualenv,
virtualenvwrapper, pyenv or whatever tool you'd like).


Create the virtualenv:

```bash
mkvirtualenv rdstation-client
```

Install development dependencies:

```bash
pip install -r requirements-development.txt
```

Use py.test

```bash
py.test --verbose --assert=plain --color=yes --cov-report=term-missing --cov=rdstation_client tests/
```

Use pep8

```bash
pycodestyle rdstation_client tests
```

[pypi-rdstation-client]: https://pypi.org/project/rdstation-client/
