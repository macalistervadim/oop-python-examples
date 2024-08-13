"""
В данном примере рассматриваются DEFAULTDICT и COUNTER
"""


from typing import DefaultDict
from collections import Counter


def counterDefaultDict(sequence):
    result = DefaultDict(int)
    for i in sequence:
        result[i] += 1

    return result


print(counterDefaultDict([5, 2, 6, 7, 8, 9, 5, 5, 5, 5]))


def counterCounter(sequence):
    return Counter(sequence)

lst = [
    "1",
    "2",
    "3",
    "1",
    "2",
    "2",
    "7",
    "3"
]
print(counterCounter(lst))