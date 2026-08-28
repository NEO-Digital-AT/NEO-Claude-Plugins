#!/usr/bin/env python3
"""Checks the translations for completeness.

Compares the language files of a project against the source language and
reports what is missing, empty, left untranslated or deviating in its
placeholders. The last case is the most dangerous one: a placeholder that
is missing in one language is not a blemish but a runtime error, or a
message with a hole in it.

Read are:

    JSON and ARB     .json, .arb            nested or flat
    PHP return       .php                   return [ 'a' => 'b', ... ]
    Flat YAML        .yaml, .yml            key: value, by indentation

No dependencies, so the script runs in any CI.

    translations.py lang/ --source-language en
    translations.py app/locales --source-language en --languages de,fr,it
    translations.py lang/ --source-language en --sources app/,resources/
    translations.py lang/ --source-language en --report report.json

Exit code 0 when there are no findings, 1 on findings, 2 on read errors.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Placeholders of the common frameworks. They have to appear the same way in
# every language — otherwise a value is missing from the sentence, or the
# formatting breaks.
PLACEHOLDER = re.compile(
    r"\{\{\s*[\w.]+\s*\}\}"          # {{ name }}       Vue, Angular, Blade
    r"|\{[\w.]+\}"                    # {name}           ICU, Flutter, .NET
    r"|:[a-zA-Z_]\w*"                 # :name            Laravel
    r"|%\d+\$[sd]"                    # %1$s             positional
    r"|%[sd]"                         # %s               C style
    r"|#\{[\w.]+\}"                   # #{name}
)

# Values that legitimately read the same in more than one language.
SAME_ALLOWED = {
    "ok", "e-mail", "email", "info", "status", "url", "id", "pdf", "csv",
    "json", "xml", "api", "web", "app", "server", "client", "login",
    "logout", "import", "export", "start", "stop", "reset", "admin",
    "n/a", "-", "…", "%", "€", "$",
}

ICU_PLURAL = re.compile(r"\{\s*\w+\s*,\s*(plural|select|selectordinal)\s*,", re.I)


class ReadError(Exception):
    pass


# --------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------

def flatten(tree, prefix: str = "") -> dict[str, str]:
    """Turns a nested structure into dotted keys."""
    flat: dict[str, str] = {}
    if isinstance(tree, dict):
        for key, value in tree.items():
            if key.startswith("@"):             # ARB metadata, not text
                continue
            full = f"{prefix}.{key}" if prefix else str(key)
            flat.update(flatten(value, full))
    elif isinstance(tree, list):
        for i, value in enumerate(tree):
            flat.update(flatten(value, f"{prefix}[{i}]"))
    else:
        flat[prefix] = "" if tree is None else str(tree)
    return flat


def read_json(path: pathlib.Path) -> dict[str, str]:
    try:
        return flatten(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as error:
        raise ReadError(f"{path}: not valid JSON — {error}")


PHP_ENTRY = re.compile(
    r"""(['"])(?P<key>(?:\\.|(?!\1).)*)\1\s*=>\s*"""
    r"""(?:(['"])(?P<value>(?:\\.|(?!\3).)*)\3|(?P<opens>\[))""",
    re.S,
)


def read_php(path: pathlib.Path) -> dict[str, str]:
    """Reads a PHP language file of the form return [ 'a' => 'b', 'c' => [ ... ] ].

    Deliberately kept simple. What cannot be read reliably is reported —
    not guessed.
    """
    text = path.read_text(encoding="utf-8")
    if "return" not in text:
        raise ReadError(f"{path}: no `return` array found")

    result: dict[str, str] = {}
    path_parts: list[str] = []
    depth_at: list[int] = []
    depth = 0
    i = 0
    while i < len(text):
        match = PHP_ENTRY.search(text, i)
        closing = text.find("]", i)
        if match and (closing == -1 or match.start() < closing):
            key = match.group("key")
            if match.group("opens"):
                path_parts.append(key)
                depth += 1
                depth_at.append(depth)
            else:
                full = ".".join(path_parts + [key])
                result[full] = (match.group("value") or "").replace("\\'", "'")
            i = match.end()
        elif closing != -1:
            if depth_at and depth == depth_at[-1]:
                depth_at.pop()
                if path_parts:
                    path_parts.pop()
                depth -= 1
            i = closing + 1
        else:
            break

    if not result:
        raise ReadError(f"{path}: no readable entries")
    return result


def read_yaml(path: pathlib.Path) -> dict[str, str]:
    """Flat YAML by indentation. Anchors, lists and blocks are out of reach."""
    result: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("-") or "<<:" in line or "&" in line.split(":")[0]:
            raise ReadError(
                f"{path}:{number}: this reader cannot do lists and anchors — "
                f"please check the file as JSON"
            )
        indent = len(line) - len(line.lstrip())
        if ":" not in line:
            continue
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"').strip("'")
        while stack and stack[-1][0] >= indent:
            stack.pop()
        full = ".".join([s[1] for s in stack] + [key.strip()])
        if value == "":
            stack.append((indent, key.strip()))
        else:
            result[full] = value
    return result


READERS = {".json": read_json, ".arb": read_json, ".php": read_php,
           ".yaml": read_yaml, ".yml": read_yaml}


def read_language(root: pathlib.Path, language: str) -> tuple[dict[str, str], list[str]]:
    """Collects all language files of one language — as a file or as a folder."""
    entries: dict[str, str] = {}
    errors: list[str] = []
    candidates: list[pathlib.Path] = []

    folder = root / language
    if folder.is_dir():
        candidates = sorted(p for p in folder.rglob("*") if p.suffix in READERS)
        prefix_from = folder
    else:
        candidates = sorted(p for p in root.glob(language + ".*") if p.suffix in READERS)
        candidates += sorted(p for p in root.rglob("*")
                             if p.suffix in READERS and p.stem == language)
        prefix_from = None

    for path in dict.fromkeys(candidates):
        try:
            part = READERS[path.suffix](path)
        except ReadError as error:
            errors.append(str(error))
            continue
        if prefix_from is not None:
            relative = path.relative_to(prefix_from).with_suffix("")
            group = ".".join(relative.parts)
            part = {f"{group}.{k}": v for k, v in part.items()}
        entries.update(part)

    return entries, errors


# --------------------------------------------------------------------------
# Comparing
# --------------------------------------------------------------------------

def placeholders(text: str) -> list[str]:
    return sorted(m.group(0) for m in PLACEHOLDER.finditer(text))


def compare(source: dict[str, str], source_name: str,
            others: dict[str, dict[str, str]]) -> list[dict]:
    findings: list[dict] = []

    for language, entries in others.items():
        for key, source_value in source.items():
            value = entries.get(key)

            if value is None:
                findings.append({"kind": "missing", "language": language,
                                 "key": key, "what": "key is missing",
                                 "text": source_value[:60]})
                continue

            if not value.strip():
                findings.append({"kind": "empty", "language": language,
                                 "key": key, "what": "value is empty",
                                 "text": source_value[:60]})
                continue

            if (value.strip() == source_value.strip()
                    and value.strip().lower() not in SAME_ALLOWED
                    and len(value.strip()) > 3
                    and not value.strip().isdigit()):
                findings.append({"kind": "untranslated", "language": language,
                                 "key": key,
                                 "what": f"same as {source_name}",
                                 "text": value[:60]})

            a, b = placeholders(source_value), placeholders(value)
            if a != b:
                missing = [p for p in a if p not in b]
                surplus = [p for p in b if p not in a]
                parts = []
                if missing:
                    parts.append("missing " + ", ".join(missing))
                if surplus:
                    parts.append("surplus " + ", ".join(surplus))
                findings.append({"kind": "placeholder", "language": language,
                                 "key": key,
                                 "what": "; ".join(parts), "text": value[:60]})

            if ICU_PLURAL.search(source_value) and not ICU_PLURAL.search(value):
                findings.append({"kind": "plural", "language": language,
                                 "key": key,
                                 "what": f"{source_name} has a plural form, this language does not",
                                 "text": value[:60]})

        for key in entries:
            if key not in source:
                findings.append({"kind": "orphan", "language": language,
                                 "key": key,
                                 "what": f"not present in {source_name}",
                                 "text": entries[key][:60]})

    return findings


KEY_IN_CODE = re.compile(r"""['"`]([a-zA-Z][\w.\-]*(?:\.[\w\-]+)+)['"`]""")


def dead_keys(source: dict[str, str], sources: list[pathlib.Path]) -> list[dict]:
    """Keys that appear nowhere in the source code. Heuristic."""
    used: set[str] = set()
    suffixes = {".vue", ".ts", ".js", ".tsx", ".jsx", ".php", ".dart", ".cs",
                ".html", ".twig", ".blade.php"}
    for root in sources:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            used.update(KEY_IN_CODE.findall(text))

    findings = []
    for key in source:
        if key in used:
            continue
        # Allow a partial path as well: groups are often built dynamically.
        if any(key.startswith(u + ".") or u.startswith(key + ".") for u in used):
            continue
        findings.append({"kind": "dead", "language": "—", "key": key,
                         "what": "not found in the source code (suspected)",
                         "text": source[key][:60]})
    return findings


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def count(number: int, singular: str, plural: str | None = None) -> str:
    """Number with its noun, so the report reads like a sentence."""
    return f"{number} {singular if number == 1 else (plural or singular + 's')}"


KIND_NAMES = {
    "missing": "Key is missing",
    "empty": "Value is empty",
    "placeholder": "Placeholder deviates",
    "plural": "Plural form is missing",
    "untranslated": "Left untranslated",
    "orphan": "Orphaned key",
    "dead": "Key without a use (suspected)",
}
ORDER = ["missing", "placeholder", "empty", "plural", "untranslated", "orphan", "dead"]


def print_report(findings: list[dict], source: dict[str, str], source_name: str,
                 others: dict[str, dict[str, str]], limit: int) -> None:
    print(f"Translation check — source language {source_name} "
          f"with {count(len(source), 'key')}\n")

    for language in sorted(others):
        own = [f for f in findings if f["language"] == language]
        gaps = sum(1 for f in own if f["kind"] in ("missing", "empty"))
        coverage = 100.0 * (len(source) - gaps) / len(source) if source else 100.0
        marker = "OK  " if not own else "FAIL"
        keys = f"{len(others[language]):>5} " + ("key " if len(others[language]) == 1 else "keys")
        print(f"  {marker}  {language:<6} {keys}"
              f"   coverage {coverage:5.1f} %   {count(len(own), 'finding')}")

    if not findings:
        print("\nPassed. Every key in every language, placeholders match.")
        return

    print(f"\n{count(len(findings), 'finding')}:")
    for kind in ORDER:
        part = [f for f in findings if f["kind"] == kind]
        if not part:
            continue
        print(f"\n  {KIND_NAMES[kind]} ({len(part)}):")
        for f in part[:limit]:
            print(f"    [{f['language']}] {f['key']}")
            print(f"           {f['what']}" + (f'  "{f["text"]}"' if f["text"] else ""))
        if len(part) > limit:
            print(f"    … and {len(part) - limit} more")

    blocking = [f for f in findings
                if f["kind"] in ("missing", "empty", "placeholder", "plural")]
    print(f"\n{len(blocking)} of them "
          f"{'is a blocker' if len(blocking) == 1 else 'are blockers'} "
          f"(missing, empty, placeholder, plural).")
    if any(f["kind"] == "placeholder" for f in findings):
        print("Deviating placeholders first: they break at runtime or leave "
              "a hole in the sentence.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check the translations for completeness.",
        epilog="Reads JSON, ARB, PHP return arrays and flat YAML.",
    )
    parser.add_argument("root", help="folder holding the language files")
    parser.add_argument("--source-language", required=True, help="for example en")
    parser.add_argument("--languages", help="comma separated; detected automatically if omitted")
    parser.add_argument("--sources", help="comma separated folders, for dead keys")
    parser.add_argument("--limit", type=int, default=15, help="lines per kind of finding")
    parser.add_argument("--report", help="additionally write the result as JSON")
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2

    if args.languages:
        languages = [s.strip() for s in args.languages.split(",") if s.strip()]
    else:
        languages = sorted({p.name for p in root.iterdir() if p.is_dir()}
                           | {p.stem for p in root.glob("*") if p.suffix in READERS})
    languages = [s for s in languages if s != args.source_language]

    source, errors = read_language(root, args.source_language)
    if not source:
        print(f"No entries for the source language {args.source_language} in {root}.",
              file=sys.stderr)
        for error in errors:
            print("  " + error, file=sys.stderr)
        return 2
    if not languages:
        print(f"No further languages besides {args.source_language} found.",
              file=sys.stderr)
        return 2

    others: dict[str, dict[str, str]] = {}
    for language in languages:
        others[language], part = read_language(root, language)
        errors += part

    for error in errors:
        print("Read error: " + error, file=sys.stderr)

    findings = compare(source, args.source_language, others)
    if args.sources:
        sources = [pathlib.Path(s.strip()) for s in args.sources.split(",")]
        findings += dead_keys(source, [s for s in sources if s.is_dir()])

    print_report(findings, source, args.source_language, others, args.limit)

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"source_language": args.source_language,
                        "keys": len(source), "findings": findings},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if (findings or errors) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
