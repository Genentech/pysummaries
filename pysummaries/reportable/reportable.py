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
import random
import os

import jinja2
import pandas as pd

from .intermediate_representation import df_to_intermediate_rep
from .styles import get_styles

dirpath = os.path.dirname(os.path.realpath(__file__))


def pandas_to_report_html(df, strat_numbers=None, caption=None, footer=None, customstyles=None, customcss=None, value_styles=None, styles='default', table_id=None, show_index=True):
    """
    Generate a nice html table from a pandas dataframe.

    :param df: Pandas dataframe. Can have simple or multi indexes and columns.
    :type df: pandas dataframe, mandatory
    :param strat_numbers: a dictionary where the key is a column name and value is a number to be displayed as N=xx
        below each column on the table header. If columns are multiindex, then the keys should be 
        a tuple with all the levels of the multiindex.
    :type strat_numbers: dictionary, optional
    :param caption: caption or title to set for the table.
    :type caption:  str, optional
    :param footer: footer for the table. Can be a string or a list of strings. If a list then every element
        will appear in a different line.
    :type footer: str or list of str, optional
    :param customstyles: dictionary where the keys are our internal classes and values are css styles. These styles
        will be appended to the styles. You can use an empty styles to completely override the defaults
        with your own styles.
    :type customstyles: dict, optional
    :param customcss: A string with css targeting classes or ids. It will be pre-pended to the table in a html <style> element
        without any further processing.
    :type customcss: str, optional 
    :param value_styles: css styles to apply to values, it will be appended to the "values" styles from the default styles. If a 2D structure
        each element represents the style for the corresponding value in the dataframe. If 1D each element is applied to
        every element on each row. If a string it will be applied to all elements.
    :type value_styles: str, list or list of lists, numpy 2d array or pandas dataframe
    :param styles: css styles to use. empty has no styles and is used to override all styles with yours.
    :type styles: str, {'default', 'empty'}
    :param table_id: id for the table, and as prefix for ids for every element on the table. If not provided,
        a random id will be generated internally. It can be an empty string.
    :type table_id: str, optional
    :param show_index: if False, dataframe indexes (row labels) will not be shown on the table.
    :type show_index: bool, optional
    :return: an object encapsulating the html representation of the table formatted in a nice way.
    :rtype: Pandas2HTMLSummaryTable 

    :Example:
    
    >>> from pyreportable import pandas_to_report_html  
    >>> html = pandas_to_report_html(df)

    """
    templateLoader = jinja2.FileSystemLoader(searchpath=dirpath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "template.html"
    jintemplate = templateEnv.get_template(template_file)

    styles = get_styles(styles)

    if customstyles:
        if type(customstyles) != dict:
            raise Exception("customstyles must be a dictionary")
        for k, v in styles.items():
            custom = customstyles.get(k)
            if custom:
                styles[k] = v + custom

    if footer and type(footer) != str:
        footer = "<br>".join(footer)

    if table_id is None:
        table_id = "pyt_" + str(random.getrandbits(16))

    if not strat_numbers:
        strat_numbers = dict()

    if not value_styles:
        value_styles = None
    elif type(value_styles) == str:
        value_styles = [value_styles] * len(df)
    elif hasattr(value_styles, '__iter__'):
        if len(value_styles) != len(df):
            raise Exception("value_styles must have the same name of rows and columns as the dataframe")
        if hasattr(value_styles[0], '__iter__') and type(value_styles[0]) != str:
            if len(value_styles[0]) != len(df.columns):
                raise Exception("value_styles must have the same name of rows and columns as the dataframe")
        else:
            value_styles = [[x]*len(df.columns) for x in value_styles]

    superheaders, tabheaders, numcols, bodyblocks = df_to_intermediate_rep(df, table_id, strat_numbers=strat_numbers, value_styles=value_styles, styles=styles, show_index=show_index)
    rendered = jintemplate.render(tabheaders=tabheaders,
                superheaders=superheaders,
                bodyblocks=bodyblocks,
                numcols=numcols, 
                caption=caption, 
                footer=footer, 
                styles=styles,
                customcss=customcss,
                tabid=table_id,
                )
    return  Pandas2HTMLSummaryTable(rendered)


class Pandas2HTMLSummaryTable:
    """
    A class to encapsulate the html representation
    of the summary table
    """
    def __init__(self, html):
        self.html = html

    def _repr_html_(self):
        return self.html

    def get_raw_html(self):
        """
        Get the raw HTML string representing the table

        :return: the html as a string
        :rtype: str 
        """
        return self.html

