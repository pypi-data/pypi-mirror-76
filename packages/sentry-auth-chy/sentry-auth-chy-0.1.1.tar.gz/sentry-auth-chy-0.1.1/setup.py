#!/usr/bin/env python
"""
sentry-auth-chy
==================

:copyright: (c) 2016 Functional Software, Inc
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=7.0.0',
]

tests_require = [
    'flake8>=2.0,<2.1',
]

setup(
    name='sentry-auth-chy',
    version='0.1.1',
    author='lisipeng',
    author_email='77629296@qq.com',
    url='https://www.getsentry.com',
    description='Chy authentication provider for Sentry',
    long_description=__doc__,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'auth_chy = sentry_auth_chy',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
