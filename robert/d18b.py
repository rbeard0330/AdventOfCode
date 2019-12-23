from collections import defaultdict
from itertools import chain

from util.point import Point
from util.file_ops import get_input_file_name
from d18a import KeyMaze, parse_array, trim_graph


def solve_mazes(mazes):
    available_keys = set()
    for i, m in enumerate(mazes):
        available_keys |= {
        (i, k) for k, p in m.keys.items() if p in m.c_dict[m.start_comp]}



    
    subtour_list = [    # Tours of len(n) in dict at subtour_list[n]
        {frozenset(k):
            {frozenset(i, k): m.dists[m.start_pos][m.keys[k]]}
            for m in mazes
            for (i, k) in available_keys
        }]
    # Each dict is keyed by visited_keys to another dict.  Inner dict has
    # cost to visit those keys by last key visisted

    while len(subtour_list) < 26:
        subtour_data = subtour_list[-1]
        subtours_to_extend = frozenset(subtour_data.keys()) # set of sets
        subtour_list.append(defaultdict(dict))
        for subtour in subtours_to_extend:
            cost_data = subtour_data[subtour]
            for next_key in chain((gen_next_key(m, subtour) for m in mazes)):
                key_pos = keys[next_key]
                shortest = NaN
                for ending_key in cost_data:
                    total = (cost_data[ending_key]
                            + maze.dists[keys[ending_key]][key_pos])
                    if total < shortest:
                        shortest = total 
                subtour_list[-1][subtour | {next_key}][next_key] = shortest
    return subtour_list[-1]




array = []
fn = get_input_file_name("d18m.txt")
with open(fn, "r") as f:
    array = [line.strip() for line in f.readlines()]

top_half, bottom_half = array[:41], array[40:]  # Midline wall is shared
left_top = [line[:41] for line in top_half]
right_top = [line[40:] for line in top_half]

arrays = [[line[:41] for line in array[:41]],
          [line[40:] for line in array[:41]],
          [line[:41] for line in array[40:]],
          [line[40:] for line in array[40:]]]
for a in arrays:
    for b in arrays:
        assert len(a) * len(a[0]) == len(b) * len(b[0])
mazes = []
for a in arrays:
    graph, keys, door_connects, start_pos = parse_array(a)
    trim_graph(graph, keys, door_connects, start_pos)
    a.append(KeyMaze(graph, start_pos, keys, door_connects))

maze_dict = {}
for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for m in mazes:
        if c in m.keys:
            maze_dict[c] = m
        
