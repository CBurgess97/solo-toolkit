from solo_toolkit.dice import DiceResult
from solo_toolkit.dice.nodes import BinOp, Dice, Node, Num


def write(result: DiceResult, node: Node) -> str:
    rollgroups = iter(result.rolls)
    parts: list[str] = []

    def _walk(n: Node):
        match n:
            case Dice(count, sides):
                rg = next(rollgroups)
                parts.append(f"{count}d{sides}: {rg.rolls}")
            case Num(value):
                parts.append(str(value))
            case BinOp(op, left, right):
                _walk(left)
                parts.append(op)
                _walk(right)

    _walk(node)
    return " ".join(parts) + f" = {result.total}"
