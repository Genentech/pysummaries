---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

Native Backend Quickstart
============================

This section describes how to use the native backend of PySummaries to generate the html reports.
The relevant function is pandas_to_report_html. **Any of the parameters for this function can be passed
to get_table_summary to customize the appearance of the table**.

Let's say you have a dataframe "df" (you can display the code generating it).
It has multiindexes for rows and
columns. This is the way it gets displayed by default.

```{code-cell}
:tags: [hide-input]

import sys
sys.path.insert(0, "../..")

import pandas as pd

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

```

```{code-cell}
from IPython.core.display import display 

display(df)
```

Not bad ... but a bit ugly ... let's improve its appearance with PySummaries pandas_to_report_html function !!!

```{code-cell}
from pysummaries import pandas_to_report_html  

# convert the pandas dataframe to the nice html representation
# let's add a caption, foot notes and numbers for columns

caption = "Table 1: A demo table"
footers = ["A foot note", "Another foot note"]
strat_numbers = {("Specific","Alive", ""):"134",
    ("Specific", "Death", "Melanoma death"):"57",
    ("Specific", "Death", "Non-melanoma death"):"14",	
    ("", "Overall", ""):"205"}

html_table = pandas_to_report_html(df, strat_numbers=strat_numbers)

# if you are working on jupyternotebook or jupyterbook, 
# you can display the html directly
html_table

``` 

You can add custom css and more!. Explore the documentation to see more examples!
  


