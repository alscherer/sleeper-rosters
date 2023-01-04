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
from get_transactions import *
from get_rosters import get_rosters
from parse_players import *
from get_users import *
from final import combine_data

# ---------------------------------------------------------
FANTASY_POSNS = { "WR", "QB", "RB", "TE", "K", "DEF" }

LEAGUE_ID = "787796366440124416"

DATA_DIR = "/Users/alscherer/football/sleeper/data/2022/"
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
def main() -> None:
    """ Main function of app """

    args = get_args()
    verbose = args.verbose
   
    players = get_players(PLAYER_DATA, verbose)
    users = get_users(USERS_URL)
    rosters = get_rosters(ROSTERS_URL)

    # Look at both draft $s and weekly waiver transactions
    draft =  get_draft_data()
    transactions = get_transactions(TRANSACTIONS_URL)
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

