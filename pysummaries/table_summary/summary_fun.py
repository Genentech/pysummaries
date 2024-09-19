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
    mean = str(round(curseries.mean(), 1))
    std = curseries.std()
    if rounding is not None:
        std = round(std, rounding)
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
        median = round(median, rounding)
        iqr = round(iqr, rounding)
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
        median = round(median, rounding)
        q1 = round(q1, rounding)
        q3 = round(q3, rounding)
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
        minimum = round(minimum, rounding)
        maximum = round(maximum,rounding)
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


