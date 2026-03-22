from dataclasses import dataclass


@dataclass
class RollGroup:
    count: int
    sides: int
    rolls: list[int]


@dataclass
class DiceResult:
    expression: str
    rolls: list[RollGroup]
    modifiers: list[int]
    total: int
