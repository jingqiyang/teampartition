from math import ceil

from partition_constants import *


"""LOAD DATA FUNCTIONS"""

"""
get data from worksheet as dict with first column values as keys, and top row as fields of each element.
"""
def getData(ws):
    data = {}
    cols = [cell.value for cell in ws[1]]

    r = 2
    key = ws.cell(column=1, row=r).value

    while key:
        element = {}
        for c in range(0, len(cols)):
            col = cols[c]
            if col not in element:
                element[col] = ws.cell(column=c + 1, row=r).value

        if key in data:
            print("warning: duplicate element " + key + ", skipping duplicate")
        else:
            data[key] = element

        r += 1
        key = ws.cell(column=1, row=r).value

    return data



"""INTERPRETING PLAYER DATA FUNCTIONS"""

def isSenior(player):
    return player[SENIOR] == YES

def isSetter(player):
    return player[SETTER] == YES


"""
convert yankee rating to numerical score.
"""
def getScore(rating):
    letter = rating[0].upper()
    if letter < "A" or letter > "D":
        print("warning: invalid yankee letter rating")
        return None

    # use ascii value of letter with D as min score of 0
    score = 68 - ord(letter)

    if rating.endswith("-"):
        return score - 1/3
    elif rating.endswith("+"):
        return score + 1/3
    return score

"""
get float score value as string.
"""
def getScoreString(score):
    return str(round(score, 2))


"""
print all scores of players in gender/position/age groups.
"""
def printScores(player_groups, players):
    for player_keys in player_groups:
        for p in player_keys:
            print(p + ": " + getScoreString(players[p][OVERALL]))
        print()


"""DATA MANIPULATION FUNCTIONS"""

"""
partition a sub list from an original list based on a lambda function returning true for each element.
the elements of the sub list are removed from the original list.
"""
def splitList(original_list, f):
    sub_list = []
    for i in range(len(original_list) - 1, -1, -1):
        if f(original_list[i]):
            element = original_list.pop(i)
            sub_list.insert(0, element)

    return sub_list, original_list



"""TEAM LIST MANIPULAITON FUNCTIONS"""

"""
create list of empty teams.
"""
def initTeams(num_players):
    return [set() for x in range(0, ceil(num_players / MAX_TEAM_SIZE))]


"""
change order of teams for reseeding.
"""
def invert(teams):
    midpoint = int(len(teams) / 2)

    return list(reversed(teams[:midpoint])) + list(reversed(teams[midpoint:]))


"""
recursively assign players to teams by first assigning the start and end of the player list.
"""
def assignPlayers(player_keys, teams, players):
    num_teams = len(teams)
    num_players = len(player_keys)

    # base case and repeat every recursive iteration: assign "outer rows" of players
    if num_players < num_teams:
        sortTeams(teams, players, reverse=True)
    assignSequential(player_keys[:num_teams], teams, players)
    assignSequential(list(reversed(player_keys[num_teams:])), teams, players)

    # assign inner rows
    if num_players > num_teams * 2:
        assignPlayers(player_keys[num_teams:-num_teams], teams, players)


"""
assign a list of players directly to the teams in sequential order.
the number of players should be less than or equal to the number of teams.
"""
def assignSequential(player_keys, teams, players):
    i = 0
    for team in teams:
        # TODO: handle conflicts
        if i >= len(player_keys):
            return

        team.add(player_keys[i])
        i += 1


"""
sort teams by average player score.
"""
def sortTeams(teams, players, reverse=False):
    teams.sort(key=lambda t: getTeamScore(t, players), reverse=reverse)


"""
print average player score of each team.
"""
def printTeamScores(teams, players):
    for team in teams:
        if len(team) == 0:
            print("warning: empty team")
            continue

        for p in team:
            print(p + " " + getScoreString(players[p][OVERALL]))
        print("Team Score: " + getScoreString(getTeamScore(team, players)) + " (size " + str(len(team)) + ")\n")


"""
get average overall score of players of a team.
"""
def getTeamScore(team, players):
    if len(team) == 0:
        return 0
    return sum(map(lambda p: players[p][OVERALL], team)) / len(team)

