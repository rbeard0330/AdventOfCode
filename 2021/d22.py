from dataclasses import dataclass
from itertools import product

from utils import read_input, time_fn


@dataclass
class Point3D:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Region:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def __post_init__(self):
        assert self.x_min <= self.x_max, self
        assert self.y_min <= self.y_max, self
        assert self.z_min <= self.z_max, self

    def overlaps(self, other: 'Region'):
        return not (self.x_max < other.x_min or self.y_max < other.y_min or self.z_max < other.z_min
                    or self.x_min > other.x_max or self.y_min > other.y_max or self.z_min > other.z_max)

    def modified(self, x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None):
        return Region(x_min=x_min if x_min is not None else self.x_min,
                      x_max=x_max if x_max is not None else self.x_max,
                      y_min=y_min if y_min is not None else self.y_min,
                      y_max=y_max if y_max is not None else self.y_max,
                      z_min=z_min if z_min is not None else self.z_min,
                      z_max=z_max if z_max is not None else self.z_max)

    def __and__(self, other):
        overlap_x_min = max(self.x_min, other.x_min)
        overlap_x_max = min(self.x_max, other.x_max)
        overlap_y_min = max(self.y_min, other.y_min)
        overlap_y_max = min(self.y_max, other.y_max)
        overlap_z_min = max(self.z_min, other.z_min)
        overlap_z_max = min(self.z_max, other.z_max)
        if not self.overlaps(other):
            raise ValueError
        return Region(x_min=overlap_x_min, x_max=overlap_x_max, y_min=overlap_y_min, y_max=overlap_y_max,
                      z_min=overlap_z_min, z_max=overlap_z_max)

    def exclude_region(self, other):
        if not self.overlaps(other):
            yield self
        else:
            overlap_x_min = max(self.x_min, other.x_min)
            overlap_x_max = min(self.x_max, other.x_max)
            overlap_y_min = max(self.y_min, other.y_min)
            overlap_y_max = min(self.y_max, other.y_max)
            overlap_z_min = max(self.z_min, other.z_min)
            overlap_z_max = min(self.z_max, other.z_max)
            bits = []
            if overlap_x_min > self.x_min:
                bit = self.modified(x_max=overlap_x_min - 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            if overlap_x_max < self.x_max:
                bit = self.modified(x_min=overlap_x_max + 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            x_overlap_args = {'x_min': overlap_x_min, 'x_max': overlap_x_max}
            if overlap_y_min > self.y_min:
                bit = self.modified(**x_overlap_args, y_max=overlap_y_min - 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            if overlap_y_max < self.y_max:
                bit = self.modified(**x_overlap_args, y_min=overlap_y_max + 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            y_overlap_args = {'y_min': overlap_y_min, 'y_max': overlap_y_max}
            if overlap_z_min > self.z_min:
                bit = self.modified(**x_overlap_args, **y_overlap_args, z_max=overlap_z_min - 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            if overlap_z_max < self.z_max:
                bit = self.modified(**x_overlap_args, **y_overlap_args, z_min=overlap_z_max + 1)
                assert not bit.overlaps(other), bit
                bits.append(bit)
                yield bit
            bits.append(self & other)
            total_size = sum(len(bit) for bit in bits)
            # print('total size', total_size)
            assert total_size == len(self), f'original size was {len(self)}, but bits {bits} have size {total_size}'

    def __contains__(self, item):
        return (self.x_min <= item.x <= self.x_max
                and self.y_min <= item.y <= self.y_max
                and self.z_min <= item.z <= self.z_max)

    def __iter__(self):
        for x, y, z in product(range(self.x_min, self.x_max + 1), range(self.y_min, self.y_max + 1),
                               range(self.z_min, self.z_max + 1)):
            yield Point3D(x=x, y=y, z=z)

    def __len__(self):
        return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)


r1 = Region(x_min=0, x_max=1, y_min=0, y_max=1, z_min=0, z_max=1)
r2 = Region(x_min=-2, x_max=-1, y_min=0, y_max=1, z_min=0, z_max=1)
assert not r1.overlaps(r2)
assert not r2.overlaps(r1)
r3 = Region(x_min=-2, x_max=0, y_min=0, y_max=1, z_min=0, z_max=1)
assert r1.overlaps(r3)
assert r2.overlaps(r3)
assert r3.overlaps(r1)
assert r3.overlaps(r2)
r4 = Region(x_min=-2, x_max=0, y_min=2, y_max=3, z_min=0, z_max=1)
assert not any(r4.overlaps(r) for r in (r1, r2, r3))

assert list(r1.exclude_region(r2)) == [r1]
assert list(r2.exclude_region(r3)) == []
r3_without_r2 = list(r3.exclude_region(r2))[0]

assert Point3D(x=0, y=0, z=1) in r1
assert Point3D(x=-2, y=1, z=0) not in r3_without_r2
assert Point3D(x=-2, y=1, z=0) in r3
assert Point3D(x=-2, y=1, z=0) in r2


@dataclass
class InitializationStep:
    region: Region
    result: bool


def read_range(s):
    range_min, range_max = s[2:].split('..')
    return int(range_min), int(range_max)


def read_step(line):
    command, coords = line.strip().split()
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = [read_range(bit) for bit in coords.split(',')]
    return InitializationStep(region=Region(x_min=x_min, y_min=y_min, z_min=z_min,
                                            x_max=x_max, y_max=y_max, z_max=z_max),
                              result=command == 'on')


assert read_step('on x=-20..26,y=-36..17,z=-47..7\n') == \
       InitializationStep(region=Region(x_min=-20, x_max=26, y_min=-36, y_max=17, z_min=-47, z_max=7), result=True)


def read_steps(lines):
    return list(map(read_step, lines))


test_lines = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".splitlines()
real_lines = read_input(22)


def part_1(lines):
    test_region = Region(x_min=-50, x_max=50, y_min=-50, y_max=50, z_min=-50, z_max=50)
    relevant_steps = [step for step in read_steps(lines) if test_region.overlaps(step.region)]
    return sum(len(region) for region in (run_reboot_steps(relevant_steps)))


def run_reboot_steps(steps):
    on_regions = []
    for step in steps:
        if step.result is True:
            on_regions.append(step.region)
        else:
            new_on_regions = []
            for region in on_regions:
                original_size = len(region)
                remaining_size = sum(len(region) for region in region.exclude_region(step.region))
                if region.overlaps(step.region):
                    overlap_size = len(region & step.region)
                    assert overlap_size + remaining_size == original_size, f'overlap: {overlap_size}, remaining {remaining_size}, original {original_size}'
                else:
                    assert original_size == remaining_size
                new_on_regions.extend(region.exclude_region(step.region))
            on_regions = new_on_regions
    regions_to_add = set(on_regions)
    disjoint_regions = []
    while regions_to_add:
        new_region = regions_to_add.pop()
        if not any(new_region.overlaps(region) for region in disjoint_regions):
            disjoint_regions.append(new_region)
        else:
            new_region_bits = [new_region]
            conflicting_old_regions = [region for region in disjoint_regions if region.overlaps(new_region)]
            for conflict_region in conflicting_old_regions:
                start_size = sum(len(bit) for bit in new_region_bits)
                conflicts = [bit & conflict_region for bit in new_region_bits if bit.overlaps(conflict_region)]
                overlap_size = sum(len(conflict) for conflict in conflicts)
                new_region_bits = sum((list(bit.exclude_region(conflict_region)) for bit in new_region_bits), [])
                new_region_size = sum(len(bit) for bit in new_region_bits)
                assert start_size == overlap_size + new_region_size
                for bit in new_region_bits:
                    assert not bit.overlaps(conflict_region), f'new {bit} old {conflict_region}'

            disjoint_regions.extend(new_region_bits)
    print(len(disjoint_regions))
    return disjoint_regions


small_test_lines = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11""".splitlines()

small_test_answer = part_1(small_test_lines)
assert small_test_answer == 27 + 19 - 8, small_test_answer

test_answer = part_1(test_lines)
assert test_answer == 590784, test_answer

print(part_1(real_lines))


@time_fn
def part_2(lines):
    return sum(len(region) for region in run_reboot_steps(read_steps(lines)))

part_2_test_lines = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".splitlines()

test_answer = part_2(part_2_test_lines)
assert test_answer == 2758514936282235, test_answer
print(part_2(real_lines))
