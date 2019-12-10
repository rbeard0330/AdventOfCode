from intcode import IntcodeProgram

with open('nate/inputs/in9.txt', 'r') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

program = IntcodeProgram(code, [1])
program.runUntilOutput()
print(program.outputStream[0])
program = IntcodeProgram(code, [2])
program.runUntilOutput()
print(program.outputStream[0])