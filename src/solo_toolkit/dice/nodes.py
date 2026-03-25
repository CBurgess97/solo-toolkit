from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Modifier:
    kind: str
    arg: int | None


@dataclass
class Dice:
    count: int
    sides: int
    modifiers: list[Modifier] = field(default_factory=list)


@dataclass
class Num:
    value: int


@dataclass
class BinOp:
    op: str
    left: Node
    right: Node


Node = Dice | Num | BinOp
