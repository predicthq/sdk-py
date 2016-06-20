#!/usr/bin/env python

import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


VERSION = read("VERSION").strip()

REPO_URL = "https://github.com/predicthq/sdk-py"

PYPI_README_NOTE = """\
.. note::

   For the latest source, discussions, bug reports, etc., please visit the `GitHub repository <{}>`_
""".format(REPO_URL)

LONG_DESCRIPTION = "\n\n".join([PYPI_README_NOTE, read("README.rst")])


setup(
    name="predicthq",
    version=VERSION,
    description="PredictHQ Event Intelligence",
    long_description=LONG_DESCRIPTION,
    license="MIT",
    author="PredictHQ",
    author_email="developers@predicthq.com",
    url=REPO_URL,
    packages=find_packages(exclude=("tests*",)),
    test_suite="nose.collector",
    setup_requires=[
        "nose==1.3.7"
    ],
    tests_require=[
        "nose==1.3.7",
        "coverage>=4.0.0",
        "responses==0.5.1",
        "mock==1.3.0",
    ],
    install_requires=[
        "six>=1.9.0",
        "requests>=2.7.0",
        "schematics==2.0.0.dev2",
        "python-dateutil>=2.4.2",
        "pytz>=2015.4",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
