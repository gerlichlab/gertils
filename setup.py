#! /usr/bin/env python

import os
import sys
from setuptools import setup


with open("gertils/_version.py", "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

with open("README.md") as f:
    long_description = f.read()

setup(
    name="gertils",
    packages=["gertils"],
    version=version,
    description="General utilities used in the Gerlich group at IMBA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    url="https://github.com/gerlichlab/gertils",
    author="Vince Reuter",
    license="BSD2",
    scripts=None,
    test_suite="tests",
    tests_require=["mock", "pytest"],
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
)
