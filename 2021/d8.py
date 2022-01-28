from utils import read_input, time_fn


def read_notes(lines):
    result = []
    for line in lines:
        left, right = line.split(' | ')
        result.append((left.split(), right.split()))
    return result


def part_1(lines):
    notes = read_notes(lines)
    return sum(sum(is_1_4_7_8(group) for group in note[1]) for note in notes)


def is_1_4_7_8(group):
    return len(group) in [2, 3, 4, 7]


test_lines = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()

assert part_1(test_lines) == 26
real_lines = read_input(8)
print(part_1(real_lines))

DIGIT_MAPS = {
    0: {0, 1, 2, 3, 4, 5},
    1: {1, 2},
    2: {0, 1, 3, 4, 6},
    3: {0, 1, 2, 3, 6},
    4: {1, 2, 5, 6},
    5: {0, 2, 3, 5, 6},
    6: {0, 2, 3, 4, 5, 6},
    7: {0, 1, 2},
    8: {0, 1, 2, 3, 4, 5, 6},
    9: {0, 1, 2, 3, 5, 6},
}

signals = 'abcdefg'


def possibly_valid_digit(signal_group, partial_mapping: dict[str, int]):
    segment_set = {partial_mapping[c] for c in signal_group if c in partial_mapping}
    return any(segment_set <= digit_segments for digit_segments in DIGIT_MAPS.values()
               if len(digit_segments) == len(signal_group))


assert not possibly_valid_digit('ab', {'a': 0, 'b': 1})
assert possibly_valid_digit('ab', {'b': 1})
assert possibly_valid_digit('ab', {'a': 2, 'b': 1})


solve_order = [6, 4, 1, 2, 3, 5, 0]


def parse_line(line):
    left, right = line
    mapping = build_mapping(left + right)
    base = 1
    result = 0
    for group in right[::-1]:
        result += base * read_digit(group, mapping)
        base *= 10
    return result


def build_mapping(groups, mapping=None):
    mapping = mapping or {}
    if len(mapping) == 7:
        return mapping
    target_segment = [i for i in solve_order if i not in mapping.values()][0]
    for possible_signal in set(signals) - set(mapping):
        candidate = mapping | {possible_signal: target_segment}
        if not all(possibly_valid_digit(group, candidate) for group in groups):
            continue
        extended_mapping = build_mapping(groups, candidate)
        if extended_mapping is not None:
            return extended_mapping


def read_digit(group, mapping):
    segment_set = {mapping[c] for c in group}
    for n, segments in DIGIT_MAPS.items():
        if segment_set == segments:
            return n
    raise Exception(f'invalid group {group} with mapping {mapping}')


@time_fn
def part_2(lines):
    notes = read_notes(lines)
    return sum(parse_line(note) for note in notes)


assert part_2(test_lines) == 61229
print(part_2(real_lines))
