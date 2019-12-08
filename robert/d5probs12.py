import os.path
from copy import copy
from util.intcode import AdvancedIntcoder


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
