try:
    with open('inputs/in3.txt', 'r') as f:
        w1 = f.readline().strip().split(',')
        w2 = f.readline().strip().split(',')
except:
    with open('nate/inputs/in3.txt', 'r') as f:
        w1 = f.readline().strip().split(',')
        w2 = f.readline().strip().split(',')
        
DIRS = {'U' : (0, 1), 'R' : (1, 0), 'D' : (0, -1), 'L' : (-1, 0)}

def parseToken(t):
    assert type(t) == str and t[0] in DIRS
    length = int(t[1:]) # implicit assertion
    return t[0], length

def populatePath(tokens):
    assert type(tokens) == list
    path = set()
    x, y, n = 0, 0, 0
    for token in tokens:
        d, l = parseToken(token)
        dx, dy = DIRS[d][0], DIRS[d][1]
        for _ in range(l):
           x += dx
           y += dy
           n += 1
           path.add((x, y, n))
    return path

def populatePathDict(p):
    result = {}
    for x, y, n in p:
        result[(x, y)] = n if (x, y) not in result else min(n, result[x, y])
    return result

p1, p2 = populatePath(w1), populatePath(w2)
d1, d2 = populatePathDict(p1), populatePathDict(p2)
minDistance, minSteps = len(p1) + len(p2), len(p1) + len(p2) #anything bigger than all the n will do
intersections = d1.keys() & d2.keys()
for intersection in intersections:
    if (distance := abs(intersection[0]) + abs(intersection[1])) < minDistance:
        minDistance = distance
    if (steps := d1[intersection] + d2[intersection]) < minSteps:
        minSteps = steps
print(minDistance, minSteps)