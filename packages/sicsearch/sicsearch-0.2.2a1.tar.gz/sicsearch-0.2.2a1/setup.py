#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def md2rst(filename, github_repo):
    text = ''
    incodeblock = False
    with open(filename) as fh:
        for line in fh:
            if incodeblock:
                if '```' in line:
                    incodeblock = False
                    text += '\n'
                else:
                    text += '    ' + line

            elif line[0:2] == '# ':
                text += line[2:]
                text += '=' * (len(line) - 3) + '\n'

            elif line[0:3] == '## ':
                text += line[3:]
                text += '-' * (len(line) - 4) + '\n'

            elif line[0:4] == '### ':
                text += line[4:]
                text += "'" * (len(line) - 5) + '\n'

            elif line[0:5] == '#### ':
                text += line[5:]
                text += '.' * (len(line) - 6) + '\n'

            elif '```' in line:
                incodeblock = True
                text += '.. code-block:: ' + line[3:] + '\n'

            elif '`' in line:
                text += re.sub(r'`([^`]+)`', r'``\1``', line)

            elif '![' in line:
                match = re.match(r'!\[([^\]]+)\]\(([^)]+)\)', line)
                prefix = '' if 'http' in line else github_repo + '/raw/master/'
                text += '.. image:: ' + prefix + match.group(2) + '\n'
                text += '   :alt: ' + match.group(1) + '\n'


            else:
                text += line
    return text

github_repo = 'https://github.com/ironsigma/sicsearch'

version = {}
github_archive = ''
with open("sicsearch/version.py") as fp:
    exec(fp.read(), version)
    github_archive=github_repo + '/archive/v' + version['__version__'].replace('a', '-alpha.') + '.tar.gz'


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
    long_description=md2rst('README.md', github_repo),
    author='Juan D Frias',
    author_email='juandfrias@gmail.com',
    url='https://github.com/ironsigma/sicsearch',
    packages=['sicsearch'],
    package_dir={'sicsearch': 'sicsearch'},
    install_requires=requirements,
    download_url=github_archive,
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

