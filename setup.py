#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='stored',
    version='0.0.33',
    description='Manage files and directories on different storage backends.',
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
        'click',
    ],
    entry_points='''
        [console_scripts]
        stored=stored.cli:cli
    ''',
)
