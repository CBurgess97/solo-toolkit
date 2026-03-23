from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Dice:
    count: int
    sides: int


@dataclass
class Num:
    value: int


@dataclass
class BinOp:
    op: str
    left: Node
    right: Node


Node = Dice | Num | BinOp
