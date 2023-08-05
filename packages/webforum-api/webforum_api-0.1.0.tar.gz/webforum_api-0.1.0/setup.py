#!/usr/bin/python3
# coding: utf-8
# author: Clement Onawole - dapo.onawole@gmail.com
# setup.py

from setuptools import setup, find_packages

setup(
    # Application name:
    name='webforum_api',

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Clement Onawole",
    author_email="dapo.onawole@gmail.com",  #['.'],

    # Packages
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    package_data={'': ['LICENSE']},

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/webforum_api/",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
    ],
    keywords='networking eventlet nonblocking internet',
    license="LICENSE",
    description="Useful towel-related stuff.",
    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        'fastapi', 'uvicorn', 'pymongo',
        'pymongo', 'pytest'
    ])
