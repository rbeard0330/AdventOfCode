from intcode import IntcodeProgram
from itertools import permutations

with open('nate/inputs/in7.txt', 'r') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

def thrusterSignal(code, phaseSettingSequence):
    assert len(phaseSettingSequence) == 5
    for item in phaseSettingSequence:
        assert type(item) == int
    program = IntcodeProgram(code, [phaseSettingSequence[0], 0])
    for phaseSetting in phaseSettingSequence[1:]:
        program.runUntilStop()
        temp = program.outputStream[0]
        program = IntcodeProgram(code, [phaseSetting, temp])
    program.runUntilStop()
    return program.outputStream[0]

def maxThrusterSignal(code):
    biggest = 0
    for x in permutations(range(5)):
        if (curr := thrusterSignal(code, list(x))) > biggest:
            biggest = curr
    return biggest

print(maxThrusterSignal(code))