#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

import os
import re

base_dir = os.path.dirname(__file__)

long_description = ''

with open(os.path.join(base_dir, "README.md")) as readme:
    readme_lines = readme.readlines()
    for line in readme_lines:
        if not re.search(r'\(images\/\b',line):
            long_description = long_description + line

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest']

setup(
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Environment :: Console',
        'Topic :: Security'
    ],
    entry_points={
        'console_scripts': [
            'corsair=corsair_scan.corsair_cli:run_cli_scan',
        ],
    },
    install_requires=requirements,

    description="CORS testing library",
    long_description_content_type='text/markdown',
    long_description=long_description,
    include_package_data=True,
    keywords='corsair_scan',
    author='Santander UK Security Engineering',
    name='corsair_scan',
    packages=['corsair_scan'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements, 
    url='https://github.com/santandersecurityresearch/corsair_scan',
    version='0.2.0',
    zip_safe=False,
)
