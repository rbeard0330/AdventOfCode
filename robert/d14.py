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
        

# sort keys so that no reaction has an input that isn't an output of a prior
# reaction (or ORE)



def get_reqs(amt, compound):
    if compound == "ORE":
        return [(amt, "ORE")]
    req_list = []
    amt_produced, reagent_list = RXN_DICT[compound]
    n = ceil(amt / amt_produced)
    for r in reagent_list:
        req_list += get_reqs(*r)
    req_dict = defaultdict(int)
    for r in req_list:
        req_dict[r[1]] += n* r[0]
    return_list = []
    for key, val in req_dict.items():
        return_list.append((val, key))
    return return_list
        

def tests():
    for i, t in enumerate(test_list):
        RXN_DICT = {}
        USED_IN_DICT = defaultdict(list)
        for line in t.split("\n"):
            parse_rxn(line, RXN_DICT, USED_IN_DICT)


RXN_DICT = {}
USED_IN_DICT = defaultdict(list)
line_count = 0
fn = get_input_file_name("d14.txt")
with open(fn, "r") as f:
    for line in f.readlines():
        line_count += 1
        parse_rxn(line.strip(), RXN_DICT, USED_IN_DICT)
assert len(RXN_DICT) == line_count

compound_list = list(RXN_DICT.keys())
output_set = set()
for input_tup in RXN_DICT.values():
    s = {item[1] for item in input_tup[1]}
    output_set |= s
compound_sinks = {c for c in RXN_DICT} - output_set
complexity_list = deque()
print(output_set)
print(compound_list)
print(RXN_DICT["FUEL"])
tests()