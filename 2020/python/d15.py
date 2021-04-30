from collections import defaultdict, Counter
from utils import timer

@timer
def first_answer(nums, limit=2020):
    data = {num: i for i, num in enumerate(nums)}
    last_num = nums[-1]
    for round in range(len(nums), limit):
        new_num = round - 1 - data.get(last_num, round - 1)
        data[last_num] = round - 1
        last_num = new_num
    print('next')
    #for key, value in record.items():
    #    print(f'{key:>3}: {value}')
    return last_num



TEST_DATA = [0, 3, 6]

assert first_answer(TEST_DATA) == 436
assert first_answer([1,3,2]) == 1
assert first_answer([2,1,3]) == 10
assert first_answer([1,2,3]) == 27
assert first_answer([2,3,1]) == 78
assert first_answer([3,2,1]) == 438
assert first_answer([3,1,2]) == 1836

real_input = [14,3,1,0,9,5]
print(first_answer(real_input, 30000000))