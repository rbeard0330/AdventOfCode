def add(tape, ad1, ad2, ad3):
    tape[ad3] = tape[ad1] + tape[ad2]


def mult(tape, ad1, ad2, ad3):
    tape[ad3] = tape[ad1] * tape[ad2]


def run(input1, input2):

    tape = initialize_tape()
    head_pos = 0
    tape[1] = input1
    tape[2] = input2
    while True:
        code = tape[head_pos]
        if code == 1:
            add(tape, *tape[head_pos + 1: head_pos + 4])
            head_pos += 4
        elif code == 2:
            mult(tape, *tape[head_pos + 1: head_pos + 4])
            head_pos += 4
        elif code == 99:
            return tape[0]
        else:
            raise OSError


def initialize_tape():
    return [int(n) for n in """1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,
    19,23,1,10,23,27,2,27,13,31,1,31,6,35,2,6,35,39,1,39,5,43,1,6,43,47,2,6,47,
    51,1,51,5,55,2,55,9,59,1,6,59,63,1,9,63,67,1,67,10,71,2,9,71,75,1,6,75,79,
    1,5,79,83,2,83,10,87,1,87,5,91,1,91,9,95,1,6,95,99,2,99,10,103,1,103,5,107,
    2,107,6,111,1,111,5,115,1,9,115,119,2,119,10,123,1,6,123,127,2,13,127,131,
    1,131,6,135,1,135,10,139,1,13,139,143,1,143,13,147,1,5,147,151,1,151,2,155,
    1,155,5,0,99,2,0,14,0""".replace('\n', '').split(',')]


def seek_target(n):
    for i in range(100):
        for j in range(100):
            result = run(i, j)
            if result == n:
                return (i, j)
    return False


i, j = seek_target(19690720)
print(100*i + j)
