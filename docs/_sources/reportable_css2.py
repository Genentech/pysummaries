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
# # Advanced custom CSS
# You can pass your custom raw css to fine control the appearance of your tables. 
# You can take advantage of css classes and ids in order to achieve this. 

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


# %% [markdown]
# ## CSS classes
#
# Every element of the table has a class, and an id. Using these you can write
# your own css to achieve full control over the appearance of your table. You can
# use the argument customcss that is a string with your css to achieve this.
#
# For example let's change the background color of the sections. Notice
# the !important in the css, so that it overrides the default white background
# of the element. Let's also set the font color of column labels to blue and
# the N labels to red.
#
# This advantage (or disadvantage depending on what you need) of this approach is that the 
# style will propagate to all tables in the document. Therefore you will see this style automatically
# applied to all tables in this document.
#
# You can even include this piece of css in a file to be linked to all your html files
# (jupyterbook allows this by putting this file in the _static folder on your book)

# %%

customcss = """
td.rowgrouplabel.level_0 {
    background-color: lightgrey !important;
}

span.headerlabel {
    color: blue;
}

span.headern {
    color: red;
}
"""

table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 customcss=customcss)
table

# %% [markdown]
# ## CSS classes map
# Here you have a map of the classes you can use in your css. The table itself has the class Pytable1. You 
# can set all classes as children of this to achieve more specificity. Observe that multi-index column and row
# labels have a level second class starting with 0. Observe also that column headers are in the class th.header which
# contains two separate spans, one for the column name and one for the column N, so that you can control them
# togheter (with th.header) separately (with span.headerlabel and span.headern)

# %% tags=["remove-input"]
customtable = """
    <table class="Pytable1" style="font-family: Arial, sans-serif; border-collapse: collapse; padding: 0px; margin: 0px;" id="">

        <caption class="caption" colspan="6" style="padding: 0px; margin: 0px; text-align: left !important; margin-bottom: 5px;" id="_caption">caption</caption>

        <thead>

            <tr>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_0">th.superheader.level_0</th>

                <th class="superheader level_0" colspan="3" style="border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_1">th.superheader.level_0</th>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_0_2">th.superheader.level_0</th>

            </tr>

            <tr>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_0">th.superheader.level_1</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_1">th.superheader.level_1</th>

                <th class="superheader level_1" colspan="2" style="border-bottom: 1pt solid black;border-bottom: 1pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_2">th.superheader.level_1</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_01_superheader_level_1_3">th.superheader.level_1</th>

            </tr>

            <tr>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_0">th.header
                    <br>span.headerlabel
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_1">th.header
                     <br>span.headerlabel
                    <br>span.headern
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_2">th.header
                    <br> span.headerlabel
                    <br> span.headern
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_3">th.header
                    <br> span.headerlabel
                    <br> span.headern
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_01_header_4">th.header
                    <br> span.headerlabel
                    <br> span.headern
                </th>

            </tr>
        </thead>
        <tbody>

            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_0_0">td.rowgrouplabel.level_0</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_0">td.rowgrouplabel.level_1</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_0">td.rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_0_col_3">td.rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_1">td.rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_1_col_3">td.rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_1">td.rowgrouplabel.level_1</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_2">td.rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_2_col_3">td.rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_3">td.rowlabel</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_3_col_3">td.rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_0_1">td.rowgrouplabel.level_0</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_2">td.rowgrouplabel.level_1</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_4">td.rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_4_col_3">td.rowvalue</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_5">td.rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_5_col_3">td.rowvalue</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_01_rowgrouplabel_level_1_3">td.rowgrouplabel.level_1</td>
            </tr>
            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_6">td.rowlabel</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_0">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_1">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_2">td.rowvalue</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_6_col_3">td.rowvalue</td>
            </tr>

            <tr>

              <td class="rowlabel" style="border-bottom: 2pt solid black;padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_01_rowlabel_7">td.rowlabel</td>


              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_0">td.rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_1">td.rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_2">td.rowvalue</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_01_value_row_7_col_3">td.rowvalue</td>

            </tr>

        <tbody>

        <tfoot>
            <tr>
              <td class="footnote" colspan="6" style="font-size: smaller; padding: 0px; margin: 0px; text-align: left !important; " id="_footnote">
              td.footnote
            </tr>
        </tfoot>

    </table>
"""
display(HTML(customtable))

# %% [markdown]
# ## CSS ids
# As mentioned before, each element has an unique id. You can target these to gain 
# control over every single element in the table when writing your css. Ids are a combination
# of the table id (random has), the classes, the levels and a number ordering them.
# For values, we number them by row and then column
#
# In this circupstances, you can pass the argument table_id so that the id is known to you
# instead of it being a random hash.
#
# With this approach changes will apply only to the particular table you are trying to manipulate
# and not to other tables in the document.
#
# As an example, let's change the background color of "Dead", something you could
# not achieve using classes alone.
# 

# %%
table_id = "mytable1"
customcss = f"""
#{table_id}_superheader_level_1_2 {{
    background-color: lightgrey !important;
}}
"""

table = pandas_to_report_html(df, strat_numbers=strat_numbers, 
                                                 caption=caption, footer=footer, 
                                                 customcss=customcss, 
                                                 table_id=table_id)
table

