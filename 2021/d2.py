from collections import namedtuple
from dataclasses import dataclass

from utils import read_input


@dataclass
class Movement:
    x: int
    y: int

    def __add__(self, other):
        return Movement(x=self.x + other.x, y=self.y + other.y)


def parse(data: list[str]):
    result = []
    for line in data:
        command, value = line.strip().split()
        value = int(value)
        match command:
            case 'forward':
                move = Movement(x=value, y=0)
            case 'down':
                move = Movement(x=0, y=-value)
            case 'up':
                move = Movement(x=0, y=value)
            case _:
                raise Exception(f'unrecognized command: {line}')
        result.append(move)
    return result


def part_1(commands):
    displacement = sum(parse(commands), Movement(x=0, y=0))
    return displacement.x * -displacement.y


test_commands = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split('\n')
real_commands = read_input(2)

assert part_1(test_commands) == 150
print(part_1(real_commands))


@dataclass
class SubState:
    x: int = 0
    depth: int = 0
    aim: int = 0

    def update(self, command):
        verb, value = command.strip().split()
        value = int(value)
        match verb:
            case 'down':
                self.aim += value
            case 'up':
                self.aim -= value
            case 'forward':
                self.x += value
                self.depth += self.aim * value
            case _:
                raise Exception(f'unrecognized command: {command}')


def part_2(commands):
    state = SubState()
    for command in commands:
        state.update(command)
    print(state)
    return state.x * state.depth


assert part_2(test_commands) == 900
print(part_2(real_commands))
