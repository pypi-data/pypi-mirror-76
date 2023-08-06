#!/usr/bin/env python
""" Setup file for the i-flow integrator. """

from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
from io import open

import setuptools
from setuptools import setup, find_packages


HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='iflow',
    version='1.0',
    description='Monte-Carlo Integration using Neural Networks',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/isaacson/nicephasespace',
    author='Christina Gao, \
            Joshua Isaacson, \
            Claudius Krause',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ],
    packages=find_packages(),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=[
        'numpy',
        'tensorflow>=2.0',
        'tensorflow_probability>=0.8.0',
        ],
    # Provide executable script to run the main code
    entry_points={},
    extras_require={
        'test': ['pytest', 'coverage', 'pytest-cov'],
    },
)
