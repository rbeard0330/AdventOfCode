from dataclasses import dataclass
from functools import cached_property, cache
from itertools import product, permutations, combinations

from utils import read_input, time_fn


@cache
def rotate(point, rotation):
    return point.rotate(rotation)

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def from_str(cls, s):
        x, y, z = s.strip().split(',')
        return Point(x=int(x), y=int(y), z=int(z))

    def __sub__(self, other):
        return Point(x=self.x - other.x, y = self.y - other.y, z=self.z - other.z)

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    @cached_property
    def out_of_vision(self):
        return any(abs(dim) > 1000 for dim in [self.x, self.y, self.z])

    @cache
    def rotate(self, rotation):
        current = [self.x, self.y, self.z]
        x, y, z = [current[i] for i in rotation.permutation]
        x_rot, y_rot, z_rot = rotation.reflections
        if x_rot:
            x = -x
        if y_rot:
            y = -y
        if z_rot:
            z = -z
        return Point(x=x, y=y, z=z)

    def unrotate(self, rotation):
        x, y, z = self.x, self.y, self.z
        x_rot, y_rot, z_rot = rotation.reflections
        if x_rot:
            x = -x
        if y_rot:
            y = -y
        if z_rot:
            z = -z
        pts = [x, y, z]
        return Point(x=pts[rotation.permutation.index(0)], y=pts[rotation.permutation.index(1)], z=pts[rotation.permutation.index(2)])

    def roll(self):
        return Point(x=-self.y, y=self.x, z=self.z)

    def turn(self):
        return Point(x=self.x, y=self.z, z=-self.y)


@dataclass(frozen=True)
class Rotation:
    permutation: tuple[int, int, int]
    reflections: tuple[bool, bool, bool]

    @staticmethod
    def all():
        for perm in permutations([0, 1, 2]):
            yield Rotation(permutation=perm, reflections=(False, False, False))
            yield Rotation(permutation=perm, reflections=(True, True, False))
            yield Rotation(permutation=perm, reflections=(False, True, True))
            yield Rotation(permutation=perm, reflections=(True, False, True))



assert len(set(Rotation.all())) == 24
test_point = Point(x=1, y=2, z=3)
def seq(pt):
    new = pt.roll()
    yield new
    for _ in range(3):
        new = new.turn()
        yield new

s1 = list(seq(test_point))
s2 = list(seq(s1[-1]))
s3 = list(seq(s2[-1]))
p4 = s3[-1].roll().turn().roll()
s4 = list(seq(p4))
s5 = list(seq(s4[-1]))
s6 = list(seq(s5[-1]))
test_set = set(s1 + s2 + s3 + s4 + s5 + s6)


all_rotations = {Rotation(permutation=permutation, reflections=reflections)
                 for permutation in permutations([0, 1, 2])
                 for reflections in product([True, False], repeat=3)
                 if test_point.rotate(Rotation(permutation=permutation, reflections=reflections)) in test_set}

for rotation in all_rotations:
    assert test_point.rotate(rotation).unrotate(rotation) == test_point

def read_scanners(lines):
    scanners = {}
    i = -1
    for line in lines:
        if line.startswith('---'):
            i += 1
            assert line.strip() == f'--- scanner {i} ---'
            scanners[i] = []
        elif line.strip():
            scanners[i].append(Point.from_str(line))
    return scanners


def find_compatible_mapping(s1, s2):
    for rotation in all_rotations:
        s2_rotated = [rotate(point, rotation) for point in s2]
        for translation in possible_translations(s1, s2_rotated):
            if is_mapping_compatible_under_translation(s1, s2_rotated, translation):
                return rotation, translation


def possible_translations(s1: list[Point], s2: list[Point]):
    for p1, p2 in product(s1, s2):
        yield p1 - p2


def is_mapping_compatible_under_translation(s1, s2, translation):
    translated_points = {pt + translation for pt in s2}
    s1_set = set(s1)
    matching_points = s1_set & translated_points
    return len(matching_points) >= 12 and all(point.out_of_vision for point in translated_points - s1_set)



real_lines = read_input(19)
scanners = read_scanners(real_lines)
# for i, scanner in scanners.items():
#     print(i, len(scanner))


test_lines = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".splitlines()


@time_fn
def part_1(lines):
    scanners = read_scanners(lines)
    return collect_points(scanners, {0}, 0)


def collect_points(scanners, known_scanners, current_scanner):
    points = set(scanners[current_scanner])
    scanner_positions = {Point(x=0, y=0, z=0)}
    for i in scanners:
        if i in known_scanners:
            continue
        if (mapping := find_compatible_mapping(scanners[current_scanner], scanners[i])) is not None:
            rotation, translation = mapping
            new_points, covered_scanners, new_scanner_positions = collect_points(scanners, known_scanners | {i}, i)
            points |= {pt.rotate(rotation) + translation for pt in new_points}
            scanner_positions |= {scanner.rotate(rotation) + translation for scanner in new_scanner_positions}
            known_scanners |= covered_scanners
    return points, known_scanners, scanner_positions

def manhattan_dist(s1, s2):
    return sum(abs(el1 - el2) for el1, el2 in zip([s1.x, s1.y, s1.z], [s2.x, s2.y, s2.z]))

assert manhattan_dist(Point(x=-1, y=2, z=3), Point(x=2, y=3, z=2)) == 5
assert manhattan_dist(Point(x=1105,y=-1205,z=1229), Point(x=-92,y=-2380,z=-20)) == 3621

def part_2(points):
    pt_list = list(points)
    longest = 0
    for p1, p2 in combinations(pt_list, r=2):
        longest = max(longest, manhattan_dist(p1, p2))
    return longest

test_points = part_1(test_lines)
assert len(test_points[0]) == 79
# print(sorted(test_points, key=lambda pt: pt.x))
assert part_2(test_points[2]) == 3621
real_points = part_1(real_lines)
print(len(real_points[0]))
print(part_2(real_points[2]))
