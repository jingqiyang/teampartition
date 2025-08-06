from partition_constants import *
from partition_utils import *


def main():
    # load players of current year
    players = getPlayers()
    for p in players:
        getOverallScore(players[p])

    teams = initTeams(len(players))

    # assign players from each group to teams
    player_groups = getPlayerGroups(players)
    conflicts = []
    for group in player_groups:
        assignTeams(group, teams, players, conflicts)

    # clean up teams
    assignConflicts(teams, players, conflicts)
    rebalance(teams, players)
    printTeamScores(teams, players)


"""
get overall player score as a sum of offense/setting and defense, adjusted by if they're a senior.
"""
def getOverallScore(player):
    defense_rating = player[SETTING] if isSetter(player) else player[DEFENSE]
    offense_rating = player[OFFENSE]
    senior_modifier = -1/3 if isSenior(player) else 0

    player[OVERALL] = getScore(offense_rating) + getScore(defense_rating) + senior_modifier


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


"""
assign players to teams in a snaking pattern. returns unassigned conflict players.
"""
def assignTeams(player_keys, teams, players, conflicts):
    i = 0
    sortTeams(teams, players, reverse=True)

    for p in player_keys:
        assigned = False
        started = False
        init_i = i

        while not assigned and (not started or i != init_i):
            started = True
            team = teams[i]

            # don't add to team with more players until all teams reach same number of players
            if okToAdd(team, players[p], teams, players):
                team.append(p)
                assigned = True

            i += 1

            # turn the snake around
            if i == len(teams):
                teams.reverse()
                i = 0

        # track conflict player to assign later
        if not assigned:
            conflicts.append(p)


"""
add unassigned conflict players and make swaps until all teams have enough players.
"""
def assignConflicts(teams, players, conflicts):
    for i in range(len(conflicts) - 1, -1, -1):
        p = conflicts[i]
        assigned = False

        # assign conflicts to teams that aren't full where possible
        for team in teams:
            if len(team) < MAX_TEAM_SIZE and noConflict(players[p], team):
                team.append(p)
                del conflicts[i]
                assigned = True
                break

    # TODO: continually make swaps to assign remaining conflict players

    if len(conflicts) > 0:
        print("unassigned conflicts: " + ", ".join(conflicts) + "\n")


"""
make swaps to decrease team score standard deviation.
"""
def rebalance(teams, players):
    sortTeams(teams, players)
    std = getTeamStd(teams, players)

    # swap players at same index across teams with major to minor score difference
    for i in range(0, len(teams[0])):
        for j in range(0, int(len(teams) / 2)):
            # try swap with adjacent indices
            for k in range(i - 1, i + 2):
                swap(teams[j], i, teams[-1 - j], k, players)
                new_std = getTeamStd(teams, players)

                if new_std < std:
                    std = new_std
                else:
                    # swap back if no improvement
                    swap(teams[j], i, teams[-1 - j], k, players)

        sortTeams(teams, players)


if __name__ == '__main__':
    main()
