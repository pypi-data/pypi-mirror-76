#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup, find_packages

import sys

kwargs = {}
if not hasattr(sys, 'pypy_version_info'):
	kwargs['install_requires'] = ['Pillow']


def fopen(filename):
    with open(filename) as f:
        return f.read()


setup(
	name='x-captcha',
	version='0.4.200808',
	packages=find_packages(),
	url='https://www.github.com/eraare/x-captcha',
	author='Leo',
	author_email='r00kie@126.com',
	keywords = ['captcha'], 
	description='A simple and powerful captcha generation library.',
	long_description=fopen('README.rst'),
    license='BSD',
    zip_safe=False,
    include_package_data=True,
    **kwargs
)