"""
Данный пример демонстрирует работу такого принципа ООП как НАСЛЕДОВАНИЕ, ПОЛИМОРФИЗМ ПОРЯДОК РАЗРЕШЕНИЯ __mro__
"""

class BaseClass:
    num_base_calls = 0

    def call_me(self) -> None:
        print("Calling method on Base Class")
        self.num_base_calls += 1


class LeftSubclass_S(BaseClass):
    num_left_calls = 0

    def call_me(self) -> None:
        super().call_me()
        print("Calling method on LeftSubclass_S")
        self.num_base_calls += 1


class RightSubclass_S(BaseClass):
    num_right_calls = 0

    def call_me(self) -> None:
        super().call_me()
        print("Calling method on RighSubclass_S")
        self.num_right_calls += 1


class Subclass_S(LeftSubclass_S, RightSubclass_S):
    num_sub_calls = 0

    def call_me(self) -> None:
        super().call_me()
        print("Calling method on Subclass_S")
        self.num_sub_calls += 1