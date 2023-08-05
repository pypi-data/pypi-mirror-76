#!/usr/bin/env python
# -*- python -*-
#
# Copyright 2018, 2019, 2020 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


def find_version(*file_paths):
    import codecs
    import re
    import os

    MSG_VERSION_STRING_NOTFOUND = 'Unable to find version string.'

    def read_src_file(*parts):
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(dir_path, *parts), 'r') as _f:
            return _f.read()

    version_file = read_src_file(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError(MSG_VERSION_STRING_NOTFOUND)


setup(
    name='bedqr',
    version=find_version('bedqr', '__init__.py'),
    packages=['bedqr',],
    author='Liang Chen',
    license='Apache License 2.0',
    platforms='Any',
    keywords=('BED', 'bed file', 'UCSC BED format', 'Bioinformatics'),
    python_requires=">=2.7",
    tests_require=['flake8', 'pytest'],
    classifiers=CLASSIFIERS,
    long_description_markdown_filename='README.md',
)
