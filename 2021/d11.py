from dataclasses import dataclass
from itertools import count

from utils import Grid, Point, read_input


class OctopusGrid(Grid):
    ...


@dataclass
class Octopus:
    energy: int
    has_flashed: bool = False


def read_octopi(lines):
    return [[Octopus(energy=int(c)) for c in line.strip()] for line in lines]

test_lines = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()
real_lines = read_input(11)


def tick(grid):
    for point in grid.test_points():
        grid[point].energy += 1
    flashes = None
    flashed_this_tick = set()
    while flashes is None or len(flashes) > 0:
        if flashes:
            for flash in flashes:
                for neighbor in grid.neighbors(flash, include_diagonal=True):
                    grid[neighbor].energy += 1
        flashes = []
        for point in grid.test_points():
            if grid[point].energy > 9 and not grid[point].has_flashed:
                flashes.append(point)
                flashed_this_tick.add(point)
                grid[point].has_flashed = True
    for point in flashed_this_tick:
        grid[point].has_flashed = False
        grid[point].energy = 0
    return flashed_this_tick


def part_1(lines):
    grid = OctopusGrid(read_octopi(lines))
    return sum(len(tick(grid)) for _ in range(100))


assert part_1(test_lines) == 1656
print(part_1(real_lines))


def part_2(lines):
    grid = OctopusGrid(read_octopi(lines))
    total = len(list(grid.points()))
    for i in count():
        if len(tick(grid)) == total:
            return i + 1


assert part_2(test_lines) == 195
print(part_2(real_lines))