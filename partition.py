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

    for player in players:
        rating = players[player]["Offense"]
        print(player + ": " + rating + " = " + str(round(getScore(rating), 2)))


if __name__ == '__main__':
    main()
