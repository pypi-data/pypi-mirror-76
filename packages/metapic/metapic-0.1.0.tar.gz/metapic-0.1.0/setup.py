#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''metapic setup script.
'''

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = []

test_requirements = []

setup(
    author='luphord',
    author_email='luphord@protonmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='''Command line tool for modifying picture metadata from file/folder names and config.''',
    entry_points={
        'console_scripts': [
            'metapic=metapic:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    data_files=[('.', ['LICENSE', 'HISTORY.md'])],
    keywords='metapic',
    name='metapic',
    py_modules=['metapic'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luphord/metapic',
    version='0.1.0',
    zip_safe=True,
)
