with open('nate/inputs/in6.txt', 'r') as f:
    orbits = [l.strip() for l in f.readlines()]

def parseOrbit(token):
    assert ')' in token
    a, b = token.split(')')
    return a, b

d = {}
rev = {}
for a, b in map(parseOrbit, orbits):
    d[a] = d.get(a, []) + [b]
    rev[b] = a # useful for part B

# BFS

curr = 'COM'
numOrbits = {'COM' : 0}
fringe = d[curr]
for thing in fringe:
    numOrbits[thing] = 1
while fringe:
    curr = fringe.pop()
    fringe = d.get(curr, []) + fringe
    for thing in d.get(curr, []):
        numOrbits[thing] = numOrbits[curr] + 1

print(sum(numOrbits.values()))

# Also do BFS to find the shortest path
for thing in d:
    if 'YOU' in d[thing]:
        origin = thing
    if 'SAN' in d[thing]:
        target = thing
# walk back to COM from the target
curr = target
i = 1
stepsFromTarget = {}
while curr != 'COM':
    curr = rev[curr]
    stepsFromTarget[curr] = i
    i += 1
# walk back to COM from the origin
curr = origin
i = 0
while curr not in stepsFromTarget:
    curr = rev[curr]
    i += 1
print(i + stepsFromTarget[curr])