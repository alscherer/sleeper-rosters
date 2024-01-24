#!/usr/bin/env python3
 
"""
    Combine the user, player, roster & transaction data to show current rosters & salaries
    & save to a json file.

    Written by: Al Scherer   2022-11-04
"""

import argparse
import json
import requests
import time
import datetime
import sys


# ---------------------------------------------------------
USER_DATA = "data/2023/users.json" 
PLAYER_DATA = "data/2023/parsed_players.json"
ROSTER_DATA = "data/2023/rosters-20240101.json"
TRANSACTION_DATA = "data/2023/transactions.json"

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='final <json player file>',
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
def combine_data(users, players, rosters, transactions):
    ''' combine all this stuff '''
    final_data = []
    
    # Start by looking at rosters
    for roster_info in rosters:
        owner_id = roster_info['owner_id']

        roster_data = {} 
        # roster_data['owner_id'] = owner_id
        # roster_data['roster_id'] = roster_info['roster_id'] 
        roster_data['owner_name'] = users[owner_id]['display_name']
        roster_data['fantasy_team'] = users[owner_id]['team_name']
        roster_players = roster_info['players']

        # rosters is the list of player data
        roster_data['players'] = []
        for player_id in roster_players:
            player_data = {}
            # player_data['player_id'] = player_id
            player_info = players[player_id]
            player_data['full_name'] = player_info['full_name']
            player_data['nfl_team'] = player_info['team']
            player_data['positions'] = player_info['positions']
            player_data['salary'] = transactions[player_id][0]['price']
            roster_data['players'].append(player_data)   

        final_data.append(roster_data)

    return final_data

# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose
   
    users = get_data(USER_DATA)
    players = get_data(PLAYER_DATA)
    rosters = get_data(ROSTER_DATA)
    transactions = get_data(TRANSACTION_DATA)
    
    final_data = combine_data(users, players, rosters, transactions)

    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    if verbose:
        print (json.dumps(final_data, sort_keys=True, indent=2))

    out_fh.write(json.dumps(final_data, sort_keys=True))

    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()

# ---------------------------------------------------------
if __name__ == '__main__':
    main()

