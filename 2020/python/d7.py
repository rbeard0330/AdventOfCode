from functools import lru_cache as do_dynamic_programming_for_me


def parse_rule(s):
    container_part, contents_part = s.rstrip("\n.").split(' contain ')
    container = strip_suffix(container_part, " bags")
    if contents_part == 'no other bags':
        return container, []
    contents_list = [strip_suffix(content_item, 'bags') for content_item in contents_part.split(',')]
    return container, [(int(count), description.strip())
                       for count, description in (item.split(maxsplit=1) for item in contents_list)]


def strip_suffix(text, in_order_suffix):
    for letter in reversed(in_order_suffix):
        text = text.rstrip(letter)
    return text


def make_bag_graph(rules):
    contains = {}
    for rule in rules:
        container, contents = parse_rule(rule)
        assert container not in contains, f'{rule}, {contains[container]}'
        contains[container.strip()] = contents
    return contains


def first_answer(rules):
    graph = make_bag_graph(rules)

    @do_dynamic_programming_for_me
    def contains_gold_bag(start_bag):
        return any(kind == "shiny gold" or contains_gold_bag(kind) for _count, kind in graph[start_bag])

    return sum(contains_gold_bag(kind) for kind in graph)


def second_answer(rules):
    graph = make_bag_graph(rules)

    @do_dynamic_programming_for_me
    def count_contents(start_bag):
        return sum(count * count_contents(kind) for count, kind in graph[start_bag]) + 1

    return count_contents('shiny gold') - 1


FIRST_TEST_RULES = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split('\n')

SECOND_TEST_RULES = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".split('\n')

assert first_answer(FIRST_TEST_RULES) == 4
assert second_answer(SECOND_TEST_RULES) == 126

real_rules = list(open('data/d7.txt').readlines())
print(first_answer(real_rules))
print(second_answer(real_rules))
