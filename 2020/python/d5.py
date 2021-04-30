TT = str.maketrans({'B': '1', 'R': '1', 'F': '0', 'L': '0'})


def to_seat_number(s):
    s = s.translate(TT)
    return int(s[:7], 2), int(s[7:], 2)


def seat_id(s):
    row, seat = to_seat_number(s)
    return row * 8 + seat


assert to_seat_number('FBFBBFFRLR') == (44, 5)
assert to_seat_number('BFFFBBFRRR') == (70, 7)
assert to_seat_number('FFFBBBFRRR') == (14, 7)
assert to_seat_number('BBFFBBFRLL') == (102, 4)

assert seat_id('FBFBBFFRLR') == 357
assert seat_id('BFFFBBFRRR') == 567
assert seat_id('FFFBBBFRRR') == 119
assert seat_id('BBFFBBFRLL') == 820


def first_answer():
    return max(seat_id(s) for s in open('data/d5.txt').readlines())


def second_answer(max_seat):
    seats = set(seat_id(s) for s in open('data/d5.txt').readlines())
    for i in range(max_seat):
        if i not in seats and i - 1 in seats and i + 1 in seats:
            return i


max_seat_id = first_answer()
print(max_seat_id)

print(second_answer(max_seat_id))
