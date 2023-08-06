#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from codecs import open
from os import path
from shutil import copy
from sys import platform

from setuptools import Extension, setup

version = '0.0.1'

setup(
    name='snowflake-sqlalchemy-lite',
    author='Manuel Garrido',
    version=version,
    description='Snowflake SQLAlchemy Dialect LITE!',
    long_description='Snowflake SQLAlchemy Dialect LITE!',
    license='Apache License, Version 2.0',
    use_2to3=False,
    namespace_packages=['snowflake'],
    packages=[
        'snowflake.sqlalchemy',
    ],
    python_requires='>=3.5',
    install_requires=[
        'snowflake-connector-python-lite'
        'sqlalchemy<2.0.0',
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'snowflake=snowflake.sqlalchemy:dialect',
        ]
    },
)
