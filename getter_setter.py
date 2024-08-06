class UndefinedName(ValueError):
    """The user entered an invalid name."""


class Sample:
    def __init__(self, name: str, age: float) -> None:
        self._age = age
        self._name = name

    @property
    def getName(self) -> str:
        if self._name:
            return self._name
        else:
            raise UndefinedName("This name undefined.")

    @getName.setter
    def setName(self, name: str) -> None:
        self._name = name
        print("Success")



