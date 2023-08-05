#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = {}
with open("sicsearch/version.py") as fp:
    exec(fp.read(), version)

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'passlib',
    'pyperclip',
    'pycryptodome',
]

test_requirements = [
    'pytest'
]

setup(
    name='sicsearch',
    version=version['__version__'],
    description='Safe in Cloud DB Search',
    long_description=readme,
    author='Juan D Frias',
    author_email='juandfrias@gmail.com',
    url='https://github.com/ironsigma/sicsearch',
    packages=['sicsearch'],
    package_dir={'sicsearch': 'sicsearch'},
    install_requires=requirements,
    download_url='https://github.com/ironsigma/sicsearch/archive/v0.1.0-alpha.1.tar.gz',
    license='MIT',
    zip_safe=True,
    keywords=['SIC', 'SafeInCloud', 'Decryption', 'Password'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'sicsearch=sicsearch.search:main',
        ],
    },
)
