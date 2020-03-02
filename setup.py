# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pping import ABOUT

with open('README.md', encoding='utf8') as f:
    readme = f.read()

setup(
    name=ABOUT['name'],
    version=ABOUT['version'],
    author=ABOUT['author'],
    description=ABOUT['description'],
    url=ABOUT['url'],
    license=ABOUT['license'],
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
