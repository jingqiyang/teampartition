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

    for player_key in players:
        player = players[player_key]
        getOverallScore(player)

    women, men = splitByGender(players)
    sorted_women = sorted(women, key=lambda p: players[p][OVERALL])
    sorted_men = sorted(men, key=lambda p: players[p][OVERALL])

    printScores(sorted_women, players)
    print()
    printScores(sorted_men, players)


"""
get overall player score as a sum of offense/setting and defense, adjusted by if they're a senior.
"""
def getOverallScore(player):
    defense_rating = player[DEFENSE]
    offense_rating = player[SETTING] if isSetter(player) else player[OFFENSE]
    senior_modifier = -1/3 if isSenior(player) else 0

    player[OVERALL] = getScore(offense_rating) + getScore(defense_rating) + senior_modifier


"""
make 2 lists of player keys split by gender.
"""
def splitByGender(players):
    women = []
    men = []

    for player_key in players:
        if players[player_key][GENDER] == "F":
            women.append(player_key)
        else:
            men.append(player_key)

    return women, men


def printScores(player_keys, players):
    for player_key in player_keys:
        print(player_key + ": " + str(round(players[player_key][OVERALL], 2)))


if __name__ == '__main__':
    main()
