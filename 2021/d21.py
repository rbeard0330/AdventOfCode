from collections import defaultdict
from dataclasses import dataclass
from itertools import product


def gen_scores(start_space, is_p1):
    offset = 5 if is_p1 else 4
    current_space = start_space
    total_score = 0
    i = 0
    while True:
        current_space = (current_space + 8 * i + offset) % 10 + 1
        total_score += current_space
        i += 1
        yield total_score


test_p1 = gen_scores(4, True)
test_p2 = gen_scores(8, False)
for expected, actual in zip([10, 14, 20, 26], test_p1):
    assert expected == actual

for expected, actual in zip([3, 9, 16, 22], test_p2):
    assert expected == actual


def part_1(p1_start, p2_start):
    prior_p2_score = 0
    for rd, (p1_score, p2_score) in enumerate(zip(gen_scores(p1_start, True), gen_scores(p2_start, False))):
        if p1_score >= 1000:
            return (2 * rd + 1) * 3 * prior_p2_score
        prior_p2_score = p2_score
        if p2_score >= 1000:
            return (2 * rd + 2) * 3 * p1_score


@dataclass(frozen=True)
class GameState:
    p1_score: int
    p2_score: int
    p1_pos: int
    p2_pos: int

    def updated(self, **args):
        new_args = {'p1_score': self.p1_score, 'p2_score': self.p2_score, 'p1_pos': self.p1_pos, 'p2_pos': self.p2_pos} | args
        return GameState(**new_args)

assert part_1(4, 8) == 739785
print(part_1(10, 9))

ALL_SCORES = list(range(22))
ALL_POSITIONS = list(range(1, 11))


def part_2(p1_start, p2_start):
    worlds = defaultdict(int)
    worlds[GameState(p1_score=0, p2_score=0, p1_pos=p1_start, p2_pos=p2_start)] = 1
    p1_wins = p2_wins = 0
    for turn in range(21):
        new_worlds = defaultdict(int)
        for state, count in worlds.items():
            for rolls in product(range(1, 4), repeat=3):
                new_p1_pos = (state.p1_pos + sum(rolls) - 1) % 10 + 1
                new_p1_score = state.p1_score + new_p1_pos
                assert state.p1_score < 21
                assert state.p2_score < 21
                assert new_p1_score > state.p1_score
                new_state = state.updated(p1_pos=new_p1_pos, p1_score=new_p1_score)

                if new_p1_score >= 21:
                    p1_wins += count
                else:
                    assert new_state.p1_score > turn, f'state={state}, roll={rolls}, new_state={new_state}'
                    assert new_state.p1_score < 21
                    assert new_state.p1_score > state.p1_score
                    new_worlds[new_state] += count
        for state in new_worlds:
            assert state.p1_score > turn, state
        newer_worlds = defaultdict(int)
        for state, count in new_worlds.items():
            for rolls in product(range(1, 4), repeat=3):
                new_p2_pos = (state.p2_pos + sum(rolls) - 1) % 10 + 1
                new_p2_score = state.p2_score + new_p2_pos
                new_state = state.updated(p2_pos=new_p2_pos, p2_score=new_p2_score)
                if new_p2_score >= 21:
                    p2_wins += count
                else:
                    newer_worlds[new_state] += count

        for state in newer_worlds:
            assert state.p1_score > turn, state
            assert state.p2_score > turn, state
        worlds = newer_worlds

    return max(p1_wins, p2_wins)


test_part_2_answer = part_2(4, 8)
assert test_part_2_answer == 444356092776315, test_part_2_answer
print(part_2(10, 9))
