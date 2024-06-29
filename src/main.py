from enum import Enum
from typing import List

import typer

import parser as p
import sudoku_module
import weather_module


class PrinterModules(str, Enum):
    sudoku = "sudoku"
    weather = "weather"
    # xkcd = "xkcd"

    def generate(self):
        if self == "sudoku":
            return sudoku_module.generator.generate()
        elif self == "weather":
            return weather_module.generator.generate()


def main(
    modules: List[PrinterModules]
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
    # p.print_img(img_source="temp.png", id_vendor=None, id_product=None)


if __name__ == "__main__":
    typer.run(main)
