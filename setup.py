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
    description="PredictHQ Demand Intelligence",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license="MIT",
    author="PredictHQ",
    author_email="developers@predicthq.com",
    url=REPO_URL,
    packages=find_packages(exclude=("tests*",)),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2,<3",
        "requests>=2.7.0",
        "python-dateutil>=2.4.2",
        "pytz>=2017.2,<=2023.3",
        "stamina>=24.3.0,<25",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
