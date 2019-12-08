import os.path


class Pixel():
    def __init__(self, str):
        self.layers = [int(c) for c in str]

    def __getitem__(self, key):
        return self.layers[key]

    @property
    def visible(self):
        for i in self.layers:
            if i != 2:
                return i


class Photo():
    def __init__(self, w, h, data):
        self.pix_array = [[Pixel(data[x + w * y::w * h]) for x in range(w)]
                          for y in range(h)]
        self.depth = len(data) // w // h
        self.visible_array = [[None for x in range(w)] for y in range(h)]

    def __iter__(self):
        for line in self.pix_array:
            for pixel in line:
                yield pixel

    def count_in_layer(self, layer, x):
        counter = 0
        for pixel in self:
            if pixel[layer] == x:
                counter += 1
        return counter

    def decode(self):
        for y, line in enumerate(self.pix_array):
            for x, pix in enumerate(line):
                self.visible_array[y][x] = pix.visible

    def __str__(self):
        s_list = []
        for line in self.visible_array:
            for pix in line:
                if pix:
                    s_list.append("▮")
                else:
                    s_list.append(" ")
            s_list.append("\n")
        return "".join(s_list)


file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d8.txt")

with open(file_name, "r") as f:
    for line in f.readlines():
        input = line.strip()

a = Photo(25, 6, input)

best = best_layer = 151
for i in range(a.depth):
    if (current := a.count_in_layer(i, 0)) < best:
        best = current
        best_layer = i
ones, twos, = a.count_in_layer(best_layer, 1), a.count_in_layer(best_layer, 2)
answer = ones * twos
print(f"Part 1\n{answer}")

a.decode()
print(f"Part 2\n{a}")
