with open('nate/inputs/in5.txt') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

currInput = 5

def nounVerbGenerator():
    '''Quick convenience generator for part B'''
    for a in range(100):
        for b in range(100):
            yield a, b

def add(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 3 #account for implicit zeroes (extras don't hurt, right?)
    firstAddend = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    secondAddend = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    assert modes[2] == '0' # output value never in immediate mode
    l[l[ix+3]] = firstAddend + secondAddend
    return ix + 4, False

def multiply(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 3 #account for implicit zeroes (extras don't hurt, right?)
    firstFactor = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    secondFactor = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    assert modes[2] == '0' # output value never in immediate mode
    l[l[ix+3]] = firstFactor * secondFactor
    return ix + 4, False

def jumpIfTrue(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 3 #account for implicit zeroes (extras don't hurt, right?)
    comparisonValue = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    setValue = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    return (setValue if comparisonValue else ix + 3), False

def jumpIfFalse(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 3 #account for implicit zeroes (extras don't hurt, right?)
    comparisonValue = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    setValue = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    return (setValue if not comparisonValue else ix + 3), False

def lessThan(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 4 #account for implicit zeroes (extras don't hurt, right?)
    leftSide = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    rightSide = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    assert modes[3] == '0'
    l[l[ix+3]] = 1 if leftSide < rightSide else 0
    return (ix + 4), False

def equalTo(l, ix, modes):
    modes = [str(i) for i in modes] + ['0'] * 4 #account for implicit zeroes (extras don't hurt, right?)
    leftSide = l[l[ix+1]] if modes[0] == '0' else l[ix+1]
    rightSide = l[l[ix+2]] if modes[1] == '0' else l[ix+2]
    assert modes[3] == '0'
    l[l[ix+3]] = 1 if (leftSide == rightSide) else 0
    return (ix + 4), False

def takeInput(l, ix, modes, inputValue = currInput):
    modes = [str(i) for i in modes] + ['0']
    assert modes[0] == '0', modes[0]
    l[l[ix+1]] = inputValue
    return ix + 2, False

def makeOutput(l, ix, modes): # for now, just print the output
    outputValue = l[l[ix+1]]
    print("OUTPUT: " + str(outputValue))
    return ix + 2, False

def stop(l, ix, modes):
    return ix, True

def parseOp(n):
    opcode = n % 100
    modes = [int(char) for char in str(int(n / 100))[::-1]]
    return opcode, modes
        
class IntcodeProgram:
    '''A class for representing the sorts of programs
    we find in AoC 2019 problem 2'''

    ops = {
           1 : add, # adding
           2 : multiply, # multiplying
           3 : takeInput,
           4 : makeOutput,
           5 : jumpIfTrue,
           6 : jumpIfFalse,
           7 : lessThan,
           8 : equalTo,
           99 : stop,
           }

    def __init__(self, seq, inputCode = 1, noun=12, verb=2, ix=0):
        self.seq = seq.copy()
        self.init_seq = tuple(seq) # freeze the initial sequence
        self.inputCode = inputCode
        self.noun = noun
        self.verb = verb
        self.ix = ix
    
    def processCurrentOp(self):
        '''Returns whether to stop'''
        opcode, modes = parseOp(self.seq[self.ix])
        assert opcode in self.ops
        self.ix, stop = self.ops[opcode](self.seq, self.ix, modes) # this mutates the list
        return stop
    
    def runUntilStop(self, returnIndex=0):
        # self.seq[1] = self.noun
        # self.seq[2] = self.verb
        while not self.processCurrentOp():
            pass
        return self.seq[returnIndex]
    
    def reset(self, noun, verb):
        self.ix = 0
        self.seq = list(self.init_seq)
        self.noun = noun
        self.verb = verb

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
    test1()
    test2()
    test3()
    prog = IntcodeProgram(code)
    prog.runUntilStop()
