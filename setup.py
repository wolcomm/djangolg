#!/usr/bin/env python
# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Setup configuration script for djangolg."""

from setuptools import find_packages, setup


version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")

setup(
    name='djangolg',
    version=version,
    author='Workonline Communications',
    author_email='communications@workonkonline.co.za',
    description='A BGP looking glass based on the Django web framework',
    long_description='',
    license='LICENSE',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(),
    include_package_data=True,

    url='https://github.com/wolcomm/djangolg',
    download_url='https://github.com/djangolg/%s' % version,

    install_requires=requirements,
)
