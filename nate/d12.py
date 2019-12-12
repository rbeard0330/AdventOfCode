with open('nate/inputs/in12.txt', 'r') as f:
    planets = [l.strip() for l in f.readlines()]

for ix, planet in enumerate(planets):
    planets[ix] = [int(i.split('=')[1].strip('>')) for i in planet.split(',')]
