with open('nate/inputs/in5.txt') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

from intcode import IntcodeProgram

def test1():
    testProgram = [3, 0, 4, 0, 99]
    prog = IntcodeProgram(testProgram)
    prog.runUntilStop() # should output 1

def test2():
    testProgramB = [int(i) for i in '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,\
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,\
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'.split(',')]
    prog = IntcodeProgram(testProgramB)
    prog.runUntilStop()

def test3():
    testProgramC = [int(i) for i in '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'.split(',')]
    prog = IntcodeProgram(testProgramC, 10)
    prog.runUntilStop() # should output 1
    prog = IntcodeProgram(testProgramC, 0)
    prog.runUntilStop() # should output 0

if __name__=='__main__':
    prog = IntcodeProgram(code, 5)
    prog.runUntilStop()
