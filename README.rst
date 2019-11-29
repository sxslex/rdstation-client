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

Usage in python
"""""""""""""""

    >>> import rdstation_client
    >>>
    >>> if rdstation_client.assert_valid_object({"name": "SleX"}, {"name": str}):
    >>>     print('OK')
    >>>
    >>> if rdstation_client.assert_valid_object(
    >>>     [
    >>>         {"email": "sx.slex@gmail.com", "name": "SleX", "idade": 37},
    >>>         {"email": "slex@slex.com.br", "name": "Alexandre"},
    >>>     ],
    >>>     [{
    >>>         "email": lambda e: '@' in e and '.' in e,
    >>>         "name": str,
    >>>         "idade": (int, rdstation_client.TypeNone,),
    >>>     }]
    >>> ):
    >>>     print('OK')
    >>>

Installation
""""""""""""

Use ``pip`` or ``easy_install``:

    $ pip install rdstation-client


Development
"""""""""""""""

Use py.test

    $ py.test --cov-report term-missing --cov=rdstation_client tests/ -v

Use pep8

    $ pycodestyle rdstation_client
