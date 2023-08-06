#!/usr/bin/env python

from setuptools import setup

setup(
    name             = 'dz',
    version          = '0.1.1',
    description      = 'deploy zone',
    author           = 'Sebastian Wiedenroth',
    author_email     = 'sw@core.io',
    url              = 'https://github.com/wiedi/dz',
    packages=['dz'],
    entry_points={
        'console_scripts': [
            'dz = dz.__main__:main'
        ]
    },
    
    install_requires = [
        "argcomplete  == 1.12.0",
        "humanize     == 2.5.0",
        "tabulate     == 0.8.7",
        "tqdm         == 4.48.2",
    ],
)
