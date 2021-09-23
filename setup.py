#!/usr/bin/env python

import os
from datetime import datetime
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import aerospike_rest

version = '{}{}'.format(
    aerospike_rest.get_version(),
    'b{}'.format(datetime.now().strftime("%Y%m%d%H%M%S")) if os.getenv('TEST_PYPI', '') else ''
)

setup(
    name = aerospike_rest.NAME,
    version = version,
    description = "Python interface to Aerospike REST Client",
    url = "https://github.com/aerospike-community/aerospike-python-rest",
    long_description = read("README.md"),
    long_description_content_type='text/markdown',
    packages = find_packages(),
    python_requires=">=3.3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests'
    ],
)
