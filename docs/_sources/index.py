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
# # Welcome to PySumaries documentation!
#
# PySummaries is a Python package to easily produce table summarizations
# from pandas dataframes.
#
# ## Installation
# 
# You can install the package with pip directly from this repo:
# pip install git+https://github.roche.com/fajardoo/pysummaries@master

#
# ## QuickStart
#
# Let's say we have a dataframe with some data we want to summarize. 
# Let's take a look at the data:
#

# %% tags=["remove-input"]
import sys
sys.path.insert(0, "../..")

# %%
import pandas as pd
from IPython.display import display, Markdown

from pysummaries import get_table_summary, get_sample_data

df = get_sample_data()
display(df)

# %% [markdown]
# Now, let's do a table one stratifying by group 
#
# We can use two backends for the html representation: a pysummaries native representation, 
# and one using the popular [great_tables](https://posit-dev.github.io/great-tables/articles/intro.html) package.
# We can control which backend to use with the parameter 'backend'. If backend is not defined, the default is 'native'.
#
# Let's start first with the PySummaries native backend:

# %%
summary_table = get_table_summary(df, strata='group', backend='native')  
display(summary_table)

# %% [markdown]
# And now, let's try the great tables backend!

# %%
summary_table = get_table_summary(df, strata='group', backend='gt')  
display(summary_table)

# %% [markdown]
# In both cases you can enhance the table with more features. For example, let's add a title and footer to the table.
# 
# Let's do first with the native backend:
# To discover what else you can do with the native backend, you can check the documentation chapter about the Native Backend.
# In that section everything is described around the function pandas_to_report_html, but you can pass any of the arguments 
# to get_table_summary.

# %%
summary_table = get_table_summary(df, strata='group', backend='native', caption="<strong>Table 1</strong>", footer="This is the footer")  
display(summary_table)

# %% [markdown]
# And now, with the great tables backend:
# To discover what else can you do with great_tables, please visit the [great_tables documentation](https://posit-dev.github.io/great-tables/articles/intro.html)

# %%
# get the GT object and then  addg features to the GT object we got back from the function
summary_table = (get_table_summary(df, strata='group', backend='gt')  
                        .tab_header(title="Table 1")
                        .tab_source_note(source_note = "This is the footer")
                        .cols_align('center')
)
display(summary_table)

# %% [markdown]
# ## More features

# ### Controlling the order of categorical variables

# In the previous examples the variable region is ordered alphabetically.
# In case we would like to order it in a specific order, we can transform the 
# variable to a categorical variable and set the order of the categories.
#
# This applies to both native and great_tables backends.

# %%
df2 = df.copy() 
df2['region'] = pd.Categorical(df2['region'], categories=['North', 'South', 'East', 'West'], ordered=True)
summary_table = get_table_summary(df2, strata='group')  
summary_table

# %% [markdown]
# ### Rounding 

# We can round the numbers to a specific number of decimals with the rounding parameter
# In this example, let's increase the number of decimals to 2.

# %%
summary_table = get_table_summary(df, strata='group', rounding=2)
summary_table

# %% [markdown]
# ### Variables and  Variable names

# If we would like to display nicer labels for our variables, we can do so
# with the argument columns_labels. If we would like to specify what columns to
# include we could use columns_include or columns_exclude.

# %%
# Let's bring nice labels for gender and age and exclude region
labels = {'gender': 'Birth gender, n (%)', 
        "age": 'Age at Index'}
# we could also specify columns_include
# column_include = ['age', 'gender']
cols_exclude = ['region']
summary_table = get_table_summary(df, strata='group', columns_exclude=cols_exclude, columns_labels=labels)  
summary_table

# %% [markdown]
# ### Changing the Overall column name

# You can change the name of the overall column with the overall_name parameter.

# %%
summary_table = get_table_summary(df, strata='group', overall_name='Total')
summary_table


# %% [markdown]
# ### Hiding the Overall column or the N counts

