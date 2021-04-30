import os.path
from copy import copy

from util.intcode import AdvancedIntcoder


class AmpIntcoder(AdvancedIntcoder):

    def output(self, addr):
        self.op_status["halted"] = True
        return self[addr]

    def run(self, start_pos=0, return_pos=0, edits=(), reset=True):
        "Modified to add return value."

        if reset:
            self.tape = copy(self.master)
            for addr, val in edits:
                self[addr] = val
            self.pos = start_pos

        while self.valid_run_status:
            exec_f, param_f, pos_f = self.instructs[self.data[0]]
            f_inputs = param_f(self, self.data[-1])
            return_value = exec_f(*f_inputs)
            pos_f(self)

        self.reset()
        return return_value

    def reset(self, *args, **kwargs):
        for value in self.op_status:
            self.op_status[value] = False


def test_phases(phases_tried, phase_set, input):
    next_inputs = []
    for p in phase_set:
        INTCODER.input_queue = [p, input]
        output = INTCODER.run()
        rem_phase_set = phase_set - {p}
        if rem_phase_set:
            next_inputs.append((phases_tried + [p], rem_phase_set, output))
        else:
            return output  # if not rem_phase_set, p only member of phase_set
    return max([test_phases(*inputs) for inputs in next_inputs])


file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d7.txt")
s_tape = []
with open(file_name, "r") as f:
    for line in f.readlines():
        s_tape += line.split(",")
tape = [int(s) for s in s_tape]

phase_set = {0, 1, 2, 3, 4}
INTCODER = AmpIntcoder(tape, [])

print(test_phases([], phase_set, 0))
