from functools import reduce
from math import floor

from utils import read_input

openers = '([{<'
closers = ')]}>'
bracket_map = {l: r for l, r in zip(openers, closers)}
wrong_character_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

completion_character_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


class Parser:
    def __init__(self) -> None:
        self.stack = []

    def parse_character(self, c):
        if c in openers:
            self.stack.append(c)
            return True
        elif self.stack and c == bracket_map[self.stack.pop()]:
            return True
        else:
            return False

    def reset(self):
        self.stack = []

    def finish_line(self):
        yield from map(lambda c: bracket_map[c], self.stack[::-1])


def part_1(lines):
    score = 0
    parser = Parser()
    for line in lines:
        for c in line.strip():
            if not parser.parse_character(c):
                score += wrong_character_scores[c]
                break
        parser.reset()
    return score


test_lines = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()
real_lines = read_input(10)

assert part_1(test_lines) == 26397
print(part_1(real_lines))


def score_completion(brackets):
    return reduce(lambda acc, c: acc * 5 + completion_character_scores[c], brackets, 0)


test_completions = {
    '}}]])})]': 288957,
    ')}>]})': 5566,
    '}}>}>))))': 1480781,
    ']]}}]}]}>': 995444,
    '])}>': 294,
}
for string, score in test_completions.items():
    assert score_completion(string) == score


def part_2(lines):
    parser = Parser()
    completion_scores = []
    for line in lines:
        if all(parser.parse_character(c) for c in line.strip()):
            completion_scores.append(score_completion(parser.finish_line()))
        parser.reset()
    return sorted(completion_scores)[floor(len(completion_scores) / 2)]


assert part_2(test_lines) == 288957
print(part_2(real_lines))  # 1823582 too low
