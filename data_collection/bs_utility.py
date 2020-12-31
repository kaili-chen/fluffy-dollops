'''
Contains ugeneral tility functions

Functions
-------
'''

import sys
import requests
from bs4 import BeautifulSoup
import os
import json

def get_soup(url):
    '''
    Returns a BeautifulSoup object of the HTML contents of a provided url.

    Parameters:
        url (string): url of the site to generate soup object of

    Returns:
        soup (bs4.BeautifulSoup):
    '''
    webpage = requests.get(url)
    # print("{}\n\t{}".format(url, webpage))
    if webpage.status_code != 200:
        # print('webpage status code = {}, exiting'.format(webpage.status_code))
        # sys.exit()
        raise Bs4Error("{}: status code = {}, exiting get_soup function".format(url, webpage.status_code))

    soup = BeautifulSoup(webpage.text, "html.parser")
    if soup is None or soup == "":
        # print("no soup, exiting")
        # sys.exit()
        raise Bs4Error("{}: no soup, exiting get_soup function".format(url, webpage.status_code))
    return soup

def remove_children(element):
    '''
    Removes children elements from a bs4.element.Tag (changes the input element).

    Inputs:
        element (bs4.element.Tag)

    '''
    # print("input = {}".format(element))
    for child in element.children:
        try:
            child.decompose()
            # print("\tdecom = {}".format(element))
        except AttributeError:
            continue
        # print()
    return element
