from collections import defaultdict
from itertools import product


def read_two_d_state(data):
    start_state = set()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == '#':
                start_state.add((x, y))
    return start_state


def generate_neighbors(cube, dimensions):
    for offsets in product(*((-1, 0, 1) for _ in range(dimensions))):
        if any(offsets):
            yield tuple(base + offset for base, offset in zip(cube, offsets))


def tick(start_state, dimensions):
    active_neighbors = defaultdict(int)
    for active_cube in start_state:
        for neighbor in generate_neighbors(active_cube, dimensions):
            active_neighbors[neighbor] += 1
    return {cube for cube, neighbor_count in active_neighbors.items()
            if neighbor_count == 3 or cube in start_state and neighbor_count == 2}


def solve_in_n_dimensions(data, dimensions):
    assert dimensions >= 2
    extra_dimensions = tuple(0 for _ in range(dimensions - 2))
    current_state = {cube + extra_dimensions for cube in read_two_d_state(data)}
    for _ in range(6):
        current_state = tick(current_state, dimensions)
    return len(current_state)


def first_answer(data):
    return solve_in_n_dimensions(data, 3)


def second_answer(data):
    return solve_in_n_dimensions(data, 4)


TEST_DATA = """
.#.
..#
###"""

assert first_answer(TEST_DATA) == 112
assert second_answer(TEST_DATA) == 848

real_data = open('data/d17.txt').read()

print(first_answer(real_data))
print(second_answer(real_data))
