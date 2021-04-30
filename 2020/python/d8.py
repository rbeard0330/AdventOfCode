from copy import copy
from utils import timer


def build_instruction(s, flip_nop_and_jmp):
    inst, param = decode_line(s)

    if inst == 'nop' and not flip_nop_and_jmp or inst == 'jmp' and flip_nop_and_jmp:
        def no_op(pc, acc):
            return pc + 1, acc
        return no_op

    if inst == 'jmp' and not flip_nop_and_jmp or inst == 'nop' and flip_nop_and_jmp:
        def jump(pc, acc):
            return pc + param, acc
        return jump

    if inst == 'acc':
        def accumulate(pc, acc):
            return pc + 1, acc + param
        return accumulate

    raise Exception(f'unhandled instruction: {s}')


def decode_line(s):
    inst, raw_param = s.split()
    unsigned_param_value = int(raw_param.lstrip('+-'))
    assert raw_param.startswith('-') or raw_param.startswith('+')
    param = unsigned_param_value if raw_param.startswith('+') else -unsigned_param_value
    return inst, param


def build_instruction_list(lines, flip_nop_and_jmp=False):
    return [build_instruction(line, flip_nop_and_jmp) for line in lines]


def run_program(inst_list, start_state=None):
    visited_pcs = set()
    pc, acc = start_state or (0, 0)

    while pc not in visited_pcs:
        visited_pcs.add(pc)
        try:
            pc, acc = inst_list[pc](pc, acc)
        except IndexError:
            return True, acc

    return False, acc


def first_answer(lines):
    instruction_list = build_instruction_list(lines)
    terminated, acc = run_program(instruction_list)
    assert not terminated

    return acc


def second_answer_v1(lines):  # 8.48ms
    base_instruction_list = build_instruction_list(lines)
    flipped_instruction_list = build_instruction_list(lines, flip_nop_and_jmp=True)

    for flip_index, flipped_instruction in enumerate(flipped_instruction_list):
        if base_instruction_list[flip_index].__name__ == flipped_instruction.__name__:
            continue

        patched_instruction_list = copy(base_instruction_list)
        patched_instruction_list[flip_index] = flipped_instruction

        terminated, acc = run_program(patched_instruction_list)
        if terminated:
            return acc


def run_program_and_cache(inst_list, start_state=None):
    acc_cache = {}
    pc, acc, visited_pcs = start_state or (0, 0, set())
    visited_pcs -= {pc}

    while pc not in visited_pcs:
        visited_pcs.add(pc)
        try:
            pc, acc = inst_list[pc](pc, acc)
            acc_cache[pc] = acc
        except IndexError:
            return acc, True, acc_cache, visited_pcs

    return acc, False, acc_cache, visited_pcs


def second_answer_v2(lines):  # 2.59ms
    base_instruction_list = build_instruction_list(lines)
    flipped_instruction_list = build_instruction_list(lines, flip_nop_and_jmp=True)
    *_, cached_accumulators, _ = run_program_and_cache(base_instruction_list)

    for flip_index, flipped_instruction in enumerate(flipped_instruction_list):
        if base_instruction_list[flip_index].__name__ == flipped_instruction.__name__:
            continue
        if flip_index not in cached_accumulators:
            continue

        patched_instruction_list = copy(base_instruction_list)
        patched_instruction_list[flip_index] = flipped_instruction

        terminated, acc = run_program(patched_instruction_list,
                                      start_state=(flip_index, cached_accumulators[flip_index]))
        if terminated:
            return acc


def second_answer(lines):  # 1.45ms
    base_instruction_list = build_instruction_list(lines)
    flipped_instruction_list = build_instruction_list(lines, flip_nop_and_jmp=True)
    *_, cached_accumulators, visited_pcs = run_program_and_cache(base_instruction_list)

    for flip_pc, start_accumulator in cached_accumulators.items():
        flipped_instruction = flipped_instruction_list[flip_pc]
        if base_instruction_list[flip_pc].__name__ == flipped_instruction.__name__:
            continue

        patched_instruction_list = copy(base_instruction_list)
        patched_instruction_list[flip_pc] = flipped_instruction

        acc, terminated, _, visited_pcs = run_program_and_cache(patched_instruction_list,
                                                                start_state=(flip_pc, start_accumulator, visited_pcs))
        if terminated:
            return acc


TEST_PROGRAM = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".strip().split('\n')

assert first_answer(TEST_PROGRAM) == 5
assert second_answer(TEST_PROGRAM) == 8

real_program = list(open('data/d8.txt').readlines())

print(first_answer(real_program))
print(second_answer_v2(real_program))
