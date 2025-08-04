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
    return player["Senior"] == YES

def isSetter(player):
    return player["Setter"] == YES

