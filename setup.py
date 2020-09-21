#!/usr/bin/env python

from os import path

from setuptools import setup, find_packages


def load_requirements():
    try:
        with open("requirements.txt", "r") as f:
            return f.readlines()
    except Exception:
        print("Exception getting requirements.txt file, returning []")
    return []


here = path.abspath(path.dirname(__file__))

setup(
    name="captcha-api",
    version="0.1.0",
    description="CERN CAPTCHA service",
    url="https://github.com/CERN/captcha-api",
    author="MALT IAM team",
    author_email="authzsvc-admins@cern.ch",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=load_requirements(),
    keywords=["captcha", "service", "Flask", "SQLAlchemy", "CLI"],
    packages=find_packages(exclude=("tests*", "*tests", "tests")),
    include_package_data=True
)
