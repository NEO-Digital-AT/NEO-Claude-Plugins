#!/usr/bin/env python3
"""Inventory of an assistant prompt.

Measures a system prompt that has grown over time and names what makes it
hard to change. The script does not judge the content — it counts, finds
patterns and names the places with a line number. What follows from that
is for a human to decide.

It looks for the four causes large prompts fail on:

  1. Keyword branching — words of natural language steer the flow. Breaks
     with every new language.
  2. Embedded schemas — JSON blocks and field lists in prose instead of
     in the tool schema, where they would be enforced.
  3. Repetition — the same instruction more than once, often slightly
     different. Change one and the other one works against you.
  4. Size — sections too large to still be honoured.

The patterns below match German and English wording, because the prompts
being measured are usually not written in English.

No dependencies, so the script runs in any CI.

    prompt-inventory.py prompts/assistant.md
    prompt-inventory.py prompts/*.md --max-lines 100
    prompt-inventory.py prompts/assistant.md --report inventory.json

Exit code 0 when there are no findings, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Characters per token — a rough approximation, for the order of magnitude only.
CHARS_PER_TOKEN = 4

# Branching on natural language. Deliberately narrow: what is looked for is a
# condition that rests on the wording of the user's input.
KEYWORD_BRANCH = [
    (re.compile(r"\bwenn\s+(der|die|das)\s+(benutzer|nutzer|kunde|gast|anwender)\b", re.I),
     "branch in prose"),
    (re.compile(r"\bsagt\s+(der|die|das)\s+(benutzer|nutzer|kunde|gast)\b", re.I),
     "branch in prose"),
    (re.compile(r"\bif\s+the\s+(user|customer|guest|client)\s+(says|writes|asks|mentions|types|wants)\b", re.I),
     "branch in prose"),
    (re.compile(r"\b(enthält|enthaelt)\b.{0,40}?\b(das\s+)?(wort|begriff|schlüsselwort|schluesselwort)\b", re.I),
     "condition on a word"),
    (re.compile(r"\bcontains?\b.{0,40}?\b(the\s+)?(word|term|keyword|phrase)\b", re.I),
     "condition on a word"),
    (re.compile(r"\b(schlüsselwörter|schluesselwoerter|keywords?|trigger\s*words?)\b\s*:", re.I),
     "list of keywords"),
    (re.compile(r"\b(bei|for)\s+(den\s+)?(wörtern|woertern|words)\b", re.I),
     "condition on words"),
]

# A branch that also quotes the wording is the harder case: it is guaranteed
# to break with the next language.
QUOTED_WORDING = re.compile(r"[\"„“«‘’\']\s*\w{3,}\s*[\"“”»‘’\']")

# Instructions aiming at a tool call — used for the size measurement.
TOOL_HINT = re.compile(
    r"\b(rufe?\s+\w*\s*(das\s+)?werkzeug|use\s+the\s+tool|call\s+the\s+tool|verwende\s+(das\s+)?werkzeug|tool\s*:)\b",
    re.I,
)

PROHIBITION = re.compile(r"\b(nie|niemals|never|nicht|do\s+not|don't|kein|keine)\b", re.I)
OBLIGATION = re.compile(r"\b(immer|always|muss|müssen|muessen|must|stets)\b", re.I)


def normalise(line: str) -> str:
    """For the repetition comparison: drop punctuation, case and list markers.

    German letters are kept, because the prompts being measured are often
    German and would otherwise be cut apart at every umlaut.
    """
    t = line.strip().lower()
    t = re.sub(r"^[-*\d.)\s]+", "", t)
    t = re.sub(r"[^\wäöüß ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def split_sections(lines: list[str]) -> list[dict]:
    """Splits at Markdown headings; without headings one section remains."""
    sections: list[dict] = []
    current = {"title": "(no heading)", "from_line": 1, "lines": []}
    for number, line in enumerate(lines, 1):
        if re.match(r"^#{1,6}\s+\S", line):
            if current["lines"]:
                sections.append(current)
            current = {"title": line.strip("# ").strip(), "from_line": number, "lines": []}
        current["lines"].append(line)
    sections.append(current)
    return sections


def measure_file(path: pathlib.Path, max_lines: int) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    content = [line for line in lines if line.strip()]

    findings: list[dict] = []

    # 1. Keyword branching.
    for number, line in enumerate(lines, 1):
        for pattern, what in KEYWORD_BRANCH:
            if pattern.search(line):
                if what == "branch in prose" and QUOTED_WORDING.search(line):
                    what = "branch on quoted wording"
                findings.append({
                    "kind": "keyword-branch",
                    "line": number,
                    "what": what,
                    "text": line.strip()[:100],
                })
                break

    # 2. Embedded schemas.
    inside = False
    block_start = 0
    block_language = ""
    for number, line in enumerate(lines, 1):
        fence = re.match(r"^\s*```(\w*)", line)
        if fence and not inside:
            inside, block_start, block_language = True, number, fence.group(1).lower()
        elif fence and inside:
            inside = False
            if block_language in ("json", "jsonc", "yaml", "yml", "ts", "typescript"):
                length = number - block_start - 1
                findings.append({
                    "kind": "schema-in-prose",
                    "line": block_start,
                    "what": "%s block over %s"
                            % (block_language.upper(),
                               "1 line" if length == 1 else f"{length} lines"),
                    "text": "belongs in the tool schema, where it is enforced",
                })

    # 3. Repetition.
    seen: dict[str, list[int]] = {}
    for number, line in enumerate(lines, 1):
        normalised = normalise(line)
        if len(normalised) < 25:     # short lines repeat harmlessly
            continue
        seen.setdefault(normalised, []).append(number)
    for normalised, places in seen.items():
        if len(places) > 1:
            findings.append({
                "kind": "repetition",
                "line": places[0],
                "what": f"{len(places)}x word for word, also line "
                        + ", ".join(str(p) for p in places[1:]),
                "text": normalised[:100],
            })

    # 4. Size per section.
    sections = []
    for section in split_sections(lines):
        filled = [line for line in section["lines"] if line.strip()]
        sections.append({
            "title": section["title"],
            "from_line": section["from_line"],
            "lines": len(filled),
        })
        if len(filled) > max_lines:
            findings.append({
                "kind": "section-too-large",
                "line": section["from_line"],
                "what": f"{len(filled)} lines (limit {max_lines})",
                "text": section["title"],
            })

    return {
        "file": str(path),
        "lines": len(lines),
        "content_lines": len(content),
        "characters": len(text),
        "tokens_estimated": len(text) // CHARS_PER_TOKEN,
        "sections": sections,
        "obligations": sum(1 for line in content if OBLIGATION.search(line)),
        "prohibitions": sum(1 for line in content if PROHIBITION.search(line)),
        "tool_hints": sum(1 for line in content if TOOL_HINT.search(line)),
        "findings": findings,
    }


KIND_NAMES = {
    "keyword-branch": "Keyword branching",
    "schema-in-prose": "Schema in the prose",
    "repetition": "Repeated instruction",
    "section-too-large": "Section too large",
}

KIND_ORDER = ["keyword-branch", "schema-in-prose", "repetition", "section-too-large"]


def print_report(measurements: list[dict], max_lines: int) -> None:
    for m in measurements:
        print(f"\n{m['file']}")
        print(
            f"  {m['lines']} lines, {m['content_lines']} of them with content · "
            f"{m['characters']} characters · roughly {m['tokens_estimated']} tokens"
        )
        print(
            f"  {m['obligations']} lines with an obligation, {m['prohibitions']} "
            f"with a prohibition, {m['tool_hints']} with a tool hint"
        )

        if len(m["sections"]) > 1:
            print("\n  Sections:")
            for s in sorted(m["sections"], key=lambda x: -x["lines"]):
                marker = "  <<" if s["lines"] > max_lines else ""
                print(f"    {s['lines']:4}  L{s['from_line']:<5} {s['title'][:56]}{marker}")

        if not m["findings"]:
            print("\n  No findings.")
            continue

        total = len(m["findings"])
        print(f"\n  {total} finding{'' if total == 1 else 's'}:")
        for kind in KIND_ORDER:
            part = [f for f in m["findings"] if f["kind"] == kind]
            if not part:
                continue
            print(f"\n  {KIND_NAMES[kind]} ({len(part)}):")
            for f in sorted(part, key=lambda x: x["line"]):
                print(f"    L{f['line']:<5} {f['what']}")
                print(f"           {f['text']}")

    total = sum(len(m["findings"]) for m in measurements)
    print()
    if total:
        per_kind = {
            kind: sum(1 for m in measurements for f in m["findings"] if f["kind"] == kind)
            for kind in KIND_ORDER
        }
        print(
            "In total "
            + ", ".join(f"{per_kind[k]}x {KIND_NAMES[k]}" for k in KIND_ORDER if per_kind[k])
            + "."
        )
        if per_kind["keyword-branch"]:
            print(
                "Keyword branching is the heaviest finding: it breaks with "
                "every new language."
            )
    else:
        print("No findings.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure an assistant prompt.",
        epilog="The script counts and finds patterns. It does not judge — "
               "what follows from that is for a human to decide.",
    )
    parser.add_argument("files", nargs="+", help="prompt files")
    parser.add_argument("--max-lines", type=int, default=80,
                        help="line limit per section (default 80)")
    parser.add_argument("--report", help="additionally write the result as JSON")
    args = parser.parse_args()

    measurements = []
    for name in args.files:
        path = pathlib.Path(name)
        if not path.is_file():
            print(f"Cannot be read: {path}", file=sys.stderr)
            return 2
        measurements.append(measure_file(path, args.max_lines))

    print_report(measurements, args.max_lines)

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps(measurements, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return 1 if any(m["findings"] for m in measurements) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
