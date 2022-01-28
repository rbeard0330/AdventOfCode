from collections import Counter

from utils import read_input, time_fn


def get_initial_pop(lines):
    c = Counter(int(fish) for fish in lines[0].split(','))
    return [c[i] for i in range(9)]


def tick(pop):
    reproducing, *next_pop = pop
    next_pop.append(reproducing)
    next_pop[6] += reproducing
    return next_pop


@time_fn
def part_1(lines):
    pop = get_initial_pop(lines)
    for _ in range(80):
        pop = tick(pop)
    return sum(pop)


test_input = ['3,4,3,1,2']
assert part_1(test_input) == 5934
print(part_1(read_input(6)))


@time_fn
def part_2(lines):
    pop = get_initial_pop(lines)
    for _ in range(256):
        pop = tick(pop)
    return sum(pop)


assert part_2(test_input) == 26984457539
print(part_2(read_input(6)))
