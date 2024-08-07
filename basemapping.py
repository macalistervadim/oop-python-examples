"""
Данный пример демонстрирует СОЗДАНИЕ СОБСТВЕННЫХ КОЛЛЕКЦИЙ ДАННЫХ ПРИ
ПОМОЩИ collections.abc
"""

import collections.abc
from typing import Iterable, Any, Sequence, Protocol


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...


BaseMapping = collections.abc.Mapping[Comparable, Any]


class Lookup(BaseMapping):
    @overload
    def __init__(
        self,
        source: Iterable[tuple[Comparable, Any]]
    ) -> None:
        ...

    @overload
    def __init__(self, source: BaseMapping) -> None:
        ...

    def __init__(
            self,
            source: Iterable[
                tuple[Comparable, Any]]
                | BaseMapping | None = None
    ) -> None:
        sortedPairs: Sequence[tuple[Comparable, Any]]
        if isinstance(source, Sequence):
            sortedPairs = sorted(source)
        elif isinstance(source, collections.abc.Mapping):
            sortedPairs = sorted(source.items())
        else:
            sortedPairs = []
        self.keyList = [p[0] for p in sortedPairs]
        self.valueList = [p[1] for p in sortedPairs]
