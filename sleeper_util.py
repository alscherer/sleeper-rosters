#!/usr/bin/env python3
 
"""
    Utilities for inputs

    Written by: Al Scherer   2023-01-03
"""

import json
import requests
import sys

# ---------------------------------------------------------
def read_from_file(file_name):
    ''' get data from json file '''
    with open(file_name,'r') as data_file:
        data = data_file.read()
    details = json.loads(data)
    return details

# ---------------------------------------------------------
def read_from_url(url):
    print(f'Getting Data from {url}')
    response = requests.get(url)
    if response.status_code != 200:
        print(f'{response} nope')
        sys.exit(1)
    return response

