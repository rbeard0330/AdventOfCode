from math import ceil
from collections import Counter
from itertools import chain

from util.decorators import timer

my_data = "59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590"

test_list =     ["80871224585914546619083218645595",
                 "19617804207202209144916044189917",
                 "69317163492948606335995924319873"]
answer_list =   ["24176176",
                 "73745418",
                 "52432133"]


def generate_slices(max_length):
    "Return dicts of slices corresponding to patterns up to length."
    
    p_slices = {}
    n_slices = {}
    first_cutoff = ceil(max_length / 3)     # One positive slice above this val
    second_cutoff = ceil(max_length / 5)    # One positive and one negative
    
    for i in range(second_cutoff, max_length):
        # One positive slice
        patt_len = i + 1
        p_slices[i] = (slice(i, i + patt_len),)
        n_slices[i] = []
    for i in range(second_cutoff, first_cutoff):
        patt_len = i + 1
        n_slices[i] = (slice(i + 2 * patt_len, i + 3 * patt_len),)
    for i in range(second_cutoff):
        patt_len = i + 1
        p_list = []
        n_list = []
        for j in range(patt_len):
            p_list.append(
                slice(i + j, max_length, 4 * patt_len))
            n_list.append(
                slice(i + 2 * patt_len + j, max_length, 4 * patt_len))
        p_slices[i] = tuple(p_list)
        n_slices[i] = tuple(n_list)
    return p_slices, n_slices


def opt_fft(data, iters, p_slices, n_slices):
    ix_list = [i for i in range(len(data))]  # Store so we don't recompute
    d = bytearray(data)
    view = memoryview(d)
    counter = Counter()
    while iters > 0:
        iters -= 1
        for i in ix_list:
            counter.update(chain(*(view[s] for s in p_slices[i])))
            counter.subtract(chain(*(view[s] for s in n_slices[i])))
            # d[i] does not impact values above i (each pattern starts with i
            # 0's), so we can work in place.
            output = abs(sum(val * k for val, k in counter.items()))
            output %= 10
            d[i] = output
            for val in counter:
                counter[val] = 0
        data = list(d)
    return list(d)
                

def fft(data, runs):
    counter = 0
    while counter < runs:
        counter += 1
        old_data = data
        data = []
        for output in range(len(old_data)):
            out_sum = 0
            for ix, val in enumerate(old_data):
                if mul := patterns[output + 1][ix]:
                    out_sum += val * mul
            data.append(int(str(out_sum)[-1]))
    return data


def baby_test():
    data = "12345678"
    answer = [int(c) for c in "01029498"]
    data = [int(c) for c in data]
    p_s, n_s = generate_slices(len(data))
    could_be = opt_fft(data, 4, p_s, n_s)
    assert could_be == answer


def tests():
    for i in range(3):
        data = [int(c) for c in test_list[i]]
        p_s, n_s = generate_slices(len(data))
        data = opt_fft(data, 100, p_s, n_s)[:8]
        answer = [int(c) for c in answer_list[i]]
        assert answer == data

@timer
def solve(reps=1):
    data = [int(c) for c in my_data] * reps
    p_s, n_s = generate_slices(len(data))
    return "".join(str(d) for d in opt_fft(data, 100, p_s, n_s)[:8])


baby_test()
tests()
#print("Part 1:\n", solve())
print("Part 2:\n", solve(3))