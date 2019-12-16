from util.file_ops import get_input_file_name
from util.intcode import AdvancedIntcoder, parse_input
from util.point import Point

from collections import defaultdict, deque

class RepairBot(AdvancedIntcoder):

    def output(self, val):
        self.output_queue = val


def DFS(pos):
    visited.add(pos)
    for d in r_directs:
        if (next_pos := pos + d) not in visited:
            if move(d, next_pos):
                connections[pos].append(next_pos)
                connections[next_pos].append(pos)
                DFS(next_pos)
                move(-1 * d, pos)

def move(d, next_pos):
    bot.input_queue.append(r_directs[d])
    bot.run()
    status = bot.output_queue
    if status == 2:
        oxy_pos.append(next_pos)
    elif status == 0:
        return False
    return True


def a_star(connections, target):
    curr = Point(0, 0)
    open_set = {curr}
    prior = {}
    g_score = defaultdict(lambda: 10**6, {curr: 0})
    f_score = {curr: man_dist(curr, target)}
    while open_set:
        last = curr
        open_set.remove(curr := min(open_set, key=lambda n: f_score[n]))
        g_score[curr] = g_score[last] + 1
        if curr == target:
            for p1, p2 in prior.items():
                assert p2 - p1 in r_directs
            path = [curr]
            while curr in prior:
                curr = prior[curr]
                path.append(curr)
            return len(path) - 1
        else:
            for neighb in connections[curr]:
                new_g = g_score[curr] + 1
                if g_score[neighb] > new_g:
                    assert curr - neighb in r_directs
                    prior[neighb] = curr
                    g_score[neighb] = new_g
                    f_score[neighb] = new_g + man_dist(neighb, target)
                    open_set.add(neighb)
    return False


def man_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def oxy(connections, start):
    has_air = set()
    no_air = {r for r in connections} - {start}
    just_got_air = {start}
    t = 0
    while no_air:
        t += 1
        new_air = set()
        has_air |= just_got_air
        while just_got_air:
            r = just_got_air.pop()
            for neighb in connections[r]:
                if neighb not in has_air:
                    new_air.add(neighb)
                    no_air.discard(neighb)
        just_got_air = new_air
        if t > len(connections):
            return False
    return t


file_name = get_input_file_name("d15.txt")
bot = RepairBot(parse_input(file_name), [])
connections = defaultdict(list)
directs = {1: Point(0, 1), 2: Point(0, -1), 3: Point(-1, 0), 4: Point(1, 0)}
r_directs = {Point(0, 1): 1, Point(0, -1): 2, Point(-1, 0): 3, Point(1, 0): 4}
oxy_pos = list()
current_pos = Point(0, 0)
visited = set()
bot.run()
DFS(Point(0, 0))
for p1, l in connections.items():
    for p2 in l:
        assert p2 - p1 in r_directs
print("Part 1:\n", a_star(connections, oxy_pos[0]))
print("Part 2:\n", oxy(connections, oxy_pos[0]))
