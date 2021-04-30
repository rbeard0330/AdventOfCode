from fractions import Fraction
from collections import defaultdict
import itertools

from util.file_ops import get_input_file_name
from util.point import Point
from d10tests import test_list
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
def find_nth_destroyed(ast_list, n, log=False):
    # Repeat code from Part 1
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
            site = cand

    # Start new code --------------
    site_p = ast_list[site]
    slope_bin = defaultdict(set)
    for key in slopes:
        if site_p in key:
            slope_bin[slopes[key]] |= key
    vert_list = sorted(list(slope_bin.pop("vert") | {site_p}), key=Point.sort)
    cut = vert_list.index(site_p)
    verts = {"up":   sorted(vert_list[:cut], key=Point.sort, reverse=True),
             "down": vert_list[cut + 1:]}

    positives = []
    negatives = []
    for m in sorted(slope_bin.keys()):
        m_list = sorted(list(slope_bin[m] | {site_p}), key=Point.sort)
        cut = m_list.index(site_p)
        positives.append(m_list[cut + 1:])
        negatives.append(sorted(m_list[:cut], key=Point.sort, reverse=True))

    blasted = 0
    zap = generate_asteroid(positives, negatives, verts)
    log_list = []
    if log:
        to_log = log.pop(0)
    else:
        to_log = None
    while blasted < n:
        blast = next(zap)
        blasted += 1
        if blasted == to_log:
            log_list.append(blast)
            if log:
                to_log = log.pop(0)
    if log_list:
        return log_list
    return blast


def generate_asteroid(pos, neg, vert):
    while True:
        gen = itertools.chain([vert["up"]], pos, [vert["down"]], neg)
        for row in gen:
            if row:
                yield row.pop(0)


def test():
    ast_list = parse_input(test_list[-1].split("\n"))
    log = [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]
    results_list = find_nth_destroyed(ast_list, 299, log)
    answers = [Point(11, 12), Point(12, 1), Point(12, 2), Point(12, 8),
               Point(16, 0), Point(16, 9), Point(10, 16), Point(9, 6),
               Point(8, 2), Point(10, 9), Point(11, 1)]
    assert len(results_list) == len(answers)
    for i in range(len(results_list)):
        try:
            assert results_list[i] == answers[i]
        except AssertionError:
            print(results_list[i], answers[i])
            raise AssertionError


input_list = []
file_name = get_input_file_name("d10.txt")
with open(file_name, "r") as f:
    for line in f.readlines():
        input_list.append(line)

ast_list = parse_input(input_list)
p = find_nth_destroyed(ast_list, 200)
print(p.x * 100 + p.y)
