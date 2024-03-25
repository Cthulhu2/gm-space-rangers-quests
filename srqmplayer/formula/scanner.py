import re
from typing import Callable, Optional

from srqmplayer.formula.types import (SyntaxKind, Token, SyntaxException)

CHARACTERS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM01234567890_'

KEYWORD_KINDS = {
    'mod': SyntaxKind.MOD,
    'div': SyntaxKind.DIV,
    'to': SyntaxKind.TO,
    'in': SyntaxKind.IN,
    'and': SyntaxKind.AND,
    'or': SyntaxKind.OR
}


# TODO: Rewrite to a decorator
class SanityCheck:
    origStr: str
    constructedStr: str
    origScan: Callable[[], Token]

    def __init__(self, orig_str: str, orig_scan: Callable[[], Token]):
        self.constructedStr = ''
        self.origStr = orig_str
        self.origScan = orig_scan

    def scan(self) -> Token:
        token = self.origScan()
        if token.end - token.start <= 0 and token.kind != SyntaxKind.END:
            raise SyntaxException(
                f'Scanner fail: end={token.end} start={token.start}'
                f' str=\'{self.origStr}\'')
        if self.origStr[token.start:token.end] != token.text:
            raise SyntaxException(f'Scanner fail: token slice differs')
        if token.kind != SyntaxKind.END:
            self.constructedStr += token.text
        else:
            if self.constructedStr != self.origStr:
                raise SyntaxException(
                    f'Scanner fail: constructed string differs!'
                    f' {self.constructedStr} <> {self.origStr}')
        return token


def is_whitespace(ch: str):
    # ch.isspace()
    return ch in (' ', '\n', '\r', '\t')


def is_digit(ch: str):
    return len(ch) == 1 and ch in '0123456789'


def one_char_token_to_kind(ch: str) -> Optional[SyntaxKind]:
    return SyntaxKind.OPEN_BRACE if ch == '(' \
        else SyntaxKind.CLOSE_BRACE if ch == ')' \
        else SyntaxKind.OPEN_PAREN if ch == '[' \
        else SyntaxKind.CLOSE_PAREN if ch == ']' \
        else SyntaxKind.SLASH if ch == '/' \
        else SyntaxKind.ASTERISK if ch == '*' \
        else SyntaxKind.PLUS if ch == '+' \
        else SyntaxKind.MINUS if ch == '-' \
        else SyntaxKind.EQ if ch == '=' \
        else SyntaxKind.SEMICOLON if ch == ';' \
        else None


class Scanner:
    pos: int = 0
    end: int
    str_: str
    sanity_check: SanityCheck

    def __init__(self, str_: str):
        self.end = len(str_)
        self.str_ = str_
        self.sanity_check = SanityCheck(str_, self.scan)
        self.scan = self.sanity_check.scan

    def scan_whitespace(self) -> Token:
        start_ = self.pos
        while self.pos < self.end and is_whitespace(self.str_[self.pos]):
            self.pos += 1

        return Token(kind=SyntaxKind.WHITE_SPACE, start=start_, end=self.pos,
                     text=self.str_[start_:self.pos])

    def look_ahead(self, count: int = 1):
        return self.str_[
            self.pos + count] if self.pos + count < self.end else None

    def scan_identifier_or_keyword(self) -> Token:
        start = self.pos
        text = ''
        keyword_kind: Optional[SyntaxKind] = None
        while self.pos < self.end and self.str_[self.pos] in CHARACTERS:
            self.pos += 1
            text = self.str_[start:self.pos]
            keyword_kind = KEYWORD_KINDS.get(text)
            if keyword_kind:
                # Some quests have "[p1] mod1000" (without spaces)
                break

        kind: SyntaxKind = keyword_kind or SyntaxKind.IDENTIFIER
        if start == self.pos:
            raise SyntaxException(f'Unknown char {self.str_[self.pos]}')

        return Token(kind=kind, start=start, end=self.pos, text=text)

    def scan_number(self):
        dot_seen = False
        start = self.pos

        trailing_spaces_starts_at_pos: Optional[int] = None
        while self.pos < self.end:
            this_character_is_space = False
            ch = self.str_[self.pos]
            if is_digit(ch):
                pass  # ok
            elif ch in ('.', ','):
                if dot_seen:
                    break

                next_next_char = self.look_ahead()
                if next_next_char not in ('.', ','):
                    dot_seen = True
                else:
                    break
                # } else if (char === "-" && pos === start) {
                # Ok here
            elif ch == ' ':
                this_character_is_space = True
            else:
                break

            # Allow spaces inside digits but keep spaces as separate token
            # if they are trailing spaces
            if this_character_is_space:
                if trailing_spaces_starts_at_pos is None:
                    # Ok, looks like a series of spaces have been begun
                    trailing_spaces_starts_at_pos = self.pos
                else:
                    pass  # Series of spaces is still continues
            else:
                # Character is not a space and belongs to digit chars set.
                # So, spaces are not a trailing spaces
                trailing_spaces_starts_at_pos = None
            self.pos += 1

        if trailing_spaces_starts_at_pos is not None:
            # health check
            if not re.match(r'^\s*$',
                            self.str_[trailing_spaces_starts_at_pos:self.pos]):
                raise SyntaxException(
                    'Unknown internal state: trailing_spaces_starts_at_pos'
                    ' is set but tail is not spaces')
            self.pos = trailing_spaces_starts_at_pos

        return Token(kind=SyntaxKind.NUM_LITERAL, start=start, end=self.pos,
                     text=self.str_[start:self.pos])

    def scan(self) -> Token:
        if self.pos >= self.end:
            return Token(kind=SyntaxKind.END, start=self.pos, end=self.pos,
                         text='')
        ch = self.str_[self.pos]
        if is_whitespace(ch):
            return self.scan_whitespace()

        look_ahead_char = self.look_ahead()
        if ch == '.' and look_ahead_char == '.':
            token = Token(kind=SyntaxKind.DOTDOT, start=self.pos,
                          end=self.pos + 2,
                          text=ch + look_ahead_char)
            self.pos += 2
            return token

        if ch == '<' and look_ahead_char == '>':
            token = Token(kind=SyntaxKind.NEQ, start=self.pos, end=self.pos + 2,
                          text=ch + look_ahead_char)
            self.pos += 2
            return token

        if ch == '>' and look_ahead_char == '=':
            token = Token(kind=SyntaxKind.GT_EQ, start=self.pos,
                          end=self.pos + 2,
                          text=ch + look_ahead_char)
            self.pos += 2
            return token

        if ch == '<' and look_ahead_char == '=':
            token = Token(kind=SyntaxKind.LT_EQ, start=self.pos,
                          end=self.pos + 2,
                          text=ch + look_ahead_char)
            self.pos += 2
            return token

        if ch == '>' and look_ahead_char != '=':
            token = Token(kind=SyntaxKind.GT, start=self.pos, end=self.pos + 1,
                          text=ch)
            self.pos += 1
            return token

        if ch == '<' and look_ahead_char != '=':
            token = Token(kind=SyntaxKind.LT, start=self.pos, end=self.pos + 1,
                          text=ch)
            self.pos += 1
            return token

        if is_digit(ch):
            # or (char === "-" && look_ahead_char && isDigit(look_ahead_char))
            return self.scan_number()

        one_char_kind = one_char_token_to_kind(ch)
        if one_char_kind:
            token = Token(kind=one_char_kind, start=self.pos, end=self.pos + 1,
                          text=ch)
            self.pos += 1
            return token

        return self.scan_identifier_or_keyword()
