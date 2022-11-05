#!/usr/bin/env python3
 
"""
    Get league info
	https://api.sleeper.app/v1/league/650130288072040448
	2022	https://api.sleeper.app/v1/league/787796366440124416
    That league # is my "XFL" league 2022.

    Data is a list...
    Example API output:
{"total_rosters":10,"status":"complete","sport":"nfl","shard":224,"settings":{"max_keepers":1,"draft_rounds":4,"trade_review_days":0,"squads":1,"reserve_allow_dnr":1,"capacity_override":0,"pick_trading":1,"disable_trades":0,"taxi_years":0,"taxi_allow_vets":0,"best_ball":0,"last_report":14,"disable_adds":0,"waiver_type":2,"bench_lock":1,"reserve_allow_sus":0,"type":2,"reserve_allow_cov":1,"waiver_clear_days":1,"daily_waivers_last_ran":16,"waiver_day_of_week":2,"start_week":1,"playoff_teams":6,"num_teams":10,"reserve_slots":5,"playoff_round_type":0,"daily_waivers_hour":8,"waiver_budget":100,"reserve_allow_out":0,"offseason_adds":1,"last_scored_leg":17,"playoff_seed_type":1,"daily_waivers":1,"divisions":2,"playoff_week_start":15,"daily_waivers_days":2186,"league_average_match":0,"leg":17,"trade_deadline":12,"reserve_allow_doubtful":0,"taxi_deadline":0,"reserve_allow_na":0,"taxi_slots":0,"playoff_type":1},"season_type":"regular","season":"2021","scoring_settings":{"pass_2pt":2.0,"pass_int":-2.0,"fgmiss":-1.0,"rec_yd":0.10000000149011612,"xpmiss":-1.0,"def_pr_td":0.0,"fgm_30_39":3.0,"blk_kick":2.0,"pts_allow_7_13":4.0,"ff":1.0,"fgm_20_29":3.0,"fgm_40_49":4.0,"pts_allow_1_6":7.0,"st_fum_rec":1.0,"def_st_ff":1.0,"st_ff":1.0,"bonus_rec_te":0.5,"pts_allow_28_34":-1.0,"fgm_50p":5.0,"fum_rec":2.0,"def_td":6.0,"fgm_0_19":3.0,"int":2.0,"pts_allow_0":10.0,"pts_allow_21_27":0.0,"rec_2pt":2.0,"rec":1.0,"xpm":1.0,"st_td":6.0,"def_st_fum_rec":1.0,"def_st_td":6.0,"sack":1.0,"fum_rec_td":6.0,"rush_2pt":2.0,"rec_td":6.0,"pts_allow_35p":-4.0,"pts_allow_14_20":1.0,"rush_yd":0.10000000149011612,"pass_yd":0.05000000074505806,"pass_td":6.0,"rush_td":6.0,"def_kr_td":0.0,"fum_lost":-2.0,"fum":0.0,"safe":2.0},"roster_positions":["QB","RB","WR","TE","FLEX","FLEX","FLEX","FLEX","FLEX","SUPER_FLEX","BN","BN","BN","BN","BN","BN","BN","BN","BN","BN","BN","BN","BN","BN"],"previous_league_id":"523547292980486144","name":"The Flex and the Furious","metadata":{"trophy_winner_banner_text":"JON","trophy_winner_background":"fireworks","trophy_winner":"winner4","continued":"yes"},"loser_bracket_id":776729467954618369,"league_id":"650130288072040448","last_read_id":null,"last_pinned_message_id":null,"last_message_time":1641687315035,"last_message_text_map":null,"last_message_id":"785697181989654528","last_message_attachment":null,"last_author_is_bot":false,"last_author_id":"378716407027937280","last_author_display_name":"elwzink","last_author_avatar":"f60b537ac01af0c68dfefc5b0a93ea87","group_id":null,"draft_id":"650130288072040449","company_id":null,"bracket_id":776729467950424064,"avatar":"3d9194b27181c114f6b0e3c6da7e9c56"}

    Written by: Al Scherer   2022-01-16
"""

import argparse
import json
import requests
import time
import datetime
import sys


# ---------------------------------------------------------
PLAYER_FILE = "data/parsed-players.json"
URL = "https://api.sleeper.app/v1/league/"

# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='get-teams <json player file>',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('league_id',help='League Id',type=int)

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
def get_league_info(league_id):
    ''' Get league info '''
    print(league_id)
    league_info = {} 
    print(f'Getting League Data for {league_id}')
    url = f'{URL}{league_id}/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'{response} nope')
        sys.exit(1)

    json_data = json.loads(response.text)
    # print(f'json data: {json_data}')

    league_info = {}
    league_info["name"]=json_data["name"]
    league_info["season"]=json_data["season"]
    league_info["season_type"]=json_data["season_type"]

    return league_info


# ---------------------------------------------------------
def main() -> None:
    """ Main function of app """
    args = get_args()
    verbose = args.verbose
    league_id = args.league_id
    print(get_league_info(league_id))


# ---------------------------------------------------------
if __name__ == '__main__':
    main()

