from copy import copy
import math

from .file_ops import get_input_file_name


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


class AdvancedIntcoder():

    def __init__(self, tape, input_queue):
        self.master = copy(tape)
        self.instructs = {

            1:  (self.add_and_store,
                 self.build_parser(3, store_in_last=True),
                 self.build_positioner(3)),

            2:  (self.mult_and_store,
                 self.build_parser(3, store_in_last=True),
                 self.build_positioner(3)),

            3:  (self.try_to_store_input,
                 self.build_parser(1, store_in_last=True),
                 self.build_positioner(1)),

            4:  (self.output,
                 self.build_parser(1, store_in_last=True),
                 self.build_positioner(1)),

            5:  (self.jump_if_true,
                 self.build_parser(2, store_in_last=False),
                 lambda _: _),  # Null function

            6:  (self.jump_if_false,
                 self.build_parser(2, store_in_last=False),
                 lambda _: _),  # Null function

            7:  (self.less_than,
                 self.build_parser(3, store_in_last=True),
                 self.build_positioner(3)),

            8:  (self.equals,
                 self.build_parser(3, store_in_last=True),
                 self.build_positioner(3)),

            9:  (self.adjust_relative_base,
                 self.build_parser(1, store_in_last=False),
                 self.build_positioner(1)),

            99: (self.halt,
                 lambda *args, **kwargs: [None],
                 lambda *args, **kwargs: [None])
        }
        self.reset(input_queue, clear_tape=True)

    def reset(self, input_queue, clear_tape=False):
        if clear_tape:
            self.tape = copy(self.master)
        self.op_status = {"halted": False, "need input": False}
        self.pos = 0
        self.input_queue = input_queue
        self.storage_address = None
        self.relative_base = 0

    # ----------Factory Methods for Processing Ops---------

    def build_parser(self, param_count, store_in_last=False):
        """Return parameter-parsing function.

        Parameters for storing the results of operations are handled
        differently from data parameters.  For data parameters, this method
        looks up the data from the relevant addresses (in relative/position
        mode).  For storage parameters, the target address is return.

        store_in_last - If True, last paramater is a storage address.
        """

        def parse(self, mode_str):

            # Normalize number of modes to param_count
            length = len(mode_str)
            if (to_add := (param_count - length)) > 0:
                mode_str = "0" * to_add + mode_str

            mode_list = [int(c) for c in mode_str[::-1]]
            data_list = []
            data_params = param_count - 1 if store_in_last else param_count
            for i in range(1, data_params + 1):
                mode = mode_list[i - 1]
                raw_data = self[self.pos + i]
                if mode == 0:       # Position mode
                    data_list.append(self[raw_data])
                elif mode == 1:     # Immediate mode
                    data_list.append(raw_data)
                elif mode == 2:     # Relative mode
                    data_list.append(self[raw_data + self.relative_base])
                else:
                    raise ValueError(f"Unsupported mode at {self.pos}: {mode}")
            if store_in_last:
                raw_data = self[self.pos + param_count]
                if mode_list[-1] == 0:      # Position mode
                    data_list.append(raw_data)
                elif mode_list[-1] == 2:    # Relative mode
                    data_list.append(raw_data + self.relative_base)
                else:                      # Immediate mode invalid for storage
                    raise ValueError(f"Unsupported mode for storage parameter"
                                     f"at {self.pos}: {mode_list[-1]}")
            return data_list

        return parse

    def build_positioner(self, to_advance):

        def pos(self):
            self.pos += to_advance + 1

        return pos

    # --------------Instructions------------------

    def add_and_store(self, addend1, addend2, store_addr):
        self[store_addr] = addend1 + addend2

    def mult_and_store(self, mult1, mult2, store_addr):
        self[store_addr] = mult1 * mult2

    def try_to_store_input(self, addr):
        # Note that the positioner function runs after this method, even if
        # there was no input to process.

        if self.input_queue:
            self.tape[addr] = self.input_queue.pop(0)
        else:
            assert self.storage_address is None
            self.storage_address = addr
            self.op_status["need input"] = True

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

    def less_than(self, arg1, arg2, addr):
        if arg1 < arg2:
            self[addr] = 1
        else:
            self[addr] = 0

    def equals(self, arg1, arg2, addr):
        if arg1 == arg2:
            self[addr] = 1
        else:
            self[addr] = 0

    def adjust_relative_base(self, arg1):
        self.relative_base += arg1

    def halt(self, *args, **kwargs):
        self.op_status["halted"] = True

    # -------------Core Loop-----------------------------

    def run(self, start_pos=0, return_pos=0, edits=(), reset=False):

        if reset:
            self.tape = copy(self.master)
            for addr, val in edits:
                self[addr] = val
            self.pos = start_pos

        while self.valid_run_status:
            exec_f, param_f, pos_f = self.instructs[self.data[0]]
            f_inputs = param_f(self, self.data[-1])
            exec_f(*f_inputs)
            pos_f(self)

    # ------------Internals--------------------------------

    @property
    def data(self):
        s = str(self[self.pos])
        instruct_code = int(s[-2:])
        modes = s[:-2]
        return (instruct_code, modes)

    @property
    def valid_run_status(self):
        return not (
            self.op_status["halted"]
            or (
                self.op_status["need input"]
                and not self.input_queue))

    def __getitem__(self, addr):
        if (val := self.tape[addr]) is not None:
            return val
        else:
            raise Exception("Attempted to read from uninitialized memory"
                            f"address: {addr}")

    def __setitem__(self, addr, val):

        # Extend tape as needed to provide extra memory
        if (ext_length := (addr - len(self.tape) + 1)) > 0:
            if ext_length > 10**6:
                print(f"Creating {ext_length} slots of empty memory!")
            self.tape += [None for _ in range(ext_length)]
        self.tape[addr] = val


def parse_input(file_name):
    s_tape = []
    with open(get_input_file_name(file_name), "r") as f:
        for line in f.readlines():
            s_tape += line.split(",")
    print(f"tape is {len(s_tape)} positions long.")
    return [int(s) for s in s_tape]
