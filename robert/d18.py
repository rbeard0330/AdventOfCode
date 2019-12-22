from copy import deepcopy
from collections import deque

from util.point import Point, Dirs
from util.file_ops import get_input_file_name

DOORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEYS = "abcdefghijklmnopqrstuvwxyz"


def find_shortest_paths(graph):
    "Implements Floyd-Warshall."
    
    global NaN
    NaN = len(graph) ** 2
    distances = {p1:{p2: NaN for p2 in graph} for p1 in graph}
    # next_step = {p1:{p2: None for p2 in graph} for p1 in graph}

    assert len(graph) == len(distances)
    # assert len(graph) == len(next_step)
    for p in distances:
        assert len(graph) == len(distances[p])
    # for p in next_step:
        # assert len(graph) == len(next_step[p])

    for u, v in edges(graph):  # edge is tuple of points
        distances[u][v] = (d := graph[u][v])
        distances[v][u] = d
        # next_step[u][v] = v
        # next_step[v][u] = u
    for v in graph:
        distances[v][v] = 0
        # next_step[v][v] = v  
    for k in graph:
        for i in graph:
            for j in graph:
                d_ij = distances[i][j]
                d_ik = distances[i][k]
                d_jk = distances[j][k]
                if d_ij > d_ik + d_jk:
                    distances[i][j] = d_ik + d_jk
                    distances[j][i] = d_ik + d_jk
                    # next_step[i][j] = next_step[i][k]
                    # next_step[j][i] = next_step[j][k]
    assert (distances[p1][p2] + distances[p2][p3] >= distances[p1][p3]
            for p1 in graph for p2 in graph for p3 in graph)
        # Readable triple loop!
    return distances #, next_step


def get_components(point_set, dists):
    base_p = point_set.pop()
    point_set.add(base_p)   # Get a point at random but put it back
    this_component = set()
    other_components = set()
    for p1 in point_set:
        if dists[base_p][p1] != NaN:
            this_component.add(p1)
        else:
            other_components.add(p1)
    if other_components:
        return [this_component] + get_components(other_components, dists)
    else:
        return [this_component]


def component_from_p(p, comp_list=None):
    if comp_list is None:
        for i, c in C_DICT.items():
            if p in c:
                return i
    else:
        for c in comp_list:
            if p in c:
                return c


def create_component_graph(graph, dists, doors, door_connects):
    door_connects = deepcopy(door_connects)
    comp_list = get_components(set(graph.keys()), dists)
    c_dict = {i: comp_list[i] for i in range(len(comp_list))}
    c_graph = {i: {} for i in c_dict}
    # iterate over doors and see which join which
    for door, connected_ps in door_connects.items():
        p1 = connected_ps.pop()
        c1 = comp_list.index(component_from_p(p1, comp_list))
        p2 = connected_ps.pop()
        c2 = comp_list.index(component_from_p(p2, comp_list))
        assert not connected_ps
        c_graph[c1][door] = c2
        c_graph[c2][door] = c1
    return c_dict, c_graph


def open_door(graph, distances, p, connects, components):
    distances[p] = {p2: NaN for p2 in graph}
    graph[p] = {}
    for p2 in graph:
        distances[p2][p] = NaN
    # add paths through the door to graph
    for n in connects:
        graph[p][n] = 1
        distances[p][n] = 1
        graph[n][p] = 1
        distances[n][p] = 1
        for n2 in connects:
            if n != n2:
                graph[n][n2] = 2
                distances[n][n2] = 2
                graph[n2][n] = 2
                distances[n2][n] = 2
    # extend Floyd-Warshall for new k
    connects.add(p)
    for k in connects:
        for i in graph:
            for j in graph:
                d_ij = distances[i][j]
                d_ik = distances[i][k]
                d_jk = distances[j][k]
                if d_ij > d_ik + d_jk:
                    distances[i][j] = d_ik + d_jk
                    distances[j][i] = d_ik + d_jk
    components = get_components(set(graph.keys()), distances)

def edges(graph):
    "Yields undirected edges in graph."

    visited = set()
    for u in graph:
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                yield (u, v)

def open_all_doors(graph, dists, doors, door_connects):
    components = get_components(set(graph.keys()), dists)
    for d in doors:
        open_door(graph, dists, doors[d], door_connects[d], components)


def check_prereqs(key, have_keys):
    target = KEY_COMP_LOCATIONS[key]
    visited = set()
    reachable = deque()
    reachable.append(START_COMP)
    while reachable:
        curr = reachable.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        if target == curr:
            return True
        for out_key in C_GRAPH[curr]:
            if out_key in have_keys:
                new_comp = C_GRAPH[curr][out_key]
                reachable.append(C_GRAPH[curr][out_key])
    return False

def _test_prereq_func():
    assert check_prereqs("Q", {})
    assert check_prereqs("A", {"U"})
    assert not check_prereqs("A", {})
    assert check_prereqs("B", {
        "N", "O", "K", "D", "G", "H", "F", "C", "V", "P", "I"})
    assert not check_prereqs("B", {
        "N", "O", "K", "D", "G", "H", "F", "C", "V", "P"})
    assert not check_prereqs("B", {"N", "O"})
    assert check_prereqs("C", {"S", "R", "L", "Z"})
    assert not check_prereqs("C", {"S", "R", "L"})
    assert check_prereqs("I",{"S", "R", "L", "Z"})

