import math
from dataclasses import dataclass
from functools import reduce
from typing import Union, List

from srqmplayer.formula.types import (
    ExpressionCommon, ParamValues, ExpressionType, SyntaxKind,
    BinaryExpression, RangeExpression, RangePart, NumberExpression,
    ParameterExpression, UnaryExpression
)
from srqmplayer.randomFunc import RandomFunc

MAX_NUMBER = 2000000000


def number_min_max(n: Union[int, float]):
    return min(max(n, -MAX_NUMBER), MAX_NUMBER)


@dataclass
class RangeCalculated:
    from_: int
    to: int


def floor_ceil(val: Union[int, float]):
    return math.floor(val) if val > 0 else math.ceil(val)


def pick_random_for_ranges(ranges_calc: List[RangeCalculated],
                           rnd_func: RandomFunc):
    total_values_amount = reduce(lambda total, r_: total + r_.to - r_.from_ + 1,
                                 ranges_calc, 0)
    rnd = rnd_func(total_values_amount)
    # console.info(
    #      `new ranges=[${ranges
    #         .map(x => `${x.from}..${x.to}`)
    #         .join("; ")}] rnd=${rnd} pickedRandom=${pickedRandom}
    #         totalValuesAmount=${totalValuesAmount}`
    # );
    for r in ranges_calc:
        len_ = r.to - r.from_ + 1
        # console.info(`Range=${range[0]}..${range[1]}, rnd=${rnd}, len=${len}`)
        if rnd >= len_:
            rnd -= len_
        else:
            result = rnd + r.from_
            # debug(0, `Range ${arg} returned random ${result}`);
            return result
    raise Exception(f'Error in finding random value for {ranges_calc} {rnd}')


def val_to_ranges(val: int) -> List[RangeCalculated]:
    return [RangeCalculated(from_=val, to=val)]


def floor_ceil_range(rp: RangePart, rnd: RandomFunc,
                     params: ParamValues = None) -> RangeCalculated:
    from_ = floor_ceil(calculate_ast(rp.from_, rnd, params))
    to = floor_ceil(calculate_ast(rp.to, rnd, params)) if rp.to else from_
    return RangeCalculated(from_=min(from_, to), to=max(from_, to))


def js_mod(a, b):
    res = a - int(a/b) * b
    return res


def calculate_ast(ast: ExpressionCommon, rnd: RandomFunc,
                  params: ParamValues = None) -> Union[int, float]:
    def transform_to_into_ranges(node: ExpressionCommon) \
            -> List[RangeCalculated]:
        if (not isinstance(node, BinaryExpression)
                or node.operator != SyntaxKind.TO):
            raise Exception("Wrong usage")

        l_ = node.left
        r_ = node.right
        l_ranges = calc_range(l_) if isinstance(l_, RangeExpression) \
            else val_to_ranges(floor_ceil(calculate_ast(l_, rnd, params)))

        right_ranges = calc_range(r_) if isinstance(r_, RangeExpression) \
            else val_to_ranges(floor_ceil(calculate_ast(r_, rnd, params)))

        left_range_max = max(*map(lambda x: x.to, l_ranges), 0)
        right_range_max = max(*map(lambda x: x.to, right_ranges), 0)

        left_range_min = min(*map(lambda x: x.from_, l_ranges), MAX_NUMBER)
        right_range_min = min(*map(lambda x: x.from_, right_ranges), MAX_NUMBER)
        return [RangeCalculated(from_=min(left_range_min, right_range_min),
                                to=max(left_range_max, right_range_max))]

    def calc_range(node: ExpressionCommon) -> List[RangeCalculated]:
        if not isinstance(node, RangeExpression):
            raise Exception('Wrong usage')

        return [floor_ceil_range(x, rnd, params) for x in node.ranges]

    if isinstance(ast, NumberExpression):
        return ast.value
    elif isinstance(ast, ParameterExpression):
        val = params[ast.parameterId]
        if val is None:
            raise Exception(f'Parameter p{ast.parameterId + 1} is not defined')
        return val
    elif isinstance(ast, BinaryExpression):
        if ast.operator == SyntaxKind.PLUS:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return number_min_max(a + b)
        elif ast.operator == SyntaxKind.MINUS:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return number_min_max(a - b)
        elif ast.operator == SyntaxKind.SLASH:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return number_min_max(a / b if b != 0
                                  else (MAX_NUMBER if a > 0 else -MAX_NUMBER))
        elif ast.operator == SyntaxKind.DIV:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            if b != 0:
                return number_min_max(floor_ceil(a / b))
            else:
                return MAX_NUMBER if a > 0 else -MAX_NUMBER
        elif ast.operator == SyntaxKind.MOD:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return number_min_max(js_mod(a, b) if b != 0
                                  else (MAX_NUMBER if a > 0 else -MAX_NUMBER))
        elif ast.operator == SyntaxKind.ASTERISK:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return number_min_max(a * b)
        elif ast.operator == SyntaxKind.TO:
            new_ranges = transform_to_into_ranges(ast)
            return pick_random_for_ranges(new_ranges, rnd)
        elif ast.operator == SyntaxKind.IN:
            reversed_ = (ast.left.type == ExpressionType.RANGE
                         and ast.right.type != ExpressionType.RANGE)
            left = ast.right if reversed_ else ast.left
            right = ast.left if reversed_ else ast.right

            left_val = number_min_max(calculate_ast(left, rnd, params))
            ranges = calc_range(right) if isinstance(right, RangeExpression) \
                else transform_to_into_ranges(right) \
                if (isinstance(right, BinaryExpression)
                    and right.operator == SyntaxKind.TO) \
                else None
            if ranges:
                for r in ranges:
                    if r.from_ <= left_val <= r.to:
                        return 1
                return 0
            else:
                right_val = number_min_max(
                    calculate_ast(ast.right, rnd, params))
                return 1 if left_val == right_val else 0
        elif ast.operator == SyntaxKind.GT_EQ:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a >= b else 0
        elif ast.operator == SyntaxKind.GT:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a > b else 0
        elif ast.operator == SyntaxKind.LT_EQ:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a <= b else 0
        elif ast.operator == SyntaxKind.LT:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a < b else 0
        elif ast.operator == SyntaxKind.EQ:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a == b else 0
        elif ast.operator == SyntaxKind.NEQ:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a != b else 0
        elif ast.operator == SyntaxKind.AND:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a and b else 0
        elif ast.operator == SyntaxKind.OR:
            a = calculate_ast(ast.left, rnd, params)
            b = calculate_ast(ast.right, rnd, params)
            return 1 if a or b else 0
        else:
            raise Exception(f'Unexpected operator {ast.operator}')
    elif isinstance(ast, UnaryExpression):
        if ast.operator == SyntaxKind.MINUS:
            return -calculate_ast(ast.expression, rnd, params)
        else:
            raise Exception(f'Unexpected ast {ast}')
    elif isinstance(ast, RangeExpression):
        return pick_random_for_ranges(calc_range(ast), rnd)
    else:
        raise Exception(f'Unexpected ast {ast}')
