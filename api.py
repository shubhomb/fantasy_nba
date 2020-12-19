import espn_api
import pandas as pd
from espn_api.basketball import League

#
# League IDs
SEASON_ID = 2021
ESPN_S2 = "AEBDWt3aJF82r1VhHZhHNOxjjwGhE03%2F5FPDbX5TWXvxDll3oh9%2FV5LpNVpNGxmOuobeYrbVodo2DMC2atXS5YY8Ipek%2F5P0nbJNlxd91pUCMrdYc1Z5NS1ats5CxccgHZHliKgrWet0S6eMMVd6x0IAa231se6JIK9J934CDPmLTjexpfatHFyNACZrOvwEZ1yfgk9D%2BSZSM2gfVCxD3AYq89dtQ99s77vpFjNXNfo0mbflXTqHkgoIYMH%2BBQP06Vvo1V8zSSua4%2FwIHsAGDD4B"
ESPN_SWID  = "{8AAB425F-D076-4B19-8E67-E55ED77D3C46}"
CORNELL = {"leagueID" :35812962, "teamID": 1}
ALPH = {"leagueID": 1239647372, "teamID": 3}

SCORE_WEIGHTS = pd.DataFrame.from_dict({
                                        "PTS": 1,
                                        "3PTM": 1,
                                        "FGA": -1,
                                        "FGM": 2,
                                        "FTA": -1,
                                        "FTM": 1,
                                        "REB": 1,
                                        "AST": 2,
                                        "STL": 4,
                                        "BLK": 4,
                                        "TO": -2,
                                    }, orient='index')

cornell_league = League(league_id=CORNELL["leagueID"], year=SEASON_ID, espn_s2=ESPN_S2, swid=ESPN_SWID)
cornell_team_ids = [team.team_id for team in cornell_league.standings()]

alph_league = League(league_id=ALPH["leagueID"], year=SEASON_ID, espn_s2=ESPN_S2, swid=ESPN_SWID)
alph_team_ids = [team.team_id for team in alph_league.standings()]

def current_rostered_and_stats(league):
    rosters = {}
    stats = {}
    for team in league.teams:
        for player in team.roster:
            rosters[player.playerId] = player.name, team.team_id, team.team_name
            for key in player.stats:
                stats[(player.playerId, key)] = player.stats[key]['avg']
    for player in alph_league.free_agents(size=150):
        rosters[player.playerId] = player.name, -1, "FA"
        for key in player.stats:
            stats[(player.playerId, key)] = player.stats[key]['avg']
    rosters = pd.DataFrame.from_dict(rosters, orient="index")
    rosters.columns = ["name", "team_id", "team_name"]
    stats = pd.DataFrame.from_dict(stats, orient="index")
    return rosters, stats

