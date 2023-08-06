#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import rdmi

setup(
    name='rdmi',
    version=rdmi.__version__,
    packages=find_packages(),
    author='Kanchen Monnin',
    author_email='kanchen@mail.com',
    description='Print a range of numbers in random order',
    long_description="README on github : https://github.com/Teal-Projects/rdmi",
    install_requires=[
        'sys',
        'random',
    ],
    url='https://github.com/Teal-Projects/rdmi',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: System',
    ],
    entry_points={
        'console_scripts': [
            'rdmi = rdmi.rdmi:main',
        ],
    },
)
