from collections import Counter
from functools import cache
from itertools import product

from utils import read_input, time_fn


def read_template_and_rules(lines):
    template, _, *rules = lines
    template = list(template.strip())
    products = {}
    for rule in rules:
        lhs, rhs = rule.strip().split(' -> ')
        products[(lhs[0], lhs[1])] = [lhs[0], rhs]
    return template, products


def tick(polymer, products):
    result = []
    for p1, p2 in zip(polymer, polymer[1:]):
        result.extend(products.get((p1, p2), (p1,)))
    result.append(polymer[-1])
    return result


def compute_difference(polymer):
    c = Counter(polymer)
    most_common, *_, least_common = c.most_common()
    return most_common[1] - least_common[1]


def part_1(lines):
    polymer, rules = read_template_and_rules(lines)
    for _ in range(10):
        polymer = tick(polymer, rules)
    return compute_difference(polymer)


test_lines = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()
real_lines = read_input(14)


@time_fn
def part_2(lines):
    polymer, rules = read_template_and_rules(lines)
    alphabet = set(polymer)
    for rule_output in rules.values():
        alphabet |= set(rule_output)

    @cache
    def tick_20(p):
        for _ in range(20):
            p = tick(p, rules)
        return p

    products = {(c1, c2): tick_20(c1 + c2)[:-1] for c1, c2 in product(alphabet, alphabet)}
    step_20_polymer = tick(polymer, products)
    product_components = {key: Counter(value) for key, value in products.items()}
    step_20_pair_count = Counter(zip(step_20_polymer, step_20_polymer[1:]))
    total_components = Counter()
    for pair, count in step_20_pair_count.items():
        total_components.update({component: count * amount for component, amount in product_components[pair].items()})
    total_components[step_20_polymer[-1]] += 1
    most_common, *_, least_common = total_components.most_common()
    return most_common[1] - least_common[1]


def read_template_and_rules_v2(lines):
    template, _, *rules = lines
    template = list(template.strip())
    products = {}
    for rule in rules:
        lhs, rhs = rule.strip().split(' -> ')
        products[(lhs[0], lhs[1])] = [(lhs[0], rhs), (rhs, lhs[1])]
    return template, products


def tick_v2(pairs, rules):
    next_pairs = Counter()
    for pair, count in pairs.items():
        for new_pair in rules[pair]:
            next_pairs[new_pair] += count
    return next_pairs


@time_fn
def part_2_v2(lines):
    polymer, rules = read_template_and_rules_v2(lines)
    pair_counts = Counter(zip(polymer, polymer[1:]))

    for _ in range(40):
        pair_counts = tick_v2(pair_counts, rules)

    component_counter = count_components_from_pairs(pair_counts, polymer)
    most_common, *_, least_common = component_counter.most_common()
    return int(most_common[1] - least_common[1])


def count_components_from_pairs(pair_counts, template):
    component_counter = Counter()
    for pair, count in pair_counts.items():
        for component in pair:
            component_counter[component] += count / 2
    component_counter[template[0]] += 0.5
    component_counter[template[-1]] += 0.5
    return component_counter


assert part_2_v2(test_lines) == 2188189693529
print(part_2_v2(real_lines))
