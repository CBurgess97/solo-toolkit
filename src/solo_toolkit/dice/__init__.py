from dataclasses import dataclass, field


@dataclass
class RollGroup:
    count: int
    sides: int
    rolls: list[int]
    dropped: list[int] = field(default_factory=list)
    modifiers: list[str] = field(default_factory=list)


@dataclass
class DiceResult:
    rolls: list[RollGroup]
    total: int
    parts: list[str] = field(default_factory=list)
