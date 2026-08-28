#!/usr/bin/env python3
"""WCAG 2.2 contrast calculator for the NEO design rules.

Computes the contrast ratio of two colours and checks it against the
requirement for the given usage. Translucent colours are composited over
a backdrop first — exactly the way a browser does it, because a hover
surface with an alpha value is the most common cause of an unreadable
button.

No dependencies, so the script runs in any CI.

    contrast.py "#5A6273" "#FFFFFF"
    contrast.py "#FFFFFF" "#1F3A5F1F" --backdrop "#0B1220" --usage element
    contrast.py --pairs design/contrast-pairs.json
    contrast.py --example > design/contrast-pairs.json

Exit code 0 when everything passes, 1 otherwise — usable as a gate.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Requirement per usage: (AA, AAA). AAA is not defined for non-text; there
# it stays at 3:1 (WCAG 1.4.11).
USAGES: dict[str, tuple[float, float, str]] = {
    "text": (4.5, 7.0, "body text, label, help text (1.4.3/1.4.6)"),
    "large-text": (3.0, 4.5, "from 24px, or from 18.66px bold (1.4.3/1.4.6)"),
    "element": (3.0, 3.0, "border, icon, state, chart, focus ring (1.4.11)"),
}

NAMED = {
    "white": "#FFFFFF", "black": "#000000", "transparent": "#00000000",
}


class ColourError(ValueError):
    pass


def parse_colour(value: str) -> tuple[float, float, float, float]:
    """Parses #RGB, #RGBA, #RRGGBB, #RRGGBBAA, rgb() and rgba() as RGBA 0..1."""
    text = value.strip().lower()
    text = NAMED.get(text, text)

    match = re.fullmatch(r"rgba?\(([^)]*)\)", text)
    if match:
        parts = [p.strip() for p in match.group(1).replace("/", " ").replace(",", " ").split()]
        if len(parts) not in (3, 4):
            raise ColourError(f'"{value}" is not a valid rgb() value')
        numbers = []
        for i, part in enumerate(parts):
            if part.endswith("%"):
                numbers.append(float(part[:-1]) / 100)
            else:
                numbers.append(float(part) / (255 if i < 3 else 1))
        while len(numbers) < 4:
            numbers.append(1.0)
        return tuple(min(1.0, max(0.0, n)) for n in numbers)  # type: ignore[return-value]

    raw = text.lstrip("#")
    if len(raw) in (3, 4):
        raw = "".join(c * 2 for c in raw)
    if len(raw) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", raw):
        raise ColourError(
            f'"{value}" is not a colour (expected #RGB, #RRGGBB, #RRGGBBAA or rgb())')
    channels = [int(raw[i:i + 2], 16) / 255 for i in range(0, len(raw), 2)]
    if len(channels) == 3:
        channels.append(1.0)
    return tuple(channels)  # type: ignore[return-value]


