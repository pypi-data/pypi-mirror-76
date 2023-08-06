#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: thao
# Mail: thao92@126.com
# Created Time:  2020-08-05 11:08:34
#############################################


from setuptools import setup, find_packages
import sys
import importlib
importlib.reload(sys)

setup(
    name = "sanydata",
    version = "1.0.1",
    keywords = ["pip", "sanydata", "thao"],
    description = "get data list and read data tool",
    long_description = "get data list and read data tool",
    license = "MIT Licence",

    url = "",
    author = "thao",
    author_email = "thao92@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['grpcio', 'grpcio-tools', 'pandas']
#     install_requires = []
)
