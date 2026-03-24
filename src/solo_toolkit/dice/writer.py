from solo_toolkit.dice import DiceResult
from solo_toolkit.dice.nodes import BinOp, Dice, Node, Num


class Writer:
    def __init__(self, diceresult: DiceResult) -> None:
        self.diceresult = diceresult
        self.parts = []
        self.rollgroups = iter(self.diceresult.rolls)

    def _write(self, node: Node) -> str:
        match node:
            case Dice(count, sides):
                rollgroup = next(self.rollgroups)
                self.parts.append(f"{count}d{sides}: {rollgroup.rolls} ")
            case Num(value):
                self.parts.append(f"{value} ")
            case BinOp(op, left, right):
                self._write(left)
                self.parts.append(f"{op} ")
                self._write(right)
        return "".join(self.parts)

    def write(self, node: Node):
        out = self._write(node)
        return out + f"= {self.diceresult.total}"
