from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import Literal, Optional

from utils import time_fn

room_to_amphipod = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
amphipod_to_room = {amphi: room for room, amphi in room_to_amphipod.items()}
step_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000, None: 0}

test_rooms = [['A', 'B'], ['D', 'C'], ['C', 'B'], ['A', 'D']]
real_rooms = [['C', 'D'], ['C', 'B'], ['D', 'B'], ['A', 'A']]

hallway_start = [[], [], [], [], []]

MAX_ROOM_DEPTH = 2

@dataclass
class Move:
    amphipod: Literal['A', 'B', 'C', 'D']
    start_index: int
    start_depth: int
    start_is_hall: bool
    end_index: int
    end_depth: int
    end_is_hall: bool
    occupant_to_push: Optional[Literal['A', 'B', 'C', 'D']] = None

    def __post_init__(self):
        assert not (self.start_is_hall and self.end_is_hall)
        if self.end_is_hall:
            assert self.end_depth == 1, self
        if self.start_is_hall and self.start_index in [1, 2, 3]:
            assert self.start_depth == 1, self
        if self.occupant_to_push:
            assert self.end_is_hall and self.end_index in [0, 4], self
        if not self.end_is_hall:
            assert self.end_index == amphipod_to_room[self.amphipod], self

    def update_rooms_and_hallways(self, rooms, hallways):
        # assert sum(map(len, rooms)) + sum(map(len, hallways)) in (8, 16), f'{rooms}\n{hallways}'
        assert can_move_to_location(self.start_index, self.end_index, hallways, starting_in_hallway=self.start_is_hall)
        new_rooms = deepcopy(rooms)
        if self.start_is_hall or self.end_is_hall:
            new_halls = deepcopy(hallways)
        else:
            new_halls = hallways
        start_area = new_halls if self.start_is_hall else new_rooms
        # assert start_area[self.start_index][-1] == self.amphipod, f'{self}\n{rooms}\n{hallways}'
        end_area = new_halls if self.end_is_hall else new_rooms
        amphi = start_area[self.start_index].pop()
        if amphi is None:
            amphi = start_area[self.start_index].pop()
        if self.start_is_hall and len(start_area[self.start_index]) == 1:
            start_area[self.start_index].append(None)
        if end_area[self.end_index] and end_area[self.end_index][-1] is None:
            end_area[self.end_index].pop()
        end_area[self.end_index].append(amphi)
        return new_rooms, new_halls

    @property
    def cost(self):
        total_steps = self.start_depth + self.end_depth
        total_steps += 2 * abs(self.start_index - self.end_index)
        if self.start_is_hall and self.start_index > self.end_index:
            total_steps -= 2
        if self.end_is_hall:
            if self.start_index < self.end_index:
                total_steps -= 2

        base_cost = total_steps * step_costs[self.amphipod]
        return base_cost + step_costs[self.occupant_to_push]


def enumerate_moves(rooms, hallways):
    for (start_index, room) in enumerate(rooms):
        if room and any(amphipod != room_to_amphipod[start_index] for amphipod in room):
            amphi = room[-1]
            destination_index = amphipod_to_room[amphi]
            common_args = dict(amphipod=amphi, start_index=start_index, start_is_hall=False, start_depth=MAX_ROOM_DEPTH - len(room) + 1)
            if (destination_index != start_index
                    and all(occupant == amphi for occupant in rooms[destination_index])
                    and can_move_to_location(start_index, destination_index, hallways)):
                yield Move(**common_args, end_index=destination_index, end_depth=MAX_ROOM_DEPTH - len(rooms[destination_index]),
                           end_is_hall=False)
                return
            for hall_index in range(5):
                destination_hall = hallways[hall_index]
                hall_capacity = 2 if hall_index in [0, 4] else 1
                if (len(destination_hall) < hall_capacity or destination_hall[-1] is None) and can_move_to_location(start_index, hall_index, hallways):
                    yield Move(**common_args, end_index=hall_index, end_is_hall=True, end_depth=1,
                               occupant_to_push=destination_hall[-1] if destination_hall else None)

    for (start_index, hall) in enumerate(hallways):
        if hall:
            amphi = hall[-1]
            if amphi is None:
                amphi = hall[0]
            destination_index = amphipod_to_room[amphi]
            if (all(occupant == amphi for occupant in rooms[destination_index])
                    and can_move_to_location(start_index, destination_index, hallways, starting_in_hallway=True)):
                start_depth = 2 if hall[-1] is None else 1
                yield Move(amphipod=amphi, end_index=destination_index, end_depth=MAX_ROOM_DEPTH - len(rooms[destination_index]),
                           end_is_hall=False, start_index=start_index, start_is_hall=True, start_depth=start_depth)
                return


def can_move_to_location(start_index, end_index, hallways, starting_in_hallway=False):
    left_index = min(start_index, end_index)
    right_index = min(max(start_index, end_index), 3)
    if starting_in_hallway and start_index == right_index:
        right_index -= 1
    return not any(hallways[left_index + 1: right_index + 1])

def hallway_factory(*occupied):
    return [[] if i not in occupied else [1] for i in range(5)]
