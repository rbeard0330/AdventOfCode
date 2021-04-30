import os

from util.intcode import AdvancedIntcoder, parse_input
from util.file_ops import get_input_file_name

class GameCoder(AdvancedIntcoder):

    def output(self, val):
        self.output_queue.append(val)


class GraphicalGameCoder(AdvancedIntcoder):

    def __init__(self, w, h, *args, vis=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = w
        self.h = h
        self.area = w * h
        self.pixels = {}
        self.vis = vis

    def output(self, val):
        self.output_queue.append(val)
        if len(self.output_queue) == 3:
            loc = tuple(self.output_queue[:2])
            new_data = self.output_queue[-1]
            if loc not in self.pixels or self.pixels[loc] != new_data:
                self.pixels[loc] = new_data
                assert isinstance(loc, tuple)
                assert len(loc) == 2
                assert isinstance(self.pixels[loc], int)
                if loc == (-1, 0):
                    self.score = self.output_queue[2]
                elif len(self.pixels) >= self.area:
                    if self.vis:
                        self.draw()
            self.output_queue = []

    def draw(self):
        os.system("cls")
        s_list = []
        for y in range(self.h + 1):
            row_list = []
            for x in range(self.w + 1):
                row_list.append(PIXEL_KEY[self.pixels.get((x, y), 0)])
            s_list.append("".join(row_list))
        print("\n".join(s_list))


def hack(game):
    game.reset([], clear_tape=True)
    game.tape[0] = 2
    while not game.op_status["halted"]:
        game.run()
        for key in game.pixels:
            if game.pixels[key] == 4:
                b_x = key[0]
            elif game.pixels[key] == 3:
                p_x = key[0]
        i = (b_x - p_x) / abs(b_x - p_x) if b_x != p_x else 0
        game.input_queue.append(i)
    return game.score


PIXEL_KEY = {0: " ", 1: "|", 2: "▮", 3: "___", 4: "⬤"}

file_name = get_input_file_name("d13.txt")
game = GameCoder(tape := parse_input(file_name), [])
game.run()
tiles = {}
assert (t := len(game.output_queue)) % 3 == 0
for i in range(t // 3):
    tiles[(game.output_queue[i * 3], game.output_queue[i * 3 + 1])] =\
        (tile_type := game.output_queue[i * 3 + 2])
    assert tile_type in range(5)

print("Part 1:\n", sum((1 for v in tiles.values() if v == 2)))

max_x = max_y = 0
for key in tiles:
    max_x = max(max_x, key[0])
    max_y = max(max_y, key[1])

arcade = GraphicalGameCoder(max_x, max_y, tape, [])
print("Part 2:\n", hack(arcade))
