from enum import Enum
from typing import List
import typer
from dominate.tags import div
import parser as p
import sudoku_module
import weather_module

class PrinterModules(str, Enum):
    """
    Enum class representing the available printer modules.
    """
    sudoku = "sudoku"
    weather = "weather"

    def generate(self) -> div:
        """
        Generates content based on the selected printer module.

        Returns:
            str: The generated content from the selected module.
        """
        if self == PrinterModules.sudoku:
            return sudoku_module.generator.generate()
        elif self == PrinterModules.weather:
            return weather_module.generator.generate()

def main(modules: List[PrinterModules]):
    """
    Main function to generate HTML content and print an image based on the provided modules.

    Args:
        modules (List[PrinterModules]): A list of printer modules to generate content from.

    Raises:
        typer.Abort: If no modules are provided.
    """
    if not modules:
        print("No modules provided")
        raise typer.Abort()

    divs_to_add = [u.generate() for u in modules]
    p.create_html_file(contents=divs_to_add)
    with p.sync_playwright() as playwright:
        p.run(playwright)
    p.print_img(img_source="temp.png", id_vendor=None, id_product=None)

if __name__ == "__main__":
    typer.run(main)