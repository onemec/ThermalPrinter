from typing import Any

from escpos.printer import Usb
import os
from datetime import datetime

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


def testaroni():
    thingy = div(cls="row mb-3 text-center forecast")
    with thingy:
        with div(cls="col"):
            br()
            i(cls="fa-solid fa-cloud-moon fa-4x")
        with div(cls="col"):
            with div(cls="row"):
                text("<h5>70.7&degF</h5>", escape=False)
            with div(cls="row"):
                with p():
                    i(cls="fa-solid fa-wind fa-sm")
                    text(" 3.7 mph ")
                    br()
                    i(cls="fa-solid fa-arrow-up-long")
                    text(" 81.6&degF ", escape=False)
                    i(cls="fa-solid fa-arrow-down-long")
                    text(" 65.9&degF ", escape=False)
                    br()
                    i(cls="fa-regular fa-sun")
                    text(" 05:27 ")
                    i(cls="fa-solid fa-arrow-right-long")
                    text(" 20:14 ")
    return thingy


def create_html_file(
    temp_html_file: str = None,
    location_str: str = None,
    location_coordinates: tuple[float, float] = None,
    contents: list[div] | None = None,
) -> None:
    if not temp_html_file:
        temp_html_file = DEFAULT_HTML_FILE
    if not location_str:
        location_str = "Boston, MA"
    if not location_coordinates:
        location_coordinates = (42.34, -71.09)

    doc = dominate.document()
    with doc.head:
        # Font Awesome (webfont for icons)
        link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
            integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==",
            crossorigin="anonymous",
            referrerpolicy="no-referrer",
        )
        # Paper CSS (for fixed-width printer roll width)
        link(rel="stylesheet", href="style.css")
        # Bootstrap 5.3.0
        link(
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
            rel="stylesheet",
            integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM",
            crossorigin="anonymous",
        )
        link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&display=swap",
        )
    with doc.body:
        doc.body["class"] = "preview"
        with div(cls="paper"):
            with div(cls="content"):
                testaroni()
                for entry in contents:
                    div(entry)
    with open(temp_html_file, "w") as f:
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
