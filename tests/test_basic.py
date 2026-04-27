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

from datetime import datetime, timedelta, date
import unittest
import os
import sys

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Unit tests for summary functions (summary_fun.py)
# ---------------------------------------------------------------------------
class TestSummaryFunctions(unittest.TestCase):

    def setUp(self):
        self.num_series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        self.num_series_with_nan = pd.Series([1.0, 2.0, np.nan, 4.0, 5.0])
        self.cat_series = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'])
        self.cat_series_categorical = pd.Series(
            pd.Categorical(['A', 'B', 'A', 'C', 'B', 'A'], categories=['A', 'B', 'C'])
        )
        self.empty_num_series = pd.Series([], dtype=float)
        self.all_nan_series = pd.Series([np.nan, np.nan, np.nan])

    # -- categorical functions --

    def test_categorical_n(self):
        """Verify categorical_n returns correct counts per category level."""
        result = pysummaries.categorical_n(self.cat_series, rounding=1)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result['A'], 3)
        self.assertEqual(result['B'], 2)
        self.assertEqual(result['C'], 1)

    def test_categorical_n_respects_category_order(self):
        """Verify categorical_n preserves the category order for Categorical dtype."""
        result = pysummaries.categorical_n(self.cat_series_categorical, rounding=1)
        self.assertEqual(result.index.tolist(), ['A', 'B', 'C'])

    def test_categorical_n_percent(self):
        """Verify categorical_n_percent returns 'N (%)' format with correct values."""
        result = pysummaries.categorical_n_percent(self.cat_series, rounding=1)
        self.assertIsInstance(result, pd.Series)
        self.assertIn('(', result.iloc[0])
        self.assertIn('%)', result.iloc[0])
        # A has 3 out of 6 = 50.0%
        self.assertTrue(result['A'].startswith('3'))
        self.assertIn('50.0', result['A'])

    def test_categorical_n_percent_no_rounding(self):
        """Verify categorical_n_percent works when rounding is None."""
        result = pysummaries.categorical_n_percent(self.cat_series, rounding=None)
        self.assertIn('%)', result.iloc[0])

    def test_categorical_percent(self):
        """Verify categorical_percent returns percentage strings with correct values."""
        result = pysummaries.categorical_percent(self.cat_series, rounding=1)
        self.assertIn('%', result.iloc[0])
        self.assertIn('50.0', result['A'])

    # -- numerical functions --

    def test_numerical_mean_sd(self):
        """Verify numerical_mean_sd returns 'Mean (SD)' format with correct mean."""
        result = pysummaries.numerical_mean_sd(self.num_series, rounding=1)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('3.0'))
        self.assertIn('(', result)

    def test_numerical_mean_sd_with_nan(self):
        """Verify numerical_mean_sd skips NaN values when computing the mean."""
        result = pysummaries.numerical_mean_sd(self.num_series_with_nan, rounding=1)
        self.assertTrue(result.startswith('3.0'))

    def test_numerical_mean_sd_all_nan(self):
        """Verify numerical_mean_sd returns 'NA' when all values are NaN."""
        result = pysummaries.numerical_mean_sd(self.all_nan_series, rounding=1)
        self.assertIn('NA', result)

    def test_numerical_mean_sd_no_rounding(self):
        """Verify numerical_mean_sd works when rounding is None."""
        result = pysummaries.numerical_mean_sd(self.num_series, rounding=None)
        self.assertIsInstance(result, str)

    def test_numerical_median_iqr(self):
        """Verify numerical_median_iqr returns 'Median [IQR]' format with correct median."""
        result = pysummaries.numerical_median_iqr(self.num_series, rounding=1)
        self.assertTrue(result.startswith('3.0'))
        self.assertIn('[', result)

    def test_numerical_median_q1q3(self):
        """Verify numerical_median_q1q3 returns 'Median [Q1 ; Q3]' format."""
        result = pysummaries.numerical_median_q1q3(self.num_series, rounding=1)
        self.assertTrue(result.startswith('3.0'))
        self.assertIn('[', result)
        self.assertIn(';', result)

    def test_numerical_min_max(self):
        """Verify numerical_min_max returns the correct 'Min ; Max' string."""
        result = pysummaries.numerical_min_max(self.num_series, rounding=1)
        self.assertEqual(result, '1.0 ; 5.0')

    def test_numerical_min_max_all_nan(self):
        """Verify numerical_min_max returns 'NA' when all values are NaN."""
        result = pysummaries.numerical_min_max(self.all_nan_series, rounding=1)
        self.assertIn('NA', result)

    def test_numerical_missing_none(self):
        """Verify numerical_missing reports zero missing when there are no NaNs."""
        result = pysummaries.numerical_missing(self.num_series, rounding=1)
        self.assertTrue(result.startswith('0'))
        self.assertIn('0', result)

    def test_numerical_missing_with_nans(self):
        """Verify numerical_missing correctly counts NaN values and their percentage."""
        result = pysummaries.numerical_missing(self.num_series_with_nan, rounding=1)
        self.assertTrue(result.startswith('1'))
        self.assertIn('20.0', result)

    def test_numerical_missing_empty(self):
        """Verify numerical_missing handles an empty series without error."""
        result = pysummaries.numerical_missing(self.empty_num_series, rounding=1)
        self.assertTrue(result.startswith('0'))


