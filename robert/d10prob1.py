from fractions import Fraction
from collections import defaultdict

from util.file_ops import get_input_file_name
from util.point import Point
from d10tests import test_list, answer_list
from util.decorators import timer


def parse_input(input_list):
    ast_list = []
    for y, row in enumerate(input_list):
        for x, char in enumerate(row):
            if char == "#":
                ast_list.append(Point(x, y))
    return ast_list


def slope(p1, p2):
    if p1.x == p2.x:
        return "vert"
    return Fraction(p2.y - p1.y, p2.x - p1.x)


@timer
def find_best(ast_list):
    asts = len(ast_list)

    slopes = {}
    for i, p1 in enumerate(ast_list):
        for p2 in ast_list[i + 1:]:
            slopes[frozenset([p1, p2])] = slope(p1, p2)

    vis_array = [[None for i in range(asts)] for j in range(asts)]
    # Populate vis_array so that [i][j] = True if i and j can see each other
    # and i < j.  None if i >= j.

    for i, p1 in enumerate(ast_list):
        slope_bin = defaultdict(list)
        for j, p2 in enumerate(ast_list[i + 1:]):
            slope_bin[slopes[frozenset([p1, p2])]].append(i + j + 1)
        for group in slope_bin.values():  # Group of collinear points
            if (count := len(group)) == 1:
                vis_array[i][group[0]] = True
                continue
            elif vis_array[i][group[0]] is not None:
                continue  # Group was already processed
            group.append(i)
            group.sort(key=lambda ast: (ast_list[ast].x, ast_list[ast].y))
            # Sort by x-val of point, then y to get linear order
            for ix, ast1 in enumerate(group[:-1]):
                vis_array[min(s := {ast1, group[ix + 1]})][max(s)] = True
                for ast3 in group[ix + 2:]:
                    vis_array[min(s := {ast1, ast3})][max(s)] = False

    best = 0
    for cand in range(len(ast_list)):
        count = sum(1 for i in range(cand) if vis_array[i][cand])
        count += sum(1 for j in range(cand + 1, asts) if vis_array[cand][j])
        if count > best:
            best = count
            best_site = cand

    return best


def tests():
    for i, t in enumerate(test_list):
        ast_list = parse_input(t.split("\n"))
        assert find_best(ast_list) == answer_list[i]


input_list = []
file_name = get_input_file_name("d10.txt")
with open(file_name, "r") as f:
    for line in f.readlines():
        input_list.append(line)

print("Part 1\n", find_best(parse_input(input_list)))
