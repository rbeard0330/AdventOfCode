import copy


class Seat:
    def __init__(self, is_full):
        self.is_full = is_full
        self.ul = self.up = self.ur = self.left = self.right = self.dl = self.down = self.dr = Wall()

    def __add__(self, other):
        return int(other) + int(self)

    def __radd__(self, other):
        return self + other

    def __int__(self):
        return 1 if self.is_full else 0

    def __str__(self):
        return '#' if self.is_full else 'L'

    def neighbors(self):
        return sum([self.ul, self.up, self.ur, self.left, self.right, self.dl, self.down, self.dr])

    def visible_neighbors(self):
        return sum([self.look_in_direction(direction) for direction in
                    ['ul', 'up', 'ur', 'left', 'right', 'dl', 'down', 'dr']])

    def look_in_direction(self, direction):
        return self.__getattribute__(direction).occupied_seat_in_this_direction(direction)

    def occupied_seat_in_this_direction(self, direction):
        return self.is_full


class Floor(Seat):
    def __init__(self):
        super().__init__(False)

    def __str__(self):
        return '.'

    def __bool__(self):
        return False

    def occupied_seat_in_this_direction(self, direction):
        return self.look_in_direction(direction)


class Wall:
    def __init__(self):
        self.is_full = False

    def occupied_seat_in_this_direction(self, _direction):
        return False

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other


def make_seat_array(lines):
    array = []
    for line in lines:
        row = []
        for char in line.strip():
            if char == 'L':
                row.append(Seat(False))
            elif char == '.':
                row.append(Floor())
            elif char == '#':
                row.append(Seat(True))
            else:
                raise Exception(line)
        array.append(row)
    connect_seats_to_neighbors(array)

    return array


def connect_seats_to_neighbors(array):
    for i, row in enumerate(array):
        for j, seat in enumerate(row):
            if i != 0:
                seat.up = array[i - 1][j]
                if j != 0:
                    seat.ul = array[i - 1][j - 1]
                if j != len(row) - 1:
                    seat.ur = array[i - 1][j + 1]
            if j != 0:
                seat.left = array[i][j - 1]
            if j != len(row) - 1:
                seat.right = array[i][j + 1]
            if i != len(array) - 1:
                seat.down = array[i + 1][j]
                if j != 0:
                    seat.dl = array[i + 1][j - 1]
                if j != len(row) - 1:
                    seat.dr = array[i + 1][j + 1]


def first_answer(lines):
    seats = make_seat_array(lines)
    changes = True
    while changes:
        old_seats = [[copy.copy(seat) for seat in row] for row in seats]
        connect_seats_to_neighbors(old_seats)
        changes = False
        for old_row, new_row in zip(old_seats, seats):
            for old_seat, new_seat in zip(old_row, new_row):
                if not old_seat:
                    continue
                if old_seat.neighbors() >= 4:
                    changes = changes or old_seat.is_full
                    new_seat.is_full = False
                if old_seat.neighbors() == 0:
                    changes = changes or not old_seat.is_full
                    new_seat.is_full = True
    return sum(seat for row in seats for seat in row)


def second_answer(lines):
    seats = make_seat_array(lines)
    changes = True
    while changes:
        old_seats = [[copy.copy(seat) for seat in row] for row in seats]
        connect_seats_to_neighbors(old_seats)
        changes = False
        for old_row, new_row in zip(old_seats, seats):
            for old_seat, new_seat in zip(old_row, new_row):
                if not old_seat:
                    continue
                if old_seat.visible_neighbors() >= 5:
                    changes = changes or old_seat.is_full
                    new_seat.is_full = False
                if old_seat.visible_neighbors() == 0:
                    changes = changes or not old_seat.is_full
                    new_seat.is_full = True
        #_show_seats(seats)
    return sum(seat for row in seats for seat in row)


def _show_seats(seats):
    for row in seats:
        for seat in row:
            print(seat, end='')
        print()
    print()


TEST_DATA = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()


assert first_answer(TEST_DATA) == 37
assert second_answer(TEST_DATA) == 26
print("passed asserts")

real_data = open('data/d11.txt').read().splitlines()

print(first_answer(real_data))
print(second_answer(real_data))
