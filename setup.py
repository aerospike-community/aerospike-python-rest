#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import aerospike_rest

setup(
    name = aerospike_rest.NAME,
    version = aerospike_rest.get_version(),
    description = "Python interface to Aerospike REST Client",
    long_description = read("README.md"),
    packages = find_packages(),
    python_requires=">=3.3",
    install_requires = [
        'requests'
    ],
)
