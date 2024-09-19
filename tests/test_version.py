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

"""
Test if the version in pysummaries __init__ matches the version in setup.py
"""

import os
import sys
import re

script_folder = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.insert(0, script_folder)
sys.path.insert(1,os.path.join(script_folder, "docs"))

import pysummaries

pysummaries_version = pysummaries.__version__

with open(os.path.join(script_folder, "setup.py")) as h:
    content = h.read()

raw = re.findall("version=\'.*?\'", content)
setup_version = raw[0].replace("version=", "")
setup_version = setup_version.replace("'", "")

#with open(os.path.join(script_folder, "CITATION.cff")) as h:
    #content = h.readlines()
#raw = [x for x in content if x.startswith("version")]
#cff_version = raw[0].replace("version:", "").strip()

print("testing if module and setup versions match")
assert(pysummaries_version == setup_version)
#print("testing if documentation and setup versions match")
#assert(conf.release == setup_version)
#print("testing if cff and setup versions match")
#assert(cff_version == setup_version)
print("all versions match!")



