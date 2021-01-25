# -*- coding: utf-8 -*-
"""Used to validate objects cleanly and simply."""

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='rdstation-client',
    version='0.0.10',
    url='https://github.com/sxslex/rdstation-client',
    download_url=(
        'https://github.com/sxslex/rdstation-client/archive/v0.0.10.tar.gz'
    ),
    author='SleX',
    author_email='sx.slex@gmail.com',
    description=(
        "Client for access API rdstation."
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=['rdstation', 'api', 'client', 'rd'],
    packages=['rdstation_client'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
