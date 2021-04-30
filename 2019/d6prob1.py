import os.path
from collections import defaultdict, deque

orbits = defaultdict(list)

file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d6p1.txt")


with open(file_name, "r") as f:
    for line in f.readlines():
        key, value = line.strip().split(")")
        orbits[key].append(value)

node_set = set(orbits.keys())
for key in orbits:
    node_set |= set(orbits[key])

distances = dict()
for node in node_set:
    distances[node] = None

distances["COM"] = 0
shortest_paths = defaultdict(list)
to_visit = deque()
to_visit.append(("COM", distances["COM"], []))
visited = set()

while to_visit:
    node, d, path = to_visit.popleft()
    distances[node] = d
    shortest_paths[node] = path + [node]
    visited.add(node)
    if node in orbits:
        for next_node in orbits[node]:
            to_visit.append((next_node, d + 1, shortest_paths[node]))

assert visited == node_set

# Problem 1
print(sum(distances.values()))

my_path = shortest_paths["YOU"][:-1]
santa_path = shortest_paths["SAN"][:-1]
common_nodes = 0
for node in my_path:
    if node in santa_path:
        common_nodes += 1
        prior_node = node
    else:
        break

my_path = my_path[common_nodes - 1:]
santa_path = santa_path[common_nodes - 1:]
assert my_path[0] == prior_node

print(len(my_path) + len(santa_path) - 2)
