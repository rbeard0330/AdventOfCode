from functools import reduce, lru_cache
from operator import mul


def first_answer(lines):
    nums = [int(line) for line in lines] + [0]
    nums.sort()
    diffs = [b - a for a, b in zip(nums, nums[1:])]
    return sum(diff == 1 for diff in diffs) * (sum(diff == 3 for diff in diffs) + 1)


def second_answer(lines):
    nums = [int(line) for line in lines] + [0]
    nums += [max(nums) + 3]
    nums.sort()
    paths = [0 for _ in nums]
    paths[0] = 1
    for i in range(len(paths)):
        for offset in range(1, 4):
            if i + offset < len(paths) and nums[i + offset] - nums[i] <= 3:
                paths[i + offset] += paths[i]
    return paths[-1]


TEST_DATA1 = """16
10
15
5
1
11
7
19
6
12
4""".splitlines()

TEST_DATA2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".splitlines()

assert first_answer(TEST_DATA1) == 5 * 7
assert first_answer(TEST_DATA2) == 22 * 10

assert second_answer(TEST_DATA1) == 8
assert second_answer(TEST_DATA2) == 19208

real_data = open('data/d10.txt').read().splitlines()

print(first_answer(real_data))
print(second_answer(real_data))