def composite(front: tuple[float, float, float, float],
              back: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Places a translucent colour over another one (source over, sRGB)."""
    a = front[3]
    if a >= 1.0:
        return front
    b = back[3]
    out = a + b * (1 - a)
    if out == 0:
        return (0.0, 0.0, 0.0, 0.0)
    channels = tuple((front[i] * a + back[i] * b * (1 - a)) / out for i in range(3))
    return (*channels, out)  # type: ignore[return-value]


def _linearise(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(colour: tuple[float, float, float, float]) -> float:
    r, g, b = (_linearise(c) for c in colour[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(front: tuple[float, float, float, float],
          back: tuple[float, float, float, float]) -> float:
    a, b = luminance(front), luminance(back)
    lighter, darker = (a, b) if a >= b else (b, a)
    return (lighter + 0.05) / (darker + 0.05)


def to_hex(colour: tuple[float, float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in colour[:3])


def evaluate(front_raw: str, back_raw: str, backdrop_raw: str | None,
             usage: str) -> dict:
    """Composites, computes and judges one pair."""
    if usage not in USAGES:
        raise ColourError(f'unknown usage "{usage}" (allowed: {", ".join(USAGES)})')
    backdrop = parse_colour(backdrop_raw) if backdrop_raw else None
    back = parse_colour(back_raw)
    if back[3] < 1.0:
        if backdrop is None:
            raise ColourError(
                f'the background "{back_raw}" is translucent. Without --backdrop '
                "there is no way to compute what the user actually sees.")
        back = composite(back, backdrop)
    front = parse_colour(front_raw)
    if front[3] < 1.0:
        front = composite(front, back)

    value = ratio(front, back)
    aa, aaa, _ = USAGES[usage]
    return {
        "front": front_raw, "back": back_raw, "backdrop": backdrop_raw, "usage": usage,
        "computed_front": to_hex(front), "computed_back": to_hex(back),
        "ratio": value, "aa": aa, "aaa": aaa,
        "passes_aa": value >= aa, "passes_aaa": value >= aaa,
    }


EXAMPLE = {
    "_note": (
        "Contrast pairs of this project. Every colour combination a user can "
        "see belongs here — including the hover variant. Check with: "
        "contrast.py --pairs <this file>. The colours below are a placeholder "
        "set and serve as a pattern only; replace them with the tokens of "
        "your own project. "
        '"Light - field border" fails on purpose: a border that is what makes '
        "a control recognisable in the first place needs 3:1. A purely "
        "separating line without that job does not, and does not belong in "
        "this list."
    ),
    "backdrop": "#FFFFFF",
    "level": "aa",
    "pairs": [
        {"name": "Light - body text on surface", "front": "#111827", "back": "#FFFFFF"},
        {"name": "Light - muted text on surface", "front": "#5A6273", "back": "#FFFFFF"},
        {"name": "Light - primary button, rest", "front": "#FFFFFF", "back": "#1F3A5F"},
        {"name": "Light - primary button, hover", "front": "#FFFFFF", "back": "#2C5282"},
        {"name": "Light - field border", "front": "#D5D8E0", "back": "#FFFFFF", "usage": "element"},
        {"name": "Light - ghost button, hover with alpha", "front": "#1F3A5F", "back": "#1F3A5F14", "backdrop": "#FFFFFF"},
        {"name": "Dark - body text on surface", "front": "#F3F4F6", "back": "#111827", "backdrop": "#0B1220"},
        {"name": "Dark - primary button, rest", "front": "#101820", "back": "#7DD3FC"},
        {"name": "Dark - focus ring", "front": "#7DD3FC", "back": "#111827", "usage": "element"},
    ],
}


def run_file(path: pathlib.Path, level_arg: str | None) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Pair file cannot be read: {error}", file=sys.stderr)
        return 2

    pairs = data.get("pairs")
    if not isinstance(pairs, list) or not pairs:
        print('The pair file contains no "pairs" list.', file=sys.stderr)
        return 2

    level = (level_arg or data.get("level") or "aa").lower()
    shared_backdrop = data.get("backdrop")

    results, unreadable = [], []
    for number, pair in enumerate(pairs, start=1):
        name = pair.get("name") or f"Pair {number}"
        try:
            result = evaluate(
                pair["front"], pair["back"],
                pair.get("backdrop", shared_backdrop), pair.get("usage", "text"))
        except (ColourError, KeyError) as error:
            unreadable.append(f"{name}: {error}")
            continue
        result["name"] = name
        results.append(result)

    width = max((len(r["name"]) for r in results), default=10)
    failed = 0
    print(f"Contrast check per WCAG 2.2, level {level.upper()} - {path}\n")
    for r in results:
        required = r["aaa"] if level == "aaa" else r["aa"]
        ok = r["ratio"] >= required
        failed += 0 if ok else 1
        marker = "PASS" if ok else "FAIL"
        print(f"  {marker}  {r['name']:<{width}}  {r['ratio']:6.2f}:1"
              f"  (needs {required}:1, {r['usage']})")

    print()
    if unreadable:
        print("Not computable:")
        for line in unreadable:
            print(f"  - {line}")
        print()
    if failed or unreadable:
        print(f"{failed} of {len(results)} pairs below the requirement"
              f"{f', {len(unreadable)} not computable' if unreadable else ''}.")
        return 1
    print(f"All {len(results)} pairs pass level {level.upper()}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute and check a contrast ratio per WCAG 2.2.",
        epilog='Without --usage the default is "text" (4.5:1 at level AA).')
    parser.add_argument("front", nargs="?", help='foreground colour, e.g. "#111827"')
    parser.add_argument("back", nargs="?", help='background colour, e.g. "#FFFFFF"')
    parser.add_argument("--backdrop", help="opaque backdrop beneath translucent colours")
    parser.add_argument("--usage", default="text", choices=sorted(USAGES),
                        help="how the foreground is used")
    parser.add_argument("--level", choices=["aa", "aaa"], help="required level")
    parser.add_argument("--pairs", type=pathlib.Path, help="JSON file with colour pairs")
    parser.add_argument("--example", action="store_true",
                        help="print an example pair file")
    args = parser.parse_args(argv)

    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return 0

    if args.pairs:
        return run_file(args.pairs, args.level)

    if not args.front or not args.back:
        parser.print_help()
        return 2

    try:
        r = evaluate(args.front, args.back, args.backdrop, args.usage)
    except ColourError as error:
        print(str(error), file=sys.stderr)
        return 2

    level = args.level or "aa"
    required = r["aaa"] if level == "aaa" else r["aa"]
    front_note = ("  (composited from " + r["front"] + ")"
                  if r["computed_front"].lower() != r["front"].lower().rstrip() else "")
    back_note = ("  (composited from " + r["back"] + ")"
                 if r["computed_back"].lower() != r["back"].lower().rstrip() else "")
    print(f"Ratio        {r['ratio']:.2f}:1")
    print(f"Foreground   {r['computed_front']}{front_note}")
    print(f"Background   {r['computed_back']}{back_note}")
    print(f"Usage        {args.usage} - {USAGES[args.usage][2]}")
    print(f"Requirement  {required}:1 (level {level.upper()})")
    print()
    if r["ratio"] >= required:
        rest = "" if level == "aaa" or r["passes_aaa"] else "  (AAA at 7:1 not reached)"
        print(f"Passed.{rest}")
        return 0
    print(f"Failed. {required - r['ratio']:.2f} points short of {required}:1.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
