#!/usr/bin/env python3
"""Checks a project's design tokens against the original Material 3 values.

A design tool draws a design system, it does not implement it. What comes
out of it looks like Material 3 without being Material 3: the corner is
24 instead of 28, the shadow sits on the wrong level. Copied into the
token source, that inaccuracy becomes the project's truth.

This script compares every corner radius, elevation level and state layer
opacity it finds against the values Google generates from the Material 3
token set, and reports the difference as a number.

Reference values, taken from androidx.compose.material3.tokens on
android.googlesource.com (ShapeTokens.kt VERSION 14_1_0, ElevationTokens.kt
VERSION v0_210, StateTokens.kt VERSION v0_103), read 2026-08-29.

Read are:

    JSON                 .json                  nested or flat
    CSS and SCSS         .css, .scss            custom properties, variables
    Dart                 .dart                  const and map entries
    Kotlin               .kt                     val and token objects
    Anything else        line by line            name, separator, number

Point it at the token source, not at a stylesheet: a component style
legitimately holds values that are not tokens. Names that carry a scale
word without being a scale value — a shadow's blur, spread or offset, a
ripple radius — are skipped.

No dependencies, so the script runs in any CI.

    md3-token-check.py tokens/tokens.json
    md3-token-check.py lib/theme/ --scale baseline
    md3-token-check.py tokens/ --exceptions design/md3-exceptions.json
    md3-token-check.py tokens/tokens.json --report md3.json

Exit code 0 when there are no findings, 1 on findings, 2 on read errors.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# --------------------------------------------------------------------------
# The original values. Everything below is measured against these.
# --------------------------------------------------------------------------

CORNER_DP = {
    "none": 0.0,
    "extrasmall": 4.0,
    "small": 8.0,
    "medium": 12.0,
    "large": 16.0,
    "largeincreased": 20.0,
    "extralarge": 28.0,
    "extralargeincreased": 32.0,
    "extraextralarge": 48.0,
}

# The baseline scale, which is what Flutter implements. The increased steps
# arrived with the expressive stage; a project that is on the baseline must
# not use them, so the allowed set is switchable.
CORNER_BASELINE = {"none", "extrasmall", "small", "medium", "large",
                   "extralarge"}

ELEVATION_DP = {0: 0.0, 1: 1.0, 2: 3.0, 3: 6.0, 4: 8.0, 5: 12.0}

STATE_OPACITY = {"hover": 0.08, "focus": 0.10, "pressed": 0.10,
                 "dragged": 0.16}

# Longest first, so "extralarge" is not read as "large".
CORNER_STEPS = sorted(CORNER_DP, key=len, reverse=True)

# Written names of the steps, for the report.
READABLE = {
    "extrasmall": "extra-small", "largeincreased": "large-increased",
    "extralarge": "extra-large", "extralargeincreased": "extra-large-increased",
    "extraextralarge": "extra-extra-large",
}

# Carries a scale word without being a scale value: a shadow's blur is not
# a corner radius, a ripple radius is not one either.
NOT_A_SCALE = ("blur", "spread", "splash", "ripple", "glow", "offset")

RADIUS_WORDS = ("corner", "radius", "shape", "rounded")
ELEVATION_WORDS = ("elevation", "shadow")
STATE_WORDS = ("state", "layer", "opacity")
STATE_STEPS = {"hover": "hover", "focus": "focus", "press": "pressed",
               "drag": "dragged"}

# A name, a separator, and the first number behind it. The unit may be
# attached (8px), separated (8 dp) or a Kotlin extension (8.0.dp).
LINE = re.compile(
    r"""(?P<name>[A-Za-z_$@][A-Za-z0-9_.\-]{2,})   # corner-small, cornerSmall
        \s*["']?\s*[:=]\s*                          # : or =
        [^;\n]*?                                    # RoundedCornerShape(
        (?P<value>-?\d+(?:\.\d+)?)                  # 8, 8.0
        \s*\.?\s*(?P<unit>dp|px|rem|em|%)?          # dp, px, .dp, %
    """,
    re.VERBOSE,
)

COMMENT = re.compile(r"^\s*(//|/\*|\*|#(?!\w)|<!--)")

# In Dart, Kotlin and Swift the category is often the surrounding class, not
# the token: "class NeoElevation { static const level1 = 1.0; }".
CONTEXT = re.compile(
    r"^\s*(?:[\w@]+\s+)*(?:class|object|enum|struct|extension|mixin)"
    r"\s+([A-Za-z_]\w*)")
CONTEXT_END = re.compile(r"^[});]")

# Kotlin writes the name and the value on two lines:
#     inline val Level1: Dp
#         get() = 1.0.dp
DECLARED = re.compile(r"^\s*(?:[\w@]+\s+)*(?:val|var|let)\s+([A-Za-z_]\w*)"
                      r"\s*:[^=\d]*$")
GETTER = re.compile(r"^\s*get\(\)\s*=\s*(-?\d+(?:\.\d+)?)"
                    r"\s*\.?\s*(dp|px|rem|em|%)?")

TEXT_SUFFIXES = {".css", ".scss", ".sass", ".less", ".dart", ".kt", ".kts",
                 ".java", ".swift", ".ts", ".js", ".xml", ".yaml", ".yml"}
ALL_SUFFIXES = TEXT_SUFFIXES | {".json"}


class ReadError(Exception):
    pass


def canonical(name: str) -> str:
    """Strip everything that only separates words: corner-small, cornerSmall
    and corner.small are the same token."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def readable(step: str) -> str:
    return READABLE.get(step, step)


# --------------------------------------------------------------------------
# What a name means
# --------------------------------------------------------------------------

def classify(name: str):
    """Returns (kind, step) or None if the name is not a token we know.

    kind is "radius", "elevation" or "state"; step is the scale step, or
    None when the name carries a category but no step — a value that has
    to sit on the scale without having a name on it.
    """
    flat = canonical(name)

    if any(w in flat for w in NOT_A_SCALE):
        return None

    if any(w in flat for w in ELEVATION_WORDS):
        level = re.search(r"level(\d)|elevation(\d)|shadow(\d)", flat)
        if level:
            return "elevation", int(next(g for g in level.groups() if g))
        return "elevation", None

    if any(w in flat for w in STATE_WORDS):
        for fragment, step in STATE_STEPS.items():
            if fragment in flat:
                return "state", step

    if any(w in flat for w in RADIUS_WORDS):
        if "full" in flat or "circle" in flat or "stadium" in flat:
            return "radius", "full"
        for step in CORNER_STEPS:
            if step in flat:
                return "radius", step
        return "radius", None

    return None


def to_number(value: float, unit: str | None, kind: str, rem_base: float):
    """Brings a value onto the unit the reference uses: dp for radius and
    elevation, a share of 1 for a state layer. Returns None when the value
    cannot be compared."""
    if kind == "state":
        if unit == "%":
            return value / 100.0
        if unit in (None, ""):
            # 0.08 is a share, 8 is meant as a percentage.
            return value / 100.0 if value > 1.0 else value
        return None

    if unit in (None, "", "dp", "px"):
        return value
    if unit in ("rem", "em"):
        return value * rem_base
    if unit == "%":
        # A radius in percent is a circle or nothing sensible.
        return None
    return None


# --------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------

def entries_from_json(data, path, prefix=""):
    """Flattens a JSON token file. Design token files nest by category and
    often carry the number under "value"."""
    out = []
    if isinstance(data, dict):
        if "value" in data and not isinstance(data["value"], (dict, list)):
            return [(path, None, prefix, data["value"], "")]
        for key, value in data.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            out += entries_from_json(value, path, name)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            out += entries_from_json(value, path, f"{prefix}.{index}")
    elif prefix:
        out.append((path, None, prefix, data, ""))
    return out


def entries_from_text(text, path):
    out, context, declared = [], "", None
    for number, line in enumerate(text.splitlines(), start=1):
        if COMMENT.match(line):
            continue
        getter = GETTER.match(line)
        if getter and declared:
            out.append((path, number, declared,
                        getter.group(1) + (getter.group(2) or ""), context))
            declared = None
            continue
        declaration = DECLARED.match(line)
        if declaration:
            declared = declaration.group(1)
            continue
        if line.strip():
            declared = None
        block = CONTEXT.match(line)
        if block:
            context = block.group(1)
            continue
        if CONTEXT_END.match(line):
            context = ""
        found = LINE.search(line)
        if found:
            out.append((path, number, found.group("name"),
                        found.group("value") + (found.group("unit") or ""),
                        context))
    return out


def read(path: pathlib.Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ReadError(f"{path}: {error}") from error

    if path.suffix.lower() == ".json":
        try:
            return entries_from_json(json.loads(text), path)
        except json.JSONDecodeError as error:
            raise ReadError(f"{path}: {error}") from error
    return entries_from_text(text, path)


def collect(paths):
    files, errors = [], []
    for raw in paths:
        path = pathlib.Path(raw)
        if path.is_dir():
            files += sorted(p for p in path.rglob("*")
                            if p.is_file() and p.suffix.lower() in ALL_SUFFIXES)
        elif path.is_file():
            files.append(path)
        else:
            errors.append(f"{path}: not found")
    return files, errors


VALUE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(dp|px|rem|em|%)?\s*$")


def split_value(value):
    """Returns (number, unit) or None — a token whose value is a colour, a
    reference to another token or a curve is not ours to judge."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value), None
    if not isinstance(value, str):
        return None
    found = VALUE.match(value)
    if not found:
        return None
    return float(found.group(1)), found.group(2)


# --------------------------------------------------------------------------
# Checking
# --------------------------------------------------------------------------

def check(entries, scale, rem_base, exceptions):
    findings, excused = [], []
    checked = {"radius": 0, "elevation": 0, "state": 0}
    allowed_corners = {CORNER_DP[s] for s in
                       (CORNER_BASELINE if scale == "baseline" else CORNER_DP)}

    for path, line, name, raw, context in entries:
        meaning = classify(name)
        if not meaning and context:
            meaning = classify(f"{context}.{name}")
            if meaning and meaning[1] is None:
                meaning = None
        if not meaning:
            continue
        parts = split_value(raw)
        if not parts:
            continue
        kind, step = meaning
        value = to_number(parts[0], parts[1], kind, rem_base)
        if value is None:
            continue
        checked[kind] += 1

        finding = None
        if kind == "radius" and step == "full":
            pass
        elif kind == "radius" and step:
            if scale == "baseline" and step not in CORNER_BASELINE:
                finding = (f"{readable(step)} is not part of the baseline "
                           f"scale — it arrived with the expressive stage")
            elif abs(value - CORNER_DP[step]) > 0.01:
                finding = (f"corner {readable(step)}: "
                           f"{CORNER_DP[step]:g} dp expected, {value:g} dp found")
        elif kind == "radius":
            if not on_scale(value, allowed_corners):
                finding = (f"{value:g} dp is not on the shape scale "
                           f"({scale_text(allowed_corners)})")
        elif kind == "elevation" and step is not None:
            if step not in ELEVATION_DP:
                finding = f"level {step} does not exist — the scale ends at 5"
            elif abs(value - ELEVATION_DP[step]) > 0.01:
                finding = (f"elevation level {step}: {ELEVATION_DP[step]:g} dp "
                           f"expected, {value:g} dp found")
        elif kind == "elevation":
            if not on_scale(value, set(ELEVATION_DP.values())):
                finding = (f"{value:g} dp is not an elevation level "
                           f"({scale_text(set(ELEVATION_DP.values()))})")
        elif kind == "state":
            if abs(value - STATE_OPACITY[step]) > 0.001:
                finding = (f"state layer {step}: "
                           f"{STATE_OPACITY[step] * 100:g} % expected, "
                           f"{value * 100:g} % found")

        if not finding:
            continue

        reason = exceptions.get(canonical(name))
        if reason:
            excused.append((path, line, name, finding, reason))
        elif canonical(name) in exceptions:
            findings.append((path, line, name,
                             finding + " — listed as an exception without a "
                                       "reason, which does not count"))
        else:
            findings.append((path, line, name, finding))

    return findings, excused, checked


def on_scale(value, allowed):
    return any(abs(value - step) <= 0.01 for step in allowed)


def scale_text(values):
    return ", ".join(f"{v:g}" for v in sorted(values))


def read_exceptions(path):
    """{"corner-small": "reason"} — a name without a reason is no exception."""
    if not path:
        return {}
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReadError(f"{path}: {error}") from error
    if not isinstance(data, dict):
        raise ReadError(f"{path}: expected an object of name and reason")
    return {canonical(k): (v if isinstance(v, str) else "").strip()
            for k, v in data.items()}


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def print_report(findings, excused, checked, files, scale, errors):
    total = sum(checked.values())
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if findings:
        print(f"md3-token-check: {len(findings)} "
              f"{'finding' if len(findings) == 1 else 'findings'}\n")
        current = None
        for path, line, name, text in findings:
            if path != current:
                print(f"{path}")
                current = path
            place = f"{line:>5}  " if line else "       "
            print(f"{place}{name:<32} {text}")
        print()
    else:
        print("md3-token-check: no findings"
              + (" in what could be read" if errors else "") + "\n")

    print(f"Checked {total} token "
          f"{'value' if total == 1 else 'values'} in {len(files)} "
          f"{'file' if len(files) == 1 else 'files'}, scale \"{scale}\": "
          f"{checked['radius']} radius, {checked['elevation']} elevation, "
          f"{checked['state']} state layer.")

    if excused:
        print(f"Exceptions honoured: {len(excused)}")
        for path, line, name, text, reason in excused:
            print(f"  {name} — {reason}")

    if total == 0 and not errors:
        print("No radius, elevation or state layer token was recognised. "
              "Is this the token source?")


def main():
    parser = argparse.ArgumentParser(
        description="Compares design tokens against the original Material 3 "
                    "values for corner radius, elevation and state layers.")
    parser.add_argument("paths", nargs="+",
                        help="token files or directories")
    parser.add_argument("--scale", choices=("full", "baseline"), default="full",
                        help="full: the current shape scale including the "
                             "increased steps (default). baseline: 0, 4, 8, "
                             "12, 16, 28 — what Flutter implements.")
    parser.add_argument("--exceptions",
                        help="JSON file of token name and reason; a name "
                             "without a reason stays a finding")
    parser.add_argument("--rem-base", type=float, default=16.0,
                        help="pixels per rem for values written in rem "
                             "(default 16)")
    parser.add_argument("--report", help="write the findings as JSON")
    args = parser.parse_args()

    files, errors = collect(args.paths)
    try:
        exceptions = read_exceptions(args.exceptions)
    except ReadError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    entries = []
    for path in files:
        try:
            entries += read(path)
        except ReadError as error:
            errors.append(str(error))

    findings, excused, checked = check(entries, args.scale, args.rem_base,
                                       exceptions)
    print_report(findings, excused, checked, files, args.scale, errors)

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"scale": args.scale, "checked": checked,
                        "files": len(files),
                        "findings": [{"file": str(p), "line": l, "token": n,
                                      "finding": t}
                                     for p, l, n, t in findings],
                        "exceptions": [{"file": str(p), "line": l, "token": n,
                                        "finding": t, "reason": r}
                                       for p, l, n, t, r in excused]},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    if errors:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
