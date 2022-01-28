from collections import defaultdict
from functools import reduce
from operator import mul

from utils import Point, read_input, Grid


class Cave(Grid):
    def flows_to(self, p: Point):
        return min(self.neighbors(p), key=lambda neighbor: self[neighbor])

    def minima(self):
        return [point for point in self.points()
                if all(self[point] < self[neighbor] for neighbor in self.neighbors(point))]


def read_cave(lines):
    return list(map(lambda line: [int(c) for c in line.strip()], lines))


test_lines = """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()
real_lines = read_input(9)

test_cave = Cave(read_cave(test_lines))
assert test_cave[Point(x=1, y=2)] == 8
assert set(test_cave.neighbors(Point(x=0, y=2))) == {Point(x=1, y=2), Point(x=0, y=1), Point(x=0, y=3)}, set(test_cave.neighbors(Point(x=0, y=2)))


def part_1(lines):
    cave = Cave(read_cave(lines))
    return sum(cave[point] + 1 for point in cave.minima())


def part_2(lines):
    cave = Cave(read_cave(lines))
    outlet_map = {p: cave.flows_to(p) for p in cave.points() if cave[p] < 9}
    inlet_map = defaultdict(list)
    for source, sink in outlet_map.items():
        inlet_map[sink].append(source)
    basins = {minimum: set() for minimum in cave.minima()}
    frontier = list((basin, basin) for basin in basins)
    while frontier:
        next_frontier = []
        for pt, basin in frontier:
            new_sources = {source for source in inlet_map[pt] if source not in basins[basin]}
            basins[basin] |= new_sources
            next_frontier.extend((new_source, basin) for new_source in new_sources)
        frontier = next_frontier
    sorted_basins = sorted(basins.values(), key=lambda basin_pts: len(basin_pts), reverse=True)
    return reduce(mul, (len(basin) for basin in sorted_basins[:3]))


assert (part_1(test_lines)) == 15
print(part_1(real_lines))

assert part_2(test_lines) == 1134
print(part_2(real_lines))
