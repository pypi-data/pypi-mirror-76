#!/usr/bin/env python

import re
import sys
from os import path
from setuptools import setup, find_packages


requirements = [
    "aiohttp>=3.5.4",
    "async-timeout>=3.0.1",
    "attrs>=18.2.0",
    "chardet>=3.0.4",
    "idna>=2.8",
    "multidict>=4.5.2",
    "typing-extensions>=3.7.2",
    "yarl>=1.3.0",
    "ujson>=1.35",
    "PyYAML>=3.13",
    "frozendict>=1.2",
    "deepmerge>=0.1",
]


version_file = path.join(path.dirname(__file__), "aiohttp_rest_api", "__version__.py")
with open(version_file, "r") as fp:
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fp.read(), re.M)
    version = m.groups(1)[0]

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="aiohttp_rest_api_redoc",
    version=version,
    license="MIT",
    url="https://github.com/oplik0/aiohttp_rest_api/tree/redoc",
    author="Andrey Korchak",
    author_email="me@akorchak.software",
    description="RESTful API servers with aiohttp - forked to use redoc instead of swagger",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: AsyncIO",
    ],
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6.0",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    extras_require={"docs": "sphinx",},
)
