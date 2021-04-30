from collections import Counter
from functools import reduce
from operator import mul
import re

TILE_REGEX = re.compile('^Tile (\d+):\n([.#\n]+)$')

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Tile:
    def __init__(self, text):
        match = TILE_REGEX.match(text)
        self.tile_id = int(match[1])
        self.contents = match[2]
        rows = self.contents.split('\n')
        top = rows[0]
        bottom = rows[-1]
        left = ''.join(row[0] for row in rows)
        right = ''.join(row[-1] for row in rows)
        forward_edges = [int(''.join('0' if char == '.' else '1' for char in edge), 2)
                         for edge in [top, right, bottom, left]]
        reversed_edges = [int(''.join('0' if char == '.' else '1' for char in edge[::-1]), 2)
                          for edge in [top, right, bottom, left]]
        self.edge_reverser = {**{f: r for f, r in zip(forward_edges, reversed_edges)},
                              **{r: f for f, r in zip(forward_edges, reversed_edges)}}
        self.current_edges = [self.top_edge, self.right_edge, self.bottom_edge, self.left_edge]
        self.all_edges = {*forward_edges, *reversed_edges}
        self.contents = '\n'.join(row[1: -1] for row in rows[1: -1]).strip()
        self.neighbors = {}

    @property
    def top_edge(self):
        return edge_to_number(self.contents.splitlines()[0])

    @property
    def right_edge(self):
        return edge_to_number(''.join(row[-1] for row in self.contents.splitlines()))

    @property
    def bottom_edge(self):
        return edge_to_number(self.contents.splitlines()[-1])

    @property
    def left_edge(self):
        return edge_to_number(''.join(row[0] for row in self.contents.splitlines()))

    def count_matched_edges(self, tile_set):
        self.matched_edges = self._count_matched_edges(tile_set)
        assert len(self.matched_edges) >= 2, self.tile_id

    def _count_matched_edges(self, tile_set):
        matched_edges = []
        for edge in self.all_edges:
            matches = 0
            for other_tile in tile_set:
                if other_tile == self:
                    continue
                if edge in other_tile.all_edges:
                    matched_edges.append(edge)
                    matches += 1
            assert matches <= 1, f'{self.tile_id}, {matches}'

        return matched_edges

    def __eq__(self, other):
        return self.tile_id == other.tile_id

    def join(self, tile_set, target_edge, orientation):
        opposite_orientation = cross_orientation(orientation)
        assert target_edge in self.all_edges, target_edge
        for i in range(9):
            if self.current_edges[orientation] == target_edge:
                break
            if i == 4:
                self.flip()
            else:
                self.rotate_90_right()
        assert self.current_edges[orientation] == target_edge
        next_edge = self.opposite_edge_from_list(target_edge, self.current_edges)
        for tile in tile_set:
            if tile != self and (next_edge in tile.all_edges):
                self.neighbors[opposite_orientation] = tile
                return [self, *tile.join(tile_set, next_edge, orientation)]
        return [self]

    def flip(self):
        self.contents = '\n'.join(row[::-1] for row in self.contents.splitlines())
        self.current_edges = self.current_edges[:1] + list(reversed(self.current_edges[1:]))
        self.reverse_edge(TOP)
        self.reverse_edge(BOTTOM)

    def rotate_90_right(self):
        rows = self.contents.splitlines()[::-1]
        self.contents = '\n'.join(''.join(tup) for tup in zip(*rows))
        self.current_edges = self.current_edges[-1:] + self.current_edges[:-1]
        self.reverse_edge(TOP)
        self.reverse_edge(BOTTOM)

    def reverse_edge(self, orientation):
        self.current_edges[orientation] = self.edge_reverser[self.current_edges[orientation]]

    def opposite_edge(self, edge):
        if edge not in self.all_edges:
            raise Exception('No match')
        return self.opposite_edge_from_list(edge, self.current_edges) if edge in self.matched_edges else None

    def opposite_edge_from_list(self, edge, edge_list):
        return edge_list[cross_orientation(edge_list.index(edge))]

    def stitch(self):
        return '\n'.join(''.join(row) for row in self._stitch())

    def _stitch(self):
        right_neighbor = self.neighbors.get(RIGHT)
        own_contents = self.contents.splitlines()
        if right_neighbor is None:
            return own_contents
        else:
            combined_rows = [[row, *other_rows] for row, other_rows in zip(own_contents, right_neighbor._stitch())]
            return combined_rows

    def __str__(self):
        return str(self.tile_id)

    def __repr__(self):
        return str(self.tile_id)


