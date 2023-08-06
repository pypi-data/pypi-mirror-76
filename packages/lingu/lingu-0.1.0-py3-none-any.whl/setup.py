#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import sys

from glob import glob
from os.path import basename, splitext

from setuptools import setup, find_packages


if sys.version_info < (3, 5):
    print("Lingu requires Python >= 3.5")
    sys.exit(1)


setup(
    name="lingu",
    version="0.1.0",
    license="gplv3",
    description="Natural Language Processing library for Icelandic",
    author="Lingu ehf", author_email="lingu@lingu.is",
    url="https://www.lingu.is", packages=find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob("./*.py")],
    package_data={"lingu": ["py.typed"]},
    include_package_data=True,
    zip_safe=True,
    classifiers=["Intended Audience :: Developers",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                "Operating System :: Unix",
                "Operating System :: POSIX",
                "Operating System :: Microsoft :: Windows",
                "Operating System :: MacOS",
                "Natural Language :: Icelandic",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: Implementation :: CPython",
                "Programming Language :: Python :: Implementation :: PyPy",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Utilities", "Topic :: Text Processing :: Linguistic", ],
    keywords=["nlp", "icelandic", "ocr"],
    install_requires=["reynir", "icegrams","reynir-correct","tokenizer","nltk"],
)
