OP = {1 : 'ADD', 2 : 'MULT', 99 : 'STOP'}

with open('inputs/in2.txt') as f:
    code = [int(i) for i in f.readline().strip().split(',')]

fixed_code = tuple(code) # to reset in part B

def runIntcode(code):
    ix = 0
    op = OP[code[ix]]
    while op != 'STOP':
        if op == 'ADD':
            code[code[ix + 3]] = code[code[ix + 2]] + code[code[ix + 1]]
        else:
            assert op == 'MULT'
            code[code[ix + 3]] = code[code[ix + 2]] * code[code[ix + 1]]
        ix += 4
        op = OP[code[ix]]
    return code[0]

def nounVerbGenerator():
    '''Quick convenience generator for part B'''
    for a in range(100):
        for b in range(100):
            yield a, b

# as per instructions
code[1] = 12
code[2] = 2

print(runIntcode(code))

# Part B

TARGET = 19690720

result = None

g = nounVerbGenerator()
while result != TARGET:
    noun, verb = next(g)
    memory = list(fixed_code)
    memory[1] = noun
    memory[2] = verb
    result = runIntcode(memory)

print(100 * noun + verb)