# ---------------------------------------------------------------------------
# Unit tests for column type detection (utils.py)
# ---------------------------------------------------------------------------
class TestDetectColTypes(unittest.TestCase):

    def test_basic_numeric_types(self):
        """Verify int and float columns are detected as numerical."""
        df = pd.DataFrame({
            'num_int': [1, 2, 3],
            'num_float': [1.0, 2.0, 3.0],
        })
        result = detect_df_col_types(df)
        self.assertEqual(result['num_int'], 'numerical')
        self.assertEqual(result['num_float'], 'numerical')

    def test_categorical_types(self):
        """Verify string, bool, and pd.Categorical columns are detected as categorical."""
        df = pd.DataFrame({
            'cat_str': ['a', 'b', 'c'],
            'cat_bool': [True, False, True],
            'cat_pd': pd.Categorical(['x', 'y', 'z']),
        })
        result = detect_df_col_types(df)
        self.assertEqual(result['cat_str'], 'categorical')
        self.assertEqual(result['cat_bool'], 'categorical')
        self.assertEqual(result['cat_pd'], 'categorical')

    def test_datetime_type(self):
        """Verify datetime columns are detected as datetime."""
        df = pd.DataFrame({
            'dt': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']),
        })
        result = detect_df_col_types(df)
        self.assertEqual(result['dt'], 'datetime')

    def test_pyarrow_backend(self):
        """Verify type detection works correctly with PyArrow-backed dtypes."""
        df = pd.DataFrame({'num': [1, 2, 3], 'text': ['a', 'b', 'c']})
        df_pa = df.convert_dtypes(dtype_backend='pyarrow')
        result = detect_df_col_types(df_pa)
        self.assertEqual(result['num'], 'numerical')
        self.assertEqual(result['text'], 'categorical')

    def test_mixed_object_column(self):
        """Verify a column with mixed types falls back to categorical."""
        df = pd.DataFrame({'mixed': pd.Series([1, 'a', True], dtype=object)})
        result = detect_df_col_types(df)
        self.assertEqual(result['mixed'], 'categorical')

    def test_all_nan_object_column(self):
        """Verify an all-NaN object column is classified as numerical (empty after dropna)."""
        df = pd.DataFrame({'empty': pd.Series([np.nan, np.nan], dtype=object)})
        result = detect_df_col_types(df)
        self.assertEqual(result['empty'], 'numerical')


