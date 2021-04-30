from collections import deque
from itertools import islice


def parse_deck(lines):
    return deque(int(line) for line in lines)


def compute_score(winner):
    return sum((index + 1) * value for index, value in enumerate(reversed(winner)))


def make_decks(data):
    p1_block, p2_block, *_ = data.split('\n\n')
    p1 = parse_deck(p1_block.split(':')[1].strip().splitlines())
    p2 = parse_deck(p2_block.split(':')[1].strip().splitlines())
    return p1, p2


def recursive_combat(p1, p2):
    SEPARATOR = deque([Ellipsis])
    seen = set()
    while p1 and p2:
        game_state = tuple(p1 + SEPARATOR + p2)
        if game_state in seen:
            return "p1", p1
        seen.add(game_state)
        p1_card, p2_card = p1.popleft(), p2.popleft()
        if len(p1) >= p1_card and len(p2) >= p2_card:
            winner, _ = recursive_combat(deque(islice(p1, 0, p1_card)), deque(islice(p2, 0, p2_card)))
        else:
            winner = "p1" if p1_card > p2_card else "p2"
        if winner == "p1":
            p1.append(p1_card)
            p1.append(p2_card)
        else:
            assert winner == "p2"
            p2.append(p2_card)
            p2.append(p1_card)

    if p1:
        return "p1", p1
    else:
        return "p2", p2


def first_answer(data):
    p1, p2 = make_decks(data)

    while p1 and p2:
        p1_card, p2_card = p1.popleft(), p2.popleft()
        assert p1_card != p2_card
        if p1_card > p2_card:
            p1.append(p1_card)
            p1.append(p2_card)
        else:
            p2.append(p2_card)
            p2.append(p1_card)

    winner = p1 or p2
    return compute_score(winner)


def second_answer(data):
    p1, p2 = make_decks(data)
    winner, winning_deck = recursive_combat(p1, p2)
    return compute_score(winning_deck)


TEST_DATA = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

assert first_answer(TEST_DATA) == 306
assert second_answer(TEST_DATA) == 291

real_data = open('data/d22.txt').read()

print(first_answer(real_data))
print(second_answer(real_data))
