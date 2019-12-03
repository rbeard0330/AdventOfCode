OP = {1 : 'ADD', 2 : 'MULT', 99 : 'STOP'}

def nounVerbGenerator():
    '''Quick convenience generator for part B'''
    for a in range(100):
        for b in range(100):
            yield a, b

def add(l, ix):
    l[l[ix+3]] = l[l[ix+2]] + l[l[ix+1]]
    return ix + 4, False

def multiply(l, ix):
    l[l[ix+3]] = l[l[ix+2]] * l[l[ix+1]]
    return ix + 4, False

def stop(l, ix):
    return ix, True

class IntcodeProgram:
    '''A class for representing the sorts of programs
    we find in AoC 2019 problem 2'''

    ops = {1 : add, # adding
           2 : multiply, # multiplying
           99 : stop,
           }

    def __init__(self, seq, noun=12, verb=2, ix=0):
        self.seq = seq.copy()
        self.init_seq = tuple(seq) # freeze the initial sequence
        self.noun = noun
        self.verb = verb
        self.ix = ix
    
    def processCurrentOp(self):
        '''Returns whether to stop'''
        assert (curr := self.seq[self.ix]) in self.ops
        self.ix, stop = self.ops[curr](self.seq, self.ix) # this mutates the list
        return stop
    
    def runUntilStop(self, returnIndex=0):
        self.seq[1] = self.noun
        self.seq[2] = self.verb
        while not self.processCurrentOp():
            pass
        return self.seq[returnIndex]
    
    def reset(self, noun, verb):
        self.ix = 0
        self.seq = list(self.init_seq)
        self.noun = noun
        self.verb = verb

with open('inputs/in2.txt') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

program = IntcodeProgram(code)
print(program.runUntilStop()) # part 1

TARGET = 19690720
for noun in range(100):
    for verb in range(100):
        program.reset(noun, verb)
        if (curr := program.runUntilStop()) == TARGET:
            print(100 * noun + verb)
            break