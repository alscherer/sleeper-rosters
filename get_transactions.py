#!/usr/bin/env python3
 
"""
    Download & parse all weekly transactions from 
         https://api.sleeper.app/v1/league/650130288072040448/transactions/<week #>
    & save to a json file.
    That league # is my "Flex" league 2021.


    todo:  Just have this app pull in the transactions into a file.
    todo:  Have a separate app that brings in all the transactions, draft, rosters & owners

    Written by: Al Scherer   2022-01-15
"""

import argparse
import json
import requests
import time
import datetime
import sys


# ---------------------------------------------------------
PLAYER_FILE = "data/parsed-players.json"
# URL = "http://api.sleeper.app/v1/league/787796366440124416/transactions/"  # add week # to end - 2022
# URL = "http://api.sleeper.app/v1/league/919353924837056512/transactions/"  # add week # to end
URL = "https://api.sleeper.app/v1/league/1051604880055566336/transactions/"

DRAFT = 'data/2024/parsed_draft.json'
DRAFT_DATE = 'Aug 28, 2023'

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='get-transactions <json player file>',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename (default: )',
                        metavar='outfile',
                        type=str,
                        default='')

    parser.add_argument('-v',
                        '--verbose',
                        help='Be chatty',
                        action='store_true')

    args = parser.parse_args()

    return args

# ---------------------------------------------------------
def get_data(file_name):
    ''' get data from json file '''
    with open(file_name,'r') as data_file:
        data = data_file.read()

    details = json.loads(data)
    return details

# ---------------------------------------------------------
def is_a_waiver_claim(item):
    ''' Figure out if this is a waiver claim '''
    return item["adds"] is not None \
               and item["status"] == "complete" \
               and item['type'] == 'waiver'



# ---------------------------------------------------------
def get_waiver_data(item):
    ''' Extract the trans data I want '''
    trans = {}
    trans['player_id']=list(item['adds'].keys())[0]
    trans['type']=item['type']
    trans['roster_id']=item['roster_ids'][0]
    trans['price']=item['settings']['waiver_bid']
    trans['date']=time.strftime('%b %d, %Y', time.localtime(item['created']/1000))
    return trans


# ---------------------------------------------------------
def get_transactions():
    ''' Get all transactions for every week this year for this player            '''
    ''' Return dictionary with key = player_id, value = dict of transaction info '''
    transactions = {}
    for i in range(1,19):
        print(f'Getting Week {i} Transactions')
        response = requests.get(URL + str(i))
        if response.status_code != 200:
            print(f'breaking {response.status_code}')
            break
        print(f'Processing Week {i} transactions')
        for item in response.json():
            if is_a_waiver_claim(item):
               waiver_data = get_waiver_data(item)
               player_id = waiver_data['player_id']
               del waiver_data['player_id']
               transactions.setdefault(player_id,[]).append(waiver_data)

    return transactions


# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose
   
    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    transactions = get_transactions()
    if verbose:
        print (json.dumps(transactions, sort_keys=True, indent=2))

    # out_fh.write(json.dumps(transactions))
    # print(f'Transactions is a {type(transactions)}')
    draft = get_data(DRAFT)
    # print(f'Draft is a {type(draft)}')
    # print(draft)
	
    merged = { key:draft.get(key,[])+transactions.get(key,[]) \
                  for key in set(list(draft.keys())+list(transactions.keys())) }

    for (key, value) in merged.items():
        merged[key] = sorted(value, key=lambda d: d['price'], reverse=True)

    out_fh.write(json.dumps(merged, sort_keys=True))
    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()

# ---------------------------------------------------------
if __name__ == '__main__':
    main()

