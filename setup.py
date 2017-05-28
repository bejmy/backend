#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='bejmy',
    version='0.1',
    description='Home Money Management',
    long_description=long_description,
    author='Rafał Selewońko',
    author_email='rafal@selewonko.com',
    maintainer='Rafał Selewońko',
    maintainer_email='rafal@selewonko.com',
    url='https://github.org/bejmy/backend/',
    download_url='https://github.com/bejmy/backend/archive/v0.1.zip',
    packages=[
        'bejmy'
    ],
)
