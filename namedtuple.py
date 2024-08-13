"""
Данный пример демонстрирует работу ИМЕННОВАНЫХ КОРТЕЖЕЙ И ДАТАКЛАССОВ
"""

from typing import NamedTuple
from dataclasses import dataclass


class Manager(NamedTuple):
    name: str
    age: int
    jobstatus: str = "NoName"


man1 = Manager("Aleksey", 55)
print(man1.name)


@dataclass
class ManagerProfiler:
    name: str
    age: int
    jobstatus: str = "NoName"


man2 = ManagerProfiler("Vadim", 44)
print(man2.age)
