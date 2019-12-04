from dataclasses import dataclass
from copy import copy
import os.path


from util.decorators import timer


@dataclass
class Point:
    x:  int
    y:  int

    def __iadd__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        else:
            raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            return Point(self.x + other[0], self.y + other[1])
        elif isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        else:
            raise NotImplementedError


@dataclass
class Segment:
    p1: Point
    p2: Point
    dir: str

    @property
    def x_min(self):
        if self.p1.x <= self.p2.x:
            return self.p1.x
        else:
            return self.p2.x

    @property
    def x_max(self):
        if self.p1.x >= self.p2.x:
            return self.p1.x
        else:
            return self.p2.x

    @property
    def y_min(self):
        if self.p1.y <= self.p2.y:
            return self.p1.y
        else:
            return self.p2.y

    @property
    def y_max(self):
        if self.p1.y >= self.p2.y:
            return self.p1.y
        else:
            return self.p2.y


class Wire:
    def __init__(self, line):
        self.segment_list = []
        self.current_pos = Point(0, 0)
        self._process_input(line)

    def _process_input(self, line):
        p2 = Point(*dir_to_vect(line[0]))
        for turn in line.split(","):
            p1 = p2
            d_vect = Point(*dir_to_vect(turn[0]))
            dir = "H" if d_vect.x != 0 else "V"
            self.current_pos += d_vect * int(turn[1:])
            p2 = copy(self.current_pos)
            self.segment_list.append(Segment(p1, p2, dir))

    def __str__(self):
        s_list = [str(turn) for turn in self.segment_list]
        return "".join(s_list)

    @timer
    def find_closest_intersect(self, other):
        intersect_list = []
        for my_seg in self.segment_list:
            for other_seg in other.segment_list:
                if point := intersect(my_seg, other_seg):
                    intersect_list.append(point)
        return intersect_list


def dir_to_vect(char):
    if char == "R":
        return (1, 0)
    elif char == "L":
        return (-1, 0)
    elif char == "D":
        return (0, -1)
    elif char == "U":
        return (0, 1)
    else:
        raise ValueError(char)


def manhattan_distance(p1, p2=None):
    if p2 is None:
        p2 = ORIGIN
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def intersect(s1, s2):
    "Return point where p1-p2 and p3-p4 intersect, or False if none."

    if s1.dir == s2.dir:
        if s1.dir == "V":
            if s1.p1.x != s2.p1.x:
                return False
            elif s1.y_max == s2.y_min:
                return Point(s1.p1.x, s1.y_max)
            elif s1.y_min == s2.y_max:
                return Point(s1.p1.x, s1.y_min)
            elif (s1.y_min <= s2.y_min <= s1.y_max
                    or s1.y_min <= s2.y_max <= s1.y_max):
                raise NotImplementedError("""Not implemented for overlapping
                                            segments""")
        elif s1.dir == "H":
            if s1.p1.y != s2.p1.y:
                return False
            elif s1.x_max == s2.x_min:
                return Point(s1.p1.y, s1.x_max)
            elif s1.x_min == s2.x_max:
                return Point(s1.p1.y, s1.x_min)
            elif (s1.x_min <= s2.x_min <= s1.x_max
                    or s1.x_min <= s2.x_max <= s1.x_max):
                raise NotImplementedError("""Not implemented for overlapping
                                            segments""")
    if s1.dir == "H":
        h_seg, v_seg = (s1, s2)
    else:
        h_seg, v_seg = (s2, s1)
    if (h_seg.x_min <= v_seg.p1.x <= h_seg.x_max and
            v_seg.y_min <= h_seg.p1.y <= v_seg.y_max):
        return Point(v_seg.p1.x, h_seg.p1.y)
    else:
        return False


ORIGIN = Point(0, 0)
file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d3p1.txt")

wire_list = []
with open(file_name, "r") as f:
    for line in f.readlines():
        wire_list.append(Wire(line))

intersect_list = wire_list[0].find_closest_intersect(wire_list[1])
print(intersect_list)
print(min([manhattan_distance(p) for p in intersect_list]))
