#!/usr/bin/env python3
 
"""
    Get rosters from 
        https://api.sleeper.app/v1/league/650130288072040448/rosters
    & save to a json file.
    That league # is my "Flex" league 2021.
	Flex 2021 = 650130288072040448
	XFL 2022 = 787796366440124416

    It's a list of these dicts:
    Example API output:
{"taxi":null,"starters":["4984","1535","6794","2505","7607","1479","2197","3225","5045","7610"],"settings":{"wins":6,"waiver_position":8,"waiver_budget_used":100,"total_moves":0,"ties":0,"rank":6,"ppts_decimal":15,"ppts":2729,"losses":8,"fpts_decimal":70,"fpts_against_decimal":45,"fpts_against":2242,"fpts":2263,"division":1},"roster_id":1,"reserve":["2251","2306","2749","4034","5870"],"players":["1387","1479","1535","1837","2168","2197","2251","2306","2505","2749","3202","3225","4034","4984","5045","5131","5284","536","5870","5985","6794","6955","7066","7565","7585","7607","7610","947","954"],"player_map":null,"owner_id":"378716407027937280","metadata":{"streak":"1W","record":"WLLLLLLWWWWLLW"},"league_id":"650130288072040448","co_owners":null}

   This app pulls the data from the URL & formats it for our use
	our desired format is key = roster_id, value = list of players

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
URL = "https://api.sleeper.app/v1/league/787796366440124416/rosters"

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='get-rosters <json player file>',
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
def get_rosters():
    ''' Get all rosters data '''
    roster_list = []
    print(f'Getting Roster Data')
    response = requests.get(URL)
    if response.status_code != 200:
        print(f'{response} nope')
        sys.exit(1)
    
    for roster_data in response.json():
        roster = {} 
        roster['owner_id'] = roster_data['owner_id']
        roster['roster_id'] = roster_data['roster_id']
        roster['players'] = roster_data['players']
        roster_list.append(roster)

    return roster_list

# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose
   
    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    rosters = get_rosters()
    if verbose:
        print (json.dumps(rosters, sort_keys=True, indent=2))
    out_fh.write(json.dumps(rosters))

    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()

# ---------------------------------------------------------
if __name__ == '__main__':
    main()

