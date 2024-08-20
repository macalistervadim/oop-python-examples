"""
В данном примере реализуется ДЕКОРАТОР ПОСРЕДСТВОМ ЗАМЫКАНИЯ
"""

def decor(func):
    print("i'm outer")

    def decorInner():
        func()
        return print("i'm inner")

    return decorInner


@decor
def defc():
    print("im decorated")


defc()
