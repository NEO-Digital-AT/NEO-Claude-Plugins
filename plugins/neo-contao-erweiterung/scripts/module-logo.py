"""Builds the square logo of a Contao extension for the Contao Manager.

Every extension of the family gets the same logo; only the icon differs:

- a square tile (1:1) in the brand violet with rounded corners,
- the icon of the extension in neon green, large, tilted and cut off at the
  left edge of the tile,
- the NEO wordmark small at the bottom right, with a margin in the tile
  colour, so lines of the icon stop before it.

The icon is an SVG on a 64 x 64 grid (viewBox="0 0 64 64") drawn with lines:
shapes without fill, which this tool strokes in neon green with one visible
stroke width for all icons. Allowed elements: path, rect, circle, ellipse,
line, polyline, polygon and g. Allowed fills: none (the default), currentColor
(a filled detail in neon green, without outline) and the tile colour #2a025f
(a shape that covers the lines behind it, with outline). Not allowed: text,
images, styles, scripts, links, gradients, own strokes or colours; the tool
sets them for every icon alike.

The name is the English name of the extension without "NEO" ("Cookie
Consent"); the title of the logo becomes "NEO Cookie Consent".

    module-logo.py icon.svg --name "Cookie Consent" --out logo.svg
    module-logo.py icon.svg --name "Cookie Consent" --out logo.svg \\
        --preview preview.html

--preview writes an HTML page with the logo in the size of the Contao Manager
list and larger, on a light and a dark background, to look at before use.

Exit code 0 when the logo was written, 1 when the icon or the name is not
accepted (then nothing is written), 2 on wrong use.
"""
from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

TILE = "#2a025f"
INK = "#a8f20d"
SVG_NS = "http://www.w3.org/2000/svg"

# Placement of the icon (centre on the 64 grid, angle, scale) and of the
# wordmark (top left corner, width), the same for every extension.
ICON_CENTRE = (22.0, 25.0)
ICON_ANGLE = -12
ICON_SCALE = 1.25
STROKE = 2.4  # visible stroke width on the 64 grid
CORNER = 14
WORDMARK_AT = (38.5, 50.5)
WORDMARK_WIDTH = 18.5
WORDMARK_MARGIN = 2.0

# The NEO wordmark (viewBox 0 0 449.4872499 143.1987762): N, E, O.
WORDMARK_SIZE = (449.4872499, 143.1987762)
WORDMARK = (
    '<polygon points="21.7203382 66.7419315 28.6396993 71.9830104 28.6396993 143.1984965 0 143.1984965 0 50.291305 21.7203382 66.7419315"/>'
    '<polygon points="141.6748798 0 141.6748798 92.9243571 119.9488082 76.4679971 113.0351806 71.2326517 113.0351806 0 141.6748798 0"/>'
    '<polygon points="141.6748798 107.2900401 141.6748798 143.1984965 141.6576792 143.1984965 113.0351806 121.5239567 28.6396993 57.6115939 0 35.9198885 0 0 .0057335 0 28.6396993 21.6859719 113.0351806 85.5983346 141.6748798 107.2900401"/>'
    '<rect x="153.143836" y=".0002714" width="141.6737862" height="28.6396993"/>'
    '<rect x="153.143836" y="114.5590685" width="141.6737862" height="28.6396993"/>'
    '<rect x="153.143836" y="57.2796699" width="141.6737862" height="28.6396993"/>'
    '<path d="M420.8475506,28.639979v85.9190979h-85.9190979V28.639979h85.9190979ZM449.4872499.0002797h-143.1984965v143.1984965h143.1984965V.0002797h0Z"/>'
)

ELEMENTS = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "g"}
ATTRIBUTES = {
    "path": {"d"},
    "rect": {"x", "y", "width", "height", "rx", "ry"},
    "circle": {"cx", "cy", "r"},
    "ellipse": {"cx", "cy", "rx", "ry"},
    "line": {"x1", "y1", "x2", "y2"},
    "polyline": {"points"},
    "polygon": {"points"},
    "g": set(),
}
COMMON = {"fill", "transform"}
FILLS = {"none": "none", "currentcolor": INK, TILE: TILE}
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .-]{0,38}[A-Za-z0-9]$")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_icon(path: pathlib.Path, findings: list[str]) -> list[ET.Element]:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ET.ParseError) as error:
        findings.append(f"{path}: not a readable SVG ({error})")
        return []

    if local(root.tag) != "svg":
        findings.append(f"{path}: the root element is <{local(root.tag)}>, not <svg>")
    if " ".join((root.get("viewBox") or "").split()) != "0 0 64 64":
        findings.append(f'{path}: viewBox must be "0 0 64 64" (the grid of all icons), is "{root.get("viewBox")}"')

    shapes = [child for child in root if local(child.tag) not in {"title", "desc"}]
    if not shapes:
        findings.append(f"{path}: no shape inside the <svg>")

    def check(element: ET.Element, where: str) -> None:
        name = local(element.tag)
        if name not in ELEMENTS:
            findings.append(f"{where}: <{name}> is not allowed (only {', '.join(sorted(ELEMENTS))})")
            return
        for attribute, value in element.attrib.items():
            key = local(attribute)
            if key not in ATTRIBUTES[name] | COMMON:
                findings.append(f'{where}: attribute {key}="{value}" on <{name}> is not allowed (colours and strokes come from the tool)')
            elif key == "fill" and value.strip().lower() not in FILLS:
                findings.append(f'{where}: fill="{value}" on <{name}> is not allowed (none, currentColor or {TILE})')
            elif key == "transform" and re.search(r"[^a-zA-Z0-9 ,.()+-]", value):
                findings.append(f'{where}: transform="{value}" on <{name}> has characters that do not belong there')
        if (element.text or "").strip():
            findings.append(f"{where}: <{name}> contains text")
        for index, child in enumerate(element):
            check(child, f"{where} > {local(child.tag)}[{index}]")

    for index, shape in enumerate(shapes):
        check(shape, f"{path.name}: {local(shape.tag)}[{index}]")

    return shapes


