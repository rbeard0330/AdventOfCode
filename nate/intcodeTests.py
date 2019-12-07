from intcode import IntcodeProgram
    
#Testing jumps
seq = [int(i) for i in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(',')]
program = IntcodeProgram(seq, 0)
print("SHOULD OUTPUT 0 [jump test]:")
program.runUntilStop() # should output zero
program = IntcodeProgram(seq, 3)
print("SHOULD OUTPUT 1 [jump test]:")
program.runUntilStop()