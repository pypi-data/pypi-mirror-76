#! /usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='mdSlides',
    license="MIT",
    version="0.0.3",
    description='A tool for generating slides from markdown files using different backends.',
    url='https://github.com/CD3/mdSlides',
    author='C.D. Clark III',
    packages=find_packages(),
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    mdSlides=mdSlides.scripts.mdSlides:main
    ''',
)