def markup(element: ET.Element) -> str:
    name = local(element.tag)
    attributes = []
    filled = False
    for attribute, value in element.attrib.items():
        key = local(attribute)
        if key == "fill":
            colour = FILLS[value.strip().lower()]
            filled = colour == INK
            value = colour
        attributes.append(f'{key}="{html.escape(value, quote=True)}"')
    if filled:
        # A filled detail in neon green gets no outline: its size is its shape.
        attributes.append('stroke="none"')
    children = "".join(markup(child) for child in element)
    attrs = (" " + " ".join(attributes)) if attributes else ""
    return f"<{name}{attrs}>{children}</{name}>" if children else f"<{name}{attrs}/>"


def logo(shapes: list[ET.Element], name: str) -> str:
    title = html.escape(f"NEO {name}")
    icon = "".join(markup(shape) for shape in shapes)
    cx, cy = ICON_CENTRE
    wx, wy = WORDMARK_AT
    width = WORDMARK_WIDTH
    height = width * WORDMARK_SIZE[1] / WORDMARK_SIZE[0]
    margin = WORDMARK_MARGIN

    return (
        f'<svg xmlns="{SVG_NS}" viewBox="0 0 64 64" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        f'<defs><clipPath id="tile"><rect width="64" height="64" rx="{CORNER}"/></clipPath></defs>'
        f'<g clip-path="url(#tile)">'
        f'<rect width="64" height="64" fill="{TILE}"/>'
        f'<g transform="translate({cx:g} {cy:g}) rotate({ICON_ANGLE}) scale({ICON_SCALE:g}) translate(-32 -32)" '
        f'fill="none" stroke="{INK}" stroke-width="{STROKE / ICON_SCALE:.2f}" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
        f'<rect x="{wx - margin:g}" y="{wy - margin:g}" width="{width + 2 * margin:g}" height="{height + 2 * margin:.2f}" rx="1.5" fill="{TILE}"/>'
        f"</g>"
        f'<g fill="{INK}" transform="translate({wx:g} {wy:g}) scale({width / WORDMARK_SIZE[0]:.6f})">{WORDMARK}</g>'
        f"</svg>\n"
    )


def preview(svg: str, name: str) -> str:
    copies = iter(range(1000))

    def copy() -> str:
        # Each copy on the page gets its own id for the clip path.
        n = next(copies)
        return svg.replace('id="tile"', f'id="tile-{n}"').replace("url(#tile)", f"url(#tile-{n})")

    cells = []
    for background, colour in (("#ffffff", "#222222"), ("#f4f4f4", "#222222"), ("#1e1e1e", "#dddddd")):
        cells.append(
            f'<div style="display:flex;gap:24px;align-items:flex-end;padding:20px;background:{background};color:{colour}">'
            f'<div style="width:128px">{copy()}</div><div style="width:48px">{copy()}</div>'
            f'<div style="width:32px">{copy()}</div><span>NEO {html.escape(name)}</span></div>'
        )
    return f'<!doctype html><meta charset="utf-8"><title>NEO {html.escape(name)}</title><body style="margin:0;font:14px sans-serif">{"".join(cells)}</body>\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("icon", help="SVG of the icon on the 64 x 64 grid")
    parser.add_argument("--name", required=True, help='English name of the extension without "NEO", e.g. "Cookie Consent"')
    parser.add_argument("--out", required=True, help="file the logo is written to (logo.svg)")
    parser.add_argument("--preview", help="also write an HTML page with the logo in several sizes")
    args = parser.parse_args()

    icon = pathlib.Path(args.icon)
    if not icon.is_file():
        print(f"{icon}: no such file", file=sys.stderr)
        return 2

    findings: list[str] = []
    name = " ".join(args.name.split())
    if not NAME.match(name):
        findings.append(f'name "{args.name}": 2 to 40 characters, Latin letters, digits, spaces, dots and hyphens (the English name)')
    elif name.lower().startswith("neo"):
        findings.append(f'name "{args.name}": without "NEO", the tool adds it')

    shapes = read_icon(icon, findings)

    if findings:
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        print("No logo written.", file=sys.stderr)
        return 1

    svg = logo(shapes, name)
    out = pathlib.Path(args.out)
    out.write_text(svg, encoding="utf-8")
    print(f"{out}: NEO {name}, {len(svg)} bytes")

    if args.preview:
        page = pathlib.Path(args.preview)
        page.write_text(preview(svg, name), encoding="utf-8")
        print(f"{page}: preview")

    return 0


if __name__ == "__main__":
    sys.exit(main())
