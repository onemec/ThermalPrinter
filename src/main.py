from typing import List, Optional
from enum import Enum
import typer
from typing_extensions import Annotated
import sudoku_module
import parser as p


class PrinterModules(str, Enum):
    sudoku = "sudoku"
    # xkcd = "xkcd"

    def generate(self):
        match self:
            case "sudoku":
                return sudoku_module.generator.generate()


def main(
    modules: Annotated[
        Optional[List[PrinterModules]],
        typer.Option(
            "--modules", "-m", help="The modules to be printed in the newspaper"
        ),
    ] = None
):
    if not modules:
        print("No modules provided")
        raise typer.Abort()

    divs_to_add = []
    for u in modules:
        print(f"Processing module: {u}...")
        divs_to_add.append(u.generate())
    p.create_html_file(contents=divs_to_add)
    with p.sync_playwright() as playwright:
        p.run(playwright)


if __name__ == "__main__":
    typer.run(main)
