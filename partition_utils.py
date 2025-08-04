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

