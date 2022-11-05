# sleeper-rosters

I play in a "keeper auction" fantasy league where each player's keeper salary is 2x the prior year's salary or 5, whichever is higher.
And that prior year salary is the highest price anyone paid for that player in the initial auction or on waivers.

I am new to Python so thought it might be a good exercise to use Python to invoke the Sleeper APIs, download the necessary data and do the calculations.
I wanted it to be something I could easily update during the year to share with my leaguemates.

If I get time, I will add unit testing, consolidate and better "pythonize" the code so I don't have to run it one at a time.
I'm putting it here for now to save my updates and in case anyone stumbles on this and would like to do somethimg similar/better.

I built all of these using Python 3.9.

=================================================


Here's my to-do notes I created for myself while building it:

# DONE Rosters  https://api.sleeper.app/v1/league/650130288072040448/rosters
# DONE Users:  https://api.sleeper.app/v1/league/650130288072040448/users
DONE COMBINE Rosters & Users to be readable - done

------------------------
draft:  https://api.sleeper.app/v1/draft/<draft_id>
all drafts for lg:  https://api.sleeper.app/v1/league/650130288072040448/drafts --> 2021 is 650130288072040449?
   that draft https://api.sleeper.app/v1/draft/650130288072040449/picks
XFL 2022 = 787796366440124416

------------------------
BEFORE SEASON
1. Run get_users.py to get owners -> Save to ...data/2022/users.json
     owner id is user id? ex: my id is  841844849056550912    
     Ex:  "97088838635503616": {"display_name": "Tim_Terry", "team_name": "Vegas Vipers"}, 

2. Download player pool from URL, save as json (huge file) -> Save to ...

3. Run parse_players.py to reduce pool to usable json file -> Save to ...
	data/2022/parsed_players.json
	Ex:  {"5870": {"positions": ["QB"], "team": "NYG", "full_name": "Daniel Jones"}, ...

   TODO: Have to update each time I run it because new guys enter league/change teams!!

------------------------
AFTER DRAFT
1. Download draft data from url, save as json - to data/2022/draft-2022.json
	Ex: https://api.sleeper.app/v1/draft/650130288072040449/picks 
	 Looks like: {"round":1,"roster_id":1,"player_id":"6794","picked_by":"378716407027937280","pick_no":1,"metadata":{"years_exp":"2","team":"MIN","status":"Active","sport":"nfl","slot":"1","position":"WR","player_id":"6794","number":"18","news_updated":"1646327726661","last_name":"Jefferson","injury_status":"","first_name":"Justin","amount":"10"},"is_keeper":false,"draft_slot":1,"draft_id":"787796366440124417"}
2. Run parse_draft.py -o data/2022/parsed_draft.json   to create a consumable json 
	Ex:  {'6794': {'type': 'draft', 'roster_id': 1, 'price': '10', 'date': 'Sep 1, 2022'}, '6803': 

------------------------
TO UPDATE DATA
1. Run get_rosters.py to get current roster (looks ok 2022-11-02)
	Gets data from URL
	output is dict w key = owner_id, value = player id list
	- write to data/2022/rosters-<date>.json
       Ex:  [{"owner_id": "378716407027937280", "roster_id": 1, "players": ["1466", "1476", "1825", "4035", "4098", "421", "4881", "5955", "6083", "6786", "6794", "6803", "6945", "6955", "7525", "7571", "7611", "8121", "8137", "8148", "NE"]},


2. Run get_transactions.py (gets entire year) - gets waiver claims & prices, merge w draft, sort in dollar order desc
	Key = player_id, list of transaction dicts sorted by price hi to low, 
					each transaction dict has entries for date, price, roster_id, type (draft/waiver) - 
       merges transactions and drafts, putting results per player in reverse order of price 
        - write to data/2022/transactions.xlsx
       Ex:  {"1067": [{"date": "Sep 1, 2022", "price": 1, "roster_id": 5, "type": "draft"}], "1166": 


4. Run final.py to merge teams, rosters and transactions
     transactions have key=player_id   value = list of transaction dicts sorted in reverse price order
           	  value transaction ids have roster_id
     to get rosters, players & curr salaries

         read in user data/2022/users.json
         read in parsed_player data/2022/parsed_players.json
         read in roster data  data/2022/rosters-<date>.json
	 read in transaction data/2022/transactions.json
