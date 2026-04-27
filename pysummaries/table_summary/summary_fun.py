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


def _has_valid_values(curseries):
    """Returns True if the series has at least one non-NaN value."""
    return curseries.notna().any()


def _format_val(value, rounding):
    """Rounds a numeric value if possible, returns 'NA' string for NaN."""
    if pd.isna(value):
        return 'NA'
    if rounding is not None:
        value = round(value, rounding)
    return str(value)


def _cat_value_counts(curseries):
    """Returns value_counts preserving category order for Categorical dtype."""
    dosort = curseries.dtype.name != 'category'
    return curseries.value_counts(sort=dosort)


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
    return _cat_value_counts(curseries)

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
    counts = _cat_value_counts(curseries)
    curperc = counts.div(float(len(curseries))).mul(100)
    if rounding is not None:
        curperc = round(curperc, rounding)
    curperc = " (" + curperc.astype(str).str.cat([" %)"]*len(curperc))
    return counts.astype(str).str.cat(curperc)

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
    curperc = _cat_value_counts(curseries).div(float(len(curseries))).mul(100)
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
    if not _has_valid_values(curseries):
        return 'NA (NA)'
    mean = _format_val(curseries.mean(), rounding)
    std = _format_val(curseries.std(), rounding)
    return mean + " (" + std + ")"

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
    if not _has_valid_values(curseries):
        return 'NA [NA]'
    median = _format_val(curseries.median(), rounding)
    iqr = _format_val(curseries.quantile(0.75) - curseries.quantile(0.25), rounding)
    return median + " [" + iqr + "]"

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
    if not _has_valid_values(curseries):
        return 'NA [NA ; NA]'
    median = _format_val(curseries.median(), rounding)
    q1 = _format_val(curseries.quantile(0.25), rounding)
    q3 = _format_val(curseries.quantile(0.75), rounding)
    return median + " [" + q1 + " ; " + q3 + "]"

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
    if not _has_valid_values(curseries):
        return 'NA ; NA'
    minimum = _format_val(curseries.min(), rounding)
    maximum = _format_val(curseries.max(), rounding)
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
        perc = round(perc, rounding)
    return str(n) + " (" + str(perc) + " %)"
