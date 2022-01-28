from collections import Counter
from dataclasses import dataclass

from utils import read_input, Point


@dataclass
class Line:
    start: Point
    end: Point

    @property
    def is_straight(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    def __iter__(self):
        x_start = min(self.start.x, self.end.x)
        y_start = min(self.start.y, self.end.y)
        x_direction = y_direction = 1
        steps = range(abs(self.start.x - self.end.x) + 1)

        if self.start.x == self.end.x:
            x_direction = 0
            steps = range(abs(self.start.y - self.end.y) + 1)
        elif self.start.y == self.end.y:
            y_direction = 0
        else:
            slants_up = (self.start.x > self.end.x) == (self.start.y > self.end.y)
            if not slants_up:
                y_direction = -1
                y_start = max(self.start.y, self.end.y)

        yield from (Point(x=x_start + x_direction * step, y=y_start + y_direction * step)
                    for step in steps)


def read_lines(lines: list[str], include_diagonal=False) -> list[Line]:
    result = []
    for line in lines:
        start, end = line.strip().split(' -> ')
        line = Line(start=Point.from_str(start), end=Point.from_str(end))
        if include_diagonal or line.is_straight:
            result.append(line)
    return result


test_line = set(Line(start=Point(x=1, y=2), end=Point(x=4, y=2)))
assert test_line == {Point(x=1, y=2), Point(x=2, y=2), Point(x=3, y=2), Point(x=4, y=2)}, test_line
test_line = set(Line(start=Point(x=1, y=1), end=Point(x=4, y=4)))
assert test_line == {Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4)}, test_line
test_line = set(Line(start=Point(x=4, y=1), end=Point(x=1, y=4)))
assert test_line == {Point(x=4, y=1), Point(x=3, y=2), Point(x=2, y=3), Point(x=1, y=4)}, test_line

test_lines = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split('\n')


def count_overlaps(lines):
    points = Counter()
    for line in lines:
        points.update(line)
    return sum(count >= 2 for count in points.values())


def part_1(raw_lines):
    return count_overlaps(read_lines(raw_lines, include_diagonal=False))


assert part_1(test_lines) == 5
print(part_1(read_input(5)))


def part_2(raw_lines):
    return count_overlaps(read_lines(raw_lines, include_diagonal=True))


assert part_2(test_lines) == 12
print(part_2(read_input(5)))
