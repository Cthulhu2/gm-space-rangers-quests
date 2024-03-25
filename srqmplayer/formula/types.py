from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Union


class SyntaxException(Exception):
    pass


class ParamValues(list[int, float]):
    pass


class SyntaxKind(Enum):
    # SyntaxKindBinaryToken
    LT = "less than token"
    GT = "greater than token"
    LT_EQ = "less than eq token"
    GT_EQ = "greater than eq token"
    PLUS = "plus token"
    MINUS = "minus token"
    SLASH = "slash token"
    ASTERISK = "asterisk token"
    EQ = "equals token"
    NEQ = "not equals token"
    # SyntaxKindBinaryKeyword
    MOD = "mod keyword"
    DIV = "div keyword"
    TO = "to keyword"
    IN = "in keyword"
    AND = "and keyword"
    OR = "or keyword"
    # SyntaxKind
    WHITE_SPACE = "white space token"
    NUM_LITERAL = "numeric literal"
    OPEN_BRACE = "open brace token"
    CLOSE_BRACE = "close brace token"
    OPEN_PAREN = "open paren token"
    CLOSE_PAREN = "close paren token"
    DOTDOT = "dotdot token"
    SEMICOLON = "semicolon token"
    IDENTIFIER = "identifier"
    END = "end token"


@dataclass
class Token:
    kind: SyntaxKind
    start: int
    end: int
    text: str


class ExpressionType(Enum):
    NUMBER = "number"
    RANGE = "range"
    PARAMETER = "parameter"
    BINARY = "binary"
    UNARY = "unary"


@dataclass
class NumberExpression:
    value: Union[int, float]
    type: ExpressionType = ExpressionType.NUMBER


@dataclass
class RangePart:
    from_: 'ExpressionCommon'
    to: Optional['ExpressionCommon'] = None


@dataclass
class RangeExpression:
    ranges: List[RangePart]
    type: ExpressionType = ExpressionType.RANGE


@dataclass
class ParameterExpression:
    parameterId: int
    type: ExpressionType = ExpressionType.PARAMETER


@dataclass
class BinaryExpression:
    left: 'ExpressionCommon'
    right: 'ExpressionCommon'
    operator: SyntaxKind
    type: ExpressionType = ExpressionType.BINARY


@dataclass
class UnaryExpression:
    expression: 'ExpressionCommon'
    operator: SyntaxKind
    type: ExpressionType = ExpressionType.UNARY


ExpressionCommon = Union[UnaryExpression, BinaryExpression, ParameterExpression,
                         RangeExpression, NumberExpression]
