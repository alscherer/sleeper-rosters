#!/usr/bin/env python3

"""
    Parse fantasy player data downloaded from
    https://api.sleeper.app/v1/players/nfl
    & saved to a json file.

    Written by: Al Scherer   2022-01-14
"""

import argparse
import json
import sys

# ---------------------------------------------------------
FANTASY_POSNS = { "WR", "QB", "RB", "TE", "K", "DEF" }

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='parse_players <json player file>',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='infile',
                        type=str,
                        help="Input file name")

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
def is_a_fantasy_player(player_data):
    ''' Is this a fantasy player? '''
    positions = player_data.get("fantasy_positions")
    return positions is not None and FANTASY_POSNS & set(positions)


# ---------------------------------------------------------
def get_player_data(player_data):
    player = {}
    player['positions'] = player_data.get("fantasy_positions")
    player['team'] = player_data.get("team")
    player['full_name'] =  player_data.get("full_name")
    return player


# ---------------------------------------------------------
def get_players(file_name, verbose):
    '''
    Parse the Sleeper Json file; get just the needed player info
    :param file_name: the json player file
    :return: dict of fantasy players
    '''
    player_dict = {}
    with open(file_name) as json_file:
        data = json.load(json_file)

        for player_id, player_data in data.items():
            if is_a_fantasy_player(player_data): 
                player_dict[player_id] = get_player_data(player_data)
                if verbose:
                    print('player id: ', player_id, ' Player : ', player_dict[player_id])
                    print('------------------------')

    return player_dict


# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose

    out_fh = open(args.outfile,'wt') if args.outfile else sys.stdout
    if verbose:
        print (json.dumps(get_players(args.file, verbose), sort_keys=True, indent=2))
    out_fh.write(json.dumps(get_players(args.file, verbose)))

    print("\nBye, Al!")
    out_fh.close()


# ---------------------------------------------------------
if __name__ == '__main__':
    main()
