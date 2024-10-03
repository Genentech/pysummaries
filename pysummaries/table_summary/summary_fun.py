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
Functions to summarise pandas series
"""
import pandas as pd

def categorical_n(curseries, rounding):
    """
    Calculates the N for each category in the series.

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a series with a numerical or string value per categorical level
    :rtype: pandas series
    """
    curstat_n = len(curseries)
    dosort = True
    if curseries.dtype.name == 'category':
        dosort = False
    curn = curseries.value_counts(sort=dosort)
    return curn

def categorical_n_percent(curseries, rounding):
    """
    Calculates "N (%)" fo each category in the series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a series with a numerical or string value per categorical level
    :rtype: pandas series
    """
    curstat_n = len(curseries)
    dosort = True
    if curseries.dtype.name == 'category':
        dosort = False
    curperc = curseries.value_counts(sort=dosort).div(float(curstat_n)).mul(100)
    if rounding is not None:
        curperc = round(curperc, rounding)
    curperc = " (" + curperc.astype(str).str.cat([" %)"]*len(curperc))
    curn = curseries.value_counts(sort=dosort).astype(str).str.cat(curperc)
    return curn

def categorical_percent(curseries, rounding):
    """
    Calculates the percentage for each category in the series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a series with a numerical or string value per categorical level
    :rtype: pandas series
    """
    curstat_n = len(curseries)
    curperc = curseries.value_counts().div(float(curstat_n)).mul(100)
    if rounding is not None:
        curperc = round(curperc, rounding)
    curperc = curperc.astype(str).str.cat([" %"]*len(curperc))
    return curperc

def numerical_mean_sd(curseries, rounding):
    """
    Calculates "Mean (SD)" for the numerical series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a single value with the summary for the series
    :rtype: int, float or string
    """
    mean = curseries.mean()
    std = curseries.std()
    if rounding is not None:
        if not pd.isna(mean):
            mean = round(mean, rounding)
        if not pd.isna(std):
            std = round(std, rounding)
    if pd.isna(mean):
        mean = 'NA'
    if pd.isna(std):
        std = 'NA'
    mean = str(mean)
    std = " (" + str(std) + ")"
    return mean + std

def numerical_median_iqr(curseries, rounding):
    """
    Calculates "Median [IQR]" for the numerical series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a single value with the summary for the series
    :rtype: int, float or string
    """
    median = curseries.median()
    iqr = curseries.quantile(0.75) - curseries.quantile(0.25)
    if rounding is not None:
        if not pd.isna(median):
            median = round(median, rounding)
        if not pd.isna(iqr):
            iqr = round(iqr, rounding)
    if pd.isna(median):
        median = 'NA'
    if pd.isna(std):
        iqr = 'NA'
    median = str(median)
    iqr = " [" + str(iqr) + "]"
    return median + iqr

def numerical_median_q1q3(curseries, rounding):
    """
    Calculates "Median [Q1 ; Q3]" for the numerical series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a single value with the summary for the series
    :rtype: int, float or string
    """
    median = curseries.median()
    q1 = curseries.quantile(0.25)
    q3 = curseries.quantile(0.75)
    if rounding is not None:
        if not pd.isna(median):
            median = round(median, rounding)
        if not pd.isna(q1):
            q1 = round(q1, rounding)
        if not pd.isna(q3):
            q3 = round(q3, rounding)
    if pd.isna(median):
        median = 'NA'
    if pd.isna(q1):
        q1 = 'NA'
    if pd.isna(q3):
        q3 = 'NA'
    median = str(median)
    iqr = " [" + str(q1) +  " ; " + str(q3) + "]"
    return median + iqr

def numerical_min_max(curseries, rounding):
    """
    Calculates "Min ; Max" for the numerical series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a single value with the summary for the series
    :rtype: int, float or string
    """
    minimum = curseries.min()
    maximum = curseries.max()
    if rounding is not None:
        if not pd.isna(minimum):
            minimum = round(minimum, rounding)
        if not pd.isna(maximum):
            maximum = round(maximum,rounding)
    if pd.isna(minimum):
        minimum = 'NA'
    if pd.isna(maximum):
        maximum = 'NA'
    minimum = str(minimum)
    maximum = str(maximum)
    return minimum + " ; " + maximum

def numerical_missing(curseries, rounding):
    """
    Calculates "N (%)" of missing values (na) for the numerical series

    :param curseries: series to be summarized
    :type curseries: pandas series
    :param rounding: number of decimal points to show round the results
    :type rounding: int
    :return: a single value with the summary for the series
    :rtype: int, float or string
    """
    n = 0
    perc = 0
    if len(curseries):
        n = len(curseries[pd.isna(curseries)])
        perc = 100 * (n/len(curseries)) 
    if rounding is not None:
        perc = round(perc, 1)
    return str(n) + " (" + str(perc) + " %)"


