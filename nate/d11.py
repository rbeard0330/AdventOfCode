from intcode import IntcodeProgram

with open('nate/inputs/in11.txt', 'r') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # U, R, D, L
coord = (0, 0)
colors = {}
currDir = 0 # index within DIRS

robot = IntcodeProgram(code, [1])
robot.runUntilOutput()
robot.runUntilOutput()
o0 = robot.outputStream.pop(0)
o1 = robot.outputStream.pop(0)
while True:
    assert o0 in (0, 1)
    assert o1 in (0, 1)
    colors[coord] = o0
    currDir = (currDir + 1) % 4 if o1 else (currDir - 1) % 4
    dx, dy = DIRS[currDir]
    coord = (coord[0] + dx, coord[1] + dy)
    robot.inputStream.append(colors.get(coord, 0))
    try:
        robot.runUntilOutput()
        o0 = robot.outputStream.pop(0)
        robot.runUntilOutput()
        o1 = robot.outputStream.pop(0)
    except:
        minX = min([i[0] for i in colors.keys()])
        maxX = max([i[0] for i in colors.keys()])
        minY = min([i[1] for i in colors.keys()])
        maxY = max([i[1] for i in colors.keys()])
        for y in range(minY-1, maxY+2):
            # will print upside-down
            print(''.join(['X' if colors.get((x, y), 0) != 0 else ' ' for x in range(minX-1, maxX + 2)]))
        break

coord = (0, 0)
colors = {}
currDir = 0 # index within DIRS
robot = IntcodeProgram(code, [0])
robot.runUntilOutput()
robot.runUntilOutput()
o0 = robot.outputStream.pop(0)
o1 = robot.outputStream.pop(0)
while True:
    assert o0 in (0, 1)
    assert o1 in (0, 1)
    colors[coord] = o0
    currDir = (currDir + 1) % 4 if o1 else (currDir - 1) % 4
    dx, dy = DIRS[currDir]
    coord = (coord[0] + dx, coord[1] + dy)
    robot.inputStream.append(colors.get(coord, 0))
    try:
        robot.runUntilOutput()
        o0 = robot.outputStream.pop(0)
        robot.runUntilOutput()
        o1 = robot.outputStream.pop(0)
    except:
        break

print(len(colors))