import os.path

file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d1.txt")

input_list = []
with open(file_name, "r") as f:
    for line in f.readlines():
        input_list.append(line)


def str_to_ints(l):
    return_l = []
    for s in l:
        n = int(s[1:])
        return_l.append(-1 * n if s[0] == "-" else n)
    return return_l


int_l = str_to_ints(input_list)
print("Part 1:")
print(sum(int_l))

value_set = set()
no_answer = True
phase = 0
while no_answer:
    for i, val in enumerate(int_l):
        phase += val
        if phase in value_set:
            print(f"Part 2:\n{phase} at {i}")
            no_answer = False
            break
        else:
            value_set.add(phase)
