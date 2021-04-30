from util.file_ops import get_input_file_name
from math import ceil, floor
from collections import defaultdict, deque
from copy import copy

from d14tests import answer_list, test_list


def parse_rxn(string, RXN_DICT, USED_IN_DICT):
    lhs, rhs = string.split(" => ")
    lhs = lhs.split(", ")
    inputs = []
    num_out, out_compound = rhs.split(" ")
    for reagent in lhs:
        num_in, compound = reagent.split(" ")
        inputs.append((int(num_in), compound))
        USED_IN_DICT[compound].append(out_compound)
    assert out_compound not in RXN_DICT
    RXN_DICT[out_compound] = (int(num_out), inputs)


def topo_sort(used_in_dict):
    complexity_list = deque()
    visited = set()
    DFS("ORE", complexity_list, visited, used_in_dict)
    return complexity_list


def DFS(input, complexity_list, visited, USED_IN_DICT):
    visited.add(input)
    for output in USED_IN_DICT[input]:
        if output not in visited:
            DFS(output, complexity_list, visited, USED_IN_DICT)
    complexity_list.appendleft(input)


def find_ore_cost(quantity_out, product, complexity_list, RXN_DICT):
    reqs_list = RXN_DICT[product][1]  # list of tuples (n, input_compound)
    # Sort so high-complexity compounds are first
    reqs_list.sort(key=lambda p: complexity_list.index(p[1]), reverse=True)
    reqs_dict = defaultdict(int)
    for amt, input_c in reqs_list:
        reqs_dict[input_c] += quantity_out * amt
    leftovers = defaultdict(int)
    while len(reqs_dict) > 1:
        reagent = complexity_list.pop()
        if reagent in reqs_dict:
            amt_needed = reqs_dict[reagent]
            del(reqs_dict[reagent])
        else:
            continue  # We don't need this reagent

        # Decide how many batches we need and save extra
        batch_size, new_reqs = RXN_DICT[reagent]
        batches = ceil(amt_needed / batch_size)
        leftovers[reagent] += batch_size * batches - amt_needed

        # Add new reqs to existing dict
        for amt, input_c in new_reqs:
            reqs_dict[input_c] += batches * amt
        for avail in leftovers:
            if avail in reqs_dict:
                used = min(leftovers[avail], reqs_dict[avail])
                reqs_dict[avail] -= used
                leftovers[avail] -= used

    assert len(reqs_dict) == 1 and "ORE" in reqs_dict
    return reqs_dict["ORE"]


def tests():
    for i, t in enumerate(test_list):
        rxn_dict = {}
        used_in_dict = defaultdict(list)
        for line in t.split("\n"):
            parse_rxn(line, rxn_dict, used_in_dict)
        complexity_list = topo_sort(used_in_dict)
        a = find_ore_cost(1, "FUEL", copy(complexity_list), rxn_dict)
        assert a == answer_list[i]


RXN_DICT = {}
USED_IN_DICT = defaultdict(list)
line_count = 0
fn = get_input_file_name("d14.txt")
with open(fn, "r") as f:
    for line in f.readlines():
        line_count += 1
        parse_rxn(line.strip(), RXN_DICT, USED_IN_DICT)
assert len(RXN_DICT) == line_count

complexity_list = topo_sort(USED_IN_DICT)
assert len(complexity_list) == len(RXN_DICT) + 1 # ORE not in RXN_DICT
print(
    "Part 1:\n",
    (per := find_ore_cost(1, "FUEL", copy(complexity_list), RXN_DICT)))

# Iterate until we find right answer
guess = floor(10**12 / per)
budget = 10**12
while ((curr := find_ore_cost(guess, "FUEL", copy(complexity_list), RXN_DICT))
       < budget - per):
    guess += floor((budget - curr) / per)
print("Part 2:\n", guess)
