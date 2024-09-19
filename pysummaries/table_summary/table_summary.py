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

import pandas as pd

from .utils import detect_df_col_types
from . import summary_fun as sf


# TODO: 
# re-index
# calculate statistics by row
# control overall position end or start
# be able to specify column type
#
# optional:
# drop or insert levels according to number of functions

### 
# functions presets

categorical_presets = {
        'n_percent': (sf.categorical_n_percent, '0 (0%)'), 
        'n': (sf.categorical_n, 0),
        'percent': (sf.categorical_percent, '0%'),
}

numerical_presets = {
    'meansd_medianq1q3_minmax_missing': {"Mean (SD)": sf.numerical_mean_sd,
                            "Median [Q1 ; Q3]": sf.numerical_median_q1q3,
                            "Min ; Max" : sf.numerical_min_max,
                            "Missing": sf.numerical_missing,
                            },
    'meansd_medianiqr_minmax_missing': {"Mean (SD)": sf.numerical_mean_sd,
                            "Median [IQR]": sf.numerical_median_iqr,
                            "Min ; Max" : sf.numerical_min_max,
                            "Missing": sf.numerical_missing,
                            },

}

def calculate_stats(df, var, functions, coltype, strata=None, stratcat=None, var_label=None, rounding=1, categorical_missing_level=None):
    """
    For the dataframe df, for the variable var, apply all the functions. 
    If there is a stratum stratcat defined, then the dataframe will be sliced
    using the column strata for the stratum defined.
    If var_label is not None, then it will be used as index for the returning dataframe
    """
    if strata is None and stratcat is None:
        curseries = df.loc[:, var]
    else:
        curseries = df.loc[df[strata]==stratcat, var]
    if coltype=='categorical' and  categorical_missing_level:
        curseries = curseries.copy()
        if curseries.dtype.name=='category':
            cats = curseries.cat.categories.to_list() + [categorical_missing_level]
            curseries = curseries.cat.set_categories(cats)
        curseries = curseries.fillna(categorical_missing_level)
    curstratdf = None
    for funlabel, fun in functions.items():
        curstat = fun(curseries, rounding)
        if coltype == "categorical":
            if var_label:
                curstat.index = pd.MultiIndex.from_tuples([(str(var_label), str(a)) for a in curstat.index])
            else:
                curstat.index = pd.MultiIndex.from_tuples([(str(var), str(a)) for a in curstat.index])
        elif coltype == "numerical":
            if type(curstat) != pd.Series:
                curstat = pd.Series(curstat)
            if var_label:
                curstat.index = pd.MultiIndex.from_tuples([(str(var_label), str(funlabel))])
            else:
                curstat.index = pd.MultiIndex.from_tuples([(str(var), str(funlabel))])
        if curstratdf is None:
            curstratdf = curstat
        else: 
            curstratdf = pd.concat([curstratdf, curstat])
    return curstratdf


