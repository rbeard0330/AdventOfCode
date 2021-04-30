from itertools import product

from utils import timer, bench


@timer
def get_first_answer():
    with open('data/d1.txt') as f:
        seen = set()
        for line in f.readlines():
            n = int(line)
            complement = 2020 - n
            if complement in seen:
                return n * complement
            seen.add(n)


@bench(1000)
def get_second_answer():
    with open('data/d1.txt') as f:
        values = list(int(line) for line in f.readlines())
    missing_numbers_for_triads = {(2020 - (a + b)): (a, b)
                                  for a, b in product(values, values)
                                  if a != b}
    for value in values:
        if value in missing_numbers_for_triads:
            n1, n2 = missing_numbers_for_triads[value]
            return n1 * n2 * value


print(get_first_answer())
print(get_second_answer())
