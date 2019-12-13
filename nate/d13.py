from intcode import IntcodeProgram, intcodeLoad

seq = intcodeLoad(13)

program = IntcodeProgram(seq)
program.runUntilStop()
screen = {}
for ix in range(0, len(program.outputStream), 3):
    screen[(program.outputStream[ix], program.outputStream[ix+1])] = program.outputStream[ix+2]
print(sum([1 for k, v in screen.items() if v == 2]))