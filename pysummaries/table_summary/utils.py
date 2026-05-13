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
from decimal import Decimal

import narwhals as nw
import pandas as pd
import numpy as np


class PySummariesException(Exception):
    """Base exception for all pysummaries errors."""
    pass


def _is_pandas_object_col(df, col_name):
    """Check if a column in a pandas DataFrame has object dtype."""
    if isinstance(df, pd.DataFrame):
        return df[col_name].dtype == object
    return False


def _classify_object_col(df, col_name):
    """Classify a pandas object-dtype column by inspecting its values."""
    col = df[col_name].dropna()
    if len(col) == 0:
        return "numerical"
    curtype = type(col.iloc[0])
    equal = np.array(col.apply(lambda x: type(x) == curtype))
    if not np.all(equal):
        return "categorical"
    if curtype == str:
        return "categorical"
    if np.issubdtype(type(col.iloc[0]), np.number) or isinstance(col.iloc[0], (int, float, Decimal)):
        return "numerical"
    return "categorical"


def detect_df_col_types(df):
    """
    Gets a dataframe and returns a dictionary with keys being column
    names from the dataframe and value is the type:
    categorical, numerical or datetime.

    Supports pandas, polars and PyArrow dataframes via narwhals.
    Other narwhals-compatible backends (e.g. Modin, cuDF) may also work but are untested.
    """
    nw_df = nw.from_native(df)
    results = dict()
    for col_name, dtype in nw_df.schema.items():
        # For pandas object columns, narwhals may infer a type (e.g. String)
        # that doesn't reflect the actual mixed content. Use value inspection instead.
        if _is_pandas_object_col(df, col_name):
            results[col_name] = _classify_object_col(df, col_name)
        elif dtype.is_numeric():
            results[col_name] = "numerical"
        elif dtype.is_temporal():
            results[col_name] = "datetime"
        elif dtype == nw.Boolean or dtype == nw.Categorical or dtype == nw.String or dtype == nw.Enum:
            results[col_name] = "categorical"
        elif dtype == nw.Object:
            results[col_name] = _classify_object_col(df, col_name)
        else:
            results[col_name] = "categorical"
    return results
