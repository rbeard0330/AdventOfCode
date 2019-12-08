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

def iterateChain(programs):
    '''Given a (chained) list of programs,
    returns the list, with some program updated'''
    for ix in range(len(programs)):
        if programs[ix].inputStream:
            output, program = programs[ix].runUntilOutput()
            nextIx = (ix + 1) % len(programs)
            programs[nextIx].inputStream.append(output[0])
            programs[ix] = program
            return output[0], programs # keep track of the last output
    return False

def initChain(code, phaseSettings, n=5):
    programs = [IntcodeProgram(code, [phaseSettings[i]]) for i in range(n)]
    programs[0].inputStream.append(0)
    return programs

def runToLastOutput(code, phaseSettings, n=5):
    chain = initChain(code, phaseSettings)
    lastOutput = None
    while chain:
        try:
            lastOutput, chain = iterateChain(chain)
        except:
            return lastOutput

def getMaxOutput(code, signals = (5, 6, 7, 8, 9), n=5):
    biggest = -9999 #sloppy
    for p in permutations(signals):
        if (temp := runToLastOutput(code, list(p))) > biggest:
            biggest = temp
    return biggest

print(getMaxOutput(code))