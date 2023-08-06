# -*- coding: utf-8 -*-
"""
:copyright: Nokia Networks
:author: mrmino
:contact: example@example.com
:maintainer: mrmino
:contact: example@example.com
"""

import os
from setuptools import setup, find_packages

req_path = os.path.join(os.path.dirname(__file__), 'requirements', 'base.txt')
requirements = [line.strip() for line in open(req_path).readlines()]

setup(name='mrmino-test',
      version='0.1.0',
      description='mrmino-test library',
      author='mrmino',
      author_email='example@example.com',
      maintainer='mrmino',
      maintainer_email='example@example.com',
      packages=find_packages(exclude=['test']),
      install_requires=requirements
      )
