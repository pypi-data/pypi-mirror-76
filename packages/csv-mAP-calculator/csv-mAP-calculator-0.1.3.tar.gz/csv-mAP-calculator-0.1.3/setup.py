#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import csv_mAP_calculator

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="csv-mAP-calculator",
    version = "0.1.3",
    author="Autumn",
    author_email="zhao_qyu@163.com",
    description="Calculate mAP for CSV format detection result",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://https://gitee.com/zhao_qy/csv_mAP_calculator",
    packages=find_packages(),
    install_requires=[
        "numpy", "pandas", "cython" 
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',

    ],
)
