from typing import Any

from escpos.printer import Usb

from playwright.sync_api import sync_playwright
import dominate
from dominate.tags import div, link
from pathlib import Path

# Inspired largely by: https://codepen.io/silkine/pen/QWBxVX
DEFAULT_HTML_FILE = Path("temp.html")
DEFAULT_PNG_FILE = Path("temp.png")


def run(_playwright: sync_playwright) -> None:
    """
    Launches a Chromium browser instance, navigates to a local HTML file,
    takes a screenshot of the content, and saves it as a PNG file.

    Args:
        _playwright (sync_playwright): The Playwright instance used to control the browser.
    """
    browser = _playwright.chromium.launch()
    page = browser.new_page()
    page.goto(DEFAULT_HTML_FILE.absolute().as_uri(), wait_until="networkidle")
    page.locator(".content").screenshot(path=DEFAULT_PNG_FILE)
    browser.close()


def create_html_file(contents: list[div] | None = None) -> None:
    """
    Creates an HTML file with the specified contents and saves it to a default location.

    Args:
        contents (list[div] | None): A list of div elements to be included in the HTML file.
                                      If None, an empty content section will be created.

    Returns:
        None
    """
    doc = dominate.document()
    with doc.head:
        link(rel="stylesheet", href="src/style.css")
        link(rel="preconnect", href="https://fonts.googleapis.com")
        link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous")
        link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap",
        )
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
