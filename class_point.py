import math


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.move(x, y)

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def reset(self) -> None:
        self.move(0, 0)

    def calculate_distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


a = 10000000000000
b = 1_000_000_000_00_000
print(a, b)

point1 = Point(3, 5)
point2 = Point(3, 5)

point1.reset()
point2.move(5, 0)
print(point2.calculate_distance(point1))

assert point2.calculate_distance(point1) == point1.calculate_distance(point2)

point1.move(3, 4)
print(point1.calculate_distance(point2))
print(point1.calculate_distance(point1))