def prove_no_shortcuts(graph, dists, doors, door_connects):
    all_points = set(graph.keys())
    test_dists = deepcopy(dists)
    open_all_doors(graph, test_dists, doors, door_connects)
    for c in C_DICT.values():
        p_list = [p for p in c]
        other_p_list = list(all_points - set(p_list))
        for i in range(len(p_list)):
            p1 = p_list[i]
            for j in range(i, len(p_list)):
                p2 = p_list[j]
                assert dists[p1][p2] == test_dists[p1][p2], f"{p1}, {p2}"
            for j in range(len(other_p_list)):
                p2 = other_p_list[j]
                assert dists[p1][p2] > test_dists[p1][p2], f"{p1}, {p2}"


def get_keys(dists, available_keys, have_keys):
    pass

def gen_extended_sets(visited):
    missing_keys = {c in DOORS} - visited
    available_keys = {k for k in missing_keys if check_prereqs(k, visited)}
    for k in available_keys:
        yield visited.add(k)

array = []
fn = get_input_file_name("d18.txt")
with open(fn, "r") as f:
    array = [line.strip() for line in f.readlines()]

print(f"array dims are width: {len(array[0])} and height: {len(array)}")

graph = {}
keys = {}
doors = {}
door_connects = {}  # Edges to be added when door is opened
for y in range(len(array)):
    for x in range(len(array[0])):
        if (c := array[y][x]) == "#":
            continue
        else:
            p = Point(x, y)
            p_edges = set()
            for x2, y2 in [d.value for d in Dirs]:
                if ((c2 := array[y + y2][x + x2]) == "."
                        or c2 in KEYS
                        or c2 == "@"):
                    p_edges.add(Point(x + x2, y + y2))
            if c == ".":
                graph[p] = {p2: 1 for p2 in p_edges}
            elif c in KEYS:
                graph[p] = {p2: 1 for p2 in p_edges}
                keys[c.upper()] = p
            elif c in DOORS:
                door_connects[c] = p_edges
                doors[c] = p
            elif c == "@":
                start_pos = p
                graph[p] = {p2: 1 for p2 in p_edges}

special_tiles = {p for p in doors.values()} | {p for p in keys.values()}
special_tiles.add(start_pos)
for s in door_connects.values():
    special_tiles |= s

for key in keys.values():
    assert key in special_tiles
for door in doors:
    assert doors[door] in special_tiles
    for connect in door_connects[door]:
        assert connect in special_tiles

to_delete = {p for p in graph if (
    len(graph[p]) <= 2
    and p not in special_tiles)}
while to_delete:
    while to_delete:
        p_delete = to_delete.pop()
        assert len(graph[p_delete]) <= 2
        assert p_delete not in keys
        assert p_delete not in doors
        # If p is dead-end, just delete
        if len(graph[p_delete]) == 1:
            neighb = [key for key, _ in graph[p_delete].items()][0]
            # ^ Must be a better way?
            del(graph[p_delete])
            del(graph[neighb][p_delete])
            continue
        # if p connects two nodes, connect them directly
        p_neighb1, p_neighb2 = graph[p_delete].keys()
        d_n1_to_n2 = graph[p_neighb1][p_delete] + graph[p_delete][p_neighb2]
        assert (
            d_n1_to_n2
            == graph[p_neighb2][p_delete] + graph[p_delete][p_neighb1])
        del([graph[p_neighb1][p_delete],
            graph[p_neighb2][p_delete],
            graph[p_delete]])
        graph[p_neighb1][p_neighb2] = d_n1_to_n2
        graph[p_neighb2][p_neighb1] = d_n1_to_n2
    to_delete = {p for p in graph if (
        len(graph[p]) <= 2
        and p not in special_tiles)}

# Tests
for p in graph:
    if p not in special_tiles:
        assert len(graph[p]) > 2, f"{p}"
for p_s in graph.values():
    for p in p_s:
        assert p in graph, f"{p}"
for p in keys.values():
    assert p in graph
for d in doors:
    for p in door_connects[d]:
        assert p in graph

print(f"graph shortened: {len(graph)}")

dists = find_shortest_paths(graph)
components = get_components(set(graph.keys()), dists)

C_DICT, C_GRAPH = create_component_graph(graph, dists, doors, door_connects)
my_comp_id = component_from_p(start_pos)
START_COMP = my_comp_id

# Problem is a modified travelling salesman problem. (Note that if all keys
# are available from the start, it reduces to TSP.) Approach is to use
# Held-Karp algorithm, which caches the cost to visit subsets of keys.  One
# key concern is that the distance matrix can change as we collect keys, which
# may create lower-cost paths.  Thus, we first prove that there are no
# shortcuts in the graph.  Assuming this is true, we can use the distance
# matrix with all doors open, and test all permissible permutations of keys.

prove_no_shortcuts(graph, dists, doors, door_connects)
KEY_COMP_LOCATIONS = {key: component_from_p(keys[key]) for key in keys}
open_all_doors(graph, dists, doors, door_connects)  # mutates distances
length = 0
#_test_prereq_func()
available_keys = {k for k, v in keys.items() if v in C_DICT[my_comp_id]}

for i in gen_extended_sets({}):
    print(i)
while length < 26:
    for k in available_keys:
        costs = {}
        for prior_p in visited:
            pass


