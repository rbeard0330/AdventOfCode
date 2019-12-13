from intcode import IntcodeProgram, intcodeLoad

seq = intcodeLoad(13)

def display(stream):
    screen = {}
    for ix in range(0, len(stream), 3):
        screen[(program.outputStream[ix], program.outputStream[ix+1])] = program.outputStream[ix+2]
    xVals, yVals = [i[0] for i in screen.keys()], [i[1] for i in screen.keys()]
    minX, maxX, minY, maxY = min(xVals), max(xVals), min(yVals), max(yVals)
    for y in range(minY, maxY+1):
        print(''.join([str(screen.get((x, y),'?')) for x in range(minX, maxX+1)]))
    print(screen.get((-1, 0), '?'))
        
program = IntcodeProgram(seq)
program.runUntilStop()
screen = {}
for ix in range(0, len(program.outputStream), 3):
    screen[(program.outputStream[ix], program.outputStream[ix+1])] = program.outputStream[ix+2]
print(sum([1 for k, v in screen.items() if v == 2]))
display(program.outputStream.copy())