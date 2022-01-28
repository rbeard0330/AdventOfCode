all_rounds = [
    (13, 6, False),
    (15, 7, False),
    (15, 10, False),
(11, 2, False),
(-7, 15, True),
(10, 8, False),
(10, 1, False),
(-5, 10, True),
(15, 5, False),
(-3, 3, True),
(0, 5, True),
(-5, 11, True),
(-9, 12, True),
(0, 10, True),
]
assert len(all_rounds) == 14

INPUT_RANGE = set(range(1, 10))
ALL_STATES = set(range(26))


def valid_states_by_round(valid_end_states, rounds=None, states_by_round=None):
    rounds = rounds if rounds is not None else all_rounds
    states_by_round = states_by_round or {14: [[]]}

    *prior_rounds, (input_adjust, output_adjust, discard_top) = rounds
    matchable_tops = {i - input_adjust for i in INPUT_RANGE}
    valid_start_states = []
    for valid_end_state in valid_end_states:
        if discard_top:
            # One way to get a valid end state is to have a full valid state, and a matching top, then
            # pop the prior state and not add anything
            valid_start_states.append([*valid_end_state, matchable_tops])
            # Otherwise we need a near-complete valid state with a non-matching top, then we discard the
            # matching top and push a valid state on top
            if len(valid_end_state) < 1:
                continue
            inputs_pushing_valid_top = {result - output_adjust for result in valid_end_state[-1]} & INPUT_RANGE
            if len(inputs_pushing_valid_top) == 0:
                continue
            valid_start_states.append([*valid_end_state[:-1], (ALL_STATES if len(inputs_pushing_valid_top) > 1
                                                               else ALL_STATES - inputs_pushing_valid_top)])
        else:
            # If we aren't popping, the top must also be a valid input and also be matchable
            valid_state_with_matching_tops = valid_end_state[-1] & matchable_tops
            if valid_state_with_matching_tops:
                valid_start_states.append([*valid_end_state[:-1], valid_state_with_matching_tops])
            # Otherwise we need a near-complete valid state with a non-matching top, then we push a valid state on top
                # inputs_creating_valid_top = ({i + output_adjust for i in INPUT_RANGE} & valid_end_state[-1])
            if len(valid_end_state) < 2:
                continue
            *rest_stack, start_top, end_top = valid_end_state
            inputs_pushing_valid_top = {result - output_adjust for result in end_top} & INPUT_RANGE
            if len(inputs_pushing_valid_top) == 0:
                continue
            start_top = start_top if len(inputs_pushing_valid_top) > 1 else start_top - {inputs_pushing_valid_top.pop() - input_adjust}
            valid_start_states.append([*valid_end_state[:-2], start_top])
    states_by_round[len(rounds) - 1] = valid_start_states or [[]]
    if not prior_rounds:
        return states_by_round
    else:
        return valid_states_by_round(valid_start_states, prior_rounds, states_by_round)


allowable_states = valid_states_by_round([[]])
for rd, states in allowable_states.items():
    print(f'round #{rd}')
    for state in states:
        print('depth', len(state), state)


def part_1():
    allowable_states = valid_states_by_round([[]])
    sn = 0
    state = []
    for i in range(14):
        print(f'round #{i}')
        for digit in range(9, 0, -1):
            resulting_state = update_state_for_input(i, state, digit)
            if is_state_allowable(resulting_state, allowable_states[i + 1]):
                print(f'matched {digit}')
                sn *= 10
                sn += digit
                state = resulting_state
                break
            else:
                print(f'{digit} results in {resulting_state} which is not allowed')
        else:
            raise Exception
    return sn




def update_state_for_input(round_num, current_state, input_value):
    input_adjust, output_adjust, discard_top = all_rounds[round_num]
    top_value = current_state[-1] if current_state else 0
    base_stack = current_state[:-1] if discard_top else current_state
    if top_value + input_adjust != input_value:
        return [*base_stack, input_value + output_adjust]
    else:
        return base_stack

def is_state_allowable(state, permitted_states):
    return any(len(state) == len(permitted_state)
               and all(actual_value in allowed_values for actual_value, allowed_values in zip(state, permitted_state))
               for permitted_state in permitted_states)

assert is_state_allowable([1, 12], [[{0}], [set(range(4)), {11, 12, 14}]])


def part_2():
    allowable_states = valid_states_by_round([[]])
    sn = 0
    state = []
    for i in range(14):
        print(f'round #{i}')
        for digit in range(1, 10):
            resulting_state = update_state_for_input(i, state, digit)
            if is_state_allowable(resulting_state, allowable_states[i + 1]):
                print(f'matched {digit}')
                sn *= 10
                sn += digit
                state = resulting_state
                break
            else:
                print(f'{digit} results in {resulting_state} which is not allowed')
        else:
            raise Exception
    return sn

print(part_1())
print(part_2())