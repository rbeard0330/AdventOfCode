def getParams(l, ix, modes, numParams):
    '''Given the current sequence <l>
    and the current index <ix>
    and the explicit modes <modes>
    and the number of parameters taken by the op <numParams>,
    returns the parameter values.'''
    result = []
    for i in range(numParams):
        try:
            result.append(l[ix+i+1] if modes[i] == 1 else l[l[ix+i+1]])
        except:
            result.append(l[l[ix+i+1]])
    return result, l[ix+numParams] # for cases where you need to jump / write

def add(l, ix, modes):
    values, toWrite = getParams(l, ix, modes, 3)
    s = values[0] + values[1]
    l[toWrite] = s
    return ix + 4, False

def multiply(l, ix, modes):
    values, toWrite = getParams(l, ix, modes, 3)
    s = values[0] * values[1]
    l[toWrite] = s
    return ix + 4, False

def jumpIfTrue(l, ix, modes):
    values, _ = getParams(l, ix, modes, 2)
    return (values[1] if values[0] else ix + 3), False

def jumpIfFalse(l, ix, modes):
    values, _ = getParams(l, ix, modes, 2)
    return (values[1] if not values[0] else ix + 3), False

def lessThan(l, ix, modes):
    values, toWrite = getParams(l, ix, modes, 3)
    l[toWrite] = 1 if values[0] < values[1] else 0
    return (ix + 4), False

def equalTo(l, ix, modes):
    values, toWrite = getParams(l, ix, modes, 3)
    l[toWrite] = 1 if values[0] == values[1] else 0
    return (ix + 4), False

def takeInput(l, ix, modes, inputValue):
    _, toWrite = getParams(l, ix, modes, 1)
    l[toWrite] = inputValue
    return ix + 2, False

def makeOutput(l, ix, modes): # for now, just print the output
    _, toOutput = getParams(l, ix, modes, 1)
    outputValue = l[toOutput]
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

    def __init__(self, seq, inputCode = 1, ix=0):
        self.seq = seq.copy()
        self.init_seq = tuple(seq) # freeze the initial sequence
        self.inputCode = inputCode
        self.ix = ix
    
    def processCurrentOp(self):
        '''Returns whether to stop'''
        opcode, modes = parseOp(self.seq[self.ix])
        assert opcode in self.ops
        if opcode != 3:
            self.ix, stop = self.ops[opcode](self.seq, self.ix, modes) # this mutates the list
        else:
            self.ix, stop = self.ops[opcode](self.seq, self.ix, modes, self.inputCode) # this mutates the list
        return stop
    
    def runUntilStop(self, returnIndex=0):
        while not self.processCurrentOp():
            pass
        return self.seq[returnIndex]