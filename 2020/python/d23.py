from utils import timer

class Node:
    __slots__ = ['val', 'prev', 'succ']

    def __init__(self, val, prev=None):
        self.val = val
        self.prev = prev
        if self.prev:
            self.prev.succ = self
        self.succ = None

    def disconnect_successor(self):
        succ = self.succ
        self.succ = None
        succ.prev = None
        return succ

    def connect_successor(self, succ):
        self.succ = succ
        succ.prev = self


def shuffle(cups, current_index):
    current_value = cups[current_index]
    first_index_to_pick = (current_index + 1) % 9
    last_index_to_pick = (current_index + 4) % 9
    if first_index_to_pick < last_index_to_pick:
        cups_left = cups[:first_index_to_pick] + cups[last_index_to_pick:]
        picked_cups = cups[first_index_to_pick: last_index_to_pick]
    else:
        cups_left = cups[last_index_to_pick: first_index_to_pick]
        picked_cups = cups[first_index_to_pick:] + cups[:last_index_to_pick]
    if current_value == min(cups_left):
        destination_index = cups_left.index(max(cups_left))
    else:
        target_val = next(current_value - val for val in (1, 2, 3) if current_value - val in cups_left)
        destination_index = cups_left.index(target_val)
    new_cup_list = cups_left[: (destination_index + 1)] + picked_cups + cups_left[(destination_index + 1):]
    return new_cup_list, (new_cup_list.index(current_value) + 1) % 9


def first_answer(cup_list):
    current_index = 0
    for _ in range(100):
        cup_list, current_index = shuffle(cup_list, current_index)

    index_of_1 = cup_list.index(1)
    cup_list = cup_list[index_of_1 + 1:] + cup_list[:index_of_1]

    return ''.join(str(cup) for cup in cup_list)


def shuffle_linked_list(index, current_cup):
    first_lifted_cup = current_cup.disconnect_successor()
    last_lifted_cup = first_lifted_cup.succ.succ
    cup_after_last_lifted = last_lifted_cup.disconnect_successor()
    current_cup.connect_successor(cup_after_last_lifted)

    lifted_values = [first_lifted_cup.val, first_lifted_cup.succ.val, last_lifted_cup.val]
    target_value = current_cup.val - 1
    while True:
        if target_value == 0:
            target_value = 1_000_000
        if target_value in lifted_values:
            target_value -= 1
        else:
            break

    destination = index[target_value]
    cup_after_destination = destination.disconnect_successor()
    destination.connect_successor(first_lifted_cup)
    last_lifted_cup.connect_successor(cup_after_destination)

    return current_cup.succ


@timer
def second_answer(cup_list):
    head = None
    tail = None
    index = {}
    for n in cup_list:
        new_cup = Node(n, tail)
        index[n] = new_cup
        tail = new_cup
        head = head or new_cup
    for n in range(10, 1_000_001):
        new_cup = Node(n, tail)
        index[n] = new_cup
        tail = new_cup

    tail.connect_successor(head)
    current_cup = head
    for _ in range(10_000_000):
        current_cup = shuffle_linked_list(index, current_cup)

    cup_1 = index[1]
    return cup_1.succ.val * cup_1.succ.succ.val





TEST_DATA = [3, 8, 9, 1, 2, 5, 4, 6, 7]

assert first_answer(TEST_DATA) == '67384529'
assert second_answer(TEST_DATA) == 149245887792

real_data = [1, 9, 3, 4, 6, 7, 2, 5, 8]

print(first_answer(real_data))
print(second_answer(real_data))