# ---------------------------------------------------------------------------
# Unit tests for calculate_table_summary (table_summary.py)
# ---------------------------------------------------------------------------
class TestCalculateTableSummary(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'value': [10.0, 20.0, 30.0, 40.0],
            'category': ['x', 'y', 'x', 'y'],
        })

    def test_returns_dataframe_and_dict(self):
        """Verify calculate_table_summary returns a DataFrame and a dict."""
        result, strat_nums = pysummaries.calculate_table_summary(self.df, strata='group')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIsInstance(strat_nums, dict)

    def test_strat_nums_correct(self):
        """Verify stratification counts match the actual group sizes."""
        _, strat_nums = pysummaries.calculate_table_summary(self.df, strata='group')
        self.assertEqual(strat_nums['A'], 2)
        self.assertEqual(strat_nums['B'], 2)
        self.assertEqual(strat_nums['Overall'], 4)

    def test_no_strata(self):
        """Verify that without strata only an 'Overall' column is produced."""
        result, strat_nums = pysummaries.calculate_table_summary(self.df)
        self.assertIn('Overall', result.columns)
        self.assertEqual(len(result.columns), 1)

    def test_show_overall_false(self):
        """Verify show_overall=False removes the Overall column and its count."""
        result, strat_nums = pysummaries.calculate_table_summary(
            self.df, strata='group', show_overall=False
        )
        self.assertNotIn('Overall', result.columns)
        self.assertNotIn('Overall', strat_nums)

    def test_columns_include(self):
        """Verify columns_include restricts the summary to the specified columns."""
        result, _ = pysummaries.calculate_table_summary(
            self.df, strata='group', columns_include=['value']
        )
        level0 = result.index.get_level_values(0).unique().tolist()
        self.assertIn('value', level0)
        self.assertNotIn('category', level0)

    def test_columns_exclude(self):
        """Verify columns_exclude removes the specified columns from the summary."""
        result, _ = pysummaries.calculate_table_summary(
            self.df, strata='group', columns_exclude=['category']
        )
        level0 = result.index.get_level_values(0).unique().tolist()
        self.assertNotIn('category', level0)

    def test_columns_labels(self):
        """Verify columns_labels renames column labels in the output index."""
        result, _ = pysummaries.calculate_table_summary(
            self.df, strata='group', columns_labels={'value': 'My Value'}
        )
        level0 = result.index.get_level_values(0).unique().tolist()
        self.assertIn('My Value', level0)
        self.assertNotIn('value', level0)

    def test_strata_with_na_raises(self):
        """Verify that NaN values in the strata column raise an exception."""
        df = self.df.copy()
        df.loc[0, 'group'] = np.nan
        with self.assertRaises(Exception):
            pysummaries.calculate_table_summary(df, strata='group')

    def test_invalid_strata_column_raises(self):
        """Verify that a nonexistent strata column raises an exception."""
        with self.assertRaises(Exception):
            pysummaries.calculate_table_summary(self.df, strata='nonexistent')

    def test_categorical_preset_n(self):
        """Verify the 'n' categorical preset produces a valid summary."""
        result, _ = pysummaries.calculate_table_summary(
            self.df, strata='group', categorical_functions='n'
        )
        self.assertIsInstance(result, pd.DataFrame)

    def test_numerical_preset_medianiqr(self):
        """Verify the median IQR numerical preset includes 'Median [IQR]' in the index."""
        result, _ = pysummaries.calculate_table_summary(
            self.df, strata='group', numerical_functions='meansd_medianiqr_minmax_missing'
        )
        level1 = result.index.get_level_values(1).unique().tolist()
        self.assertIn('Median [IQR]', level1)

    def test_invalid_categorical_preset_raises(self):
        """Verify that an invalid categorical preset name raises an exception."""
        with self.assertRaises(Exception):
            pysummaries.calculate_table_summary(
                self.df, strata='group', categorical_functions='nonexistent'
            )

    def test_categorical_missing_level(self):
        """Verify that NaN categoricals are replaced with the specified missing level label."""
        df = self.df.copy()
        df.loc[0, 'category'] = np.nan
        result, _ = pysummaries.calculate_table_summary(
            df, strata='group', categorical_missing_level='Unknown'
        )
        level1_values = result.index.get_level_values(1).tolist()
        self.assertIn('Unknown', level1_values)


# ---------------------------------------------------------------------------
# Unit tests for get_table_summary (pysummaries.py)
# ---------------------------------------------------------------------------
class TestGetTableSummary(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'value': [10.0, 20.0, 30.0, 40.0],
            'category': ['x', 'y', 'x', 'y'],
        })
        self.table_id = 'pyt_test'

    def test_native_backend_returns_summary_table(self):
        """Verify native backend returns a Pandas2HTMLSummaryTable instance."""
        result = pysummaries.get_table_summary(
            self.df, strata='group', backend='native', table_id=self.table_id
        )
        self.assertIsInstance(result, pysummaries.Pandas2HTMLSummaryTable)

    def test_native_backend_html_content(self):
        """Verify native backend HTML contains the table ID and variable names."""
        result = pysummaries.get_table_summary(
            self.df, strata='group', backend='native', table_id=self.table_id
        )
        html_str = result.get_raw_html()
        self.assertIn(self.table_id, html_str)
        self.assertIn('<table', html_str)
        self.assertIn('value', html_str)
        self.assertIn('category', html_str)

    def test_gt_backend_returns_gt_object(self):
        """Verify GT backend returns a great_tables GT instance."""
        result = pysummaries.get_table_summary(
            self.df, strata='group', backend='gt', id=self.table_id
        )
        self.assertIsInstance(result, GT)

    def test_invalid_backend_raises(self):
        """Verify that an unsupported backend name raises an exception."""
        with self.assertRaises(Exception):
            pysummaries.get_table_summary(self.df, backend='invalid')

    def test_show_n_false(self):
        """Verify show_n=False omits observation counts from the HTML header."""
        result = pysummaries.get_table_summary(
            self.df, strata='group', backend='native',
            table_id=self.table_id, show_n=False
        )
        html_str = result.get_raw_html()
        self.assertNotIn('N=', html_str)


