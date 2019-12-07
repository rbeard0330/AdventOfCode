from intcode import IntcodeProgram
from d7 import thrusterSignal, maxThrusterSignal

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