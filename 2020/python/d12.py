def parse_simple_instruction(instruction, state):
    code = instruction[0]
    arg = int(instruction[1:])

    if code == 'F':
        if state['heading'] == 0:
            code = 'E'
        elif state['heading'] == 1:
            code = 'N'
        elif state['heading'] == 2:
            code = 'W'
        elif state['heading'] == 3:
            code = 'S'
    apply_compass_instruction(arg, code, state)
    if code == 'L' or code == 'R':
        direction = 1 if code == 'L' else -1
        assert arg % 90 == 0
        quarter_turns = direction * arg / 90
        state['heading'] = (state['heading'] + quarter_turns) % 4
    return state


def parse_complex_instruction(instruction, state):
    code = instruction[0]
    arg = int(instruction[1:])

    apply_compass_instruction(arg, code, state)
    if code == 'F':
        state['ship_ns'] += arg * state['ns']
        state['ship_ew'] += arg * state['ew']
    if code == 'L' or code == 'R':
        direction = 1 if code == 'L' else -1
        assert arg % 90 == 0
        quarter_turns = (direction * arg / 90) % 4
        if quarter_turns == 0:
            print(f'skipped {instruction}')
            return state
        if quarter_turns == 1 or quarter_turns == 3:
            invert = True
            transform = (1, -1) if quarter_turns == 1 else (-1, 1)
        if quarter_turns == 2:
            invert = False
            transform = (-1, -1)
        state['ew'] *= transform[0]
        state['ns'] *= transform[1]
        if invert:
            state['ns'], state['ew'] = state['ew'], state['ns']
    return state


def apply_compass_instruction(arg, code, state):
    if code == 'N':
        state['ns'] += arg
    if code == 'S':
        state['ns'] -= arg
    if code == 'E':
        state['ew'] += arg
    if code == 'W':
        state['ew'] -= arg


def first_answer(lines):
    state = {'ns': 0, 'ew': 0, 'heading': 0}
    for line in lines:
        state = parse_simple_instruction(line, state)

    return abs(state['ns']) + abs(state['ew'])


def second_answer(lines):
    state = {'ns': 1, 'ew': 10, 'ship_ns': 0, 'ship_ew': 0}
    for line in lines:
        state = parse_complex_instruction(line, state)

    return abs(state['ship_ns']) + abs(state['ship_ew'])


TEST_DATA = """F10
N3
F7
R90
F11""".splitlines()

assert first_answer(TEST_DATA) == 25
assert second_answer(TEST_DATA) == 286

real_data = open('data/d12.txt').read().splitlines()

print(first_answer(real_data))
print(second_answer(real_data))