# ---------------------------------------------------------------------------
# Integration tests with full sample data
# ---------------------------------------------------------------------------
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.sample_data = pysummaries.get_test_data()
        sample_data_pyarrow = self.sample_data.convert_dtypes(
            dtype_backend="pyarrow", convert_integer=False
        )
        sample_data_pyarrow['procedures'] = sample_data_pyarrow['procedures'].convert_dtypes(
            dtype_backend="pyarrow"
        )
        self.sample_data_pyarrow = sample_data_pyarrow
        self.table_id = "pyt_1234"

    def test_simple_table_summary_df(self):
        """Verify full pipeline produces correct structure, columns, and strat counts."""
        sum_table, strat_nums = pysummaries.calculate_table_summary(
            self.sample_data, strata='group'
        )
        self.assertIsInstance(sum_table, pd.DataFrame)
        self.assertEqual(strat_nums['Overall'], len(self.sample_data))
        self.assertIn('Overall', sum_table.columns)
        self.assertIn('Control', sum_table.columns)
        self.assertIn('Experimental', sum_table.columns)
        level0 = sum_table.index.get_level_values(0).unique().tolist()
        for var in ['gender', 'age', 'region', 'has_diabetes', 'procedures', 'colmissing']:
            self.assertIn(var, level0)
        self.assertEqual(
            strat_nums['Control'],
            len(self.sample_data[self.sample_data['group'] == 'Control'])
        )

    def test_simple_table_summary_df_pyarrow(self):
        """Verify PyArrow-backed dtypes produce identical results to numpy-backed dtypes."""
        sum_table_np, _ = pysummaries.calculate_table_summary(
            self.sample_data, strata='group'
        )
        sum_table_pa, strat_nums = pysummaries.calculate_table_summary(
            self.sample_data_pyarrow, strata='group'
        )
        self.assertTrue(sum_table_np.equals(sum_table_pa))
        self.assertEqual(strat_nums['Overall'], len(self.sample_data))

    def test_simple_table_summary_native(self):
        """Verify native backend HTML contains expected variables and strata levels."""
        result = pysummaries.get_table_summary(
            self.sample_data, strata='group', backend='native', table_id=self.table_id
        )
        html_str = result.get_raw_html()
        self.assertIsInstance(html_str, str)
        self.assertIn(self.table_id, html_str)
        self.assertIn('<table', html_str)
        for var in ['gender', 'age', 'region']:
            self.assertIn(var, html_str)
        self.assertIn('Overall', html_str)
        self.assertIn('Control', html_str)
        self.assertIn('Experimental', html_str)

    def test_simple_table_summary_gt(self):
        """Verify GT backend HTML contains expected variables and strata levels."""
        gt_obj = pysummaries.get_table_summary(
            self.sample_data, strata='group', backend='gt', id=self.table_id
        )
        html_str = gt_obj.as_raw_html()
        self.assertIsInstance(html_str, str)
        self.assertGreater(len(html_str), 100)
        self.assertIn(self.table_id, html_str)
        self.assertIn('<table', html_str)
        for var in ['gender', 'age', 'region']:
            self.assertIn(var, html_str)
        self.assertIn('Overall', html_str)
        self.assertIn('Control', html_str)


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    script_folder = os.path.split(os.path.realpath(__file__))[0]
    repo_folder = os.path.split(script_folder)[0]

    if "--inplace" in sys.argv:
        sys.path.insert(0, repo_folder)
        sys.argv.remove('--inplace')

    import pysummaries
    from pysummaries.table_summary.utils import detect_df_col_types
    from great_tables import GT

    print("package location:", pysummaries.__file__)

    unittest.main()
