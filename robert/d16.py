from collections import Counter

from util.decorators import timer

my_data = "59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590"

test1_list = ["80871224585914546619083218645595",
              "19617804207202209144916044189917",
              "69317163492948606335995924319873"]
test2_list = ["03036732577212944063491565474664",
              "02935109699940807407585447034323",
              "03081770884921959731165446850517"]
answer1_list = ["24176176",
                "73745418",
                "52432133"]
answer2_list = ["84462026",
                "78725270",
                "53553731"]


def opt_fft(data, iters, read_start=0):
    length = len(data[read_start:])
    d = bytearray(data)
    view = memoryview(d)
    while iters > 0:
        iters -= 1
        for i in range(length):
            counter = Counter()
            patt_len = i + 1
            curr = i
            while curr <= length:
                counter.update(view[curr: curr + patt_len])
                curr += 2 * patt_len
                counter.subtract(view[curr: curr + patt_len])
                curr += 2 * patt_len
            # d[i] does not impact values above i (each pattern starts with i
            # 0's), so we can work in place.
            answer = abs(sum(val * k for val, k in counter.items())) % 10
            d[i] = answer
    return list(d)


def fft_repeats(data, mult, iters):
    start = int("".join(str(c) for c in data[:7]))
    length = len(data) * mult
    data = (data * mult)
    data = data[start:]
    if start < length / 2:
        raise(NotImplementedError("Read code too low: {start}"))
    d = bytearray(data)
    view = memoryview(d)
    while iters > 0:
        iters -= 1
        counter = Counter(view)  # pattern longer than remaining string
        prior_d = d[0]
        d[0] = abs(sum(val * k for val, k in counter.items())) % 10
        for i in range(1, len(d)):
            current_d = d[i]
            d[i] = (d[i - 1] - prior_d) % 10
            prior_d = current_d
    return list(d[:8])


def baby_test():
    data = "12345678"
    answer = [int(c) for c in "01029498"]
    data = [int(c) for c in data]
    could_be = opt_fft(data, 4)
    assert could_be == answer


def tests_for_1():
    for i in range(3):
        data = [int(c) for c in test1_list[i]]
        data = opt_fft(data, 100)[:8]
        answer = [int(c) for c in answer1_list[i]]
        assert answer == data


def tests_for_2():
    for i in range(3):
        data = [int(c) for c in test2_list[i]]
        data = fft_repeats(data, 10**4, 100)[:8]
        answer = [int(c) for c in answer2_list[i]]
        assert answer == data


@timer
def solve():
    data = [int(c) for c in my_data]
    ans1 = "".join(str(d) for d in opt_fft(data, 100)[:8])
    ans2 = "".join(str(d) for d in fft_repeats(data, 10**4, 100))
    return ans1, ans2


baby_test()
tests_for_1()
tests_for_2()
ans1, ans2 = solve()
print("Part 1:\n", ans1)
print("Part 2:\n", ans2)
