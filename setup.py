# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    licence = f.read()

setup(
    name='srqmplayer',
    version='0.1.0',
    description='Space Rangers Quest Player',
    long_description=readme,
    author='Cthulhu Fhtagn',
    license=licence,
    packages=find_packages(exclude=('tests', 'docs'))
)
