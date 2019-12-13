import numpy as np

with open('nate/inputs/in12.txt', 'r') as f:
    planets = [l.strip() for l in f.readlines()]

for ix, planet in enumerate(planets):
    planets[ix] = [int(i.split('=')[1].strip('>')) for i in planet.split(',')]

velocities = [[0] * 3 for _ in range(len(planets))]
#update velocity
def update(planets, velocities):
    for axis in range(len(planets[0])):
        for ix1, planet1 in enumerate(planets):
            for ix2, planet2 in enumerate(planets):
                if ix2 > ix1:
                    v1, v2 = planet1[axis], planet2[axis]
                    if v1 < v2:
                        velocities[ix1][axis] += 1
                        velocities[ix2][axis] -= 1
                    elif v2 < v1:
                        velocities[ix1][axis] -= 1
                        velocities[ix2][axis] += 1

    # update position
    for ix in range(len(planets)):
        planets[ix] = [planets[ix][i] + velocities[ix][i] for i in range(len(planets[ix]))]

def KE(planet_velocity):
    return sum([abs(v) for v in planet_velocity])

def PE(planet_position):
    return sum([abs(i) for i in planet_position])

def totE(p, v):
    return sum([PE(p) * KE(v) for p, v in zip(p, v)])

def pickle(p, v):
    temp = []
    for planet in p:
        temp += planet
    for velocity in v:
        temp += velocity
    return tuple(temp)

def periodOfCoordinate(planets, velocities):
    assert len(planets[0]) == 1
    seen = set()
    temp = None
    while temp not in seen:
        seen.add(temp)
        update(planets, velocities)
        temp = pickle(planets, velocities)
        # for ix, planet in enumerate(planets):
         #   print(planet, velocities[ix], ke := KE(velocities[ix]), pe := PE(planet), ke * pe)
        #print('===')
    return(len(seen) - 1)

periods = []
for ix in range(len(planets[0])):
    tempP, tempV = [[i[ix]] for i in planets], [[i[ix]] for i in velocities]
    periods.append(periodOfCoordinate(tempP, tempV))
temp = periods[0]
for period in periods:
    temp = np.lcm(temp, period)
print(periods)
print(temp) # having overflow issues
# Here I went to an online LCM calculator