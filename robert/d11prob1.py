from util.intcode import AdvancedIntcoder, parse_input

from util.file_ops import get_input_file_name
from util.point import Point


VECT = {0: Point(0, 1), 90: Point(1, 0), 180: Point(0, -1), 270: Point(-1, 0)}


class PixGrid():

    def __init__(self):
        self.pos = Point(0, 0)
        self.facing = 0
        self.painted = {}

    def paint(self, val1, val2):
        "Takes two inputs: color to paint and bool for turn direction."
        assert val1 == 0 or val1 == 1
        assert val2 == 0 or val2 == 1

        self.painted[self.pos] = val1
        self.facing = (self.facing + 90 * (2 * val2 - 1)) % 360
        self.pos = self.pos + VECT[self.facing]

    def return_color(self):
        return self.painted.get(self.pos, 0)

    def __str__(self):
        min_y = max_y = min_x = max_x = 0
        for p in self.painted.keys():
            min_y = min(min_y, p.y)
            min_x = min(min_x, p.x)
            max_y = max(max_y, p.y)
            max_x = max(max_x, p.x)
        s_list = []
        for y in range(max_y, min_y - 1, -1):
            s_sublist = []
            for x in range(min_x, max_x + 1):
                color = self.painted.get(Point(x, y), 0)
                s_sublist.append("▮" if color else " ")
            s_list.append("".join(s_sublist))
        return "\n".join(s_list)


class PaintBot(AdvancedIntcoder):
    def __init__(self, tape, input_queue):
        super().__init__(tape, input_queue)
        self.array = PixGrid()
        self.output = None

    # -------------Core Loop-----------------------------

    def run(self, start_pos=0, return_pos=0, edits=(), reset=False):

        if reset:
            for addr, val in edits:
                self[addr] = val
            self.pos = start_pos

        while self.valid_run_status:
            exec_f, param_f, pos_f = self.instructs[self.data[0]]
            f_inputs = param_f(self, self.data[-1])
            exec_f(*f_inputs)
            pos_f(self)

    # -------------IO-------------------------------------

    def try_to_store_input(self, addr):
        self[addr] = self.array.return_color()

    def output(self, val):
        if self.output is not None:
            self.array.paint(self.output, val)
            self.output = None
        else:
            self.output = val


file_name = get_input_file_name("d11.txt")
bot = PaintBot(parse_input(file_name), [])
bot.run()
print("Part1\n", len(bot.array.painted))
bot2 = PaintBot(parse_input(file_name), [])
bot2.array.painted[Point(0, 0)] = 1
bot2.run()
print(bot2.array)
