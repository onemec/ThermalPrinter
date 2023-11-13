from typing import Any

from escpos.printer import Usb

from playwright.sync_api import sync_playwright
import dominate
from dominate.tags import *
from dominate.util import text
from pathlib import Path

# Inspired largely by: https://codepen.io/silkine/pen/QWBxVX
DEFAULT_HTML_FILE = Path("temp.html")
DEFAULT_PNG_FILE = Path("temp.png")


def run(_playwright: sync_playwright) -> None:
    browser = _playwright.chromium.launch()
    page = browser.new_page()
    page.goto(DEFAULT_HTML_FILE.absolute().as_uri(), wait_until="networkidle")
    # Screenshot the "content" section of the HTML
    page.locator(".content").screenshot(path=DEFAULT_PNG_FILE)
    browser.close()


def create_html_file(
    contents: list[div] | None = None,
) -> None:
    doc = dominate.document()
    with doc.head:
        # Paper CSS (for fixed-width printer roll width)
        link(rel="stylesheet", href="src/style.css")
    with doc.body:
        doc.body["class"] = "preview"
        with div(cls="paper"):
            with div(cls="content"):
                for entry in contents:
                    div(entry)
    with open(DEFAULT_HTML_FILE, "w") as f:
        f.write(doc.render())


def print_img(img_source: Any, id_vendor: Any | None, id_product: Any | None) -> None:
    """
    Prints an image to a thermal printer.

    Args:
        img_source (Any): The source of the image to be printed.
        id_vendor (Any | None): The vendor ID of the USB printer. If not provided, the default value of 0x1FC9 will be used.
        id_product (Any | None): The product ID of the USB printer. If not provided, the default value of 0x2016 will be used.

    Raises:
        ValueError: If there is an error while printing the image.

    Returns:
        None
    """
    if not id_vendor:
        print("Setting default id_vendor of 0x1fc9...")
        id_vendor = 0x1FC9
    if not id_product:
        print("Setting default id_product of 0x2016...")
        id_product = 0x2016
    printer = Usb(idVendor=id_vendor, idProduct=id_product)
    # Attempt to print the image then cut the paper
    try:
        printer.image(img_source=img_source, center=True)
        printer.cut()
    except Exception as e:
        raise ValueError(f"Error while printing image: {e}") from e
