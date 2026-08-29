#!/usr/bin/env python3
"""Checks where the texts of an interface come from.

Every visible text has an origin: the approved design, an approved text
list, or an instruction from the project owner. A text without one was
invented — and an invented text is not a blemish. It promises the user
something the application does not do, and the user has no second place
to look it up.

The script compares the texts of a project against the approved stock and
reports what is not in it. It also lists the texts that make a promise
about the system's behaviour — reachable under, automatically, within,
you can choose — because those have to be proven against the code before
they are written.

Read are:

    JSON and ARB     .json, .arb            nested or flat
    PHP return       .php                   return [ 'a' => 'b', ... ]
    Flat YAML        .yaml, .yml            key: value, by indentation
    Design export    .html, .htm            visible text and labels

The approved stock is a JSON object of text and origin:

    { "Auftrag anlegen": "Artboard B28", "Speichern": "Entwurf 2026-08" }

A text without an origin does not count as approved — the same rule that
applies to every other exception in these plugins.

No dependencies, so the script runs in any CI.

    ui-text-check.py lang/de.json --approved design/texte.json
    ui-text-check.py lang/ --source-language de --approved design/texte.json
    ui-text-check.py lang/de.json --approved design/texte.json --accept
    ui-text-check.py lang/de.json

Exit code 0 when every text has an origin, 1 on findings, 2 on read errors.
"""
from __future__ import annotations

import argparse
import difflib
import html.parser
import json
import pathlib
import re
import sys

# Placeholders of the common frameworks. A text that carries one cannot be
# compared literally: the design shows a name, the language file a hole.
PLACEHOLDER = re.compile(
    r"\{\{\s*[\w.]+\s*\}\}"          # {{ name }}       Vue, Angular, Blade
    r"|\{[\w.]+\}"                    # {name}           ICU, Flutter, .NET
    r"|:[a-zA-Z_]\w*"                 # :name            Laravel
    r"|%\d+\$[sd]"                    # %1$s             positional
    r"|%[sd]"                         # %s               C style
    r"|#\{[\w.]+\}"                   # #{name}
)

# A text that says what the system does is not a text, it is a promise. It
# is proven against the code before it is written, not afterwards.
PROMISE = (
    (re.compile(r"https?://|www\.|\.[a-z]{2,6}/", re.I), "an address"),
    (re.compile(r"\berreichbar\b|\babrufbar\b|\bfinden Sie\b|\bunter\b\s+\w+/",
                re.I), "reachable under"),
    (re.compile(r"\bautomatisch\b|\bautomatically\b", re.I), "automatic"),
    (re.compile(r"\binnerhalb von\b|\bwithin\b\s+\d|\bin\s+\d+\s*"
                r"(Minuten|Stunden|Tagen|minutes|hours|days)\b", re.I), "a deadline"),
    (re.compile(r"\bjederzeit\b|\bat any time\b", re.I), "at any time"),
    (re.compile(r"\bkönnen Sie\b.*\b(wählen|auswählen|festlegen|ändern)\b"
                r"|\byou can\b.*\b(choose|select|set|change)\b", re.I),
     "a choice"),
    (re.compile(r"\bwird\b.*\b(versendet|gesendet|erstellt|gelöscht|"
                r"gespeichert|übertragen)\b", re.I), "an action of the system"),
)

TEXT_KEYS_SKIPPED = re.compile(r"^@|^_")   # ARB metadata, private keys
ATTRIBUTES = ("placeholder", "aria-label", "title", "alt", "value")
LANGUAGE_SUFFIXES = {".json", ".arb", ".php", ".yaml", ".yml"}
DESIGN_SUFFIXES = {".html", ".htm"}


class ReadError(Exception):
    pass


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------
# Reading the language files
# --------------------------------------------------------------------------

def from_json(data, path, prefix=""):
    out = []
    if isinstance(data, dict):
        for key, value in data.items():
            if TEXT_KEYS_SKIPPED.match(str(key)):
                continue
            name = f"{prefix}.{key}" if prefix else str(key)
            out += from_json(value, path, name)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            out += from_json(value, path, f"{prefix}.{index}")
    elif isinstance(data, str) and data.strip():
        out.append((path, None, prefix, data))
    return out


