from copy import copy
import math

import decorators


class GenericIntcoder:
    def __init__(self, tape, instructs, halts):
        self.tape = tape
        self.master = copy(tape)
        self.instructs = instructs
        self.halts = halts
        self.cache = dict()
        self.pos = 0

    def start(self, start_pos=0, return_pos=0, edits=(), caching=False):
        self.tape = copy(self.master)
        for addr, val in edits:
            self[addr] = val
        self.pos = start_pos

        while self.data not in self.halts:
            f, param_count = self.instructs[self.data]
            params = self.get_params(param_count)
            f_inputs = [self[i] for i in params[:-1]]
            if not caching:
                self[params[-1]] = f(f_inputs)
            else:
                key = (self.data, *f_inputs)
                if key in self.cache:
                    self[params[-1]] = self.cache[key]
                else:
                    self[params[-1]] = val = f(f_inputs)
                    self.cache[key] = val
            self.pos += param_count + 1

        return self[return_pos]

    def get_params(self, n):
        return self.tape[self.pos + 1: self.pos + 1 + n]

    @property
    def data(self):
        return self[self.pos]

    def __getitem__(self, key):
        return self.tape[key]

    def __setitem__(self, key, val):
        self.tape[key] = val


def add(*args):
    return sum(args)


def mult(*args):
    return math.prod(args)


@decorators.timer
def main(n):
    tape = [int(n) for n in """1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,
    19,23,1,10,23,27,2,27,13,31,1,31,6,35,2,6,35,39,1,39,5,43,1,6,43,47,2,6,47,
    51,1,51,5,55,2,55,9,59,1,6,59,63,1,9,63,67,1,67,10,71,2,9,71,75,1,6,75,79,
    1,5,79,83,2,83,10,87,1,87,5,91,1,91,9,95,1,6,95,99,2,99,10,103,1,103,5,107,
    2,107,6,111,1,111,5,115,1,9,115,119,2,119,10,123,1,6,123,127,2,13,127,131,
    1,131,6,135,1,135,10,139,1,13,139,143,1,143,13,147,1,5,147,151,1,151,2,155,
    1,155,5,0,99,2,0,14,0""".replace('\n', '').split(',')]
    instruction_set = {
        1:  (sum, 3),
        2:  (math.prod, 3)
    }
    halts = [99]
    intcomp = GenericIntcoder(tape, instruction_set, halts)

    # Part 1
    edits = [
        (1, 12),
        (2, 2),
    ]
    print(intcomp.start(edits=edits))

    # Part 2
    def seek(n):
        for i in range(100):
            for j in range(100):
                edits = [
                    (1, i),
                    (2, j)
                ]
                if intcomp.start(edits=edits) == n:
                    return (i, j)
        return (0, 0)

    i, j = seek(19690720)
    print(100*i + j)
    return True


if __name__ == "__main__":
    main(1)
