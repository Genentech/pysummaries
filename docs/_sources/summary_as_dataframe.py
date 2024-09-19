# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Getting the summary as a pandas dataframe
#
# The functions get_table_summary_html and get_table_summary_gt return the summary as object that can be
# nicely displayed in a Jupyter notebook. Internally they calculate the summary as a pandas dataframe
# using the function calculate_table_summary, 
# and then pass this to either the function pandas_to_report_html (described in the section Native Backend)
# or to great_tables.GT respectively.
# 
# That means you can get the summary as a pandas dataframe by calling the function calculate_table_summary directly.
#
# **OK, but why would I like to do that?**
#
# Glad you asked! Because by obtaining the summary as a pandas dataframe you can then manipulate it as you wish.
# When you are done with the manipulation, you can pass it again to either pandas_to_report_html or great_tables.GT.
#
# Let's look at an example:
#
# Let's say you have a dataframe where one individual can have multiple observations, for this example they may take one or two types of medication. 
# If you run the summary directly on this data, the percentages would be calculated on the total number of observations, 
# but you would like to calculate the percentages on the number of individuals. One of the ways of achieving this is to first calculate the summary getting only
# the counts for each medication, and then calculating the percentages on the number of individuals.
#
# Let's first create some dummy data.

# %% tags=["remove-input"]
import sys
sys.path.insert(0, "../..")


# %%
import pandas as pd
from pysummaries import calculate_table_summary, pandas_to_report_html, categorical_n

# First, let's create some dummy data
df = pd.DataFrame({'id': [1, 1, 2, 3, 3, 4],
                   'medication': ['A', 'B', 'A', 'A', 'B', 'B'],
                   'group': ['Control', 'Control', 'Experimental', 'Experimental', 'Experimental', 'Control',]})
df

# %% [markdown]
# And now we calculate the summary with only the counts.

# %%
summary_num, strat_nums = calculate_table_summary(df, strata="group", categorical_functions=(categorical_n, 0), columns_include=['medication'])
summary_num

# %% [markdown]
# strat_nums is a dictionary with the number of observations in each strata, and it can be 
# used later to display the Ns in the columns headers.
# %%
strat_nums 
# %% [markdown] 
# Here we need to calculate them ourselves
# based on the number of individuals.

# %%
strat_nums = {'Overall': len(df['id'].unique()),
               'Control': len(df[df['group'] == 'Control']['id'].unique()),
               'Experimental': len(df[df['group'] == 'Experimental']['id'].unique())}
strat_nums

# %% [markdown]
# Having that, we can calculate the percentages on the number of individuals.

# %%
summary_per = summary_num.copy()
for col in summary_per.columns:
    curn = strat_nums[col]
    summary_per[col] = round(100*summary_per[col]/curn, 2)
    summary_per[col] = " (" + summary_per[col].astype(str) + "%)"
summary_per

# %% [markdown]
# Now, we can merge the two dataframes to get the final result.

# %%
summary_df = summary_num.astype(str) + summary_per
summary_df

# %% [markdown]
# And  finally we can build the html representation of the summary.
#
# Let's do first with the native backend:

# %%
summary_html = pandas_to_report_html(summary_df, strat_numbers=strat_nums)
summary_html


# %% [markdown]
# And now with the great_tables backend

# %%
from great_tables import GT, html

col_ns = {k:html(k+f"<br>(N={v})") for k,v in strat_nums.items()}
summary_gt = (GT(summary_df.reset_index(), rowname_col="level_1", groupname_col="level_0")
                    .cols_align('center')
                    .cols_label(**col_ns)
)
summary_gt
# %%

# %% [markdown]
# ## Other options
# 
# calculate_table_summary has many options, all of them have been described already 
# when describing the options for get_table_summary_html and get_table_summary_gt.