PHP_ENTRY = re.compile(r"""['"]([^'"]+)['"]\s*=>\s*['"]([^'"]*)['"]""")
YAML_ENTRY = re.compile(r"""^\s*([\w.\-]+)\s*:\s*['"]?(.+?)['"]?\s*$""")


def from_lines(text, path, pattern):
    out = []
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith(("#", "//")):
            continue
        found = pattern.search(line)
        if found and found.group(2).strip():
            out.append((path, number, found.group(1), found.group(2)))
    return out


class DesignText(html.parser.HTMLParser):
    """Pulls the visible text out of a design export: text nodes and the
    attributes that end up on screen."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.texts, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        for name, value in attrs:
            if name in ATTRIBUTES and value and value.strip():
                self.texts.append(value)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.texts.append(data)


def read_language(path: pathlib.Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ReadError(f"{path}: {error}") from error

    suffix = path.suffix.lower()
    if suffix in (".json", ".arb"):
        try:
            return from_json(json.loads(text), path)
        except json.JSONDecodeError as error:
            raise ReadError(f"{path}: {error}") from error
    if suffix == ".php":
        return from_lines(text, path, PHP_ENTRY)
    if suffix in (".yaml", ".yml"):
        return from_lines(text, path, YAML_ENTRY)
    raise ReadError(f"{path}: no reader for {suffix}")


def read_design(path: pathlib.Path):
    try:
        parser = DesignText()
        parser.feed(path.read_text(encoding="utf-8"))
        return [normalise(t) for t in parser.texts if normalise(t)]
    except (OSError, UnicodeDecodeError) as error:
        raise ReadError(f"{path}: {error}") from error


def read_approved(path):
    if not path or not pathlib.Path(path).exists():
        return {}
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReadError(f"{path}: {error}") from error
    if isinstance(data, list):
        return {normalise(str(t)): "" for t in data}
    if isinstance(data, dict):
        return {normalise(str(k)): (v if isinstance(v, str) else "").strip()
                for k, v in data.items()}
    raise ReadError(f"{path}: expected an object of text and origin")


# --------------------------------------------------------------------------
# Checking
# --------------------------------------------------------------------------

def matches_with_placeholder(text, approved):
    """A text with a placeholder cannot be compared literally: the design
    shows "Hallo Max", the language file "Hallo {name}"."""
    pattern, last = "", 0
    for found in PLACEHOLDER.finditer(text):
        pattern += re.escape(text[last:found.start()]) + ".+?"
        last = found.end()
    pattern += re.escape(text[last:])
    try:
        rule = re.compile(f"^{pattern}$")
    except re.error:
        return False
    return any(rule.match(candidate) for candidate in approved)


def check(entries, approved):
    findings, without_origin, promises = [], [], []
    known = set(approved)

    for path, line, key, raw in entries:
        text = normalise(raw)
        if not text:
            continue

        for pattern, what in PROMISE:
            if pattern.search(text):
                promises.append((path, line, key, text, what))
                break

        if not approved:
            continue
        if text in known:
            if not approved[text]:
                without_origin.append((path, line, key, text))
            continue
        if PLACEHOLDER.search(text) and matches_with_placeholder(text, known):
            continue
        near = difflib.get_close_matches(text, known, n=1, cutoff=0.82)
        findings.append((path, line, key, text, near[0] if near else None))

    return findings, without_origin, promises


def shorten(text, width=58):
    return text if len(text) <= width else text[:width - 1] + "…"


def print_report(findings, without_origin, promises, entries, approved,
                 errors, approved_path):
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if not approved:
        print("ui-text-check: no approved stock given — only the promises "
              "below were looked at.\n")
    elif findings:
        print(f"ui-text-check: {len(findings)} "
              f"{'text' if len(findings) == 1 else 'texts'} without an "
              f"origin\n")
        current = None
        for path, line, key, text, near in findings:
            if path != current:
                print(f"{path}")
                current = path
            place = f"{line:>5}  " if line else "       "
            print(f"{place}{key}")
            print(f"       \"{shorten(text)}\"")
            if near:
                print(f"       closest approved: \"{shorten(near)}\"")
        print()
    elif without_origin:
        print(f"ui-text-check: {len(without_origin)} approved without an "
              f"origin\n")
    else:
        print("ui-text-check: every text has an origin\n")

    if without_origin:
        print(f"Listed as approved but without an origin — that does not "
              f"count ({len(without_origin)}):")
        for path, line, key, text in without_origin:
            print(f"  {key}: \"{shorten(text)}\"")
        print()

    if promises:
        print(f"Promises about the system, to be proven against the code "
              f"({len(promises)}):")
        for path, line, key, text, what in promises:
            print(f"  {key} — {what}")
            print(f"    \"{shorten(text)}\"")
        print()

    print(f"Checked {len(entries)} texts against "
          f"{len(approved)} approved "
          f"{'entry' if len(approved) == 1 else 'entries'}"
          f"{f' ({approved_path})' if approved_path else ''}.")


def accept(path, approved, findings):
    """Writes the found texts into the stock with an EMPTY origin. That is
    deliberate: the run stays red until somebody fills the origin in. The
    switch collects the texts for the decision, it does not make it."""
    approved = dict(approved)
    for _, _, _, text, _ in findings:
        approved.setdefault(text, "")
    pathlib.Path(path).write_text(
        json.dumps(dict(sorted(approved.items())), ensure_ascii=False,
                   indent=2) + "\n", encoding="utf-8")
    count = len(findings)
    print(f"\n{count} {'text' if count == 1 else 'texts'} written into "
          f"{path} — without an origin.")
    print("The check stays red until each one carries where it comes from: "
          "artboard, ticket, or an instruction. Filling that in is the "
          "project owner's decision, not the agent's.")


def collect(paths, source_language):
    files, errors = [], []
    for raw in paths:
        path = pathlib.Path(raw)
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if not candidate.is_file():
                    continue
                if candidate.suffix.lower() not in LANGUAGE_SUFFIXES:
                    continue
                if source_language and candidate.stem != source_language:
                    continue
                files.append(candidate)
        elif path.is_file():
            files.append(path)
        else:
            errors.append(f"{path}: not found")
    return files, errors


def main():
    parser = argparse.ArgumentParser(
        description="Checks that every visible text has an approved origin, "
                    "and lists the texts that promise something about the "
                    "system.")
    parser.add_argument("paths", nargs="+",
                        help="language files or directories")
    parser.add_argument("--approved",
                        help="JSON file of approved text and its origin")
    parser.add_argument("--design", action="append", default=[],
                        help="design export whose texts count as approved; "
                             "may be given more than once")
    parser.add_argument("--source-language",
                        help="when a directory is given, read only this "
                             "language, e.g. de")
    parser.add_argument("--accept", action="store_true",
                        help="write the found texts into the approved file "
                             "with an empty origin, for the decision; the "
                             "check stays red until each origin is filled in")
    parser.add_argument("--report", help="write the findings as JSON")
    args = parser.parse_args()

    files, errors = collect(args.paths, args.source_language)
    try:
        approved = read_approved(args.approved)
    except ReadError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    for export in args.design:
        try:
            for text in read_design(pathlib.Path(export)):
                approved.setdefault(text, f"Entwurf: {export}")
        except ReadError as error:
            errors.append(str(error))

    entries = []
    for path in files:
        try:
            entries += read_language(path)
        except ReadError as error:
            errors.append(str(error))

    findings, without_origin, promises = check(entries, approved)
    print_report(findings, without_origin, promises, entries, approved,
                 errors, args.approved)

    if args.accept and args.approved and findings:
        accept(args.approved, approved, findings)

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"checked": len(entries), "approved": len(approved),
                        "findings": [{"file": str(p), "line": l, "key": k,
                                      "text": t, "closest": n}
                                     for p, l, k, t, n in findings],
                        "promises": [{"file": str(p), "line": l, "key": k,
                                      "text": t, "kind": w}
                                     for p, l, k, t, w in promises]},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    if errors:
        return 2
    return 1 if (findings or without_origin) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
