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
    w_setters, w_seniors, w_young_hitters = partitionByType(women, players)
    m_setters, m_seniors, m_young_hitters = partitionByType(men, players)

    printScores([w_setters, w_seniors, w_young_hitters, m_setters, m_seniors, m_young_hitters], players)

    teams = initTeams(len(players))
    assignPlayers(w_setters, teams, players)

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


def printScores(player_key_groups, players):
    for player_keys in player_key_groups:
        for p in player_keys:
            print(p + ": " + str(round(players[p][OVERALL], 2)))
        print()


if __name__ == '__main__':
    main()
