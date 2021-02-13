'''
Contains general tility functions

Functions
-------
- save_json(data, filename) : saves data (dict) to a json file
'''

import os
import json

### GENERAL UTILITY FUNCTIONS
def save_json(data, filename):
    '''
    Saves data to a json file.

    Parameters:
        data (dict): data to save to json file
        filename (string): filename to save json file as (saves to current dir by default)

    Returns:
        path (string): absolute path to json file
    '''

    # TODO: use path_out instead of filename instead?

    # checks if file already has json extension
    if ".json" not in filename:
        filename = "{}.json".format(filename)

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4, sort_keys=True)

    return os.path.abspath(filename)
