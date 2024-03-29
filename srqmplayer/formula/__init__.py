from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN

from srqmplayer.formula.calculator import calculate_ast
from srqmplayer.formula.parser import parse_expression
from srqmplayer.formula.scanner import Scanner
from srqmplayer.formula.types import ParamValues
from srqmplayer import RandomFunc


def parse(str_: str):
    str_no_line_breaks = str_.replace('\r', ' ').replace('\n', ' ')
    scanner_ = Scanner(str_no_line_breaks)
    ast = parse_expression(scanner_.scan)
    # console.info(JSON.stringify(ast, null, 4));
    return ast


def calculate(str_: str, rnd: RandomFunc, params: ParamValues = None) -> int:
    ast = parse(str_)
    if params is None:
        params = []
    value = Decimal(calculate_ast(ast, rnd, params))
    if value >= 0:
        return int(value.quantize(0, ROUND_HALF_UP))
    else:
        return int(value.quantize(0, ROUND_HALF_DOWN))
