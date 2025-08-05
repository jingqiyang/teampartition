from partition_constants import *
from partition_utils import *


def main():
    # load players of current year
    players = getPlayers()

    # get player overall scores and sort
    for p in players:
        getOverallScore(players[p])

    teams = initTeams(len(players))

    # form teams from player groups
    player_groups = getPlayerGroups(players)
    for group in player_groups:
        assignTeams(group, teams, players)

    finalSwaps(teams, players)
    printTeamScores(teams, players)


"""
get list of alternating women and men setter, senior, and young hitter groups.
"""
def getPlayerGroups(players):
    player_keys = sorted(players.keys(), key=lambda p: players[p][OVERALL])

    # split by gender, setting, senior
    women, men = splitList(player_keys, lambda p: players[p][GENDER] == F)
    w_groups = partitionByType(women, players)
    m_groups = partitionByType(men, players)

    zipped_groups = list(zip(w_groups, m_groups))

    # flatten list of tuples into list of values
    return list(sum(zipped_groups, ()))


"""
sort and partition a list of player keys into setters, seniors, and young hitters.
"""
def partitionByType(player_keys, players):
    setters, hitters = splitList(player_keys, lambda p: isSetter(players[p]))
    seniors, young_hitters = splitList(hitters, lambda p: isSenior(players[p]))

    return setters, seniors, young_hitters


if __name__ == '__main__':
    main()
