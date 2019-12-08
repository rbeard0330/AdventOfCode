from intcode import IntcodeProgram
from d7 import thrusterSignal, maxThrusterSignal, runToLastOutput, getMaxOutput

#Testing jumps
seq = [int(i) for i in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(',')]
program = IntcodeProgram(seq, [0])
program.runUntilStop() # should output zero
assert program.outputStream == [0]
program = IntcodeProgram(seq, [3])
program.runUntilStop()
assert program.outputStream == [1], program.outputStream

#Testing the thruster signal
seq = [int(i) for i in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(',')]
assert (result := thrusterSignal(seq, [4, 3, 2, 1, 0])) == 43210, result 
assert (result := maxThrusterSignal(seq)) == 43210, result

#Testing the boosted chains thing
seq = [int(i) for i in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,\
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(',')]
assert (result := runToLastOutput(seq, [9, 8, 7, 6, 5])) == 139629729, result
assert (result := getMaxOutput(seq)) == 139629729, result