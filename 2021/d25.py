from itertools import cycle, count, product

from utils import Point, read_input

right = Point(x=1, y=0)
down = Point(x=0, y=1)

def read_cucumbers(lines):
    seafloor = {}
    print(lines)
    for y, line in enumerate(lines):
        print(len(line))
        for x, space in enumerate(line.strip()):
            if space == '>':
                print(f'right at {x, y}')
                seafloor[Point(x=x, y=y)] = right
            elif space == 'v':
                print(f'down at {x, y}')
                seafloor[Point(x=x, y=y)] = down
            else:
                print(f'empty at {x, y}')
    return seafloor, (x, y)


def wrapping_add(pt_1, pt_2, dimensions):
    max_x, max_y = dimensions
    x = (pt_1.x + pt_2.x) % (max_x + 1)
    y = (pt_1.y + pt_2.y) % (max_y + 1)
    return Point(x=x, y=y)

def tick(seafloor, dimensions):
    any_moved = False
    interim_seafloor = {}
    for current_location, cucumber in seafloor.items():
        if cucumber == right and (destination := wrapping_add(current_location, cucumber, dimensions)) not in seafloor:
            any_moved = True
            interim_seafloor[destination] = cucumber
        else:
            interim_seafloor[current_location] = cucumber
    new_seafloor = {}
    for current_location, cucumber in interim_seafloor.items():
        if cucumber == down and (destination := wrapping_add(current_location, cucumber, dimensions)) not in interim_seafloor:
            any_moved = True
            new_seafloor[destination] = cucumber
        else:
            new_seafloor[current_location] = cucumber

    return new_seafloor, any_moved


def part_1(lines):
    seafloor, dimensions = read_cucumbers(lines)
    print_seafloor(seafloor, dimensions)
    for step in count(1):
        # print(f'\nafter {step}\n')
        # print_seafloor(seafloor, dimensions)
        seafloor, any_moved = tick(seafloor, dimensions)
        if not any_moved:
            return step


def print_seafloor(seafloor, dimensions):
    max_x, max_y = dimensions
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            value = seafloor.get(Point(x=x, y=y))
            if value is None:
                print('.', end='')
            elif value == right:
                print('>', end='')
            elif value == down:
                print('v', end='')
        print()

# small_test_lines = """...>...
# .......
# ......>
# v.....>
# ......>
# .......
# ..vvv..""".splitlines()
#
# sf, dim = read_cucumbers(small_test_lines)
# print_seafloor(sf, dim)
# print()
# for _ in range(3):
#     sf, _ = tick(sf, dim)
#     print_seafloor(sf, dim)
#     print()


test_lines = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".splitlines()
real_lines = read_input(25)

assert part_1(test_lines) == 58
print(part_1(real_lines))
