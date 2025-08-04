from partition_constants import *


"""LOADING DATA FUNCTIONS"""

"""
get data from worksheet as dict with columns as fields of each element.
keys are in the form "First Name_Last Name".
"""
def getData(ws):
    data = {}
    cols = [cell.value for cell in ws[1]]

    r = 2
    key = getKey(ws, r)

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
        key = getKey(ws, r)

    return data


"""
get key formed from first 2 columns in the form "First Name_Last Name"
"""
def getKey(ws, r):
    if not ws.cell(column=1, row=r).value:
        return None

    return ws.cell(column=1, row=r).value + "_" + ws.cell(column=2, row=r).value



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

