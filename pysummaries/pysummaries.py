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
from great_tables import GT, html

from .table_summary import calculate_table_summary
from .reportable import pandas_to_report_html

# TODO:

def get_table_summary(df, strata=None, backend='native', show_n=True, show_overall=True, columns_labels=None, overall_name="Overall",
        columns_include=None, columns_exclude=None,
        rounding=1, categorical_functions=None, numerical_functions=None,
        categorical_missing_level='Missing', **kwargs):
    """
    Calculates a summary table for the pandas dataframe df and returns an object for nice display.

    :param df: pandas dataframe from which to calculate the table one
    :type df: pandas dataframe, mandatory
    :param strata: the name of a column in the dataframe to stratify the table one (columns)
    :type strata: str, optional
    :param backend: the backend used to display the summary, either 'native' or 'gt' (great_tables)
    :type backend: str, optional
    :param show_n: Show the number of observations on the column header
    :type show_n: bool, optional
    :param show_overall: Show the Overall column. By default True. If False it will take effect only if strata is defined, otherwise ignored
    :type show_overall: bool, optional
    :param columns_labels: A dictionary defining labels for the columns. Keys should be the column name and values a string with the label. Non existing
        columns will be ignored.
    :type columns_labels: dict, optional
    :param overall_name: name for the column Overall
    :type overall_name: string, optional
    :param columns_include: columns to include in the report, also determines the order of columns in the report
    :type columns_include: list, optional
    :param columns_exclude: columns to exclude from the report
    :type columns_exclude: list, optional
    :param rounding: number of decimal points to show, by default 1.
    :type rounding: int, optional
    :param categorical_functions: if a string, one of the presets for categorical summarization will be applied, by default n_percent. If a tuple or list, 
        the first element must be a function to apply to categorical functions, the second element must be a string or number with the value to report if there are no 
        elements in a categorical level (for example '(0%)' for n_percent). If None those will be reported as nan.
    :type categorical_functions: str,  list or tuple, optional
    :param numerical_functions: if a string, one of the presets for numerical summarization will be applied, the default one is 'meansd_medianq1q3_minmax_missing. 
        If a dictionary it should have a label (as it should appear in the rows index) and as a values 
        functions to apply to the numerical columns of the dataframe. Multiple pairs of labels and functions are supported. 
    :type numerical_functions: str or dict, optional
    :param categorical_missing_level: if a categorical column has NAs, they will be replaced by the string indicated here, by default 'Missing'. That will create a new level 
        in the category. If set to None, the NAs will not be replaced.
    :type categorical_missing_level: str, optional
    :param kwargs: keyword arguemnts to pass to the pandas_to_report_html function or the great_tables.GT constructor. See the documentation for those for further details.
    :return: An object with the html representation of the table
    :rtype: Pandas2HTMLSummaryTable if backend is native or great_tables.GT if backend is gt
        
    :Example:
    
    >>> from pysummaries import get_table_summary
    >>> tone = get_table_summary(df, strata="age_groups")

    """
    if backend not in ('native', 'gt'):
        raise Exception(f"Available backends are 'native' or 'gt', got {backend}")

    tone, strat_numbers = calculate_table_summary(df, strata=strata, show_overall=show_overall, columns_labels=columns_labels, overall_name=overall_name, rounding=rounding, 
            columns_include=columns_include, columns_exclude=columns_exclude,
            categorical_functions=categorical_functions, numerical_functions=numerical_functions,
            categorical_missing_level=categorical_missing_level)  
    if backend == 'native':
        if show_n:
            tone_html = pandas_to_report_html(tone, strat_numbers=strat_numbers, **kwargs) 
        else:
            tone_html = pandas_to_report_html(tone, strat_numbers=None, **kwargs) 
    elif backend == 'gt':
        tone_html = GT(tone.reset_index(), rowname_col="level_1", groupname_col="level_0", **kwargs)
        # Ns 
        if show_n:
            col_ns = {k:html(k+f"<br>(N={v})") for k,v in strat_numbers.items()}
            tone_html = tone_html.cols_label(**col_ns)
    return tone_html

