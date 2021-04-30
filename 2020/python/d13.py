from functools import reduce


def first_answer(time, buses):
    buses = [int(bus) for bus in buses.split(',') if bus != 'x']
    bus, wait = min(((bus, bus - time % bus) for bus in buses), key=lambda tup: tup[1])
    return bus * wait


def second_answer(buses):
    congruences = [((base - offset) % base, base)
                   # convert and enumerate relevant buses and filter out the rest
                   for offset, base in (
                       (i, int(raw_base))
                       for i, raw_base in enumerate(bus for bus in buses.split(','))
                       if raw_base != 'x'
                   )]

    congruences.sort(key=lambda tup: tup[1], reverse=True)
    return reduce(solve_congruence_pair_by_sieving, congruences)[0]


def solve_congruence_pair_by_sieving(congruence1, congruence2):
    test_value, base1 = congruence1
    target, base2 = congruence2
    assert base1 % base2 != 0 and base2 % base1 != 0
    while test_value % base2 != target:
        test_value += base1
    assert test_value % base1 == congruence1[0] and test_value % base2 == congruence2[0]
    return test_value, base1 * base2


TEST_TIME, TEST_BUSES = """939
7,13,x,x,59,x,31,19""".splitlines()

assert first_answer(int(TEST_TIME), TEST_BUSES) == 295
assert second_answer(TEST_BUSES) == 1068781
assert second_answer('17,x,13,19') == 3417
assert second_answer('67,7,59,61') == 754018
assert second_answer('67,x,7,59,61') == 779210
assert second_answer('67,7,x,59,61') == 1261476
assert second_answer('1789,37,47,1889') == 1202161486

real_time, real_buses = open('data/d13.txt').read().splitlines()

print(first_answer(int(real_time), real_buses))
print(second_answer(real_buses))
