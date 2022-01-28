from math import floor

from utils import read_input


def parse(lines):
    max_len = max(len(line.strip()) for line in lines)
    return [int(line, 2) for line in lines], max_len


def part_1(nums, max_len):
    gamma = epsilon = 0
    for shift in range(max_len):
        if most_common_bit(nums, shift):
            gamma += 1 << shift
        else:
            epsilon += 1 << shift
    return gamma * epsilon


def most_common_bit(nums, shift):
    mask = 1 << shift
    positive_bits = sum((mask & num) >> shift for num in nums)
    return 1 if positive_bits >= len(nums) - positive_bits else 0


def part_2(nums, max_len):
    oxy_nums = list(nums)
    co2_nums = list(nums)
    for shift_offset in range(max_len):
        shift = max_len - shift_offset - 1
        mask = 1 << shift
        if len(oxy_nums) > 1:
            oxy_filter_bit = most_common_bit(oxy_nums, shift) << shift
            oxy_nums = [num for num in oxy_nums if not (num ^ oxy_filter_bit) & mask]
        if len(co2_nums) > 1:
            co2_filter_bit = int(not most_common_bit(co2_nums, shift)) << shift
            co2_nums = [num for num in co2_nums if not (num ^ co2_filter_bit) & mask]
    return oxy_nums[0] * co2_nums[0]


def print_binary_list(nums):
    print('\n'.join(f'{num:b}' for num in nums))

test_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split()


assert part_1(*parse(test_input)) == 198
print(part_1(*parse(read_input(3))))  # 8958300 is too high

assert part_2(*parse(test_input)) == 230
print(part_2(*parse(read_input(3))))
