RDStation-client
================


.. image:: https://img.shields.io/badge/pypi-v0.0.5-orange.svg
    :target: https://pypi.python.org/pypi/rdstation-client

.. image:: https://img.shields.io/badge/python-2.6%2C%202.7%2C%203.3+-blue.svg
    :target: https://travis-ci.org/sxslex/rdstation-client.svg?branch=master

.. image:: https://travis-ci.org/sxslex/rdstation-client.svg?branch=master
    :target: https://travis-ci.org/sxslex/rdstation-client

.. image:: https://img.shields.io/badge/license--blue.svg
    :target: https://github.com/sxslex/capitalize-name/blob/master/LICENSE


Client for access API rdstation.

Usage
"""""""""""""""
    Install

>>> pip install rdstation-client

    Create file auth rdstation_client.json

>>> {
>>>  "client_id": "049bf777-bbbb-0000-9e09-7ebe2972b8b0",
>>>  "client_secret": "952e14d9dbad9c28d2247da9a19645d8",
>>>  "redirect_url": "https://appname.org/auth/callback"
>>> }


    python code

>>> from rdstation_client import RDStationClient
>>> rdsc = RDStationClient('/home/var/rdstation_client.json')
>>> rdsc.account_info_get()
>>> # Visite link
>>> # Enter CODE in url param
>>> print(rdsc.contacts_patch(
>>>     {
>>>         "name": "RD Station Developer",
>>>         "email": "contact@example.com",
>>>         "job_title": "Developer",
>>>         "bio": "This documentation explains the RD Station API.",
>>>         "website": "https://developers.rdstation.com/",
>>>         "linkedin": "rd_station",
>>>         "personal_phone": "+55 48 3037-3600",
>>>         "city": "Florianópolis",
>>>         "state": "SC",
>>>         "country": "Brasil",
>>>         "tags": ["developer", "rdstation", "api"]
>>>     }
>>> ))

Installation
""""""""""""

Use ``pip`` or ``easy_install``:

    $ pip install rdstation-client


Development
"""""""""""""""

Use py.test

    $ pip install -r requirements-development.txt

    $ py.test --cov-report term-missing --cov=rdstation_client tests/ -v

    $ py.test --cov-report term-missing --cov=rdstation_client --cov-report html tests/ -v


Use pep8

    $ pycodestyle rdstation_client
