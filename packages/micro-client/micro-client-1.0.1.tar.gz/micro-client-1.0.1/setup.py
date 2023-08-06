#!/usr/bin/env python
# Copyright (c) 2017 Steve 'Ashcrow' Milner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import io

import requests
import setuptools
from setuptools import setup, find_packages

# use a consistent encoding
from codecs import open
import os
import json
import sys

is_python_2 = sys.version_info < (3, 0)

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)

# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to':'rst','from':'markdown'},
                      files={'input_files[]':open(from_file,'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)

md_to_rst("README.md", "README.rst")
if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()
else:
	long_description = 'micro client for service discovery'

if os.path.exists("requirements.txt"):
    install_requires = io.open("requirements.txt").read().split("\n")
else:
    install_requires = []


# readme_rst = os.path.join(here, 'README.md')
# package_json = os.path.join(here, 'package.json')
#
# # a workaround when installing locally from git repository with pip install -e .
# if not os.path.isfile(package_json):
#     package_json = os.path.join(root, 'package.json')
#
# # long description from README file
# with open(readme_rst, encoding='utf-8') as f:
#     long_description = f.read()
#
# # version number and all other params from package.json
# with open(package_json, encoding='utf-8') as f:
#     package = json.load(f)

setup(
    name="micro-client",
    version="1.0.1",
    author="zhuleixiao",
    author_email="zhuleixiao666@gmail.com",  # 作者邮箱
    description="Python 3 resolver for go-micro grpc services.",
    long_description=long_description,
    url="https://github.com/zhuleixiao6666/python-micro_client",

    classifiers=[  # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",  # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",  # 根据MIT许可证开源
        "Operating System :: OS Independent",  # 与操作系统无关
    ],

    packages=setuptools.find_packages(),

    install_requires=install_requires,

    extras_require={
        ':python_version>="3.6.5"': [
        ],
        'qa': [
            'flake8==3.5.0'
        ],
        'doc': [
            'Sphinx==1.7.0'
        ]
    }
)