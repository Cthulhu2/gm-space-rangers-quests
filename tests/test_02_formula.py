import logging

import pytest

from srqmplayer.formula import calculate, ParamValues
from srqmplayer.formula.types import SyntaxException

log = logging.getLogger()


# noinspection PyRedundantParentheses
@pytest.mark.parametrize(('formula'), (('2+'),
                                       ('2 + 2 {'),
                                       ('-'),
                                       ('-3..'),
                                       ('Кек'),
                                       ('%'),
                                       ('2%4'),
                                       ('2 div '),
                                       (' div 54'),
                                       ('#'),
                                       ('[pp]'),
                                       ('[p1sss] + 2')))
def test_formula_parser_throws(formula: str):
    with pytest.raises(SyntaxException):
        assert calculate(formula, lambda x: 0, ParamValues([0, 0, 0, 0, 0]))
