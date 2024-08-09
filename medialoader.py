"""
Данный пример демонстрирует работу АБСТРАКТНЫХ БАЗОВЫХ КЛАССОВ И ИХ СОЗДАНИЕ
"""

import abc


class MediaLoader(abc.ABC):
    @abc.abstractmethod
    def play(self) -> None:
        ...

    @property
    @abc.abstractmethod
    def ext(self) -> str:
        ...