# %% [markdown]
# ## CSS Ids map
# Here you have a map of the ids you can use in your css. The table itself has the as id either a random hash.
# or the id you set with table_id. We will call it id here. For all elements the id is the concatenation of
# the table id, with the class with the order of appearance.

# %% tags=["remove-input"]
customtable = """
    <table class="Pytable1" style="font-family: Arial, sans-serif; border-collapse: collapse; padding: 0px; margin: 0px;" id="">

        <caption class="caption" colspan="6" style="padding: 0px; margin: 0px; text-align: left !important; margin-bottom: 5px;" id="_caption">id_caption</caption>

        <thead>

            <tr>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_0_0">id_superheader_level_0_0</th>

                <th class="superheader level_0" colspan="3" style="border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;border-bottom: 1pt solid black;border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_0_1">id_superheader_level_0_1</th>

                <th class="superheader level_0" colspan="1" style="border-top: 2pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_0_2">id_superheader_level_0_2</th>

            </tr>

            <tr>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_1_0">id_superheader_level_1_0</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_1_1">id_superheader_level_1_1</th>

                <th class="superheader level_1" colspan="2" style="border-bottom: 1pt solid black;border-bottom: 1pt solid black;padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_1_2">id_superheader_level_1_2</th>

                <th class="superheader level_1" colspan="1" style="padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;" id="custompyt_02_superheader_level_1_3">id_superheader_level_1_3</th>

            </tr>

            <tr>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_02_header_0">id_header_0
                    <br>id_headerlabel_0
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_02_header_1">id_header_1
                    <br>id_headerlabel_1
                    <br>id_headern_1
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_02_header_2">id_header_2
                    <br>id_headerlabel_2
                    <br>id_headern_2
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_02_header_3">id_header_3
                    <br>id_headerlabel_3
                    <br>id_headern_3
                </th>

                <th class="header" style="border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;" id="custompyt_02_header_4">id_header_4
                    <br>id_headerlabel_4
                    <br>id_headern_4
                </th>

            </tr>
        </thead>
        <tbody>

            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_0_0">id_rowgrouplabel_level_0_0</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_1_0">id_rowgrouplabel_level_1_0</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_0">id_rowlabel_0</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_0_col_0">id_rowvalue_row_0_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_0_col_1">id_rowvalue_row_0_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_0_col_2">id_rowvalue_row_0_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_0_col_3">id_rowvalue_row_0_col_3</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_1">id_rowlabel_1</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_1_col_0">id_rowvalue_row_1_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_1_col_1">id_rowvalue_row_1_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_1_col_2">id_rowvalue_row_1_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_1_col_3">id_rowvalue_row_1_col_3</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_1_1">id_rowgrouplabel_level_1_1</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_2">id_rowlabel_3</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_2_col_0">id_rowvalue_row_2_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_2_col_1">id_rowvalue_row_2_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_2_col_2">id_rowvalue_row_2_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_2_col_3">id_rowvalue_row_2_col_3</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_3">id_rowlabel_3</td>


              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_3_col_0">id_rowvalue_row_3_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_3_col_1">id_rowvalue_row_3_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_3_col_2">id_rowvalue_row_3_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_3_col_3">id_rowvalue_row_3_col_3</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_0" class="varlabel" colspan="6" style="padding-left: 0.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_0_1">id_rowgrouplabel_level_0_1</td>
            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_1_2">id_rowgrouplabel_level_1_2</td>
            </tr>


            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_4">id_rowlabel_4</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_4_col_0">id_rowvalue_row_4_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_4_col_1">id_rowvalue_row_4_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_4_col_2">id_rowvalue_row_4_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_4_col_3">id_rowvalue_row_4_col_3</td>

            </tr>

            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_5">id_rowlabel_5</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_5_col_0">id_rowvalue_row_5_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_5_col_1">id_rowvalue_row_5_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_5_col_2">id_rowvalue_row_5_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_5_col_3">id_rowvalue_row_5_col_3</td>

            </tr>

            <tr>
              <td class="rowgrouplabel level_1" class="varlabel" colspan="6" style="padding-left: 2.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;" id="custompyt_02_rowgrouplabel_level_1_3">id_rowgrouplabel_level_1_3</td>
            </tr>
            <tr>

              <td class="rowlabel" style="padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_6">id_rowlabel_6</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_6_col_0">id_rowvalue_row_6_col_0</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_6_col_1">id_rowvalue_row_6_col_1</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_6_col_2">id_rowvalue_row_6_col_2</td>

              <td class="rowvalue" style="text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_6_col_3">id_rowvalue_row_6_col_3</td>
            </tr>

            <tr>

              <td class="rowlabel" style="border-bottom: 2pt solid black;padding-left: 4.5ex;padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;" id="custompyt_02_rowlabel_7">id_rowlabel_7</td>


              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_7_col_0">id_rowvalue_row_7_col_0</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_7_col_1">id_rowvalue_row_7_col_1</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_7_col_2">id_rowvalue_row_7_col_2</td>

              <td class="rowvalue" style="border-bottom: 2pt solid black;text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;" id="custompyt_02_value_row_7_col_3">id_rowvalue_row_7_col_3</td>

            </tr>

        <tbody>

        <tfoot>
            <tr>
              <td class="footnote" colspan="6" style="font-size: smaller; padding: 0px; margin: 0px; text-align: left !important; " id="_footnote">
               id_footnote
            </tr>
        </tfoot>

    </table>
"""
display(HTML(customtable))

