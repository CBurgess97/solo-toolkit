from collections.abc import Callable
from dataclasses import dataclass
from random import randint

from solo_toolkit.dice import DiceResult, RollGroup
from solo_toolkit.dice.nodes import BinOp, Dice, Modifier, Node, Num


@dataclass
class ModifierResult:
    kept: list[int]
    dropped: list[int]


def _kh(rolls: list[int], n: int | None) -> ModifierResult:
    s = sorted(rolls, reverse=True)
    return ModifierResult(kept=s[:n], dropped=s[n:])


def _kl(rolls: list[int], n: int | None) -> ModifierResult:
    s = sorted(rolls)
    return ModifierResult(kept=s[:n], dropped=s[n:])


_MODIFIERS: dict[str, Callable[[list[int], int | None], ModifierResult]] = {
    "kh": _kh,
    "kl": _kl,
}


def _roll(count: int, sides: int) -> RollGroup:
    return RollGroup(count, sides, [randint(1, sides) for a in range(0, count)])


def _apply_modifiers(group: RollGroup, modifiers: list[Modifier]) -> ModifierResult:
    dropped: list[int] = []
    for mod in modifiers:
        fn = _MODIFIERS.get(mod.kind)
        if fn is None:
            raise ValueError(f"unknown modifier: {mod.kind!r}")
        result = fn(group.rolls, mod.arg)
        group.rolls = result.kept
        dropped.extend(result.dropped)
    return ModifierResult(kept=group.rolls, dropped=dropped)


def evaluate(node: Node) -> DiceResult:
    match node:
        case Dice(count, sides, modifiers):
            group = _roll(count, sides)
            if modifiers:
                mod_result = _apply_modifiers(group, modifiers)
                group.dropped = mod_result.dropped
                group.modifiers = [m.kind for m in modifiers]
            return DiceResult(
                rolls=[group],
                total=sum(group.rolls),
            )
        case Num(value):
            return DiceResult(rolls=[], total=value)
        case BinOp(op, left, right):
            left_nodes = evaluate(left)
            right_nodes = evaluate(right)
            rolls = left_nodes.rolls + right_nodes.rolls
            if op == "+":
                return DiceResult(
                    rolls=rolls, total=left_nodes.total + right_nodes.total
                )
            if op == "-":
                return DiceResult(
                    rolls=rolls, total=left_nodes.total - right_nodes.total
                )
    raise ValueError(f"unexpected node type: {type(node)}")
