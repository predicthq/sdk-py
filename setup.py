#!/usr/bin/env python

import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


about = {}

# Load version number dynamically
with open(os.path.join(here, 'predicthq', 'version.py'), 'r') as f:
    exec(f.read(), about)


REPO_URL = "https://github.com/predicthq/sdk-py"
PYPI_README_NOTE = f"For the latest source, discussions, bug reports, etc., please visit the [GitHub repository]({REPO_URL})"
LONG_DESCRIPTION = "\n\n".join([PYPI_README_NOTE, read("README.md")])


setup(
    name="predicthq",
    version=about['__version__'],
    description="PredictHQ Event Intelligence",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license="MIT",
    author="PredictHQ",
    author_email="developers@predicthq.com",
    url=REPO_URL,
    packages=find_packages(exclude=("tests*",)),
    setup_requires=[
        'pytest-runner>=5.1,<6.0',
    ],
    install_requires=[
        "requests>=2.7.0",
        "schematics==2.0.0.dev2",
        "python-dateutil>=2.4.2",
        "pytz>=2017.2,<=2021.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
