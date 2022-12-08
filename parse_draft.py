#!/usr/bin/env python3
  
"""
    Reduce the draft data to a manageable dict
    Result is a dict - key is the player_id, list of transactions

    Written by: Al Scherer   2022-01-14
"""

import argparse
import json
import sys
import datetime

DRAFT = 'data/2022/draft-2022.json'
DRAFT_DATE = 'Sep 1, 2022'

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='combine_rosters <json player file>',
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

    return parser.parse_args()


# ---------------------------------------------------------
def get_data(file_name):
    ''' get data from json file '''
    with open(file_name,'r') as data_file:
        data = data_file.read()

    details = json.loads(data)
    return details

# ---------------------------------------------------------
def get_usable_draft_data(draft):
    usable = {}
    for draft_data in draft:
        player_id = draft_data["metadata"]["player_id"]
        usable[player_id] = {}
        event_list = []
        event_info = {}
        event_info["type"] = 'draft'
        event_info["roster_id"] = draft_data["roster_id"]
        event_info["price"] = int(draft_data["metadata"]["amount"])
        event_info["date"] = DRAFT_DATE
        event_list.append(event_info)
        usable[player_id] = event_list
    
    return usable


# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose

    draft = get_data(DRAFT)
    usable_draft_data = get_usable_draft_data(draft)  

    if verbose:
        print (json.dumps(usable_draft_data))

    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    out_fh.write(json.dumps(usable_draft_data))

    print("\nBye, Al!")
    print('\nRun at {:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))
    out_fh.close()


# ---------------------------------------------------------
if __name__ == '__main__':
    main()
