from itertools import product

from utils import read_input


class BingoCard:
    def __init__(self, lines) -> None:
        self.lines = [[(int(num.strip()), False) for num in line.split()] for line in lines]
        assert len(self.lines) == 5
        assert all(len(line) == 5 for line in self.lines)

    def call_number(self, n):
        for i, j in product(range(5), range(5)):
            if self.lines[i][j][0] == n:
                assert not self.lines[i][j][1]
                self.lines[i][j] = (n, True)
        return self.is_winner()

    def is_winner(self):
        def eval_sequence(squares):
            if all(marked for _, marked in squares):
                total_unmarked = 0
                for i, j in product(range(5), range(5)):
                    if not self.lines[i][j][1]:
                        total_unmarked += self.lines[i][j][0]

                return total_unmarked

            return False

        result = False
        for i in range(5):
            result = (result
                      or eval_sequence(self.lines[i])
                      or eval_sequence([line[i] for line in self.lines]))
        # result = (result
        #           or eval_sequence([self.lines[i][4 - i] for i in range(5)])
        #           or eval_sequence([self.lines[i][i] for i in range(5)]))
        return result


card = BingoCard(['1 2 3 4 5', '6 7 8 9 10', '11 12 13 14 15', '16 17 18 19 20', '21 22 23 24 25'])
for i in range(1, 5):
    assert not card.call_number(i)
assert card.call_number(5)

card = BingoCard(['1 2 3 4 5', '6 7 8 9 10', '11 12 13 14 15', '16 17 18 19 20', '21 22 23 24 25'])
for i in range(4):
    assert not card.call_number(5 * i + 1)
assert card.call_number(21)

# card = BingoCard(['1 2 3 4 5', '6 7 8 9 10', '11 12 13 14 15', '16 17 18 19 20', '21 22 23 24 25'])
# assert not card.call_number(1)
# assert not card.call_number(7)
# assert not card.call_number(13)
# assert not card.call_number(19)
# assert card.call_number(25) == 1 + 7 + 13 + 19 + 25
#
# card = BingoCard(['1 2 3 4 5', '6 7 8 9 10', '11 12 13 14 15', '16 17 18 19 20', '21 22 23 24 25'])
# assert not card.call_number(5)
# assert not card.call_number(9)
# assert not card.call_number(13)
# assert not card.call_number(17)
# assert not card.call_number(22)
# assert card.call_number(21) == 5 + 9 + 13 + 17 + 21

test_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".split('\n')


def part_1(lines):
    called, *card_lines = lines
    card_start = 1
    cards = []
    while card_start < len(card_lines):
        cards.append(BingoCard(card_lines[card_start: card_start + 5]))
        card_start += 6
    for num in [int(n.strip()) for n in called.split(',')]:
        results = [card.call_number(num) for card in cards]
        wins = list(filter(bool, results))
        if wins:
            return wins[0] * num


assert part_1(test_input) == 4512
print(part_1(read_input(4)))


def part_2(lines):
    called, *card_lines = lines
    card_start = 1
    cards = []
    while card_start < len(card_lines):
        cards.append(BingoCard(card_lines[card_start: card_start + 5]))
        card_start += 6
    for num in [int(n.strip()) for n in called.split(',')]:
        results = [card.call_number(num) for card in cards]
        if len(results) == 1 and results[0]:
            return results[0] * num
        cards = [card for card, result in zip(cards, results) if not result]


assert part_2(test_input) == 1924
print(part_2(read_input(4)))
