import operator
from functools import reduce

from utils import windows, read_input

LOGGING = False


def log(s, depth=0):
    if LOGGING:
        print('  ' * depth + str(s))


def truncate(s):
    return f'{s[:20]}...' if len(s) > 20 else s


class Packet:
    _type_id = None
    _registry = {}
    VERSION_MASK = (2 ** 3 - 1) << 3
    PACKET_TYPE_MASK = (2 ** 3 - 1)
    _callbacks = []

    def __init__(self, version) -> None:
        self.version = version

    @classmethod
    def read_header(cls, bits):
        header = int(bits[:6], 2)
        version = (header & cls.VERSION_MASK) >> 3
        packet_type = (header & cls.PACKET_TYPE_MASK)
        return version, packet_type

    @classmethod
    def add_parser_callback(cls, fn):
        cls._callbacks.append(fn)

    @classmethod
    def clear_parser_callbacks(cls):
        cls._callbacks = []

    @classmethod
    def parse_bits(cls, bits, depth=0):
        log(f'parsing {truncate(bits)}', depth)
        version, packet_type = cls.read_header(bits)
        log(f'version = {version}, packet_type = {packet_type}', depth)
        packet_class = cls._registry.get(packet_type, Operator)
        assert packet_class is not Packet
        log(f'packet class is {packet_class.__name__}', depth)
        result, rest_bits = packet_class.parse_bits(bits, version=version, depth=depth)
        for callback in Packet._callbacks:
            callback(result)
        log(f'successfully parsed: {result}', depth)
        return result, rest_bits

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, type_id) -> None:
        Packet._registry[type_id] = cls
        cls._type_id = type_id
        super().__init_subclass__()

    @classmethod
    def parse_hex(cls, hex_string):
        log(f'parsing {truncate(hex_string)}')
        bit_groups = [f'{int(c, 16):04b}' for c in hex_string]
        return cls.parse_bits(''.join(bit_groups))

    @property
    def value(self):
        raise NotImplementedError


class Literal(Packet, type_id=4):
    def __init__(self, val, **kwargs) -> None:
        super().__init__(**kwargs)
        self.val = val

    @classmethod
    def parse_bits(cls, bits, version=None, depth=0):
        version, packet_type = cls.read_header(bits)
        log(f'parsed version {version} and type_id {packet_type} from {bits[:7]}', depth)
        assert packet_type == cls._type_id
        value = 0
        group_iter = windows(bits[6:], 5, overlapping=False, yield_remainder=True)
        continue_bit = '1'
        while continue_bit == '1':
            continue_bit, *group = next(group_iter)
            value <<= 4
            value += int(''.join(group), 2)
        rest_input = []
        for group in group_iter:
            rest_input.extend(group)
        return cls(value, version=version), ''.join(rest_input)

    def __str__(self):
        return f'Literal (value={self.val})'

    @property
    def value(self):
        return self.val


class Operator(Packet, type_id=None):
    op = None

    def __init__(self, children, **kwargs) -> None:
        self.children = children
        super().__init__(**kwargs)

    @classmethod
    def parse_bits(cls, bits, version=None, depth=0):
        if cls.read_length_id(bits, depth) == 1:
            header_end = 7 + 11
            content = bits[header_end:]
            children, rest_bits = cls.read_n_packets(content, int(bits[7:header_end], 2), depth=depth)
        else:
            header_end = 7 + 15
            content = bits[header_end:]
            content_length = int(bits[7:header_end], 2)
            children = cls.read_packets_from_n_bits(content, content_length, depth=depth)
            rest_bits = bits[(header_end + content_length):]
        return cls(children, version=version), rest_bits

    @staticmethod
    def read_length_id(bits, depth=0):
        log(f'reading length_id from {bits[:7]}', depth)
        return int(bits[6] == '1')

    @staticmethod
    def read_n_packets(bits, n, depth=0):
        rest_bits = bits
        result = []
        for i in range(n):
            log(f'reading {n - i} packets from {len(rest_bits)} bits', depth)
            packet, rest_bits = Packet.parse_bits(rest_bits, depth=depth + 1)
            result.append(packet)
        return result, rest_bits

    @staticmethod
    def read_packets_from_n_bits(bits, n, depth=0):
        log(f'reading packets from {n} bits', depth)
        rest_bits = bits[:n]
        result = []
        while '1' in rest_bits:
            packet, rest_bits = Packet.parse_bits(rest_bits, depth=depth + 1)
            result.append(packet)
        # log(result)
        return result

    def __str__(self):
        return f'{self.__class__.__name__} with {len(self.children)} children'

    @property
    def _child_vals(self):
        return [child.value for child in self.children]

    @property
    def value(self):
        return self.op(self._child_vals)


