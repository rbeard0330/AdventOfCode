from util.file_ops import get_input_file_name
from math import ceil
from collections import defaultdict, deque

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


def find_ore_costs(complexity_list, RXN_DICT):
    # Entries are tuples: (ore cost per batch, size of
    # batch, list of byproducts per batch)
    synthesis = {"ORE": (1, 1, [])}  
    for target in complexity_list:
        if target == "ORE":
            continue
        batch_size, inputs = RXN_DICT[target]
        # reqs is a list of (amt, compound) tuples
        reqs = sorted(inputs,
                      key=lambda c: complexity_list.index(c[1]),
                      reverse=True)
        on_hand = defaultdict(int)  # key = cmpd, val = amt
        ore_cost = 0
        for c in reqs:
            c0, c1 = c
            if c1 in on_hand:
                c0 -= (used := min(c0, on_hand[c1]))
                on_hand[c1] -= used
            if c0 == 0:
                continue
            c_cost, c_size, c_lefts = synthesis[c1]
            if c1 != "ORE":
                on_hand[c1] += c_size - c0 % c_size
            for amt, left_comp in c_lefts:
                on_hand[left_comp] += amt
            batches_needed = ceil(c0 / c_size)
            ore_cost += c_cost * batches_needed
        synthesis[target] = (
            ore_cost, batch_size, [(v, k) for k, v in on_hand.items()])
    
    return synthesis


def tests():
    for i, t in enumerate(test_list):
        rxn_dict = {}
        used_in_dict = defaultdict(list)
        for line in t.split("\n"):
            parse_rxn(line, rxn_dict, used_in_dict)
        complexity_list = topo_sort(used_in_dict)
        a = find_ore_costs(complexity_list, rxn_dict)
        print(a)
        print(a["FUEL"][0], answer_list[i])

"""
RXN_DICT = {}
USED_IN_DICT = defaultdict(list)
line_count = 0
fn = get_input_file_name("d14.txt")
with open(fn, "r") as f:
    for line in f.readlines():
        line_count += 1
        parse_rxn(line.strip(), RXN_DICT, USED_IN_DICT)
assert len(RXN_DICT) == line_count

complexity_list = topo_sort()
assert len(complexity_list) == len(RXN_DICT) + 1 # ORE not in RXN_DICT
cost_dict = find_ore_costs(complexity_list)
print(cost_dict["FUEL"])
"""

tests()