from random import randint

from solo_toolkit.dice import DiceResult, RollGroup
from solo_toolkit.dice.nodes import BinOp, Dice, Node, Num


def _roll(count: int, sides: int) -> RollGroup:
    return RollGroup(count, sides, [randint(1, sides) for a in range(0, count)])


def evaluate(node: Node) -> DiceResult:
    match node:
        case Dice(count, sides):
            group = _roll(count, sides)
            result = DiceResult(rolls=[group], total=sum(group.rolls))
            return result
        case Num(value):
            result = DiceResult(rolls=[], total=value)
            return result
        case BinOp(op, left, right):
            left_nodes = evaluate(left)
            right_nodes = evaluate(right)
            ops = [*left_nodes.ops, op, *right_nodes.ops]
            if op == "+":
                return DiceResult(
                    rolls=left_nodes.rolls + right_nodes.rolls,
                    total=left_nodes.total + right_nodes.total,
                    ops=ops,
                )
            if op == "-":
                return DiceResult(
                    rolls=left_nodes.rolls + right_nodes.rolls,
                    total=left_nodes.total - right_nodes.total,
                    ops=ops,
                )
        case _:
            raise ValueError(f"unknown node: {node}")
    return DiceResult([], 0)
