#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

version = '0.0.1'

setup(
    name='snowconn-lite',
    version=version,
    description='Python utilities for connection to the Snowflake data warehouse LITE',
    long_description='Python utilities for connection to the Snowflake data warehouse LITE',
    author='Manuel Garrido',
    packages=['snowconn'],
    license='MIT License',
    install_requires=[
        'boto3',
        'pandas',
        'snowflake-sqlalchemy-lite',
    ],
)