test_move = Move(amphipod='A', start_index=4, start_depth=1, start_is_hall=True, end_index=0, end_depth=1, end_is_hall=False, occupant_to_push=None)
rooms = [['A'] * 3, ['B'] * 3, ['C'] * 4, ['D'] * 4]
halls = [[], [], [], [], ['B', 'A']]
print(test_move.update_rooms_and_hallways(rooms, halls))
# raise Exception


def parse_diagram(s):
    print('parsing', s)
    halls, *rooms = s.splitlines(keepends=False)[1:-1]
    halls = [c if c not in ['.'] else None for c in halls[1:-1]]
    h0 = halls[:2]
    h4 = halls[-2:][::-1]
    h1 = [halls[3]]
    h2 = [halls[5]]
    h3 = [halls[7]]
    halls = [h0, h1, h2, h3, h4]
    halls = tuple([tuple([c for c in hall if c is not None]) for hall in halls])
    result = [[], [], [], []]
    for layer in rooms:
        for room_index, occupant in enumerate(layer.strip().strip('#').split('#')):
            if occupant != '.':
                result[room_index].append(occupant)
    result = tuple([tuple(room[::-1]) for room in result])
    return halls, result

def check_move_ok(start, end):
    global MAX_ROOM_DEPTH
    MAX_ROOM_DEPTH = 4
    start_halls, start_rooms = parse_diagram(start)
    end_halls, end_rooms = parse_diagram(end)
    occupant_to_push = occupant_to_pop = None
    for i in range(5):
        if len(start_halls[i]) > len(end_halls[i]):
            print(start_halls[i], end_halls[i])
            amphi = start_halls[i][-1]
            start_index = i
            start_depth = 1
            start_is_hall = True
            if len(start_halls[i]) == 2:
                occupant_to_pop = start_halls[i][0]
        elif len(start_halls[i]) < len(end_halls[i]):
            print('end', start_halls[i], end_halls[i])
            end_index = i
            end_is_hall = True
            end_depth = 1
            if len(end_halls[i]) == 2:
                occupant_to_push = start_halls[i][0]
        if i == 4:
            continue
        if len(start_rooms[i]) > len(end_rooms[i]):
            amphi = start_rooms[i][-1]
            start_index = i
            start_depth = 4 - len(start_rooms[i]) + 1
            start_is_hall = False
        elif len(start_rooms[i]) < len(end_rooms[i]):
            end_index = i
            end_is_hall = False
            end_depth = 4 - len(end_rooms[i]) + 1
    move = Move(amphipod=amphi, start_depth=start_depth, end_depth=end_depth, start_index=start_index,
                end_index=end_index, end_is_hall=end_is_hall, start_is_hall=start_is_hall,
                occupant_to_push=occupant_to_push)
    moves = list(enumerate_moves(start_rooms, start_halls))
    nl = '\n'
    assert move in moves, f'{move} from\n{start} to\n{end} not in\n{nl.join(str(move) for move in moves)}'
    MAX_ROOM_DEPTH = 2


states = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#D#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A........AD#
###.#B#C#.###
  #.#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".split('\n\n')

# for start, end in zip(states, states[1:]):
#     check_move_ok(start, end)

print(len(states))
parsed_states = {parse_diagram(s) for s in states}

parse_diagram("""#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########""")


assert can_move_to_location(0, 0, hallway_factory(1))
assert can_move_to_location(0, 0, hallway_factory(1, 2))
assert can_move_to_location(0, 0, hallway_factory(1, 3))
for i, j in product(range(4), repeat=2):
    for hall_states in product([True, False], repeat=3):
        hallways = []
        for hall_index, hall in enumerate(hall_states):
            if hall:
                hallways.append(hall_index + 1)
        expected = True
        if hall_states[0]:
            expected = expected and (i < 1) == (j < 1)
        if hall_states[1]:
            expected = expected and (i < 2) == (j < 2)
        if hall_states[2]:
            expected = expected and (i < 3) == (j < 3)
        assert can_move_to_location(j, i, hallway_factory(*hallways)) == expected
        assert can_move_to_location(j, i, hallway_factory(0, *hallways)) == expected
        assert can_move_to_location(j, i, hallway_factory(4, *hallways)) == expected
        assert can_move_to_location(j, i, hallway_factory(0, 4, *hallways)) == expected


assert not can_move_to_location(3, 1, [[], [], ['D'], ['B'], []], True)
assert can_move_to_location(3, 1, [['A'], ['B'], [], ['B'], ['A']], True)

def valid_solution(rooms):

    return rooms == [['A'] * MAX_ROOM_DEPTH, ['B'] * MAX_ROOM_DEPTH, ['C'] * MAX_ROOM_DEPTH, ['D'] * MAX_ROOM_DEPTH]


GLOBAL_MIN = 10**9


@time_fn
def part_1(rooms):
    return move_amphipods(rooms, hallway_start)


