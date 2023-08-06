#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for text_cosine.

    This file was generated with PyScaffold 2.5.1, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except Exception:
    README = ""

setup(
    name='text_cosine',
    version="0.0.1",
    description='text_cosine',
    author='spenly',
    author_email='i@spenly.com',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/spenly/text_cosine.git",
    packages=find_packages(),
    install_requires=[],
    extras_require={},
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
