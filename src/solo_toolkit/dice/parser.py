from solo_toolkit.dice.lexer import Token, TokenKind, tokenize
from solo_toolkit.dice.nodes import BinOp, Dice, Node, Num


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _advance(self) -> Token:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _expect(self, kind: TokenKind) -> Token:
        tok = self._peek()
        if tok is None or tok.kind != kind:
            raise ParseError(f"expected {kind.name}, got {tok}")
        return self._advance()

    def parse_expr(self) -> Node:
        left = self._parse_term()
        while (tok := self._peek()) and tok.kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self._advance().value
            right = self._parse_term()
            left = BinOp(op, left, right)
        return left

    def _parse_term(self) -> Node:
        tok = self._expect(TokenKind.INT)
        n = int(tok.value)
        if (nxt := self._peek()) and nxt.kind == TokenKind.D:
            self._advance()
            sides_tok = self._expect(TokenKind.INT)
            sides = int(sides_tok.value)
            if n < 1 or sides < 1:
                raise ParseError(f"dice must be at least 1d1, got {n}d{sides}")
            return Dice(n, sides)
        return Num(n)


def parse(expression: str) -> Node:
    tokens = tokenize(expression)
    if not tokens:
        raise ParseError("empty expression")
    p = Parser(tokens)
    tree = p.parse_expr()
    if p._peek() is not None:
        raise ParseError(f"unexpected trailing tokens: {p._tokens[p._pos :]}")
    return tree
