#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='stored',
    version='0.0.1',
    description='A simple storage abstraction for interacting with files and directories on different backends.',
    author='Triage Technologies Inc.',
    author_email='ai@triage.com',
    url='https://www.triage.com/',
    packages=find_packages(exclude=['tests', '.cache', '.venv', '.git', 'dist']),
    scripts=[
    ],
    install_requires=[
        'backports.tempfile',
        'requests',
        'google-cloud-storage',
    ]
)
