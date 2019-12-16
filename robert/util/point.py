from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x:  int
    y:  int

    def __iadd__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        else:
            raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            return Point(self.x + other[0], self.y + other[1])
        elif isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise NotImplementedError

    def __sub__(self, other):
        try:
            return self + other * -1
        except (NotImplementedError, TypeError):
            raise TypeError(f"Cannot subtract {type(other)} from Point")

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            raise TypeError(f"Cannot compare Point with {type(other)}")

    def __repr__(self):
        return f"p({self.x}, {self.y})"

    def transpose(self):
        return Point(self.y, self.x)

    @staticmethod
    def sort(p):
        return (p.x, p.y)


@dataclass
class ThreeDVect():
    x:  int
    y:  int
    z:  int

    def __iadd__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
            return self
        elif isinstance(other, ThreeDVect):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        else:
            raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            return ThreeDVect(self.x + other[0], self.y + other[1], self.z +
                              other[2])
        elif isinstance(other, Point):
            return ThreeDVect(
                self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise NotImplementedError

    def __sub__(self, other):
        try:
            return self + other * -1
        except (NotImplementedError, TypeError):
            raise TypeError(f"Cannot subtract {type(other)} from Point")

    def __mul__(self, other):
        if isinstance(other, int):
            return ThreeDVect(self.x * other, self.y * other, self.z * other)
        else:
            raise NotImplementedError

    def __eq__(self, other):
        try:
            return (
                self.x == other.x and self.y == other.y and self.z == other.z)
        except AttributeError:
            raise TypeError(f"Cannot compare Point with {type(other)}")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    @staticmethod
    def sort(v):
        return (v.x, v.y, v.z)


@dataclass
class Segment:
    p1: Point
    p2: Point
    direction: str

    @property
    def x_min(self):
        if self.p1.x <= self.p2.x:
            return self.p1.x
        else:
            return self.p2.x

    @property
    def x_max(self):
        if self.p1.x >= self.p2.x:
            return self.p1.x
        else:
            return self.p2.x

    @property
    def y_min(self):
        if self.p1.y <= self.p2.y:
            return self.p1.y
        else:
            return self.p2.y

    @property
    def y_max(self):
        if self.p1.y >= self.p2.y:
            return self.p1.y
        else:
            return self.p2.y
