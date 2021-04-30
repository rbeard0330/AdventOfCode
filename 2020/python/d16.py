from functools import reduce
from operator import mul
import re

from utils import strip_prefix


TICKET_RULE_REGEX = re.compile(r'^(.+): (\d+)-(\d+) or (\d+)-(\d+)$')


def parse_rule(rule):
    name, min1, max1, min2, max2 = TICKET_RULE_REGEX.fullmatch(rule).groups()
    return name, set(range(int(min1), int(max1) + 1)) | set(range(int(min2), int(max2) + 1))


def parse_input(input):
    rule_segment, my_ticket_segment, other_ticket_segment = input.split('\n\n')
    rules = {name: values for name, values in (parse_rule(rule) for rule in rule_segment.splitlines())}

    my_ticket = [int(s) for s in strip_prefix(my_ticket_segment, 'your ticket:\n').split(',')]
    print(my_ticket)

    other_tickets = [[int(s) for s in line.split(',')]
                     for line in strip_prefix(other_ticket_segment, 'nearby tickets:\n').splitlines()]

    return rules, my_ticket, other_tickets


def first_answer(input):
    rules, _, other_tickets = parse_input(input)
    all_possible_values = set().union(*rules.values())
    return sum(sum(num for num in ticket if num not in all_possible_values) for ticket in other_tickets)


def second_answer(input):
    rules, my_ticket, unfiltered_other_tickets = parse_input(input)
    all_possible_values = set().union(*rules.values())
    other_tickets = [ticket for ticket in unfiltered_other_tickets if all(num in all_possible_values for num in ticket)]
    field_values = [set(ticket[n] for ticket in other_tickets) for n in range(len(other_tickets[0]))]
    possible_fields = [set(name for name, allowed_values in rules.items() if field_value <= allowed_values)
                       for field_value in field_values]
    choice_count = [len(s) for s in possible_fields]
    assignments = [None] * len(choice_count)
    for order in range(1, len(choice_count) + 1):
        i = choice_count.index(order)
        assert len(possible_fields[i]) == 1, possible_fields[i]
        assigned_label = possible_fields[i].pop()
        possible_fields = [s - {assigned_label} for s in possible_fields]
        assignments[i] = assigned_label
    filtered_values = [value for label, value in zip(assignments, my_ticket) if label.startswith('departure')]
    assert len(filtered_values) == 6
    return reduce(mul, filtered_values)



TEST_DATA1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


assert first_answer(TEST_DATA1) == 71

TEST_DATA2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

real_data = open('data/d16.txt').read()
print(first_answer(real_data))

print(second_answer(real_data))