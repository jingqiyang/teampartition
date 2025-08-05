from datetime import datetime, timedelta
from openpyxl import load_workbook

from partition_constants import *
from partition_utils import *

# current time
now = datetime.now()
year = str(now.year)


def main():
    # load players of current year
    players_wb = load_workbook(PLAYERS_WB, data_only=True)
    players_ws = players_wb[year]
    players = getData(players_ws)

    # get player overall scores and sort
    for p in players:
        getOverallScore(players[p])
    player_keys = sorted(players.keys(), key=lambda p: players[p][OVERALL])

    # split by gender, setting, senior
    women, men = splitList(player_keys, lambda p: players[p][GENDER] == F)
    w_groups = partitionByType(women, players)
    m_groups = partitionByType(men, players)

    player_groups = w_groups + m_groups
    # printScores(player_groups, players)

    # form teams
    teams = initTeams(len(players))
    for group in player_groups:
        assignPlayers(group, teams, players)
        teams = invert(teams)

    print("Teams:")
    sortTeams(teams, players)
    printTeamScores(teams, players)


"""
get overall player score as a sum of offense/setting and defense, adjusted by if they're a senior.
"""
def getOverallScore(player):
    defense_rating = player[DEFENSE]
    offense_rating = player[SETTING] if isSetter(player) else player[OFFENSE]
    senior_modifier = -1/3 if isSenior(player) else 0

    player[OVERALL] = getScore(offense_rating) + getScore(defense_rating) + senior_modifier


"""
sort and partition a list of player keys into setters, seniors, and younger hitters.
"""
def partitionByType(player_keys, players):
    setters, hitters = splitList(player_keys, lambda p: isSetter(players[p]))
    seniors, young_hitters = splitList(hitters, lambda p: isSenior(players[p]))

    return setters, seniors, young_hitters


if __name__ == '__main__':
    main()
