from collections import defaultdict


def parse_value_mask(mask):
    return (int(''.join('1' if digit == '1' else '0' for digit in mask), 2),
            int(''.join('0' if digit == '0' else '1' for digit in mask), 2))


def parse_address_mask(mask):
    return (int(''.join('1' if digit == '1' else '0' for digit in mask), 2),
            [2 ** i for i, digit in enumerate(mask[::-1]) if digit == 'X'])


def first_answer(lines):
    mem = defaultdict(int)

    for instruction, _, value in (line.split() for line in lines):
        if instruction.strip() == 'mask':
            or_mask, and_mask = parse_value_mask(value.strip())
        else:
            addr = int(instruction.split('[')[1].rstrip(']'))
            mem[addr] = (int(value) & and_mask) | or_mask
    return sum(mem.values())


def second_answer(lines):
    mem = defaultdict(int)

    for instruction, _, value in (line.split() for line in lines):
        if instruction.strip() == 'mask':
            or_mask, flip_masks = parse_address_mask(value.strip())
        else:
            addrs = {int(instruction.split('[')[1].rstrip(']')) | or_mask}
            for flip_mask in flip_masks:
                addrs |= {addr ^ flip_mask for addr in addrs}
            for addr in addrs:
                mem[addr] = int(value)
    return sum(mem.values())


TEST_PROGRAM1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines()

TEST_PROGRAM2 ="""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()

assert first_answer(TEST_PROGRAM1) == 165
assert second_answer(TEST_PROGRAM2) == 208

real_program = open('data/d14.txt').read().splitlines()

print(first_answer(real_program))
print(second_answer(real_program))
