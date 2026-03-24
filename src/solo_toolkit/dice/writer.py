from solo_toolkit.dice import DiceResult


def write(result: DiceResult) -> str:
    return " ".join(result.parts) + f" = {result.total}"
