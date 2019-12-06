import os.path
from copy import copy


class Instruction():

    def __init__(self, tape_ref, execution_f, parsing_f, reposition_f):
        self.tape = tape_ref
        self.exec_f = execution_f
        self.parsing_f = parsing_f
        self.pos_f = reposition_f


class AdvancedIntcoder():

    def __init__(self, tape, input_queue):
        self.tape = tape
        self.master = copy(tape)
        self.instructs = {
            1:  (self.add_and_store,
                 self.build_parser(3, store=True),
                 self.build_positioner(3)),

            2:  (self.mult_and_store,
                 self.build_parser(3, store=True),
                 self.build_positioner(3)),

            3:  (self.store_input,
                 self.build_parser(1, store=True),
                 self.build_positioner(1)),

            4:  (self.output,
                 self.build_parser(1, store=True),
                 self.build_positioner(1)),

            5:  (self.jump_if_true,
                 self.build_parser(2, store=False),
                 lambda _: _),  # Null function

            6:  (self.jump_if_false,
                 self.build_parser(2, store=False),
                 lambda _: _),  # Null function

            7:  (self.less_than,
                 self.build_parser(3, store=True),
                 self.build_positioner(3)),

            8:  (self.equals,
                 self.build_parser(3, store=True),
                 self.build_positioner(3)),
        }
        self.halts = [99]
        self.pos = 0
        self.input_queue = input_queue

    def build_parser(self, param_count, store=False):
        """Return parameter-parsing function.

        store - If True, last paramater is storage address.
        """
        def parse(self, mode_str):
            # Add leading zeroes
            length = len(mode_str)
            if (to_add := (param_count - length)) > 0:
                mode_str = "0" * to_add + mode_str
            mode_list = [int(c) for c in mode_str[::-1]]
            data_list = []
            n = param_count - 1 if store else param_count
            for i in range(n):
                mode = mode_list[i]
                if mode:
                    data_list.append(self.tape[self.pos + i + 1])
                else:
                    data_list.append(self.tape[self.tape[self.pos + i + 1]])
            if store:
                data_list.append(self.tape[self.pos + param_count])
            return data_list

        return parse

    def build_positioner(self, to_advance):

        def pos(self):
            self.pos += to_advance + 1

        return pos

    def run(self, start_pos=0, return_pos=0, edits=()):

        self.tape = copy(self.master)
        for addr, val in edits:
            self[addr] = val
        self.pos = start_pos

        while self.data[0] not in self.halts:
            exec_f, param_f, pos_f = self.instructs[self.data[0]]
            f_inputs = param_f(self, self.data[1])
            exec_f(*f_inputs)
            pos_f(self)

    def add_and_store(self, addend1, addend2, store_addr):
        self.tape[store_addr] = addend1 + addend2

    def mult_and_store(self, mult1, mult2, store_addr):
        self.tape[store_addr] = mult1 * mult2

    def store_input(self, addr):
        self.tape[addr] = self.input_queue.pop(0)

    def output(self, addr):
        print(f"OUTPUT ADDRESS {addr}: {self.tape[addr]}")

    def jump_if_true(self, arg1, arg2):
        if arg1 != 0:
            self.pos = arg2
        else:
            self.pos += 3

    def jump_if_false(self, arg1, arg2):
        if arg1 == 0:
            self.pos = arg2
        else:
            self.pos += 3

    def less_than(self, arg1, arg2, arg3):
        if arg1 < arg2:
            self.tape[arg3] = 1
        else:
            self.tape[arg3] = 0

    def equals(self, arg1, arg2, arg3):
        if arg1 == arg2:
            self.tape[arg3] = 1
        else:
            self.tape[arg3] = 0

    def null_func(self, *args, **kwargs):
        pass

    @property
    def data(self):
        s = str(self[self.pos])
        instruct_code = int(s[-2:])
        if instruct_code in self.halts:
            return [instruct_code]
        modes = s[:-2]
        return (instruct_code, modes)

    def __getitem__(self, key):
        return self.tape[key]

    def __setitem__(self, key, val):
        self.tape[key] = val


s_tape = []
file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d5p1.txt")
with open(file_name, "r") as f:
    for line in f.readlines():
        s_tape += line.split(",")
tape = [int(s) for s in s_tape]

print("Part 1:")
AdvancedIntcoder(copy(tape), [1]).run()
print("Part 2:")
AdvancedIntcoder(tape, [5]).run()
