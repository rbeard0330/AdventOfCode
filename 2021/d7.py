from math import floor

from utils import read_input, time_fn


def get_crabs(lines):
    return [int(c) for c in lines[0].strip().split(',')]


def part_1(lines):
    crabs = sorted(get_crabs(lines))
    median = floor(len(crabs) / 2)
    return sum(abs(i - crabs[median]) for i in crabs)


test_lines = '16,1,2,0,4,2,7,1,2,14'.splitlines()
real_lines = read_input(7)
assert part_1(test_lines) == 37
print(part_1(real_lines))


@time_fn
def part_2(lines):
    crabs = sorted(get_crabs(lines))
    distance_traveled_right = compute_aggregate_distances(crabs)
    distance_traveled_left = compute_aggregate_distances(crabs[::-1])[::-1]
    i = 1
    while i < len(crabs) - 1:
        gap_size = crabs[i] - crabs[i - 1]
        crabs_to_left = i + 1
        crabs_to_right = len(crabs) - crabs_to_left
        shift_right_cost = crabs_to_left * (gap_size ** 2 + gap_size) + gap_size * distance_traveled_right[i]
        shift_left_cost = crabs_to_right * (gap_size ** 2 + gap_size) + gap_size * distance_traveled_left[i + 1]
        if shift_right_cost > shift_left_cost:
            break
        i += 1
    rendezvous = crabs[i]
    best = None
    while rendezvous <= crabs[i + 1]:
        total_cost = sum(cost(crab - rendezvous) for crab in crabs)
        if best is None or total_cost < best:
            best = total_cost
        rendezvous += 1
    return int(best)


@time_fn
def part_2_dumb(lines):
    crabs = sorted(get_crabs(lines))
    rendezvous = crabs[0]
    best = None
    while rendezvous <= crabs[-1]:
        total_cost = sum(cost(crab - rendezvous) for crab in crabs)
        if best is None or total_cost < best:
            best = total_cost
        rendezvous += 1
    return int(best)


def cost(n):
    n = abs(n)
    return (n + 1) * n / 2


def compute_aggregate_distances(crabs):
    distances = [0]
    for i, (last_n, next_n) in enumerate(zip(crabs, crabs[1:])):
        distances.append(distances[-1] + abs(next_n - last_n) * (i + 1))
    return distances


assert part_2(test_lines) == 168
print(part_2(real_lines)) # 96440057 too high
#print(part_2_dumb(real_lines))
