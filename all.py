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
from sleeper_util import *


# ---------------------------------------------------------
FANTASY_POSNS = { "WR", "QB", "RB", "TE", "K", "DEF" }

LEAGUE_ID = "787796366440124416"

DATA_DIR = "/Users/alscherer/football/sleeper/data/2022/"
DATA_DIR = "~/football/sleeper/data/2022/"
DRAFT_DATE = "Sep 1, 2022"

USER_DATA = DATA_DIR + "users.json" 
DRAFT_DATA = DATA_DIR + "parsed_draft.json"
PLAYER_DATA = DATA_DIR + "players-from-site.json"

LEAGUE_URL = "https://api.sleeper.app/v1/league/" + LEAGUE_ID
USERS_URL = LEAGUE_URL + "/users"
ROSTERS_URL = LEAGUE_URL + "/rosters"
TRANSACTIONS_URL = LEAGUE_URL + "/transactions/"  # We'll paste the week # at the end


# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='all <json player file>',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='infile',
                        type=str,
                        help="Json Player File")


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
def extract_user_data(user_data):
    user = {}
    user_name = user_data['display_name']
    user['display_name'] = user_name

    team_name = (user_data['metadata']).get('team_name', user_name)
    print(team_name)
    if team_name:
        user['team_name'] = team_name
    else:
        user['team_name'] = displayName
    return user


# ---------------------------------------------------------
def get_users():
    ''' Get all user data '''
    users = {}
    print(f'Getting User Data')
    response = read_from_url(USERS_URL)
    if response.status_code != 200:
        print(f'{response} nope')
        sys.exit(1)

    for user_data in response.json():
        user_id = user_data["user_id"]
        users[user_id] = extract_user_data(user_data)

    return users


# ---------------------------------------------------------
def get_draft_data():
    return read_from_file(DRAFT_DATA)

# ---------------------------------------------------------
def merge_transactions_and_draft(transactions, draft):
    merged = { key:draft.get(key,[])+transactions.get(key,[]) \
                  for key in set(list(draft.keys())+list(transactions.keys())) }

    for (key, value) in merged.items():
        merged[key] = sorted(value, key=lambda d: d['price'], reverse=True)

    return merged

# ---------------------------------------------------------
def is_a_fantasy_player(player_data):
    ''' Is this a fantasy player? '''
    positions = player_data.get("fantasy_positions")
    return positions is not None and FANTASY_POSNS & set(positions)

# ---------------------------------------------------------
def get_player_data(player_data):
    '''
    Get just this player's relevant data from a Sleeper Player entry
    :param fileName: the json player file
    :return: single player dict
    '''

    player = {}
    player['positions'] = player_data.get("fantasy_positions")
    player['team'] = player_data.get("team")
    player['full_name'] =  player_data.get("full_name")
    return player

# ---------------------------------------------------------
def parse_players(fileName, verbose):
    '''
    Parse the huge Sleeper Json file, extract just the needed player info
    :param fileName: the json player file
    :return: dict of fantasy players
    '''

    player_dict = {}
    with open(fileName) as json_file:
        data = json.load(json_file)

        for player_id, player_data in data.items():
            if is_a_fantasy_player(player_data):
                player_dict[player_id] = get_player_data(player_data)
                if verbose:
                    print('player id: ', player_id, ' Player : ', player_dict[player_id])
                    print('------------------------')

    return player_dict

# ---------------------------------------------------------
def get_rosters():
    ''' Get all rosters data '''
    roster_list = []
    print(f'Getting Roster Data')
    response = read_from_url(ROSTERS_URL)

    for roster_data in response.json():
        roster = {}
        roster['owner_id'] = roster_data['owner_id']
        roster['roster_id'] = roster_data['roster_id']
        roster['players'] = roster_data['players']
        roster_list.append(roster)

    return roster_list

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
    for i in range(1,18):
        print(f'Getting Week {i} Transactions')
        response = read_from_url(TRANSACTIONS_URL + str(i))
        if response.status_code != 200:
            print(f'breaking {response.status_code}')
            break
        print(f'Processing Week {i} transactions')
        num_transactions = 0
        for item in response.json():
            if is_a_waiver_claim(item):
               num_transactions += 1
               waiver_data = get_waiver_data(item)
               player_id = waiver_data['player_id']
               del waiver_data['player_id']
               transactions.setdefault(player_id,[]).append(waiver_data)
        print(f' Found {num_transactions} transactions')

    return transactions


# ---------------------------------------------------------
def combine_data(users, players, rosters, transactions):
    ''' combine all this stuff '''
    final_data = []
    
    # Start by looking at rosters
    for roster_info in rosters:
        owner_id = roster_info['owner_id']

        roster_data = {} 
        roster_data['owner_name'] = users[owner_id]['display_name']
        roster_data['fantasy_team'] = users[owner_id]['team_name']
        roster_players = roster_info['players']

        # rosters is the list of player data
        roster_data['players'] = []
        for player_id in roster_players:
            player_data = {}
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
   
    players = parse_players(PLAYER_DATA, verbose)
    users = get_users()
    rosters = get_rosters()

    # Look at both draft $s and weekly waiver transactions
    draft =  get_draft_data()
    transactions = get_transactions()
    merged = merge_transactions_and_draft(transactions, draft)

    final_data = combine_data(users, players, rosters, merged)

    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    if verbose:
        print (json.dumps(final_data, sort_keys=True, indent=2))

    out_fh.write(json.dumps(final_data, sort_keys=True))

    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()

# ---------------------------------------------------------
if __name__ == '__main__':
    main()

