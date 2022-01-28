import heapq
from dataclasses import dataclass, field

from utils import Grid, read_input, Point


def read_cave(lines):
    grid = Grid(list(map(lambda line: [int(c) for c in line.strip()], lines)))
    return grid, Point(x=len(grid._points[0]) - 1, y=len(grid._points) - 1)


test_lines = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".splitlines()
real_lines = read_input(15)


@dataclass(order=True)
class Edge:
    criterion: int
    cost: int = field(compare=False)
    source: Point = field(compare=False)
    target: Point = field(compare=False)


def create_heap_item(grid, source, target, distances):
    return Edge(criterion=distances[source] + grid[target] ,cost=grid[target], source=source, target=target)


def add_neighbors_to_heap(grid, point, known_distances, heap):
    for neighbor in grid.neighbors(point):
        if neighbor not in known_distances:
            heapq.heappush(heap, create_heap_item(grid, point, neighbor, known_distances))


def part_1(lines):
    grid, goal = read_cave(lines)
    return distance_to_goal(goal, grid)


def distance_to_goal(goal, grid):
    start = Point(x=0, y=0)
    distances = {start: 0}
    frontier = []
    add_neighbors_to_heap(grid, start, distances, frontier)
    while goal not in distances:
        next_edge = heapq.heappop(frontier)
        if next_edge.target not in distances:
            distances[next_edge.target] = distances[next_edge.source] + next_edge.cost
            add_neighbors_to_heap(grid, next_edge.target, distances, frontier)
    return distances[goal]


def read_expanded_cave(lines):
    def map_point(original, x_iteration, y_iteration):
        original = int(original)
        return (original + x_iteration + y_iteration - 1) % 9 + 1
    expanded_grid = []
    for y_iteration in range(5):
        for line in lines:
            row = []
            for x_iteration in range(5):
                row.extend(map(lambda c: map_point(c, x_iteration, y_iteration), line.strip()))
            expanded_grid.append(row)
    grid = Grid(expanded_grid)
    return grid, Point(x=len(grid._points[0]) - 1, y=len(grid._points) - 1)


def part_2(lines):
    grid, goal = read_expanded_cave(lines)
    return distance_to_goal(goal, grid)


assert part_1(test_lines) == 40
print(part_1(real_lines))

assert part_2(test_lines) == 315
print(part_2(real_lines))