def cross_orientation(n):
    return (n + 2) % 4


def edge_to_number(s):
    return int(''.join('0' if char == '.' else '1' for char in s), 2)


orientations = [TOP, RIGHT, BOTTOM, LEFT]
crossed_orientations = [BOTTOM, LEFT, TOP, RIGHT]

for a, b in zip(orientations, crossed_orientations):
    assert cross_orientation(a) == b
    assert cross_orientation(cross_orientation(a)) == a


def first_answer(raw_tiles):
    tiles = [Tile(text) for text in raw_tiles.split('\n\n')]
    for tile in tiles:
        tile.count_matched_edges(tiles)
    potential_corners = [tile.tile_id for tile in tiles if len(tile.matched_edges) == 4]
    if len(potential_corners) == 4:
        return reduce(mul, potential_corners)


def second_answer(raw_tiles, monster):
    tiles = [Tile(text) for text in raw_tiles.split('\n\n')]
    monster = sea_monster_coordinates(monster)
    photo_lines = make_photo(tiles).splitlines()
    y_dim = len(photo_lines)
    x_dim = len(photo_lines[0])
    assert y_dim == x_dim
    for i in range(8):
        assert y_dim == len(photo_lines), len(photo_lines)
        assert x_dim == len(photo_lines[0]), len(photo_lines[0])
        photo_lines = mark_monsters_in_orientation(photo_lines, monster)
        if i == 3:
            photo_lines = flip_photo(photo_lines)
        else:
            photo_lines = rotate_photo(photo_lines)

    return Counter('\n'.join(photo_lines))['#']


def rotate_photo(photo_lines):
    photo_lines = photo_lines[::-1]
    return [''.join(tup) for tup in zip(*photo_lines)]


assert rotate_photo(['abc', 'def', 'ghi']) == ['gda', 'heb', 'ifc']


def flip_photo(photo_lines):
    return [row[::-1] for row in photo_lines]


def mark_monsters_in_orientation(photo_lines, monster):
    x_max = len(photo_lines[0]) - max(monster, key=lambda tup: tup[0])[0]
    y_max = len(photo_lines) - max(monster, key=lambda tup: tup[1])[1]
    for y in range(y_max):
        for x in range(x_max):
            photo_lines = mark_monster_at_coords(photo_lines, x, y, monster)
    return photo_lines


def sea_monster_coordinates(monster):
    return [(x, y) for y, line in enumerate(monster.splitlines()) for x, char in enumerate(line)
            if char == '#']


def mark_monster_at_coords(photo_lines, x, y, monster_coords):
    if all(photo_lines[y + y_off][x + x_off] != '.' for x_off, y_off in monster_coords):
        pixels = [list(row) for row in photo_lines]
        for x_off, y_off in monster_coords:
            pixels[y + y_off][x + x_off] = 'O'
        return [''.join(pix_row) for pix_row in pixels]
    return photo_lines


def make_photo(tiles):
    for tile in tiles:
        tile.count_matched_edges(tiles)
    potential_corners = [tile for tile in tiles if len(tile.matched_edges) == 4]
    top_left = next(corner for corner in potential_corners)
    top_edge = next(edge for edge in top_left.current_edges if edge not in top_left.matched_edges)
    left_side = top_left.join(tiles, top_edge, TOP)
    for tile in left_side:
        tile.join(tiles, tile.current_edges[LEFT], LEFT)
        if not tile.neighbors.get(RIGHT):
            tile.flip()
            tile.join(tiles, tile.current_edges[LEFT], LEFT)
    return '\n'.join(tile.stitch() for tile in left_side).strip()


TEST_DATA = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

TEST_PHOTO = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###"""

SEA_MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

assert first_answer(TEST_DATA) == 20899048083289, first_answer(TEST_DATA)
assert second_answer(TEST_DATA, SEA_MONSTER) == 273, second_answer(TEST_DATA, SEA_MONSTER)

real_data = open('data/d20.txt').read().strip()

print(first_answer(real_data))
print(second_answer(real_data, SEA_MONSTER))
