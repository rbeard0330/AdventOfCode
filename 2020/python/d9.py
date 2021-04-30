from collections import deque


def update_sums(sums, values, new_value):
    values.append(new_value)
    sums.append(set())
    for old_value, sum_set in zip(values, sums):
        if old_value != new_value:
            sum_set.add(old_value + new_value)


def first_answer(lines, lookback=25):
    sums = deque(maxlen=lookback)
    values = deque(maxlen=lookback)
    for index, line in enumerate(lines):
        new_value = int(line.strip())
        if index >= lookback and not any(new_value in sum_set for sum_set in sums):
            return new_value
        update_sums(sums, values, new_value)


def second_answer(lines, target_sum):
    nums = [int(line.strip()) for line in lines]
    left_index = right_index = 0
    running_sum = nums[0]
    while right_index < len(nums):
        if running_sum == target_sum:
            addends = nums[left_index: right_index + 1]
            assert sum(addends) == target_sum
            return min(addends) + max(addends)
        if running_sum > target_sum:
            running_sum -= nums[left_index]
            left_index += 1
        if running_sum < target_sum:
            right_index += 1
            running_sum += nums[right_index]


TEST_DATA = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".strip().splitlines()

target_number = first_answer(TEST_DATA, lookback=5)
assert target_number == 127
assert second_answer(TEST_DATA, target_number) == 62

real_data = [line.strip() for line in open('data/d9.txt').readlines()]

target_number = first_answer(real_data)
print(target_number)
print(second_answer(real_data, target_number))
