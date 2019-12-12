def intcodeLoad(path, outputType = 'seq'):
    '''Given a path to a file containing an Intcode program,
    returns the sequence as a list suitable for initializing
    an IntcodeProgram (optionally just returns the program)'''
    if type(path) == int or path.isnumeric() or path[:-1].isnumeric(): # accept "12" or "12c"
        path = f'inputs/in{path}.txt'
    try:
        with open(path, 'r') as f:
            seq = [int(i) for i in f.readline().strip().split(',')]
    except:
        with open('nate/' + path, 'r') as f:
            seq = [int(i) for i in f.readline().strip().split(',')]
    return seq

class IntcodeProgram:
    '''See Advent of Code 2019, days 2, 5, and 9'''

    def __init__(self, seq, inputStream = [], ix=0):
        self.seq = {ix : v for ix, v in enumerate(seq)}
        self.inputStream = inputStream
        self.outputStream = []
        self.ix = ix
        self.relativeBase = 0
    
    def getParams(self, modes, numParams):
        '''Given the current sequence <l>
        and the current index <ix>
        and the explicit modes <modes>
        and the number of parameters taken by the op <numParams>,
        returns the parameter values.'''
        result = []
        for i in range(numParams):
            curr = modes[i] if i < len(modes) else 0
            if curr == 0:
                result.append(self.seq.get(self.seq.get(self.ix+i+1, 0), 0))
            elif curr == 1:
                result.append(self.seq.get(self.ix+i+1, 0))
            elif curr == 2:
                result.append(self.seq.get(self.seq.get(self.ix+i+1,0) + self.relativeBase, 0))
            else:
                raise ValueError(f"Didn't understand param {curr} [{type(curr)}].")
        return result, self.seq.get(self.ix+numParams, 0) + (0 if curr != 2 else self.relativeBase) # the latter for writing instructions

    def add(self, modes):
        values, toWrite = self.getParams(modes, 3)
        s = values[0] + values[1]
        self.seq[toWrite] = s
        self.ix += 4
        return False # doesn't halt

    def multiply(self, modes):
        values, toWrite = self.getParams(modes, 3)
        s = values[0] * values[1]
        self.seq[toWrite] = s
        self.ix += 4
        return False # doesn't halt

    def jumpIfTrue(self, modes):
        values, _ = self.getParams(modes, 2)
        self.ix = (values[1] if values[0] else self.ix + 3)
        return False

    def jumpIfFalse(self, modes):
        values, _ = self.getParams(modes, 2)
        self.ix = (values[1] if not values[0] else self.ix + 3)
        return False

    def lessThan(self, modes):
        values, toWrite = self.getParams(modes, 3)
        self.seq[toWrite] = 1 if values[0] < values[1] else 0
        self.ix += 4
        return False

    def equalTo(self, modes):
        values, toWrite = self.getParams(modes, 3)
        self.seq[toWrite] = 1 if values[0] == values[1] else 0
        self.ix += 4
        False

    def takeInput(self, modes):
        _, toWrite = self.getParams(modes, 1)
        self.seq[toWrite] = self.inputStream.pop(0)
        self.ix += 2
        return False

    def makeOutput(self, modes):
        result, _ = self.getParams(modes, 1)
        self.outputStream.append(result[-1])
        self.ix += 2
        return False

    def modifyRelativeBase(self, modes):
        params, _ = self.getParams(modes, 1)
        self.relativeBase += params[0]
        self.ix += 2
        return False

    def stop(self, modes):
        return True

    def parseOp(self, n):
        opcode = n % 100
        modes = [int(char) for char in str(int(n / 100))[::-1]]
        return opcode, modes
            
    ops = {
           1 : add,
           2 : multiply,
           3 : takeInput,
           4 : makeOutput,
           5 : jumpIfTrue,
           6 : jumpIfFalse,
           7 : lessThan,
           8 : equalTo,
           9 : modifyRelativeBase,
           99 : stop,
           }

    def processCurrentOp(self):
        '''Returns whether to stop'''
        opcode, modes = self.parseOp(self.seq[self.ix])
        assert opcode in self.ops
        stop = self.ops[opcode](self, modes) # this changes a lot of self's internal state
        return stop
    
    def runUntilStop(self, returnIndex=0):
        while not self.processCurrentOp():
            pass
        return self.seq[returnIndex]
    
    def runUntilOutput(self):
        '''returns an output and a program'''
        while not self.processCurrentOp():
            if self.outputStream:
                return self.outputStream, IntcodeProgram(self.seq.copy(), self.inputStream.copy(), self.ix)