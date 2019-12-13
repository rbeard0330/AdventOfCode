import os
from copy import copy

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
            loc = tuple(self.output_queue[:2])
            new_data = self.output_queue[-1]
            if loc not in self.pixels or self.pixels[loc] != new_data:
                self.pixels[loc] = new_data
                if tuple(self.output_queue[:2]) == (-1, 0):
                    self.score = self.output_queue[2]
                elif len(self.pixels) >= self.area:
                    self.draw()
            self.output_queue = []

    def draw(self):
        os.system("cls")
        s_list = []
        for y in range(self.h):
            row_list = []
            for x in range(self.w):
                row_list.append(PIXEL_KEY[self.pixels.get((x, y), 0)])
            s_list.append("".join(row_list))
        print("\n".join(s_list))



def hack(game):
    game.tape[0] = 2
    game.master[0] = 2 
    checkpoints = []
    t, offset = run_out_game(game)
    screen = game.pixels        # Game state when we lose
    block_set = {key for key in screen if screen[key] == 2}
    inputs = ([0] * (t - abs(offset))
              + [offset // abs(offset)] * abs(offset))
    print(inputs)
    while block_set:
        # Revert game state
        game.op_status["halted"] = False
        saved_inputs = copy(inputs)
        t, offset = run_out_game(game, inputs)
        inputs = (saved_inputs
                  # Fill goes in the middle so we don't leave the last
                  # position too early
                  + [0] * (t - abs(offset) - len(saved_inputs) - 2)
                  + [offset // abs(offset)] * abs(offset))
        clears = set()
        for block in block_set:
            if game.pixels[block] != 2:
                clears.add(block) 
        block_set -= clears
    return game.score

def run_out_game(game, inputs=None):
    elapsed = 0
    game.reset([], clear_tape=True)
    while not game.op_status["halted"]:
            game.run()
            if inputs:
                game.input_queue.append(inputs.pop(0))
            else:
                game.input_queue.append(0)
            elapsed += 1
        # Game ends... for now
    player, ball = find_player_and_ball(game.pixels)
    game.pixels[player] = 0
    game.pixels[ball] = 0       # The game will redraw
    offset = player - ball
    return elapsed, offset

def find_player_and_ball(screen):
    player = ball = None
    for key in screen:
        if screen[key] == 4:
            ball = key[0]   # Only x-value needed
        elif screen[key] == 3:
            player = key[0]
        if ball and player:
            break
    return ball, player
    
PIXEL_KEY = {0: " ", 1: "|", 2: "▮", 3:"___", 4:"⬤"}

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
hack(arcade)
