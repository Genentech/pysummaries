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
import pandas as pd

from .html_elements import TabSuperHeader, TabHeader, RowGroupLabel, RowLabel, RowValue, Block, Row


def extract_multiheader(cols, strat_numbers, styles, tabid, show_index=True):
    """
    Gets the dataframe columns and transforms to superheaders (most external columns in a multi-index),
    tabheaders (most internal column names) and numcols (number of columns/tabheaders)
    when the dataframe columns are a multi-index object

    :param cols: pandas dataframe column multi-index object
    :param strat_numbers: dict with index as key and int as value, to put the N= in the column header
    :param styles: dict with default css styles
    :param show_index: if True that means the user wants to show the row index and we need to insert here a placeholder in the first
           column
    :return: superheaders, tabheaders
    """
    default_superheader_style = styles.get("superheader")
    default_header_style = styles.get("header")
    superheaders = [list() for x in range(cols.nlevels-1)]
    tabheaders = []
    lastsuphead = [None] * (cols.nlevels-1)
    tabcnt = 0
    for colindx, idx in enumerate(cols):
        *suphead_titles, head_title = idx
        # last (more internal) header
        if colindx == 0 and show_index:
            tabheader = TabHeader("", tabid, tabcnt, style=default_header_style)
            tabheaders.append(tabheader)
            tabcnt +=1
        tabheader = TabHeader(head_title, tabid, tabcnt, n=strat_numbers.get(idx), style=default_header_style)
        tabheaders.append(tabheader)
        tabcnt +=1
        # outer headers
        for sh_idx, suphead_title in enumerate(suphead_titles):
            top = True if sh_idx==0 else False
            if superheaders[sh_idx]:
                supcnt = superheaders[sh_idx][-1].idnum + 1
            else:
                supcnt = 0
            # empty for first column
            if colindx == 0:
                tabsuperheader = TabSuperHeader("", tabid, sh_idx, supcnt, style=default_superheader_style, top=top)
                superheaders[sh_idx].append(tabsuperheader)
                supcnt += 1
            if suphead_title != lastsuphead[sh_idx]:
                tabsuperheader = TabSuperHeader(suphead_title, tabid, sh_idx, supcnt, style=default_superheader_style, top=top)
                superheaders[sh_idx].append(tabsuperheader)
                lastsuphead[sh_idx] = suphead_title
            else:
                superheaders[sh_idx][-1].span +=1
        for row in superheaders:
            for elem in row:
                elem.consolidate_styles()
    return superheaders, tabheaders

def extract_simpleheader(cols, strat_numbers, styles, tabid, show_index=True):
    """
    Gets the dataframe columns and transforms to superheaders (empty in this case),
    tabheaders (column names) and numcols (number of columns/tabheaders)
    when cols is not a multi-index

    :param cols: pandas dataframe columns index object
    :param strat_numbers: dict with index as key and int as value, to put the N= in the column header
    :param styles: dict with default css styles
    :param show_index: if True that means the user wants to show the row index and we need to insert here a placeholder in the first
           column
    :return: superheaders, tabheaders
    """
    default_header_style = styles.get("header")
    superheaders = []
    tabheaders = list()
    tabcnt = 0 
    if show_index:
        curtab = TabHeader("", tabid, tabcnt, style=default_header_style, top=True)
        tabheaders.append(curtab)
        tabcnt += 1
    for indx, coltitle in enumerate(cols):
        curtab = TabHeader(coltitle, tabid, tabcnt, n=strat_numbers.get(coltitle), style=default_header_style, top=True)
        tabheaders.append(curtab)
        tabcnt += 1
    return superheaders, tabheaders

