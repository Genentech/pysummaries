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
from itertools import count


class TabSuperHeader:
    """
    Object to represent an item in the most external column indexes
    """
    def __init__(self, title, tabid, level, count, span=1, style="", top=False):
        self.title = title
        self.span = span
        self.style = style
        self.top = top
        self.level = level
        self.idnum = count
        self.classname = "superheader level_" + str(self.level) 
        self.idname = tabid + "_" + self.classname.replace(" ", "_") + "_" + str(self.idnum)

    def consolidate_styles(self):
        if self.span > 1: 
            self.style = 'border-bottom: 1pt solid black;' + self.style
        if self.top:
            self.style = 'border-top: 2pt solid black;' + self.style

class TabHeader:
    """
    Object to represent an item in the most internal column indexes
    """
    def __init__(self, title, tabid, count, n=None, style="", top=False):
        self.title = title
        self.n = n
        self.style = style
        self.classname = "header"
        self.idnum = count
        self.idname = tabid + "_header_" + str(self.idnum)
        self.idlabelname = tabid + "_headerlabel_" + str(self.idnum)
        self.idNname = tabid + "_headern_" + str(self.idnum)
        if top:
            self.style = 'border-top: 2pt solid black;' + self.style


class RowGroupLabel:
    """
    Object to represent an item in the most external row indexes
    """
    def __init__(self, title, tabid, level, left_padding, levelcounts, style=""):
        self.title = title
        self.left_padding = left_padding
        self.style = style
        self.level = level
        self.classname = "rowgrouplabel level_" + str(self.level)
        self.levelcounts = levelcounts
        self.tabid = tabid

    def consolidate_style(self):
        self.style = f"padding-left: {self.left_padding}ex;" + self.style
        # idname can be done only now after the final list of grouplabels has been pruned
        self.idnum = self.levelcounts[self.level]
        self.levelcounts[self.level] += 1
        self.idname = self.tabid + "_" + self.classname.replace(" ", "_") + "_" + str(self.idnum)


class RowLabel:
    """
    Object to represent an item in the most internal row indexes
    """
    instance_cnt = count(0)
    def __init__(self, title, left_padding, tabid, count, last_row=False, style=""):
        self.title = title
        self.left_padding = left_padding
        self.style = style
        self.last_row = last_row
        self.classname = "rowlabel"
        self.idnum = count
        self.idname = tabid + "_rowlabel_" + str(self.idnum)

    def consolidate_style(self):
        self.style = f"padding-left: {self.left_padding}ex;" + self.style
        if self.last_row:
            self.style = "border-bottom: 2pt solid black;" + self.style


class RowValue:
    """
    Object to represent an item in the row values
    """
    def __init__(self, value, tabid, rowcount, colcount, last_row=False, style=""):
        self.value = value
        self.style = style
        self.last_row = last_row
        self.classname = "rowvalue"
        self.rownum = rowcount
        self.colnum = colcount
        self.idname = tabid + "_value_row_" + str(self.rownum) + "_col_" + str(self.colnum)

    def consolidate_style(self):
        if self.last_row:
            self.style = "border-bottom: 2pt solid black;" + self.style


class Block:
    """
    Object to represent an Block (group of rows grouped by the most
    external row index)
    """
    titles = None
    rows = None

class Row:
    """
    Object to represent an Row
    """
    def __init__(self,label, values):
        self.label = label
        self.values = values
