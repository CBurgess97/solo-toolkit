import typer

import solo_toolkit.dice.parser as parser
import solo_toolkit.dice.roller as roller
import solo_toolkit.dice.writer as writer

app = typer.Typer()


@app.command()
def roll(expression: str):
    nodes = parser.parse(expression)
    result = roller.evaluate(nodes)
    w = writer.Writer(result)
    print(w.write(nodes))