def extract_headers(df, strat_numbers, styles, tabid, show_index=True): 
    """
    Gets the dataframe columns and transforms to superheaders (most external columns in a multi-index, empty if simple index),
    tabheaders (most internal column names) and numcols (number of columns/tabheaders)

    :param df: pandas dataframe
    :param strat_numbers: dict with index as key and int as value, to put the N= in the column header
    :param styles: dict with default css styles
    :param show_index: if True that means the user wants to show the row index and we need to insert here a placeholder in the first
           column
    :return: superheaders, tabheaders, numcols
    """
    cols = df.columns
    if type(cols) == pd.MultiIndex:
        superheaders, tabheaders = extract_multiheader(cols, strat_numbers, styles, tabid, show_index=show_index)
    else:
        superheaders, tabheaders = extract_simpleheader(cols, strat_numbers, styles, tabid, show_index=show_index)

    numcols = len(tabheaders)+1
    return superheaders, tabheaders, numcols

def add_row(currows, currow_label, row_padding, row_style, default_valuestyle, value_styles, cnt, rowseries, tabid, last_row=False, show_index=True):
    """
    Add a Row object to a currows list of Rows. Each Row has a label (most inner row index in the pandas dataframe)
    and a list of Values objects. It does not return anything but adds the Row to currows in place.

    :param currows: list of rows where to add The Row.
    :param currow_label: str with the label for the Row object
    :param row_padding: int with the left padding for the Row label
    :param row_style: str with css style for the row label
    :param default_valuestyle: str with css default style for Values
    :param value_sytles: list of lists with css strings with styles for values to be added to the default
    :param cnt: int, number of row
    :param rowseries: list with the numerical or string values for the row
    :param tabid: str with the table id
    :param last_row: if True a style for a bottom border will be added
    :param show_index: if True the row index will be shown
    """

    if show_index:
        rowlabelobj = RowLabel(currow_label, row_padding, tabid, cnt, last_row=last_row, style=row_style)
        rowlabelobj.consolidate_style()
    else:
        rowlabelobj = None
    currowvalues_style = [default_valuestyle for x in range(len(rowseries))]
    if  value_styles:
        currowvalues_style =  [ x+y if y else x for x,y in zip(currowvalues_style, value_styles[cnt-1])]
    rowvalues = [RowValue(x, tabid, cnt, colidx, last_row=last_row, style=s) for colidx,(x,s) in enumerate(zip(rowseries.tolist(), currowvalues_style))]
    _ = [x.consolidate_style() for x in rowvalues]
    currow = Row(rowlabelobj, rowvalues)
    currows.append(currow)

def extract_multibodyblocks(indexes, df, value_styles, styles, tabid):
    """
    Extract blocks when there are row multi-indexes. Each block
    consist of a list of titles (the most external indexes), and
    a Row object, which has a title (most internal index) and values for that row.

    :param indexes: dataframe row indexes
    :param df: pandas dataframe
    :param value_styles: list of lists with styles for values
    :param tabid: str with id for table
    :return: list of blocks for the body.
    """
    default_valuestyle = styles.get("value")
    default_rowlabelstyle = styles.get("rowlabel")
    bodyblocks = list()
    lastblock_index = None
    prevlastblock_index = None
    curblock = Block()
    currows = list()
    cnt = 1
    leftpadding = 0.5
    left_paddings = list()
    for x in range(indexes.nlevels):
        left_paddings.append(leftpadding)
        leftpadding += 2
    *labels_paddings, row_padding = left_paddings
    rowgroup_cnts = [0] * (indexes.nlevels-1)
    for rowlabel, rowseries in df.iterrows():
        #row labels
        *rowgroup_labels, currow_label = rowlabel
        if (rowgroup_labels != lastblock_index and lastblock_index is not None) or cnt==len(df):
            rowgroupstyle = styles.get("rowgrouplabel")
            titles = [RowGroupLabel(x, tabid, level, y, rowgroup_cnts, style=rowgroupstyle) for level,(x,y) in enumerate(zip(lastblock_index, labels_paddings))]
            # prune 
            if prevlastblock_index is not None:
                indxestopop = list()
                for curindx, (prev_title, cur_title) in enumerate(zip(prevlastblock_index, lastblock_index)):
                    if prev_title == cur_title:
                        indxestopop.append(curindx)
                    else:
                        break
                indxestopop.reverse()
                for x in indxestopop:
                    titles.pop(x)
            # consolidate now that we pruned
            for tit in titles:
                tit.consolidate_style()

            curblock.titles = titles
            if cnt == len(df):
                # add values if we are handling the last row
                add_row(currows, currow_label, row_padding, default_rowlabelstyle, default_valuestyle, value_styles, cnt-1, rowseries, tabid, last_row=True)
            curblock.rows = currows
            bodyblocks.append(curblock)
            curblock = Block()
            currows = list()
            prevlastblock_index = lastblock_index
        lastblock_index = rowgroup_labels
        # values
        add_row(currows, currow_label, row_padding, default_rowlabelstyle, default_valuestyle, value_styles, cnt-1, rowseries, tabid, last_row=False)
        cnt +=1 
    return bodyblocks

