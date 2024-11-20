#!/usr/bin/env python3
 
"""
    Download & parse all users from 
	https://api.sleeper.app/v1/league/650130288072040448/users
	https://api.sleeper.app/v1/league/919353924837056512/users
	https://api.sleeper.app/v1/league/1051604880055566336/users
    & save to a json file.
    That league # is my "Flex" league 2021.

    Data is a list...
    Example API output:
{"user_id":"378716407027937280","settings":null,"metadata":{"team_name":"Cleveland Steamers","mention_pn":"on","mascot_message_emotion_leg_1":"idle","mascot_item_type_id_leg_9":"ref","mascot_item_type_id_leg_8":"ref","mascot_item_type_id_leg_7":"ref","mascot_item_type_id_leg_6":"ref","mascot_item_type_id_leg_5":"ref","mascot_item_type_id_leg_4":"ref","mascot_item_type_id_leg_3":"ref","mascot_item_type_id_leg_2":"ref","mascot_item_type_id_leg_18":"ref","mascot_item_type_id_leg_17":"ref","mascot_item_type_id_leg_16":"ref","mascot_item_type_id_leg_15":"ref","mascot_item_type_id_leg_14":"ref","mascot_item_type_id_leg_13":"ref","mascot_item_type_id_leg_12":"ref","mascot_item_type_id_leg_11":"ref","mascot_item_type_id_leg_10":"ref","mascot_item_type_id_leg_1":"ref","archived":"off","allow_pn":"on"},"league_id":"650130288072040448","is_owner":true,"is_bot":false,"display_name":"elwzink","avatar":"f60b537ac01af0c68dfefc5b0a93ea87"}

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
# PLAYER_FILE = "data/parsed-players.json"
# URL = "https://api.sleeper.app/v1/league/650130288072040448/users"
# 2022 URL = "https://api.sleeper.app/v1/league/787796366440124416/users"
# 2023 URL="https://api.sleeper.app/v1/league/919353924837056512/users"
URL = "https://api.sleeper.app/v1/league/1051604880055566336/users"

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='get-teams <json player file>',
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
def get_user_data(user_data):
    user = {}
    user_name = user_data['display_name']
    user['display_name'] = user_name

    # team_name = user_data['metadata']['team_name'] 
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
    response = requests.get(URL)
    if response.status_code != 200:
        print(f'{response} nope')
        sys.exit(1)
    
    for user_data in response.json():
        user_id = user_data["user_id"]
        users[user_id] = get_user_data(user_data)

    return users

# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose
   
    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    users = get_users()
    if verbose:
        print (json.dumps(users, sort_keys=True, indent=2))
    out_fh.write(json.dumps(users))

    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()

# ---------------------------------------------------------
if __name__ == '__main__':
    main()

