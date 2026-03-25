import re
from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    INT = "INT"
    D = "D"
    PLUS = "PLUS"
    MINUS = "MINUS"


@dataclass
class Token:
    kind: TokenKind
    value: str


class ParseError(Exception):
    pass


_TOKENS = [
    r"(?P<INT>\d+)",
    r"(?P<D>d)",
    r"(?P<PLUS>\+)",
    r"(?P<MINUS>-)",
]
_PATTERN = re.compile(r"\s*(?:" + "|".join(_TOKENS) + ")")


def tokenize(expression: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    while pos < len(expression):
        m = _PATTERN.match(expression, pos)
        if not m:
            raise ParseError(
                f"unexpected character at position {pos}: {expression[pos:]!r}"
            )
        tokens.append(Token(TokenKind[m.lastgroup], m.group(m.lastgroup)))
        pos = m.end()
    return tokens
