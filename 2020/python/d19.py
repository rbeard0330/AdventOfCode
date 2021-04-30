from functools import lru_cache
import re

from utils import timer

RULE_REGEX = re.compile('([0-9]+): (.+)')
LITERAL = re.compile('"(.)"')


def parse_rules(data):
    rules = {}
    messages = []
    for line in data.splitlines():
        match = RULE_REGEX.fullmatch(line)
        if match:
            rules[match[1]] = match[2]
        else:
            messages.append(line.strip())
    return rules, messages


def first_answer(data):
    rules, messages = parse_rules(data)

    def parse_rule(index):
        s = rules[index]
        if LITERAL.match(s):
            return LITERAL.match(s)[1]
        new_rule = '(' + '|'.join(
            ''.join(parse_rule(rule_number.strip()) for rule_number in choice.split()) for choice in s.split('|')) + ')'
        return new_rule

    rule_zero = re.compile(f'^{parse_rule("0")}$')
    return sum(rule_zero.fullmatch(message) is not None for message in messages)


@timer
def second_answer(data):
    rules, messages = parse_rules(data)
    capture_group_name_index = 0

    @lru_cache()
    def parse_rule(index):
        if index == '8':
            return f'{parse_rule("42")}+'
        if index == '11':
            nonlocal capture_group_name_index
            capture_group_name_index += 1
            rule_42 = parse_rule("42")
            rule_31 = parse_rule("31")
            return '(' + '|'.join(f'({rule_42}{{{n}}}{rule_31}{{{n}}})' for n in range(1, 46)) + ')'
        s = rules[index]
        if LITERAL.match(s):
            return LITERAL.match(s)[1]
        new_rule = '(' + '|'.join(
            ''.join(parse_rule(rule_number.strip()) for rule_number in choice.split()) for choice in s.split('|')) + ')'
        return new_rule

    rule_zero = re.compile(f'^{parse_rule("0")}$')
    return sum(rule_zero.fullmatch(message) is not None for message in messages)


TEST_DATA1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

TEST_DATA2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

ANSWER_SET = {
    'bbabbbbaabaabba',
    'babbbbaabbbbbabbbbbbaabaaabaaa',
    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
    'bbbbbbbaaaabbbbaaabbabaaa',
    'bbbababbbbaaaaaaaabbababaaababaabab',
    'ababaaaaaabaaab',
    'ababaaaaabbbaba',
    'baabbaaaabbaaaababbaababb',
    'abbbbabbbbaaaababbbbbbaaaababb',
    'aaaaabbaabaaaaababaa',
    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
}
assert first_answer(TEST_DATA1) == 2
assert first_answer(TEST_DATA2) == 3
assert second_answer(TEST_DATA2) == 12

real_data = open('data/d19.txt').read()

print(first_answer(real_data))
second_answer_value = second_answer(real_data)
assert second_answer_value < 285
print(second_answer_value)
