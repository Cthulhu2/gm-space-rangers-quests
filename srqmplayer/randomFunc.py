import math
from random import random
from typing import Union, Callable, List, Optional

RandomFunc = Callable[[int], Union[int, float]]


def rnd(n: int) -> Union[int, float]:
    return math.floor(random() * n) if n is not None else random()


def create_determenistic_random(rnd_values: List[int]):
    rnd_iterator = iter(rnd_values)

    def deterministic_rnd(n: Optional[int]):
        if n is None:
            raise Exception('todo this test')

        val = next(rnd_iterator, None)
        if val is None:
            raise Exception('Lots of randoms')

        if val >= n:
            raise Exception('Why stored random value is greater?')
        return val

    return deterministic_rnd
