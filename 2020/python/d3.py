from functools import reduce
from itertools import count, islice
from operator import mul


def count_trees(lines, x_step, y_step):
    return sum(row[x_coord % len(row.strip())] == '#'
               for x_coord, row in zip(count(step=x_step), islice(lines, 0, None, y_step)))


def first_answer(lines):
    return count_trees(lines.split('\n'), 3, 1)


def second_answer(lines):
    return reduce(mul, (count_trees(lines.split('\n'), x, y)
                        for x, y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))


TEST_DATA = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

assert first_answer(TEST_DATA) == 7
assert second_answer(TEST_DATA) == 336

real_data = open('data/d3.txt').read()
print(first_answer(real_data))
print(second_answer(real_data))
