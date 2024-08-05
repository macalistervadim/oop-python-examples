import math
from typing import Iterable


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


class Polygon:
    def __init__(self) -> None:
        self.vertices: list[Point] = []

    def add_point(self, point: Point) -> None:
        self.vertices.append((point))

    def perimeter(self) -> float:
        pairs = zip(
            self.vertices, self.vertices[1:] + self.vertices[:1]
        )
        return sum(p1.distance(p2) for p1, p2 in pairs)


class Polygon_2:
    def __init__(self, vertices: Iterable[Point] | None = None) -> None:
        self.vertices = list(vertices) if vertices else []

    def parameter(self) -> float:
        pairs = zip(
            self.vertices, self.vertices[1:] + self.vertices[:1]
        )
        return sum(p1.distance(p2) for p1, p2 in pairs)


Pair = tuple[float, float]
Point_or_Tuple = Point | Pair


class Polygon_3:
    def __init__(
        self,
        vertices: Iterable[Point_or_Tuple] | None = None,
    ) -> None:
        self.vertices: list[Point] = []
        if vertices:
            for point_or_tuple in vertices:
                self.vertices.append(self.make_point(point_or_tuple))

    @staticmethod
    def make_point(item: Point_or_Tuple) -> Point:
        return item if isinstance(item, Point) else Point(*item)
