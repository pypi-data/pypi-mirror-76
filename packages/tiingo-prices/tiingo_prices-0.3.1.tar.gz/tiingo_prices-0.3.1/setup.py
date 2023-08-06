#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'tiingo',
    'pandas'
]

test_requirements = [
    'pytest'
]

setup(
    name='tiingo_prices',
    version='0.3.1',
    description="A CLI tool to get close of day price and annual dividends",
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Robert Rennison",
    author_email='rob@robren.net',
    url='https://github.com/robren/tiingo_prices',
    packages=[
        'tiingo_prices',
    ],
    package_dir={'tiingo_prices':'tiingo_prices'},
    entry_points={
        'console_scripts': [
            'tiingo_prices=tiingo_prices.tiingo_prices:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tiingo_prices tiingo finance',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
