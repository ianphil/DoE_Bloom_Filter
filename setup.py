# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bloom',
    version='0.1.0',
    description='Design Experiments for Bloom Filters',
    long_description=readme,
    author='Ian Philpot',
    author_email='ianphil@microsoft.com',
    url='https://github.com/iphilpot/DoE_Bloom_Filter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
