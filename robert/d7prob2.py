import os.path
from copy import copy
from itertools import permutations

from util.intcode import AdvancedIntcoder


class AmpIntcoder(AdvancedIntcoder):

    def __init__(self, tape, id, debug=False):
        super().__init__(tape, [])
        self.output_queue = []
        self.id = id + 1
        self.debug = debug

    # ----------Initialization---------------------------

    def connect(self, output_machine):

        self.pass_output = output_machine.receive_input

    def reset(self, new_phase):
        self.tape = copy(self.master)
        self.input_queue = [new_phase]
        self.output_queue = []
        self.pos = 0
        self.storage_address = None
        for value in self.op_status:
            self.op_status[value] = False

    # -------------Core Loop-----------------------------

    def run(self):

        while self.valid_run_status:
            if self.input_processing_needed:
                self.process_input()
            exec_f, param_f, pos_f = self.instructs[self.data[0]]
            f_inputs = param_f(self, self.data[-1])
            exec_f(*f_inputs)
            pos_f(self)
        self.clear_output_queue()

    # -------------Input Processing-----------------------

    def try_to_store_input(self, addr):
        "Overloaded to add debugging."

        if self.input_queue:
            if self.debug:
                print(f"#{self.id} getting input from queue")
            self[addr] = self.input_queue.pop(0)
        else:
            if self.debug:
                print(f"#{self.id} needs input")
            assert self.storage_address is None
            self.storage_address = addr
            self.op_status["need input"] = True

        # Note that the positioner function runs after this method, even if
        # there was no input to process.

    def receive_input(self, input):

        if self.debug:
            print(f"#{self.id} received an input: {input}")
        self.input_queue.append(input)

    def process_input(self):
        stored_input = self.input_queue.pop(0)
        self[self.storage_address] = stored_input
        self.storage_address = None
        self.op_status["need input"] = False
        if self.debug:
            print(f"#{self.id} restarting after receiving {stored_input}")

    @property
    def input_processing_needed(self):
        return self.op_status["need input"] and self.input_queue

    # -------------Output Processing----------------------

    def output(self, addr):
        if self.debug:
            print(f"#{self.id} outputting {self[addr]} from {self.pos}")
        self.output_queue.append(self[addr])

    def clear_output_queue(self):
        "Run until machine reaches a pause, then push all outputs."

        if self.debug:
            print(f"#{self.id} clearing output queue of "
                  f"{len(self.output_queue)}")
        while self.output_queue:
            self.last_out = self.output_queue.pop(0)
            self.pass_output(self.last_out)


class AmpGroup():

    def __init__(self, num_coders):

        self.best = 0
        self.best_phases = []
        self.coders = (
            [AmpIntcoder(tape, 0)]
            + [AmpIntcoder(tape, i) for i in range(1, num_coders)])
        for i in range(num_coders - 1):
            self.coders[i].connect(self.coders[i + 1])
        self.coders[-1].connect(self.coders[0])

    def test_phase(self, phases):

        for i in range(5):
            self.coders[i].reset(phases[i])
        self.coders[0].receive_input(0)
        any_can_run = True
        while any_can_run:
            any_can_run = False
            for coder in self.coders:
                coder.run()
            for coder in self.coders:
                any_can_run = any_can_run or coder.valid_run_status

        result = self.coders[-1].last_out
        if result > self.best:
            self.best, self.best_phases = result, phases

    def test_all_phases(self, phase_set, debug=False):
        for coder in self.coders:
            coder.debug = debug
        for phase in permutations(phase_set):
            self.test_phase(phase)
        return self.best


file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d7.txt")

s_tape = []
with open(file_name, "r") as f:
    for line in f.readlines():
        s_tape += line.split(",")
tape = [int(s) for s in s_tape]

phase_set = {5, 6, 7, 8, 9}
a = AmpGroup(5)
print(a.test_all_phases(phase_set))
