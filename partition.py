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
        print(player_key + ": " + str(round(player[OVERALL], 2)))


"""
get overall player score as a sum of offense/setting and defense.
"""
def getOverallScore(player):
    defense_rating = player[DEFENSE]
    offense_rating = player[SETTING] if isSetter(player) else player[OFFENSE]
    player[OVERALL] = getScore(offense_rating) + getScore(defense_rating)


if __name__ == '__main__':
    main()
