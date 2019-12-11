from fractions import Fraction # avoid floating-point issues

with open('nate/inputs/in10.txt', 'r') as f:
    chart = [l.strip() for l in f.readlines()]

coords = set()
for y in range(len(chart)):
    for x, v in enumerate(chart[y]):
        if v == '#':
            coords.add((x, y))

linePoints = {} # line : points that go through it
for x1, y1 in coords:
    for x2, y2 in coords:
        if x1 != x2 or y1 != y2:
            #first determine m and b in y = mx + b, or None, b for lines x = b
            if x1 == x2:
                assert y1 != y2
                m, b = None, x1
            else:
                m = Fraction(y2 - y1, x2 - x1) # avoid floating-point issues
                b = y1 - m * x1
            linePoints[(m, b)] = linePoints.get((m, b), []) + [(x1, y1), (x2, y2)]

nBlocked = {}
for k, v in linePoints.items():
    #dedupe
    temp = set(v)
    temp = sorted(temp, key = lambda i: i[1])
    temp = sorted(temp, key = lambda i: i[0])
    for ix, v in enumerate(temp):
        if ix == 0 or ix == len(temp) - 1:
            nBlocked[v] = nBlocked.get(v, 0) + len(temp) - 2
        else:
            nBlocked[v] = nBlocked.get(v, 0) + len(temp) - 3
    linePoints[k] = temp

smallest = min([v for k, v in nBlocked.items()])
for k, v in nBlocked.items():
    if v == smallest:
        laser = k # not a great way to do this but iterating through this dict is fast
print(len(coords) - smallest - 1)
print(laser)
linesOfSight = {k : v for k, v in linePoints.items() if laser in v}
i = 0
directions = {}
for k, v in linesOfSight.items():
    flag = False
    for p in v:
        if p != laser:
            i += 1
            directions[(flag, k[0])] = directions.get((flag, k[0]), []) + [p]
        else:
            flag = True
l = [k for k in directions.keys()]
l.sort(key = lambda i: i[1] if type(i[1]) != type(None) else -999) # None first, then large negative slopes, then bigger ones
l.sort(key = lambda i: -1 * i[0]) # laser hits things on the right first, where things above are "right"
i = 1
j = 0
while i < len(coords)-5:
    curr = l[j % len(l)] # loop through l continuously
    j += 1
    if len(directions[curr]) > 0:
        if curr == (True, None):
            target = min(directions[curr], key = lambda i: -1 * i[1])
        elif curr == (False, None):
            target = min(directions[curr], key = lambda i: i[1])
        elif curr[0] == True:
            target = min(directions[curr], key = lambda i: i[0])
        else:
            target = min(directions[curr], key = lambda i: -1 * i[0])
        directions[curr].remove(target)
        print(i, target)
        i += 1