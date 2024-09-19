import os
import sys
import pickle

script_folder = os.path.split(os.path.realpath(__file__))[0]
repo_folder = os.path.split(script_folder)[0]
sys.path.insert(0, repo_folder)

from pysummaries import (get_table_summary, get_sample_data,
        calculate_table_summary, 
        )



table_id = "pyt_1234"
df = get_sample_data()

summary_table_df = calculate_table_summary(df, strata='group')
summary_table_html = get_table_summary(df, strata='group', backend='native', table_id=table_id).get_raw_html()
summary_table_gt = get_table_summary(df, strata='group', backend='gt', id=table_id).as_raw_html()  

test_data = {'summary_table_df' : summary_table_df, 
        'summary_table_html': summary_table_html,
        'summary_table_gt': summary_table_gt,
        }

with open(os.path.join(script_folder, 'test_data.pkl'), 'wb') as f:
    pickle.dump(test_data, f)
    
    
