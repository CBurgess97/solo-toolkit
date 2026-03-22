import re
from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    INT = "INT"
    D = "D"
    PLUS = "+"
    MINUS = "-"


@dataclass
class Token:
    kind: TokenKind
    value: str


class ParseError(Exception):
    pass


_PATTERN = re.compile(r"\s*(?:(\d+)|(d)|(\+)|(-))")


def tokenize(expression: str):
    tokens: list[Token] = []
    pos = 0
    while pos < len(expression):
        m = _PATTERN.match(expression, pos)
        if not m:
            raise ParseError(
                f"unexpected character at position {pos}: {expression[pos:]!r}"
            )
        if m.group(1):
            tokens.append(Token(TokenKind.INT, m.group(1)))
        elif m.group(2):
            tokens.append(Token(TokenKind.D, "d"))
        elif m.group(3):
            tokens.append(Token(TokenKind.PLUS, "+"))
        elif m.group(4):
            tokens.append(Token(TokenKind.MINUS, "-"))
        pos = m.end()
    return tokens
