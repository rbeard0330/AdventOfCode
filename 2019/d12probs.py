from itertools import combinations
from copy import copy
from math import gcd

from d12tests import test1, test2
from util.point import ThreeDVect
from util.file_ops import get_input_file_name


class Body():

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def exert_grav_on(self, other):
        names = ["x", "y", "z"]
        for name in names:
            my_pos = getattr(self.pos, name)
            other_pos = getattr(other.pos, name)
            other_vel = getattr(other.vel, name)
            if my_pos > other_pos:
                other_vel = other_vel + 1
            elif my_pos < other_pos:
                other_vel = other_vel - 1
            setattr(other.vel, name, other_vel)

    def move_self(self):
        self.pos += self.vel

    def __str__(self):
        return f"Body: position {self.pos}; velocity {self.vel}"


def advance(body_list, steps):
    while steps > 0:
        for b1, b2 in combinations(body_list, 2):
            b1.exert_grav_on(b2)
            b2.exert_grav_on(b1)
        for b in body_list:
            b.move_self()
        steps -= 1


def calc_total_energy(body_list):
    energy = 0
    for b in body_list:
        pot = sum(abs(i) for i in b.pos)
        kin = sum(abs(i) for i in b.vel)
        energy += pot * kin
    return energy


def parse_input(file_lines):
    body_list = []
    for line in file_lines:
        line = line[1:-2].strip()
        coords = line.split(", ")
        coords = [c.split("=")[1] for c in coords]
        coords = [int(c) for c in coords]
        body_list.append(Body(ThreeDVect(*coords), ThreeDVect(0, 0, 0)))
    return body_list


def run_tests():
    body_list = parse_input(test1.split("\n"))
    advance(body_list, 10)
    assert calc_total_energy(body_list) == 179

    body_list = parse_input(test2.split("\n"))
    advance(body_list, 100)
    assert calc_total_energy(body_list) == 1940


run_tests()
file_name = get_input_file_name("d12.txt")
file_lines = []
with open(file_name, "r") as f:
    for line in f.readlines():
        file_lines.append(line)

body_list = parse_input(file_lines)
advance(body_list, 2772)
print("Part1:\n", calc_total_energy(body_list))

body_list = parse_input(file_lines)
length = len(body_list)
names = ["x", "y", "z"]
loop_list = []
for name in names:
    pos_list = [getattr(b.pos, name) for b in body_list]
    orig_pos = copy(pos_list)
    vel_list = [0] * 4
    orig_vel = copy(vel_list)
    loops = 0
    while True:
        for i in range(length - 1):
            for j in range(i + 1, length):
                if (i_pos := pos_list[i]) > (j_pos := pos_list[j]):
                    vel_list[i] -= 1
                    vel_list[j] += 1
                elif i_pos < j_pos:
                    vel_list[i] += 1
                    vel_list[j] -= 1
        pos_list = list(map(lambda x, y: x + y, pos_list, vel_list))
        loops += 1
        if vel_list == orig_vel and pos_list == orig_pos:
            break
    loop_list.append(loops)
x, y, z = tuple(loop_list)
lcm1 = x * y // gcd(x, y)
print("Part 2:\n", lcm1 * z // gcd(lcm1, z))
