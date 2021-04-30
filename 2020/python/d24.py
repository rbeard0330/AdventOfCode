from collections import defaultdict
import enum
from itertools import product


class Direction(enum.Enum):
    EAST = (1, 0, -1)
    SOUTHEAST = (0, 1, -1)
    SOUTHWEST = (-1, 1, 0)
    WEST = (-1, 0, 1)
    NORTHWEST = (0, -1, 1)
    NORTHEAST = (1, -1, 0)

    @staticmethod
    def from_str(s: str):
        if s == 'e':
            return Direction.EAST
        if s == 'w':
            return Direction.WEST
        if s == 'se':
            return Direction.SOUTHEAST
        if s == 'sw':
            return Direction.SOUTHWEST
        if s == 'ne':
            return Direction.NORTHEAST
        if s == 'nw':
            return Direction.NORTHWEST


def follow_directions_to_tile(move_list: str):
    coords = (0, 0, 0)
    index = 0
    while index < len(move_list):
        move, index = parse_one_move(move_list, index)
        coords = tuple(coord + delta for coord, delta in zip(coords, move.value))
    return coords


def parse_one_move(move_list: str, start_index: int):
    if move_list[start_index] in ('e', 'w'):
        end_slice_index = start_index + 1
    else:
        end_slice_index = start_index + 2
    return Direction.from_str(move_list[start_index: end_slice_index]), end_slice_index


def first_answer(tile_list):
    return len(get_initial_black_tiles(tile_list))


def get_initial_black_tiles(tile_list):
    flipped_tiles = set()
    for directions in tile_list:
        flipped_tiles ^= {follow_directions_to_tile(directions)}
    return flipped_tiles


def generate_neighbors(tile):
    for direction in Direction:
        yield tuple(base + offset for base, offset in zip(tile, direction.value))


def tick(initial_black_tiles):
    black_neighbors = defaultdict(int)
    for black_tile in initial_black_tiles:
        for neighbor in generate_neighbors(black_tile):
            black_neighbors[neighbor] += 1
    return ({tile for tile, neighbor_count in black_neighbors.items() if neighbor_count == 2}
            | {tile for tile in initial_black_tiles if 0 < black_neighbors[tile] <= 2})


def second_answer(tile_list):
    black_tiles = get_initial_black_tiles(tile_list)
    for i in range(100):
        black_tiles = tick(black_tiles)
    return len(black_tiles)


TEST_DATA = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines()

assert first_answer(TEST_DATA) == 10
assert second_answer(TEST_DATA) == 2208

real_data = open('data/d24.txt').read().splitlines()

print(first_answer(real_data))
print(second_answer(real_data))
