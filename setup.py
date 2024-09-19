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


long_description="""
PySummaries is a Python package to easily produce table summarizations
from pandas dataframes.

For more detailed information, please look at the [documentation](https://improved-adventure-lmroz27.pages.github.io/)
or our [project homepage](https://github.com/Genentech/pysummaries)
"""

setup(
    name="pysummaries",
    version='0.0.1a3',
    author="Otto Fajardo",
    author_email="pleasecontactviagithub@notvalid.com",
    description="Produce table summaries from pandas dataframes",
    license="Apache License Version 2.0",
    keywords="pandas tableone table1 python table_summary tables",
    url="https://github.com/Genentech/pysummaries",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas>=2.0.0', 'great-tables>=0.11.0', 'jinja2'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Environment :: Console",
    ],
)
