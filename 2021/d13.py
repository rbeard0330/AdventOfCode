from utils import Grid, Point, read_input


class FoldableGrid(Grid):
    def fold(self, x=None, y=None):
        assert (x is None) != (y is None)
        if x is not None:
            for pt in self.points():
                if pt.x <= x:
                    continue
                folded_point = Point(x=x - abs(x - pt.x), y=pt.y)
                self[folded_point] = self[folded_point] or self[pt]
            self._points = [row[:x + 1] for row in self._points]
        elif y is not None:
            for pt in self.points():
                if pt.y <= y:
                    continue
                folded_point = Point(x=pt.x, y=y - abs(y - pt.y))
                # print(f'Folding {pt} onto {folded_point}')
                self[folded_point] = self[folded_point] or self[pt]
            self._points = self._points[:y + 1]

    def __str__(self):
        return '\n'.join(' '.join('x' if point else '.' for point in row) for row in self._points)


def read_instructions(lines):
    dots = []
    folds = []
    for line in lines:
        if line.startswith('f'):
            assert line[11] == 'y' or line[11] == 'x'
            folds.append({line[11]: int(line.strip().split('=')[1])})
        elif line.strip():
            x, y = line.strip().split(',')
            dots.append(Point(x=int(x), y=int(y)))
    return dots, folds


def grid_from_dots(dots):
    dot_set = set(dots)
    x_max = max(pt.x for pt in dots)
    y_max = max(pt.y for pt in dots)
    return FoldableGrid([[Point(x=x, y=y) in dot_set for x in range(x_max + 1)]
                         for y in range(y_max + 1)])


def part_1(lines):
    dots, folds = read_instructions(lines)
    grid = grid_from_dots(dots)
    grid.fold(**folds[0])
    return sum(grid[point] for point in grid.points())


def part_2(lines):
    dots, folds = read_instructions(lines)
    grid = grid_from_dots(dots)
    for fold in folds:
        grid.fold(**fold)
    return grid


test_lines = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".splitlines()
real_lines = read_input(13)

assert part_1(test_lines) == 17
print(part_1(real_lines))

print(part_2(test_lines))
print(part_2(real_lines))