# You can easily discard the overall column setting the show_overall parameter to False.
# In the same fashion, you can hide the N counts setting the show_n parameter to False.

# %%
summary_table = get_table_summary(df, strata='group', show_overall=False, show_n=False)
summary_table

# %% [markdown]
# ## Changing or hiding the categorical missing level

# For categorical Functions, if there are missing values in the data, they are by default
# reported creating a new level as "Missing". You can change this value with the categorical_missing_level parameter.
# if categorical_missing_level is set to None, the missing values will not be replaced and therefore not reported.
#
# In the example below, we focus on the variable gender and change "Missing" by "Unknown".
# %%
summary_table = get_table_summary(df, strata='group', categorical_missing_level="Unknown", columns_include=['gender'])
summary_table

# %% [markdown]
# ## Summary presets
#
# There are some presets on how to summarize the categorical and numerical data. Those can be passed as a string to the
# numerical_functions or categorical_functions arguments.
#
# The current available categorical presets are: (the default is n_percent)
# * 'n_percent': N (%)'
# * 'n': N
# * 'percent': '%'
# 
# The current available numerical presets are (each value on a separate row): (the default is 'meansd_medianq1q3_minmax_missing')
# * 'meansd_medianq1q3_minmax_missing': Mean (SD) / Median [Q1 ; Q3] / Min ;  Max / Missing 
# * 'meansd_medianiqr_minmax_missing': Mean (SD) / Median [IQR] / Min ;  Max / Missing 
#
# Let's change the presets to see what happens!

# %%
summary_table = get_table_summary(df, strata='group', 
            categorical_functions= 'percent',
            numerical_functions='meansd_medianiqr_minmax_missing',
)
summary_table


# %% [markdown]
# ## Other summary functions and numerical missing values
#
# There are some built-in functions to summarize the data in different ways.
# In order to use them, you have to import them and then pass them 
# to the parameters numerical_functions or categorical_functions, which will
# operate on numerical or categorical variables respectively.
# 
# In the case of numerical_functions you should pass a dictionary, where
# the keys of the dictionary should be a 
# string with the label you would like to have for the rows, the value is the
# function to be applied. You can pass multiple key:value pairs.
#
# In the case of categorical_functions, 
# you should pass a tuple or list with two elements, the first being the function (only one is allowed)
# and the second a string or number with the value to replace NAs values for a given category level (0 in this case).
# If you pass a None as a second argument, you will get a nan printed.
#
# In the below example we change the categorical to show only the N and 
# the numerical to show only the median and IQR and the Missing values, where
# we are also changing the label for the missing values to "Unknown". You could
# not include the missing by simply not including that function.

# %%
from pysummaries import (categorical_n, categorical_n_percent, categorical_percent, 
        numerical_mean_sd, numerical_median_iqr, numerical_median_q1q3, numerical_min_max, 
        numerical_missing)

summary_table = get_table_summary(df, strata='group', 
            categorical_functions=(categorical_n, 0),
            numerical_functions={"Median [IQR]": numerical_median_iqr,
                                 "Unknown": numerical_missing}
)
summary_table

# %% [markdown]
# ## Writing your own summary functions
#
# You can create your own summary functions. In order to do so you should write
# a function that takes a pandas series and a rounding parameter and returns a
# series with numerical or string values for each level of the categorical variable
# or a single value for the numerical variable.
#
# In this example we will define a function for the categorical variables
# and one for the numerical variables. 

# %%
def mycategorical(curseries, rounding):
    """
    My own function for the categorical variables
    Let's just count the number of each category.
    """
    return curseries.value_counts()

def mynumerical(curseries, rounding):
    """
    My own function for the numerical variables
    Let's just return the mean.
    """
    return round(curseries.mean(), rounding)

summary_table = get_table_summary(df, strata='group',
                categorical_functions=(mycategorical, "0"),
                numerical_functions={"Mean": mynumerical}
        )
summary_table

# %%

