import operator
from copy import copy, deepcopy
from functools import reduce
from itertools import product, permutations
from math import floor, ceil

from utils import read_input


class SnailNumber:
    def __init__(self, depth, left=None, right=None, value=None, parent=None) -> None:
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth
        self.value = value
        assert value is None or isinstance(value, int)

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        return f'[{self.left},{self.right}]'

    def __add__(self, other):
        if not isinstance(other, SnailNumber):
            other = SnailNumber(value=other, depth=1)
        result = SnailNumber(left=deepcopy(self), right=deepcopy(other), depth=0)
        result.set_depth()
        result.depth = 0
        result.set_parents()
        # print('sum', result)
        result.reduce()
        return result

    def __radd__(self, other):
        if not isinstance(other, SnailNumber):
            other = SnailNumber(value=other, depth=1)
        result = SnailNumber(left=deepcopy(other), right=deepcopy(self), depth=0)
        result.set_depth()
        result.depth = 0
        result.set_parents()
        # print('sum', result)
        result.reduce()
        return result

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def magnitude(self):
        if self.value is not None:
            return self.value
        else:
            return 3 * self.left.magnitude + 2 * self.right.magnitude
    @property
    def root(self):
        if self.parent is None:
            return self
        return self.parent.root

    def set_depth(self, depth=0):
        self.depth = depth
        for child in self.left, self.right:
            if not child:
                continue
            child.set_depth(depth + 1)

    def set_parents(self):
        for node in self.left, self.right:
            if not node:
                continue
            node.parent = self
            node.set_parents()

    @classmethod
    def from_str(cls, s):
        result = create_tree(eval(s.strip()))
        result.set_parents()
        return result

    @classmethod
    def from_list(cls, l):
        result = create_tree(l)
        result.set_parents()
        return result

    def traverse(self):
        if self.left is not None:
            yield from self.left.traverse()
        yield self
        if self.right is not None:
            yield from self.right.traverse()

    def explode_any(self):
        for node in self.traverse():
            if node.depth >= 4 and node.is_leaf():
                node.explode()

    def successor(self):
        # print('successor for', self)
        current = self
        while current is not None:
            # print(current.parent and current.parent.left, self)
            if current.parent and current.parent.left is current:
                return current.parent.right.first_child()
            else:
                current = current.parent

    def predecessor(self):
        current = self
        while current is not None:
            if current.parent and current.parent.right is current:
                return current.parent.left.last_child()
            else:
                current = current.parent

    def first_child(self):
        current = self
        while current.left is not None:
            current = current.left
        return current

    def last_child(self):
        current = self
        while current.right is not None:
            current = current.right
        return current

    def is_leaf(self):
        return self.right and self.left and self.right.value is not None and self.left.value is not None

    def add_to_successor(self, v):
        current = self
        while (parent := current.parent) is not None:
            # print(current, parent.left, parent.right, current.parent)
            if current is parent.left:

                if parent.right.value is not None:
                    parent.right.value += v
                else:
                    parent.right.add_to_first_child(v)
                return
            current = parent

    def explode(self):
        # print(f'exploding {self} in {self.root}')
        assert self.parent is not None
        assert self.is_leaf()
        assert self.depth >= 4
        if (predecessor := self.predecessor()) is not None:
            predecessor.value += self.left.value
        if (successor := self.successor()) is not None:
            successor.value += self.right.value
        self.value = 0
        self.right = None
        self.left = None

    def split(self):
        for node in self.traverse():
            if (node.value or 0) >= 10:
                # print(f'splitting {node} in {self}')
                node.left = SnailNumber(value=floor(node.value / 2), depth=node.depth + 1, parent=node)
                node.right = SnailNumber(value=ceil(node.value / 2), depth=node.depth + 1, parent=node)
                node.value = None
                # print(f'after split: {node}')
                return

    def reduce(self):
        initial = str(self)
        self.explode_any()
        self.split()
        if str(self) != initial:
            self.reduce()


def create_tree(number, depth=0):
    try:
        l, r = number
        return SnailNumber(left=create_tree(l, depth + 1), right=create_tree(r, depth + 1), depth=depth)
    except TypeError:
        return SnailNumber(value=number, depth=depth)


assert SnailNumber.from_str('[1, 2]') + SnailNumber.from_str('[[3, 4], 5]') == SnailNumber.from_str('[[1,2],[[3,4],5]]')
number = SnailNumber.from_str('[[1,5],[[3,4],6]]')
number.set_parents()
assert number.left.parent is number

explode_tests = [([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
                 ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
                 ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [7, 0]]]])]
for start, end in explode_tests:
    n = SnailNumber.from_list(start)
    n.explode_any()
    assert n == SnailNumber.from_list(end), n

n2 = SnailNumber.from_list([[[[[9, 8], 1], 2], 3], 4])
n2.explode_any()
assert n2 == SnailNumber.from_list([[[[0, 9], 2], 3], 4]), n2

n = SnailNumber.from_list([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
n.explode_any()
assert n == SnailNumber.from_list([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]), n

n3 = SnailNumber.from_list([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
n3.split()
n3.split()
n3.explode_any()
assert n3 == SnailNumber.from_list([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]), n3

s = SnailNumber.from_list([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]) + SnailNumber.from_list([1, 1])
s.reduce()
assert s == SnailNumber.from_list([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]), s

s = SnailNumber.from_list([1, 1]) + SnailNumber.from_list([2, 2]) + SnailNumber.from_list(
    [3, 3]) + SnailNumber.from_list([4, 4])
assert s == SnailNumber.from_list([[[[1,1],[2,2]],[3,3]],[4,4]]), s
s = s + SnailNumber.from_list([5, 5])
assert s == SnailNumber.from_list([[[[3,0],[5,3]],[4,4]],[5,5]]), s
s = s + SnailNumber.from_list([6, 6])
assert s == SnailNumber.from_list([[[[5,0],[7,4]],[5,5]],[6,6]]), s

tests = [
    ([7,[[[3,7],[4,3]],[[6,3],[8,8]]]], [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]),
    ([[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]], [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]),
    ([[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]], [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]),
    ([7,[5,[[3,8],[1,4]]]], [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]),
    ([[2,[2,2]],[8,[8,1]]], [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]])
]

s = SnailNumber.from_list([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]])
for add, result in tests:
    s += SnailNumber.from_list(add)
    expected = SnailNumber.from_list(result)
    assert s == expected, f'expected {expected}\ngot{s}'

first_test_lines = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()

res, *nums = [SnailNumber.from_str(l) for l in first_test_lines]
for num in nums:
    res = res + num


def part_1(lines):
    nums = [SnailNumber.from_str(l) for l in lines]
    return reduce(operator.add, nums).magnitude


second_test_lines = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()
r = part_1(second_test_lines)
assert r == 4140, r

real_lines = read_input(18)
print(part_1(real_lines))

# second_test_lines = """[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
# [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]""".splitlines()

def part_2(lines):
    nums = [SnailNumber.from_str(l) for l in lines]
    highest = 0
    for n1, n2 in permutations(nums, 2):
        mag = (n1 + n2).magnitude
        if mag > highest:
            # print(n1, n2, mag)
            highest = mag
    return highest

assert part_2(second_test_lines) == 3993
print(part_2(real_lines))