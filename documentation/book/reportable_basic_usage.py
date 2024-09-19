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
# # Native Backend basic usage
#
# ## A simple dataframe
#
# Let's start with a simple pandas  dataframe you have obtained by summarizing
# some data. Here for simplicity we are going to enter the data manually rather than
# summarizing it. 
# 
#  Using the function 
# pandas_to_report_html we can convert it to a nice html table.
#

# %% tags=["remove-input"]
import sys
sys.path.insert(0, "../..")

# %%
import pandas as pd
from IPython.core.display import display

from pysummaries import pandas_to_report_html

# create the dataframe
nums = [["Male", "91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["Female", "43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"]]
cols = ['Gender', 'Alive', 'Melanoma death', 'Non-melanoma death', 'Overall' ]
df = pd.DataFrame(nums, columns=cols)

# transform the dataframe to a nice html table
table = pandas_to_report_html(df)

# show the report table
table

# %% [markdown]
# ## Hiding the row index
# As you can see however, the row indexes of the data frame are displayed. If this is not what
# you would like to have, there are two options.
# The first one is to hide the indexes with the parameter show_index=False.
# It looks much nicer now!

# %%
table = pandas_to_report_html(df, show_index=False)
table

# %% [markdown]
# ## Taking advantage of row indexes
# A second alternative is to set the categorical column as row index. 
# For this particular example it may not be the best option because the word
# Gender is hidden, but this approach will let us build on more powerful 
# visualizations later.

# %%
df2 = df.set_index('Gender')
table = pandas_to_report_html(df2)
table

# %% [markdown]
# ## Setting Numbers of cases for columns
# Now that we set the row index, we can set the number of cases per columns to be
# displayed below the column names. We achieve this using the argument
# strat_numbers, which is a dictionary where they keys are the column names and 
# the values are the number of cases

# %%
strat_numbers = {"Alive" :"134",
     "Melanoma death": "57",
    "Non-melanoma death": "14",	
     "Overall": "205"}

table = pandas_to_report_html(df2, strat_numbers=strat_numbers)
table

# %% [markdown]
# ## Multiple Row indices
# What if we would like to show statistics breaken not only by gender, but also by age?
# In such case we can use a pandas Multindex to set the different levels. 
#
# There are many ways to create multi-indices in pandas. Here we create them from
# exististing columns, but there are other ways (for example pd.Multiindex.from_tuples
# or pd.Multiindex.from_product). You can learn more about 
# pandas multi-indices [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html)

# %%
# build the dataframe
nums = [["Gender","Male","91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["Gender", "Female", "43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["Age", "Mean (SD)", "50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["Age", "Median [mix max]", "52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"]]
cols = ["Category1", 'Category2', 'Alive', 'Melanoma death', 'Non-melanoma death', 'Overall' ]
df = pd.DataFrame(nums, columns=cols)
# set the multiindex
df = df.set_index(['Category1', "Category2"])
# strat numbers
strat_numbers = {"Alive" :"134",
     "Melanoma death": "57",
    "Non-melanoma death": "14",	
     "Overall": "205"}
# beautify and show
table = pandas_to_report_html(df, strat_numbers=strat_numbers)
table

# %% [markdown]
# What if you need even more levels on rows? No problem! You can set an arbitrary number
# of index leves. Here for the sake of the example, let's duplicate the data into section
# 1 and 2

# %%
nums = [["Section 1", "Gender","Male","91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["Section 1", "Gender", "Female", "43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["Section 1", "Age", "Mean (SD)", "50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["Section 1", "Age", "Median [mix max]", "52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"],
["Section 2", "Gender","Male","91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["Section 2", "Gender", "Female", "43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["Section 2", "Age", "Mean (SD)", "50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["Section 2", "Age", "Median [mix max]", "52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"]]

cols = ["Section", "Category1", 'Category2', 'Alive', 'Melanoma death', 'Non-melanoma death', 'Overall' ]
df = pd.DataFrame(nums, columns=cols)
# set the multiindex
df = df.set_index(["Section", 'Category1', "Category2"])
# strat numbers
strat_numbers = {"Alive" :"134",
     "Melanoma death": "57",
    "Non-melanoma death": "14",	
     "Overall": "205"}
# beautify and show
table = pandas_to_report_html(df, strat_numbers=strat_numbers)
table

# %% [markdown]
# ## Multiple Column indices
# In the same way as we set multiple levels for rows, we can use multiple leves for columns
# by setting the columns as a multi-index.
#
# Here we set the columns and row multi-index manually from tuples, but there are other ways (for example pd.Multiindex.from_arrays
# or pd.Multiindex.from_product). You can learn more about 
# pandas multi-indices [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html)
#
# Notice that strat_numbers keys has to change to reflect the new column multi-indices

# %%
nums = [["91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"],
["91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"]]

cols = [("Specific","Alive", ""),
("Specific","Death", "Melanoma death"),
("Specific","Death", "Non-melanoma death"),	
("","Overall", "")]


rows = [("Section 1", "Gender", "Male"), ("Section 1", "Gender", "Female"),
    ("Section 1", "Age", "Mean (SD)"), ("Section 1", "Age", "Median [min max]"),
    ("Section 2", "Gender", "Male"), ("Section 2", "Gender", "Female"),
    ("Section 2", "Age", "Mean (SD)"), ("Section 2", "Age", "Median [min max]")]

df = pd.DataFrame(nums, columns=pd.MultiIndex.from_tuples(cols), index=pd.MultiIndex.from_tuples(rows))

# notice that now strat numbers must make reference to all the hierarchy of multi-indices
strat_numbers = {("Specific","Alive", ""):"134",
    ("Specific", "Death", "Melanoma death"):"57",
    ("Specific", "Death", "Non-melanoma death"):"14",	
    ("", "Overall", ""):"205"}

# beautify and show
table = pandas_to_report_html(df, strat_numbers=strat_numbers)
table

# %% [markdown]
# ## Table captions and foot notes
#
# Adding table captions and foot notes is easy. Just use the arguments caption 
# and footer. The later can be either a string or a list of strings to set several foot notes.

# %%

 # %%
 # let's use the last dataframe
caption = "Table 1: a nice report table with multiple indices, caption and foot notes"
footer = ["This is a foot note", "Another foot note"]
table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer)
table

# %% [markdown]
# If you would like to use special symbols, you just have to add them as strings using html
# codes or html tags such as <sup> or <sub> for superscript and subscripts respectively. Notice however that if you use them in columns, you also need to change the 
# strat_numbers to match the columns with symbols.

# %%
# a couple of symbols with html codes or html tags
dagger = "&#8224;"
sup = "<sup>1</sup>"
sub = "<sub>2</sub>"

nums = [["91 (67.9%) " + sup, "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["52.0 [4.00, 84.0] " + sub, "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"],
["91 (67.9%)", "28 (49.1%)", "7 (50.0%)", "126 (61.5%)"],
["43 (32.1%)", "29 (50.9%)",	"7 (50.0%)", "79 (38.5%)"],
["50.0 (15.9)", "55.1 (17.9)", "65.3 (10.9)", "52.5 (16.7)"],
["52.0 [4.00, 84.0]", "56.0 [14.0, 95.0]", "65.0 [49.0, 86.0]", "54.0 [4.00, 95.0]"]]

cols = [("Specific","Alive " + dagger, ""),
("Specific","Death", "Melanoma death"),
("Specific","Death", "Non-melanoma death"),	
("","Overall", "")]


rows = [("Section 1", "Gender", "Male"), ("Section 1", "Gender", "Female"),
    ("Section 1", "Age", "Mean (SD)"), ("Section 1", "Age", "Median [min max]"),
    ("Section 2", "Gender", "Male"), ("Section 2", "Gender", "Female"),
    ("Section 2", "Age", "Mean (SD)"), ("Section 2", "Age", "Median [min max]")]

df = pd.DataFrame(nums, columns=pd.MultiIndex.from_tuples(cols), index=pd.MultiIndex.from_tuples(rows))

# notice that now strat numbers must make reference to all the hierarchy of multi-indices
strat_numbers = {("Specific","Alive " + dagger, ""):"134",
    ("Specific", "Death", "Melanoma death"):"57",
    ("Specific", "Death", "Non-melanoma death"):"14",	
    ("", "Overall", ""):"205"}

# beautify and show
caption = "Table 1: a nice report table with multiple indices and symbols"
footer = [dagger + " This is a foot note",  "1.  Another foot note", "2. Yet another footnote"]
table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer)
table
# %%
