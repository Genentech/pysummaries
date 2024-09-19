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

default_styles = {"table": 'font-family: Arial, sans-serif; border-collapse: collapse; padding: 0px; margin: 0px;',
          "caption": 'padding: 0px; margin: 0px; text-align: left !important; margin-bottom: 5px;',
          "superheader": 'padding: 0.5ex 1.5ex; margin-left: 1.5ex; margin-right: 1.5ex; text-align: center !important; margin: 0px; background-color: white;',
          "header":'border-bottom: 1pt solid black; text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white;',
          "rowgrouplabel": 'padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex;font-weight: bold; text-align: left !important;  white-space: nowrap; background-color: white;',
          "rowlabel": 'padding-top: 0.5ex; padding-right:1.5ex; padding-bottom:0.5ex; text-align: left !important; white-space: nowrap; background-color: white;',
          "footnote": 'font-size: smaller; padding: 0px; margin: 0px; text-align: left !important; ',
          "value": 'text-align: center !important; padding: 0.5ex 1.5ex; margin: 0px; background-color: white; white-space: nowrap;',
    }

empty_styles = {"table": '',
          "caption": '',
          "superheader": '',
          "header":'',
          "rowgrouplabel": '',
          "rowlabel": '',
          "footnote": '',
          "value": '',
    }


def get_styles(style):
    """
    Get the dictionary representing the available internal default styles

    :param style: what style to get. empty contains just keys with empty strings as values. Useful to
        override internal styles.
    :type style: dict
    :return: dictionary with internal class name as key and a string with css styles as values.
    :rtype: dict

    :Example:

    >>> from pyreportable import get_styles  
    >>> style = get_styles('default')
    """

    if style == "default":
        return default_styles
    elif style == "empty":
        return empty_styles
    else:
        raise Exception("No recognized styles")


