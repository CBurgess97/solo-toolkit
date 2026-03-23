from dataclasses import dataclass, field


@dataclass
class RollGroup:
    count: int
    sides: int
    rolls: list[int]


@dataclass
class DiceResult:
    rolls: list[RollGroup]
    total: int
    ops: list[str] = field(default_factory=list)
