#!/usr/bin/env python3

from setuptools import setup

import os

__pgdr = 'PG Drange <pgdr@equinor.com>'
__source = 'https://github.com/pgdr/cdecorator'
__webpage = __source
__description = "cdecorator magically makes Python into C"


def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))

def _read_file(fname, op):
    with open(src(fname), 'r') as fin:
        return op(fin.readlines())


def requirements():
    return []


def readme():
    try:
        return _read_file('README.md',
                          lambda lines: ''.join(lines))
    except:
        return __description

setup(
    name='cdecorator',
    packages=['cdecorator'],
    description=__description,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='PG Drange',
    author_email='pgdr@equinor.com',
    maintainer=__pgdr,
    url=__webpage,
    project_urls={
        'Bug Tracker': '{}/issues'.format(__source),
        'Documentation': '{}/blob/master/README.md'.format(__source),
        'Source Code': __source,
    },
    license='MIT',
    keywords='cdecorator python c decorator',
    version='0.0.0',
    install_requires=requirements(),
    entry_points={},
    test_suite='tests',
)
