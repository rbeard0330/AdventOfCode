import re

from utils import bench


@bench(100)
def first_answer():
    return sum(int(min_count) <= pw.count(key_letter) <= int(max_count)
               for min_count, max_count, key_letter, pw
               in map(lambda line: re.split(r'-|:\s|\s', line.strip()),
                      open('data/d2.txt').readlines()))


@bench(100)
def second_answer():
    return sum((pw[int(first_index) - 1] == key_letter) ^ (pw[int(second_index) - 1] == key_letter)
               for first_index, second_index, key_letter, pw
               in map(lambda line: re.split(r'-|:\s|\s', line.strip()),
                      open('data/d2.txt').readlines()))


print(first_answer())
print(second_answer())
