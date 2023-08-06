#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from sekg.meta import __author__, __email__, __license__, __package__, __version__

packages = find_packages(exclude=("docs", "test"))

setup(
    name=__package__,
    version=__version__,
    keywords=("pip", "kg", "se"),
    description="knowledge graph util for software engineering",
    long_description="knowledge graph util for software engineering",
    license=__license__,

    url="https://github.com/FudanSELab/sekg",
    author=__author__,
    author_email=__email__,

    packages=packages,
    package_data={
        # If any package contains *.json files, include them:
        '': ['*.json', ".zip"],
    },
    platforms="any",
    install_requires=[
        "py2neo>=4.1.3",
        "sqlalchemy",
        "pymysql",
        "beautifulsoup4",
        "gensim>=3.8",
        "networkx==2.2",
        "bert-serving-client==1.10",
        "numpy>=1.11.2",
        "spacy>=2.2.3",
        "aiohttp",
        "async_timeout",
        "nltk",
        "kgtools",
        "textdistance[extras]",
        "neuralcoref",
        "paramiko==2.7.1",
        "Pygments==2.5.1",
    ]
)
