import typer

import solo_toolkit.dice.parser as parser
import solo_toolkit.dice.roller as roller

app = typer.Typer()


@app.command()
def roll(expression: str):
    nodes = parser.parse(expression)
    rolls = roller.evaluate(nodes)
    print(rolls)
