from collections import deque
from dataclasses import dataclass
from itertools import product
from time import perf_counter_ns


def read_input(day) -> list[str]:
    with open(f'inputs/d{day}.txt') as f:
        return list(f.readlines())

def time_fn(f):
    def inner(*args, **kwargs):
        start = perf_counter_ns()
        result = f(*args, **kwargs)
        ns = perf_counter_ns() - start
        print(f'{ns / 10**6:.2f} ms')
        return result
    return inner


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, s):
        x, y = s.strip().split(',')
        return Point(x=int(x), y=int(y))

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)


class Grid:
    def __init__(self, points):
        self._points = points

    def neighbors(self, p: Point, include_diagonal=False):
        result = []
        x_range = range(max(0, p.x - 1), min(len(self._points[0]), p.x + 2))
        y_range = range(max(0, p.y - 1), min(len(self._points), p.y + 2))

        for x, y in product(x_range, y_range):
            if x == p.x and y == p.y:
                continue
            if include_diagonal or (x == p.x or y == p.y):
                result.append(Point(x=x, y=y))
        return result

    def __getitem__(self, item):
        return self._points[item.y][item.x]

    def __setitem__(self, item, value):
        self._points[item.y][item.x] = value

    def points(self):
        for y in range(len(self._points)):
            for x in range(len(self._points[0])):
                yield Point(x=x, y=y)


def windows(it, size, overlapping=True, yield_remainder=False):
    window = deque(maxlen=size)
    for val in it:
        window.append(val)
        if len(window) == size:
            yield tuple(window)
            if not overlapping:
                window.clear()
    if yield_remainder and len(window) != size:
        yield tuple(window)


assert list(windows([1, 2, 3, 4, 5], 2)) == [(1, 2), (2, 3), (3, 4), (4, 5)]
assert list(windows([1, 2, 3, 4, 5], 2, overlapping=False)) == [(1, 2), (3, 4)]
assert list(windows([1, 2, 3, 4, 5], 2, overlapping=False, yield_remainder=True)) == [(1, 2), (3, 4), (5,)]


