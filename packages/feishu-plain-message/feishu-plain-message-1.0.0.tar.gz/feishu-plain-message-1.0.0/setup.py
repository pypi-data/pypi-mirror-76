# coding: utf-8
"""
@Author: Robby
@Module name: setup.py
@Create date: 2020-06-06
@Function: 
"""

import os
from setuptools import setup

def package_data(pkg, roots=tuple()):
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                print(os.path.relpath(os.path.join(dirname, fname), pkg))
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

with open("README.rst", "r") as f:
  long_description = f.read()

setup(
    name = 'feishu-plain-message',
    author = 'Robby',
    author_email = 'yinhuanyicn@gmail.com',
    url = 'https://github.com/yinhuanyi/feishu-plain-message',
    license = "MIT",
    version = '1.0.0',
    description = 'Send Plain Message To Feishu',
    long_description = long_description,
    packages = [
        'feishu_plain_message',
    ],
    install_requires = [
        'requests',
    ],
    dependency_links = [],
    package_data = package_data("feishu_plain_message",),
)