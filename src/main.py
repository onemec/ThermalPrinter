from enum import Enum
from typing import List
import typer
from dominate.tags import div

# Support both direct execution and package imports
try:
    from . import printer_core as p
    from . import sudoku_module
    from . import weather_module
except ImportError:
    import printer_core as p
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

def main(
    modules: List[PrinterModules],
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Generate output but do not print."
    ),
    vendor_id: str = typer.Option(
        None, "--vendor-id", help="USB Vendor ID (hex string, e.g. 0x1fc9)."
    ),
    product_id: str = typer.Option(
        None, "--product-id", help="USB Product ID (hex string, e.g. 0x2016)."
    ),
):
    """
    Main function to generate HTML content and print an image based on the provided modules.

    Args:
        modules (List[PrinterModules]): A list of printer modules to generate content from.
        dry_run (bool): If True, skip printing.
        vendor_id (str): USB Vendor ID.
        product_id (str): USB Product ID.

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

    if dry_run:
        print("Dry run: Skipping print.")
        return

    # Convert hex strings to integers if provided
    vid = int(vendor_id, 16) if vendor_id else None
    pid = int(product_id, 16) if product_id else None

    p.print_img(img_source="temp.png", id_vendor=vid, id_product=pid)

if __name__ == "__main__":
    typer.run(main)