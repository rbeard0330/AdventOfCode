import os

from util.intcode import AdvancedIntcoder, parse_input
from util.file_ops import get_input_file_name

class GameCoder(AdvancedIntcoder):

    def output(self, val):
        self.output_queue.append(val)


class GraphicalGameCoder(AdvancedIntcoder):

    def __init__(self, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = w
        self.h = h
        self.area = w * h
        self.pixels = {}

    def output(self, val):
        self.output_queue.append(val)
        if len(self.output_queue) == 3:
            self.pixels[tuple(self.output_queue[:2])] = self.output_queue[-1]
            if tuple(self.output_queue[:2]) == (-1, 0):
                self.score = self.output_queue[2]
            elif len(self.pixels) >= self.area:
                self.draw()
            self.output_queue = []

    def try_to_store_input(self, addr):
        key = input("->")
        if key == "a":
            data = -1
        elif key == "s":
            data = 0
        else:
            data = 1
        self[addr] = data

    def draw(self):
        os.system("cls")
        s_list = []
        for y in range(self.h):
            row_list = []
            for x in range(self.w):
                row_list.append(PIXEL_KEY[self.pixels.get((x, y), 0)])
            s_list.append("".join(row_list))
        print("\n".join(s_list))


PIXEL_KEY = {0: " ", 1: "|", 2: "▮", 3:"_", 4:"⬤"}

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
arcade.run(edits=[(0, 2)], reset=True)
print(arcade.score)