def calculate_table_summary(df, strata=None, show_overall=True, columns_labels=None, overall_name='Overall',
        columns_include=None, columns_exclude=None,
        categorical_functions=None, numerical_functions=None, rounding=1, 
        categorical_missing_level='Missing'):
    """
    Calculates  a table summary from a pandas dataframe.

    :param df: pandas dataframe from which to calculate the table one
    :type df: pandas dataframe, mandatory
    :param strata: the name of a column in the dataframe to stratify the table one (columns)
    :type strata: str, optional
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
    :param categorical_functions: if a string, one of the presets for categorical summarization will be applied, by default n_percent. If a tuple or list, 
        the first element must be a function to apply to categorical functions, the second element must be a string or number with the value to report if there are no 
        elements in a categorical level (for example 0 (0%) for n_percent. If None those will be reported as nan.
    :type categorical_functions: str,  list or tuple, optional
    :param numerical_functions: if a string, one of the presets for numerical summarization will be applied, the default one is 'meansd_medianq1q3_minmax_missing. 
        If a dictionary it should have a label (as it should appear in the rows index) and as a values 
        functions to apply to the numerical columns of the dataframe. Multiple pairs of labels and functions are supported. 
    :type numerical_functions: str or dict, optional
    :param rounding: number of decimal points to show, by default 1.
    :type rounding: int, optional
    :param categorical_missing_level: if a categorical column has NAs, they will be replaced by the string indicated here, by default 'Missing'. That will create a new level 
        in the category. If set to None, the NAs will not be replaced.
    :type categorical_missing_level: str, optional
    :return: the table summary as a pandas dataframe
    :rtype: pandas dataframe
    :return: the number of observations for each column in the table summary as a dictionary where keys are column names (strata levels) and 
      the values are the counts as integers.
    :rtype: dictionary
        
    :Example:
    
    >>> from pysummaries import calculate_table_summary
    >>> tone = calculate_table_summary(df, strata="age_groups")

    """

    if categorical_functions:
        if type(categorical_functions)==str:
            temp = categorical_presets.get(categorical_functions)
            if not temp:
                raise Exception(f"categorical preset {categorical_functions} not defined!")
            categorical_functions = temp
        elif type(categorical_functions)==list or type(categorical_functions)==tuple:
            if len(categorical_functions)!=2:
                raise Exception("The length of categorical functions must be 2!")
            if not callable(categorical_functions[0]):
                raise Exception("The first element of categorical_functions must be a function")
            #if not type(categorical_functions[1])==str:
                #raise Exception("The second element of categorical_functions must be a string")
        else:
            raise Exception("categorical_functions should be either string, list or tuple")
    else:
        categorical_functions = categorical_presets["n_percent"]

    if numerical_functions:
        if type(numerical_functions)==str:
            temp = numerical_presets.get(numerical_functions)
            if not temp:
                raise Exception(f"numerical preset {numerical_functions} not defined!")
            numerical_functions = temp
        elif type(numerical_functions)==dict:
            if not all([callable(x) for x in numerical_functions.values()]):
                raise Exception("The values of numerical_functions must be functions")
            if not all([type(x)==str for x in numerical_functions.keys()]):
                raise Exception("The keys of numerical_functions must be strings")
        else:
            raise Exception("numerical_functions should be either string or dict")
    else:
        numerical_functions = numerical_presets["meansd_medianq1q3_minmax_missing"]


    coltypes = detect_df_col_types(df)
    colnames = df.columns.to_list()
    strat_cats = list()
    if strata is not None:
        if any(pd.isna(df[strata])):
            raise Exception("strata may not contain missing values")
        if strata in coltypes and strata in colnames:
            del coltypes[strata]
            colnames.remove(strata)
        else:
            raise Exception(f"strata column {strata} not found in dataframe")
        strat_cats = df[strata].unique()

    if columns_include:
        colnames = [c for c in columns_include if c in colnames]
    if columns_exclude:
        colnames = [c for c in colnames if c not in columns_exclude]
    if not colnames:
        raise Exception("No columns left after filtering for columns_include, columns_exclude and strata")

    df_list = list()
    strat_numbers = dict()
    for colname in colnames:
        coltype = coltypes[colname]
        var_dict = dict()
        if coltype == "categorical":
            curfuns, catna = categorical_functions
            curfuns = {'': curfuns}
        elif coltype == "numerical":
            curfuns = numerical_functions
        else:
            raise NotImplementedError(f"statistics for column {colname} (coltype) not implemented")
        col_label=None
        if columns_labels:
            col_label = columns_labels.get(colname)
        # overall
        overalldf = calculate_stats(df, colname, curfuns, coltype, rounding=rounding, var_label=col_label, categorical_missing_level=categorical_missing_level)
        # strata
        for stratcat in strat_cats:
            curstratdf = calculate_stats(df, colname, curfuns, coltype, strata=strata, stratcat=stratcat, rounding=rounding, var_label=col_label, categorical_missing_level=categorical_missing_level)
            var_dict[stratcat] = curstratdf
            strat_numbers[stratcat] = len(df.loc[df[strata]==stratcat])
        var_dict[overall_name] = overalldf
        strat_numbers[overall_name] = len(df)
        var_df = pd.DataFrame(var_dict)
        if coltype == "categorical":
            if catna:
                var_df = var_df.fillna(catna)
        df_list.append(var_df)

    tonedf = pd.concat(df_list)

    if not show_overall and strata:
        tonedf = tonedf.drop(columns=overall_name)
        del strat_numbers[overall_name]

    return tonedf, strat_numbers

