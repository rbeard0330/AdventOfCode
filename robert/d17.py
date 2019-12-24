import enum
from collections import deque

from util.file_ops import get_input_file_name
from util.intcode import AdvancedIntcoder, parse_input
from util.point import Point, Segment, Dirs



class VacuumBot(AdvancedIntcoder):
    def output(self, val):
        self.output_queue.append(val)
# Grid is 30 x 39


def find_instruction_set(graph, start, end):
    
    required_seqs = {{["R", 6]}, {[6, "L", 4]}}
    

def postpend(inst_set, new_inst):
    if isinstance(new_inst, int) and isinstance(inst_set[-1], int):
        inst_set[-1] += new_inst
    else:
        inst_set.append(new_inst)

def prepend(inst_set, new_inst):
    if isinstance(new_inst, int) and isinstance(inst_set[-1], int):
        inst_set[0] += new_inst
    else:
        inst_set.insert(0, new_inst)


file_name = get_input_file_name("d17.txt")
bot = VacuumBot(parse_input(file_name), [])
bot.run()
scaffolds = []
x = 0
y = 0
facing = {"^": Dirs.N, ">": Dirs.E, "<": Dirs.W, "v": Dirs.S}
output_list = []
for c in bot.output_queue:
    if c == 10:
        x = 0
        y += 1
        output_list.append("\n")
        continue

    output_list.append(chr(c))
    if c == ord('#'):
        scaffolds.append(Point(x, y))
    elif chr(c) in facing:
        bot_pos = Point(x, y)
        bot_face = facing[chr(c)]
    x += 1

scaff_graph = {tup: set() for tup in scaffolds}
for x, y in scaffolds:
    if (x + 1, y) in scaff_graph:
        scaff_graph[(x, y)].add(Point(x + 1, y))
        scaff_graph[(x + 1, y)].add(Point(x, y))
    if (x, y + 1) in scaff_graph:
        scaff_graph[(x, y)].add(Point(x, y + 1))
        scaff_graph[(x, y + 1)].add(Point(x, y))
    if (x - 1, y) in scaff_graph:
        scaff_graph[(x, y)].add(Point(x - 1, y))
        scaff_graph[(x - 1, y)].add(Point(x, y))
    if (x, y - 1) in scaff_graph:
        scaff_graph[(x, y)].add(Point(x, y - 1))
        scaff_graph[(x, y - 1)].add(Point(x, y))
crossings = []
turns = []
deadends = []
odd_verts = 0
for p, connects in scaff_graph.items():
    if len(connects) > 2:
        crossings.append(p)
    elif len(connects) == 1:
        deadends.append(p)
    else:
        p1 = connects.pop()
        p2 = connects.pop()
        if  p - p1 != p2 - p:
            turns.append(p)
        scaff_graph[p] = {p1, p2}
answer1 = 0
for c in crossings:
    answer1 += c.x * c.y

key_points = crossings + turns + deadends
segment_dict = {p: set() for p in key_points}
for p in segment_dict:
    segment_dict[p] = []
    for path in scaff_graph[p]:
        d = path - p
        steps = 1
        while path not in key_points:
            path = path + d
            steps += 1
        segment_dict[p].append((d, steps, path))

print(segment_dict)
print("".join(output_list))
print(answer1)
print(bot_pos, bot_face)
print(f"odd vertices: {odd_verts}")
print(f"vertex count: {len(cross)}")