def extract_simplebodyblocks(indexes, df, value_styles, styles, tabid, show_index=True):
    """
    Extract blocks when there is a simple index (not multi-index). The object returned
    has only one block consisting of 
    Row objects, each having a title (most internal index) and values for that row.

    :param indexes: dataframe row indexes
    :param df: pandas dataframe
    :param value_styles: list of lists with styles for values
    :param tabid: str with id for table
    :param show_index: wether to show the index
    :return: list of blocks for the body.
    """
    default_valuestyle = styles.get("value")
    default_rowlabelstyle = styles.get("rowlabel")
    curblock = Block()
    curblock.titles = list()
    currows = list()
    row_padding = 0.5
    cnt = 1
    last_row = False
    for rowlabel, rowseries in df.iterrows():
        if cnt == len(df):
            last_row = True
        add_row(currows, rowlabel, row_padding, default_rowlabelstyle, default_valuestyle, value_styles, cnt-1, rowseries, tabid, last_row=last_row, show_index=show_index)
        cnt += 1
    curblock.rows = currows
    bodyblocks = [curblock]
    return bodyblocks


def extract_bodyblocks(df, value_styles, styles, tabid, show_index=True):
    """
    Extract blocks from the dataframe. The object returned is a list of blocks, 
    one block consisting of a list of titles (most external row indexes) and a Row 
    Row object, each having a title (most internal index) and values for that row.

    :param df: pandas dataframe
    :param value_styles: list of lists with styles for values
    :param tabid: str with id for table
    :param show_index: wether to show the index. This is effective only if the dataframe has a simple
           (non-multiindex) index
    :return: list of blocks for the body.
    """
    # body
    indexes = df.index

    if type(indexes) == pd.MultiIndex and show_index:
        bodyblocks = extract_multibodyblocks(indexes, df, value_styles, styles, tabid)
    else:
        bodyblocks = extract_simplebodyblocks(indexes, df, value_styles, styles, tabid, show_index=show_index)

    return bodyblocks


def df_to_intermediate_rep(df, tabid, strat_numbers=None, value_styles=None, styles=None, show_index=True):
    """
    Transform a pandas dataframe to an intermediate representation consisting of superheaders (list of most external
    column indexes if multi-index else empty list), tabheaders (list of most internal column indexes), numcols
    (number of columns), and bodyblocks (object with a list of labels (most external row indexes) and a Row
    object consisting of a row label (most internal row index) and values)

    :param df: pandas dataframe
    :param tabid: str with the id for the table
    :param strat_numbers: dict with keys being column index and value numbers to insert in the header as N=xx
    :param value_styles: list of lists with css style for values
    :param styles: dict with default styles
    :param show_index: if True the row index must be shown, makes sense only if row index is not multi-index
    :return: superheaers, tabheaders, numcols, bodyblocks
    """

    superheaders, tabheaders, numcols = extract_headers(df, strat_numbers, styles, tabid, show_index=show_index)
    bodyblocks = extract_bodyblocks(df, value_styles, styles, tabid, show_index=show_index)
    return superheaders, tabheaders, numcols, bodyblocks

