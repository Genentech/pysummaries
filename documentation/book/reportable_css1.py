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
# # Custom CSS
#
# You can control the appearance of your table passing custom CSS. There are a few ways to achieve this. 
# 
# ## Styles for values
#
# You can set css styles for values using the argument value_styles. 
# This can be either a string (in which case the style is going to be applied to all values), 
# a list of strings (or a numpy array or strings), in which case each style will be applied to
# one row, or a list of lists (or 2D numpy array of strings) in which case each style is going
# to be applied individually. 
#
# As an example let's change the background of the values to achieve a zebra effect.
#
# We will first create the dataframe we used in the basic usage last example. You can unfold
# to see the code.

# %%
# %% tags=["remove-input"]
import sys
sys.path.insert(0, "../..")

# %% tags=["hide-input"]
import pandas as pd
from IPython.core.display import display, HTML

from pysummaries import pandas_to_report_html, get_styles
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

# %% 
# And now, let's do the zebra effect
value_styles = ["background-color: lightgrey;", ""] * 4

caption = "Table 1: a nice report table with multiple indices and symbols"
footer = [dagger + " This is a foot note",  "1.  Another foot note", "2. Yet another footnote"]
table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 value_styles=value_styles)
table

# %% [markdown]
# Now, let's say we would like to highlight only a couple of values. In this case
# we need a 2D data structure to represent all values in our table, and we change
# the styles only for those that we are interested in.

# %%
highlight = "background-color: yellow;"
value_styles = [[""] * 4 for x in range(8)]
# let's highlight the element in the first row fourth column, 
value_styles[0][3] = highlight
# and in the third row, second 
value_styles[2][1] = highlight

caption = "Table 1: a nice report table with multiple indices and symbols"
footer = [dagger + " This is a foot note",  "1.  Another foot note", "2. Yet another footnote"]
table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 value_styles=value_styles)
table

# %% [markdown]
# ## Styles for other elements with customstyles
#
# You can change the styles of other elements on the table as a block using the 
# argument customstyles. This must be a dictionary where they keys are the elements
# and the values are the styles. 
#
# You can check what are the keys and the default styles with the function get_styles, 
# using 'default' as argument.

# %%
default_styles = get_styles('default')

for k, v in default_styles.items():
    print(k, ":", v)

# %% [markdown]
# As an example, let's change the font color and size of the caption, you can achieve this by 
# passing your own customstyles dictionary

# %%
customstyles = {'caption': 'color: blue; font-size: larger;'}

table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 customstyles=customstyles)
table

# %% [markdown]
# Your customstyles will be appended to the existing default styles. Since the last css property
# is the one that takes precedence, you can effectively override any style. 
# However, if needed, you can pass the argument styles='empty' to completely get rid of
# any default styles (except a few that have to do with borders and indentation).
# Here we see some strange formatting because JupyterBook has a default formatting that now is showing_up
# once we get rid of our own formatting.

# %%
table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 styles='empty')
table

# %% [markdown]
# ## Map of custom classes
# Here we show a map of the custom classes you have on the precedent table.
# The class of the table itself is "table"

# %% tags=["remove-input"]
customtable = """
    <table class="Pytable1" style="font-family: Arial, sans-serif; border-collapse: collapse; padding: 0px; margin: 0px;" id="">

        <caption class="caption" colspan="6" style="padding: 0px; margin: 0px; text-align: left !important; margin-bottom: 5px;" id="_caption">caption</caption>

        <thead>

            <tr>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_0">superheader</th>

                <th class="superheader level_0" colspan="3" style="border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_1">superheader</th>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_2">superheader</th>

            </tr>

            <tr>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_0">superheader</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_1">superheader</th>

                <th class="superheader level_1" colspan="2" style="border-bottom: 1pt solid black;border-bottom: 1pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_2">superheader</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_3">superheader</th>

            </tr>

            <tr>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_0">
                    <span class="headerlabel"> header</span>
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_1">
                    <span class="headerlabel">header
                    <br>
                    <span class="headern"></span>

                    </span>
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_2">
                    <span class="headerlabel"> header
                    <br>
                    <span class="headern"></span>
                    </span>
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_3">
                    <span class="headerlabel">header
                    <br>
                    <span class="headern"></span>
                    </span>
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_4">
                    <span class="headerlabel">header
                    <br>
                    <span class="headern"></span>
                    </span>
                </th>

            </tr>
        </thead>
        <tbody>


            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_0_0">rowgrouplabel</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_0">rowgrouplabel</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_0">rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_3">rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_1">rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_3">rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_1">rowgrouplabel</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_2">rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_3">rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_3">rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_3">rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_0_1">rowgrouplabel</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_2">rowgrouplabel</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_4">rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_3">rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_5">rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_3">rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_3">rowgrouplabel</td>
            </tr>
            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_6">rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_0">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_1">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_2">rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_3">rowvalue</td>
            </tr>

            <tr>

              <td class="rowlabel" style="border-bottom: 2pt solid black;padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_7">rowlabel</td>


              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_0">rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_1">rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_2">rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_3">rowvalue</td>

            </tr>

        <tbody>

        <tfoot>
            <tr>
              <td class="footnote" colspan="6" style="font-size: smaller; padding: 0px; margin: 0px; text-align: left !important; " id="_footnote">
              footnote
            </tr>
        </tfoot>

    </table>
"""
display(HTML(customtable))
