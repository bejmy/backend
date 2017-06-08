#!/usr/bin/env python

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    'Django<2',
    'djangorestframework',
    'django-mptt',
    'dj-database-url',
    'whitenoise',
    'django-model-utils',
    'django-taggit',
    'django-admin-rangefilter',
    'django-flat-responsive',
]

testing_requires = [
    'coverage',
    'flake8',
    'flake8-bugbear',
    'flake8-comprehensions',
    'flake8-docstrings',
    'flake8-string-format',
    'mccabe',
]

development_requires = [
    'sphinx',
] + testing_requires


setup(
    name='bejmy',
    version='0.1',
    description='Home Money Management',
    url='https://github.org/bejmy/backend/',
    long_description=long_description,
    author='Rafał Selewońko',
    author_email='rafal@selewonko.com',
    maintainer='Rafał Selewońko',
    maintainer_email='rafal@selewonko.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='bejmy money',
    download_url='https://github.com/bejmy/backend/archive/v0.1.zip',
    # packages=(
    #     'bejmy',
    # ),
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=testing_requires,
    extras_require={
        'development': development_requires,
        'testing': testing_requires,
    },
)