class SumPacket(Operator, type_id=0):
    op = sum


class ProductPacket(Operator, type_id=1):
    @property
    def value(self):
        return reduce(operator.mul, self._child_vals)


class MinPacket(Operator, type_id=2):
    op = min


class MaxPacket(Operator, type_id=3):
    op = max


class ComparisonMixin:
    def __init__(self, children, **kwargs) -> None:
        assert len(children) == 2
        super().__init__(children, **kwargs)

    @property
    def value(self):
        lhs, rhs = self._child_vals
        return int(self.op(lhs, rhs))


class GreaterThanPacket(ComparisonMixin, Operator, type_id=5):
    op = operator.gt


class LessThanPacket(ComparisonMixin, Operator, type_id=6):
    op = operator.lt


class EqualsPacket(ComparisonMixin, Operator, type_id=7):
    op = operator.eq


assert Literal.parse_hex('D2FE28')[0].val == 2021
assert Literal.parse_hex('D2FE28')[1] == '000'

parsed, remainder = Packet.parse_hex('D2FE28')
assert parsed.value == 2021
assert remainder == '000'
assert parsed.version == 6

parsed, remainder = Packet.parse_hex('38006F45291200')
assert remainder == '0000000'
assert isinstance(parsed, Operator)
assert len(parsed.children) == 2
assert all(isinstance(child, Literal) for child in parsed.children)
child1, child2 = parsed.children
assert child1.value == 10
assert child2.value == 20
assert parsed.version == 1

parsed, remainder = Packet.parse_hex('EE00D40C823060')
assert remainder == '00000'
assert isinstance(parsed, Operator)
assert len(parsed.children) == 3
assert all(isinstance(child, Literal) for child in parsed.children)
child1, child2, child3 = parsed.children
assert child1.value == 1
assert child2.value == 2
assert child3.value == 3
assert parsed.version == 7


class VersionSummer:
    def __init__(self) -> None:
        self.total = 0

    def __call__(self, packet: Packet):
        self.total += packet.version


tests = {
    '8A004A801A8002F478': 16,
    '620080001611562C8802118E34': 12,
    'C0015000016115A2E0802F182340': 23,
    'A0016C880162017C3686B18A3D4780': 31
}

for hex_string, version_sum in tests.items():
    summer = VersionSummer()
    Packet.add_parser_callback(summer)
    Packet.parse_hex(hex_string)
    assert summer.total == version_sum
    Packet.clear_parser_callbacks()

real_packet = read_input(16)[0].strip()
summer = VersionSummer()
Packet.add_parser_callback(summer)
parse_result, _ = Packet.parse_hex(real_packet)
print(summer.total)
Packet.clear_parser_callbacks()

tests = {
    'C200B40A82': 3,
    '04005AC33890': 54,
    '880086C3E88112': 7,
    'CE00C43D881120': 9,
    'D8005AC2A8F0': 1,
    'F600BC2D8F': 0,
    '9C005AC2F8F0': 0,
    '9C0141080250320F1802104A08': 1
}

for hex_string, value in tests.items():
    parsed, _ = Packet.parse_hex(hex_string)
    assert parsed.value == value, parsed.value

print(parse_result.value)
