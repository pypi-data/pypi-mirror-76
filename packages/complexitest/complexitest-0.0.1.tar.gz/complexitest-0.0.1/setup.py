#!/usr/bin/env python

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='complexitest',
    version='0.0.1',
    description='Algorithm Complexity Estimator',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Andrew Kurauchi',
    author_email='andrew.kurauchi@gmail.com',
    url='https://github.com/toshikurauchi/complexity_estimator',
    packages=['complexitest'],
    install_requires=['numpy'],
    license="MIT",
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