def move_amphipods(rooms, hallways, current_score=0, best_score=10**9, moves=None):
    global GLOBAL_MIN
    if (tuple(tuple(hall) for hall in hallways), tuple(tuple(room) for room in rooms)) in parsed_states:
        print(f'reached {rooms} with cost {current_score}')
    if moves is None:
        print('setting min')
        GLOBAL_MIN = 10**9
    moves = moves or []
    best_solution = None
    local_best = best_score
    if valid_solution(rooms):
        return current_score, moves
    possible_moves = list(enumerate_moves(rooms, hallways))
    # print(f'{len(possible_moves)} possible moves with rooms\n{rooms}\nand halls\n{hallways}')
    for move in possible_moves:
        resulting_score = current_score + move.cost
        if resulting_score < GLOBAL_MIN:
            # print(f'{len(moves) * "  "} trying {move}; total cost {resulting_score}')
            new_rooms, new_hallways = move.update_rooms_and_hallways(rooms, hallways)
            if resulting_score + compute_heuristic(new_rooms, new_hallways) >= GLOBAL_MIN:
                continue
            result = move_amphipods(new_rooms, new_hallways, current_score + move.cost, local_best, moves + [move])
            # print(result)
            if result is not None and result[0] < local_best:

                local_best, best_solution = result
                if local_best < GLOBAL_MIN:
                    print(f'found a solution with cost {local_best}')
                    GLOBAL_MIN = local_best
        # else:
        #     print(f'skipping {move}')

    return local_best, best_solution


def compute_heuristic(rooms, hallways):
    min_cost = 0
    for room_index, room in enumerate(rooms):
        resident_amphi = room_to_amphipod[room_index]
        if MAX_ROOM_DEPTH == 2:
            if not room or room[0] != resident_amphi:
                min_cost += step_costs[resident_amphi]
        else:
            if not room or room[0] != resident_amphi:
                min_cost += 6 * step_costs[resident_amphi]
            elif len(room) == 1 or room[1] != resident_amphi:
                min_cost += 3 * step_costs[resident_amphi]
            elif len(room) == 2 or room[2] != resident_amphi:
                min_cost += 1 * step_costs[resident_amphi]
        for position, amphi in enumerate(room):
            if amphi != resident_amphi:
                steps = (2 - position) + 2 * abs(room_index - amphipod_to_room[amphi]) + 1
                min_cost += steps * step_costs[amphi]
    for hall_index, hall in enumerate(hallways):
        for position, amphi in enumerate(hall):
            if amphi is None:
                continue
            steps = 1
            if hall_index in [0, 4] and position == 0 and len(hall) == 2:
                steps += 1
            destination_index = amphipod_to_room[amphi]
            door_index = hall_index if destination_index >= hall_index else hall_index - 1
            steps += 2 * abs(door_index - destination_index) + 1
            min_cost += steps * step_costs[amphi]
    return min_cost


# rooms = [['A'], ['B'], ['C', 'C'], ['D', 'D']]
# halls = [[], [], [], ['B'], ['A']]
# for move in enumerate_moves(rooms, halls):
#     print(move)
# score, moves = move_amphipods(rooms, halls, 15424)
# print(score)
# for move in moves:
#     print(move)
# assert score == 15472, score


test_move = Move(amphipod='B', start_index=2, start_depth=1, start_is_hall=False, end_is_hall=True, end_depth=1,
                 end_index=1)
assert test_move.cost == 40
test_move = Move(amphipod='C', start_index=1, start_depth=1, start_is_hall=False, end_is_hall=False, end_depth=1,
                 end_index=2)
assert test_move.cost == 400
test_move = Move(amphipod='D', start_index=1, start_depth=2, start_is_hall=False, end_is_hall=True, end_depth=1,
                 end_index=2)
assert test_move.cost == 3000, test_move.cost
test_move = Move(amphipod='B', start_index=1, start_depth=1, start_is_hall=True, end_is_hall=False, end_depth=2,
                 end_index=1)
assert test_move.cost == 30
test_move = Move(amphipod='B', start_index=1, start_depth=1, start_is_hall=False, end_is_hall=True, end_depth=1,
                 end_index=0, occupant_to_push='D')
assert test_move.cost == 1040, test_move.cost
test_move = Move(amphipod='B', start_index=1, start_depth=1, start_is_hall=False, end_is_hall=True, end_depth=1,
                 end_index=0)
assert test_move.cost == 40, test_move.cost


score, _ = part_1(test_rooms)
assert score == 12521, score
print('part 1 test OK')
score, _ = part_1(real_rooms)
print(score)

MAX_ROOM_DEPTH = 4
@time_fn
def part_2(rooms):
    extra_rooms = [['D', 'D'], ['B', 'C'], ['A', 'B'], ['C', 'A']]
    rooms = [[first_amphi, *extra, second_amphi] for (first_amphi, second_amphi), extra in zip(rooms, extra_rooms)]
    print(rooms)
    return move_amphipods(rooms, hallway_start)

score, moves = part_2(test_rooms)
running_cost = 0
for move in moves:
    running_cost += move.cost
    print(running_cost, move.cost, move)
assert score == 44169, score
print('part 2 test OK')
score, moves = part_2(real_rooms)
print(score)
