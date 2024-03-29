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
    version="0.2.0",
    description="CERN CAPTCHA service",
    url="https://github.com/CERN/captcha-api",
    author="MALT IAM team",
    author_email="authzsvc-admins@cern.ch",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=load_requirements(),
    keywords=["captcha", "service", "Flask", "SQLAlchemy", "CLI"],
    packages=find_packages(exclude=("tests*", "*tests", "tests")),
    extras_require={
        "dev": ["pytest", "flake8", "coverage", "black==22.3.0", "isort"]
    },
    include_package_data=True,
)
