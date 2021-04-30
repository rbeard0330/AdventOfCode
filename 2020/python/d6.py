from functools import reduce
from operator import and_


def first_answer(groups):
    return sum(len(set(group) - {'\n'}) for group in groups.split('\n\n'))


def second_answer(groups):
    return sum(len(reduce(and_, (set(response) for response in group.split())))
               for group in groups.split('\n\n'))


TEST_DATA = """
abc

a
b
c

ab
ac

a
a
a
a

b"""

assert first_answer(TEST_DATA) == 11
assert second_answer(TEST_DATA) == 6

real_data = open('data/d6.txt').read()
print(first_answer(real_data))
print(second_answer(real_data))
