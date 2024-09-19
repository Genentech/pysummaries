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
import datetime

import pandas as pd
import numpy as np

numeric_types = {np.dtype('int32'), np.dtype('int16'), np.dtype('int8'), np.dtype('uint8'), np.dtype('uint16'),
             np.int32, np.int16, np.int8, np.uint8, np.uint16, int, float,
            pd.Int8Dtype(), pd.Int16Dtype(), pd.Int32Dtype(), pd.UInt8Dtype(), pd.UInt16Dtype(),
             np.dtype('int64'), np.dtype('uint64'), np.dtype('uint32'), np.dtype('float'),
               np.int64, np.uint64, np.uint32, np.float64, pd.Int64Dtype(), pd.UInt32Dtype(), pd.UInt64Dtype(),
               pd.Float64Dtype(), pd.Float32Dtype()}
datetime_types = {datetime.datetime, np.datetime64, np.dtype('<M8[ns]'), np.datetime64}
categorical_types = {pd.core.dtypes.dtypes.CategoricalDtype, bool}


def detect_df_col_types(df):
    """
    Gets a dataframe and returns a dictionary with keys being column 
    names from the dataframe and value is the type:
    categorical, numerical or datetime
    """

    types = df.dtypes.values.tolist()
    columns = df.columns.values.tolist()

    results = dict()
    for colname, coltype in zip(columns, types):
        if coltype in categorical_types:
            results[colname] = "categorical"
            continue
        elif coltype in numeric_types:
            results[colname] = "numerical"
            continue
        elif coltype in datetime_types:
            results[colname] = "datetime"
        elif coltype == object:
            col = df[colname].dropna()
            if len(col):
                curtype = type(col.iloc[0])
                equal = np.array(col.apply(lambda x: type(x) == curtype))
                if not np.all(equal):
                    results[colname] = "categorical"
                    continue
            else:
                results[colname] = "numerical"
                continue
            if curtype in categorical_types:
                results[colname] = "categorical"
                continue
            elif curtype == str:
                results[colname] = "categorical"
            elif curtype in numeric_types:
                results[colname] = "numerical"
                continue
            elif curtype in datetime_types:
                results[colname] = "datetime"
            else:
                results[colname] = "categorical"
        else:
            results[colname] = "categorical"

    return results

