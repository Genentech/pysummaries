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
import shutil
import pickle

import pandas as pd
import numpy as np


class TestBasic(unittest.TestCase):
    """
    Test suite for pysummaries.
    """

    def _prepare_data(self):

        self.sample_data = pysummaries.get_sample_data()

        self.table_id = "pyt_1234"
        with open(os.path.join(script_folder, 'test_data.pkl'), 'rb') as f:
            self.test_data = pickle.load(f)


    def setUp(self):

        self._prepare_data()

    def test_simple_table_summary_df(self):
        sum_table, strat_nums = pysummaries.calculate_table_summary(self.sample_data, strata='group')
        sum_table_test, strat_nums_test = self.test_data['summary_table_df'] 
        self.assertTrue(sum_table.equals(sum_table_test))
        self.assertTrue(strat_nums['Overall']==strat_nums_test['Overall'])

    def test_simple_table_summary_native(self):
        sum_table_html = pysummaries.get_table_summary(self.sample_data, strata='group', backend='native', table_id=self.table_id).get_raw_html()
        sum_table_html_test = self.test_data['summary_table_html'] 
        self.assertTrue(sum_table_html==sum_table_html_test)

    def test_simple_table_summary_gt(self):
        sum_table_html = pysummaries.get_table_summary(self.sample_data, strata='group', backend='gt', id=self.table_id).as_raw_html()
        sum_table_html_test = self.test_data['summary_table_gt'] 
        self.assertTrue(sum_table_html==sum_table_html_test)

if __name__ == '__main__':

    import sys

    script_folder = os.path.split(os.path.realpath(__file__))[0]
    repo_folder = os.path.split(script_folder)[0]

    if "--inplace" in sys.argv:
        sys.path.insert(0, repo_folder)
        sys.argv.remove('--inplace')

    import pysummaries

    print("package location:", pysummaries.__file__)

    unittest.main()
