import re
from typing import Optional, Callable, List

from srqmplayer.formula.types import (
    SyntaxKind, Token, ExpressionCommon, ParameterExpression, RangePart,
    RangeExpression, NumberExpression, UnaryExpression, BinaryExpression,
    SyntaxException
)

MAX_PRECEDENCE = 8


# If candidate is binary token on presedence,
# then return corresponding binary operator
def is_token_binary_operator(presedence: int,
                             candidate: SyntaxKind) -> Optional[SyntaxKind]:
    # TODO: Why or/and have different prio?
    if presedence == 8:
        return SyntaxKind.OR if candidate == SyntaxKind.OR else None
    if presedence == 7:
        return SyntaxKind.AND if candidate == SyntaxKind.AND else None
    if presedence == 6:
        return SyntaxKind.GT_EQ if candidate == SyntaxKind.GT_EQ \
            else SyntaxKind.LT_EQ if candidate == SyntaxKind.LT_EQ \
            else SyntaxKind.GT if candidate == SyntaxKind.GT \
            else SyntaxKind.LT if candidate == SyntaxKind.LT \
            else SyntaxKind.EQ if candidate == SyntaxKind.EQ \
            else SyntaxKind.NEQ if candidate == SyntaxKind.NEQ \
            else SyntaxKind.IN if candidate == SyntaxKind.IN \
            else None

    if presedence == 5:
        return None  # here was "in keyword"
    if presedence == 4:
        return SyntaxKind.TO if candidate == SyntaxKind.TO else None
    if presedence == 3:
        return SyntaxKind.PLUS if candidate == SyntaxKind.PLUS \
            else SyntaxKind.MINUS if candidate == SyntaxKind.MINUS \
            else None

    if presedence == 2:
        return SyntaxKind.ASTERISK if candidate == SyntaxKind.ASTERISK \
            else SyntaxKind.SLASH if candidate == SyntaxKind.SLASH \
            else None

    if presedence == 1:
        return SyntaxKind.DIV if candidate == SyntaxKind.DIV \
            else SyntaxKind.MOD if candidate == SyntaxKind.MOD \
            else None

    raise SyntaxException(f'Unknown presedence {presedence}')


class TokenReader:
    def current(self) -> Token:
        pass

    def read_next(self) -> None:
        pass


class SkipWhitespaceTokenReader(TokenReader):
    _reader: Callable[[], Token]
    _current_token: Token = None

    def __init__(self, reader: Callable[[], Token]):
        super(SkipWhitespaceTokenReader, self)
        self._reader = reader
        self.read_next()

    def current(self) -> Token:
        return self._current_token

    def read_next(self) -> None:
        self._current_token = self._reader()
        while self._current_token.kind == SyntaxKind.WHITE_SPACE:
            self._current_token = self._reader()


class Parser:
    reader: TokenReader

    def __init__(self, reader_func: Callable[[], Token]):
        self.reader = SkipWhitespaceTokenReader(reader_func)

    def read_paren_expression(self) -> ExpressionCommon:
        """Expects current = open paren token
           Returns when position is after "close paren token
        """
        self.reader.read_next()

        if self.reader.current().kind == SyntaxKind.IDENTIFIER:
            param_match = re.search(r'^p(\d+)$', self.reader.current().text)

            if not param_match:
                raise SyntaxException(
                    f'Unknown parameter \'{self.reader.current().text}\''
                    f' at {self.reader.current().start}')
            pid = int(param_match[1]) - 1
            exp = ParameterExpression(parameterId=pid)
            self.reader.read_next()

            if self.reader.current().kind != SyntaxKind.CLOSE_PAREN:
                raise SyntaxException(
                    f'Expected ], but got \'{self.reader.current().text}\''
                    f' at {self.reader.current().start}')
            self.reader.read_next()
            return exp
        else:
            ranges: List[RangePart] = []
            while True:
                if self.reader.current().kind == SyntaxKind.SEMICOLON:
                    self.reader.read_next()
                    continue

                if self.reader.current().kind == SyntaxKind.CLOSE_PAREN:
                    self.reader.read_next()
                    break

                from_ = self.read_expr()
                if self.reader.current().kind == SyntaxKind.DOTDOT:
                    self.reader.read_next()
                    to = self.read_expr()

                    ranges.append(RangePart(from_=from_, to=to))
                elif self.reader.current().kind in (SyntaxKind.CLOSE_PAREN,
                                                    SyntaxKind.SEMICOLON):
                    ranges.append(RangePart(from_=from_))
                else:
                    raise SyntaxException(
                        f'Unexpected token inside paren'
                        f' \'{self.reader.current().text}\''
                        f' pos={self.reader.current().start} ')
            return RangeExpression(ranges=ranges)

    def read_prim(self) -> ExpressionCommon:
        prim_start_token = self.reader.current()

        if prim_start_token.kind == SyntaxKind.NUM_LITERAL:
            val = prim_start_token.text.replace(',', '.').replace(' ', '')
            expr_ = NumberExpression(value=float(val))
            self.reader.read_next()
            return expr_
        elif prim_start_token.kind == SyntaxKind.OPEN_PAREN:
            return self.read_paren_expression()
        elif prim_start_token.kind == SyntaxKind.OPEN_BRACE:
            self.reader.read_next()
            expr_ = self.read_expr()
            if self.reader.current().kind != SyntaxKind.CLOSE_BRACE:
                raise SyntaxException(f'Expected close brace token but got'
                                      f' \'{self.reader.current().text}\''
                                      f' at {self.reader.current().start}')
            self.reader.read_next()
            return expr_
        elif prim_start_token.kind == SyntaxKind.MINUS:
            self.reader.read_next()
            inner_expr = self.read_prim()
            return UnaryExpression(expression=inner_expr,
                                   operator=SyntaxKind.MINUS)
        else:
            if self.reader.current().kind == SyntaxKind.END:
                raise SyntaxException(
                    f'Expected value at {self.reader.current().start}')
            else:
                raise SyntaxException(
                    f'Expecting primary value at {self.reader.current().start}'
                    f' but got \'{self.reader.current().text}\''
                    f' kind=${self.reader.current().kind}')

    def read_expr(self, cur_priority: int = MAX_PRECEDENCE) -> ExpressionCommon:
        if cur_priority == 0:
            return self.read_prim()

        left = self.read_expr(cur_priority - 1)
        while True:
            possible_binary_token_kind = self.reader.current().kind
            if possible_binary_token_kind == SyntaxKind.END:
                return left

            possible_binary_token = is_token_binary_operator(
                cur_priority, possible_binary_token_kind)
            if not possible_binary_token:
                return left

            self.reader.read_next()

            right = self.read_expr(cur_priority - 1)

            new_left = BinaryExpression(operator=possible_binary_token,
                                        left=left, right=right)
            left = new_left

    def parse(self):
        expr = self.read_expr()
        if self.reader.current().kind != SyntaxKind.END:
            raise SyntaxException(
                f'Unexpected data at {self.reader.current().start}:'
                f' \'{self.reader.current().text}\''
                f' kind={self.reader.current().kind}')
        return expr
