#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

# print("{} - {}".format("*" * 10, find_packages()))

setup(
    name='SWRunShell',  # 包名字
    version='1.0.1',  # 包版本
    author='shede333',  # 作者
    author_email='333wshw@163.com',  # 作者邮箱
    keywords='sw shell command',
    description='进一步封装了subprocess，Python调用shell命令',  # 简单描述
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/shede333/SWRunShell',  # 包的主页
    packages=find_packages(),  # 包
    install_requires=['SWTermColor~=1.1'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
