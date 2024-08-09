"""
В данном примере приводится пример реализации АБСТРАКТНОГО БАЗОВОГО КЛАССА и
ПЕРЕЗАГРУЗКУ ОПЕРАТОРОВ
"""

import abc
import random
from typing import Type, Iterable, Any


class Die(abc.ABC):
    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None:
        ...

    def __repr__(self) -> str:
        return f"{self.face}"


class D4(Die):
    def roll(self) -> None:
        self.face = random.choice((1, 2, 3, 4))


class D6(Die):
    def roll(self) -> None:
        self.face = random.randint(1, 6)


class Dice(abc.ABC):
    def __init__(self, n: int, dieClass: Type[Die]) -> None:
        self.dice = [dieClass() for _ in range(n)]

    @abc.abstractmethod
    def roll(self) -> None:
        ...

    @property
    def total(self) -> int:
        return sum(d.face for d in self.dice)


class SimpleDice(Dice):
    def roll(self) -> None:
        for d in self.dice:
            d.roll()


class YachtDice(Dice):
    def __init__(self) -> None:
        super().__init__(5, D6)
        self.saved: set[int] = set()

    def saving(self, positions: Iterable[int]) -> "YachtDice":
        if not all(0 <= n < 6 for n in positions):
            raise ValueError("Invalid position")

        self.saved = set(positions)
        return self

    def roll(self) -> None:
        for n, d in enumerate(self.dice):
            if n not in self.saved:
                d.roll()

        self.saved = set()


class DDice:
    def __init__(self, *dieClass: Type[Die]) -> None:
        self.dice = [dc() for dc in dieClass]
        self.adjust: int = 0

    def plus(self, adjust: int = 0) -> "DDice":
        self.adjust = adjust
        return self

    def roll(self) -> None:
        for d in self.dice:
            d.roll()

    @property
    def total(self) -> int:
        return sum(d.face for d in self.dice) + self.adjust

    def __add__(self, dieClass: Any) -> "DDice":
        if isinstance(dieClass, type) and issubclass(dieClass, Die):
            newClasses = [type(d) for d in self.dice] + [dieClass]
            new = DDice(*newClasses).plus(self.adjust)
            return new
        elif isinstance(dieClass, int):
            newClasses = [type(d) for d in self.dice]
            new = DDice(*newClasses).plus(dieClass)
            return new
        else:
            return NotImplemented

    def __radd__(self, dieClass: Any) -> "DDice":
        if isinstance(dieClass, type) and issubclass(dieClass, Die):
            newClasses = [type(d) for d in self.dice] + [dieClass]
            new = DDice(*newClasses).plus(self.adjust)
            return new
        elif isinstance(dieClass, int):
            newClasses = [type(d) for d in self.dice]
            new = DDice(*newClasses).plus(dieClass)
            return new
        else:
            return NotImplemented

    def __mul__(self, n: Any) -> "DDice":
        if isinstance(n, int):
            newClasses = [type(d) for d in self.dice for _ in range(n)]
            return DDice(*newClasses).plus(self.adjust)
        else:
            return NotImplemented

    def __rmul__(self, n: Any) -> "DDice":
        if isinstance(n, int):
            newClasses = [type(d) for d in self.dice for _ in range(n)]
            return DDice(*newClasses).plus(self.adjust)
        else:
            return NotImplemented

    def __iadd__(self, dieClass: Any) -> "DDice":
        if isinstance(dieClass, type) and issubclass(dieClass, Die):
            self.dice += [dieClass()]
            return self
        elif isinstance(dieClass, int):
            self.adjust += dieClass
            return self
        else:
            return NotImplemented
