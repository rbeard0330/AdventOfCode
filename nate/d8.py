from collections import Counter

with open('nate/inputs/in8.txt') as f:
    pic = f.readline().strip()

assert len(pic) % (25 * 6) == 0, len(pic)

def layers(pic, width=25, height=6):
    ix = 0
    while (temp := pic[ix:ix+(width * height)]):
        yield temp
        ix += width * height

def pixelAt(layers, x, y):
    for layer in layers:
        if (color := layer[25 * y + x]) != '2':
            return color
    raise ValueError(f"All layers transparent at {x}, {y}")

counters = [Counter(layer) for layer in layers(pic)]
layer = min(counters, key=lambda i: i['0'])
print(layer['1'] * layer['2']) # part 1
l = list([layer for layer in layers(pic)])
for y in range(6):
    print(''.join(['X' if pixelAt(l, x, y) == '1' else ' ' for x in range(25)]))