#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Python Taobao Open Platform API
#    Copyright 2013 wangbuke <wangbuke@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from setuptools import setup, find_packages
import os
import re

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    init = read(os.path.join('taobao', '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", init).group(1)

setup(name='python-taobao',
    version=get_version(),
    description='Library for taobao api ',
    long_description=read('README.md'),
    author='wangbuke',
    author_email='wangbuke@gmail.com',
    url='https://github.com/buke/python-taobao/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='AGPLv3+',
    use_2to3=True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
