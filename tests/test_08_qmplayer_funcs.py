import logging
from typing import Union

from srqmplayer.qmmodels import Jump
from srqmplayer.qmplayer.funcs import sort_jumps
from srqmplayer.randomFunc import create_determenistic_random

log = logging.getLogger()


# noinspection PyPep8Naming,PyShadowingBuiltins
def jump(id: int, showingOrder: int) -> Jump:
    # noinspection PyTypeChecker
    return Jump(
        id=id, showingOrder=showingOrder,
        priority=None, dayPassed=None, fromLocationId=None,
        toLocationId=None, alwaysShow=None, jumpingCountLimit=None,
        paramsConditions=None, formulaToPass=None,
        text=None, description=None, paramsChanges=None,
        img=None, sound=None, track=None)


def test_sorting_jumps():
    log.info('Empty list returns empty')

    # noinspection PyTypeChecker,PyUnusedLocal
    def no_random(x: int) -> Union[int, float]:
        assert False, 'no random'

    r = sort_jumps([], no_random)
    assert [] == r

    log.info('Sorting, all prios different')
    r = sort_jumps([jump(id=0, showingOrder=5),
                    jump(id=1, showingOrder=6),
                    jump(id=2, showingOrder=2),
                    jump(id=3, showingOrder=3),
                    jump(id=4, showingOrder=9),
                    jump(id=5, showingOrder=0)],
                   no_random)

    assert [jump(id=5, showingOrder=0),
            jump(id=2, showingOrder=2),
            jump(id=3, showingOrder=3),
            jump(id=0, showingOrder=5),
            jump(id=1, showingOrder=6),
            jump(id=4, showingOrder=9)] == r

    log.info('Sorting, have duplicated prios')
    rnd = create_determenistic_random([1, 0, 0, 1])
    r = sort_jumps([jump(id=0, showingOrder=5),
                    jump(id=1, showingOrder=6),
                    jump(id=2, showingOrder=2),
                    jump(id=3, showingOrder=3),
                    jump(id=4, showingOrder=9),
                    jump(id=5, showingOrder=0),
                    jump(id=6, showingOrder=5),
                    jump(id=7, showingOrder=2),
                    jump(id=8, showingOrder=3),
                    jump(id=9, showingOrder=3)],
                   rnd)
    assert [jump(id=5, showingOrder=0),
            jump(id=7, showingOrder=2),
            jump(id=2, showingOrder=2),
            jump(id=3, showingOrder=3),
            jump(id=8, showingOrder=3),
            jump(id=9, showingOrder=3),
            jump(id=0, showingOrder=5),
            jump(id=6, showingOrder=5),
            jump(id=1, showingOrder=6),
            jump(id=4, showingOrder=9)] == r
