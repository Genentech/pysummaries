# #############################################################################
# Copyright 2024 F. Hoffmann-La Roche
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
# #############################################################################

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pysummaries",
    version='0.0.1',
    author="Otto Fajardo",
    author_email="pleasecontactviagithub@notvalid.com",
    description="Produce table summaries from pandas dataframes",
    license="Apache License Version 2.0",
    keywords="pandas tableone table1 python table_summary tables",
    url="https://github.com/Genentech/pysummaries",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=['pandas>=2.0.0', 'great_tables>=0.11.0'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Environment :: Console",
    ],
)
