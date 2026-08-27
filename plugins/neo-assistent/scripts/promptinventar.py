#!/usr/bin/env python3
"""Inventar eines Assistenten-Prompts.

Misst einen gewachsenen Systemprompt und benennt, was ihn schwer
änderbar macht. Das Skript urteilt nicht über Inhalte — es zählt, findet
Muster und nennt Fundstellen mit Zeilennummer. Was daraus folgt,
entscheidet ein Mensch.

Gesucht wird nach den vier Ursachen, an denen große Prompts scheitern:

  1. Schlüsselwort-Verzweigung — natürlichsprachige Wörter steuern den
     Ablauf. Bricht bei jeder neuen Sprache.
  2. Eingebettete Schemata — JSON-Blöcke und Feldlisten in Prosa statt
     im Werkzeugschema, wo sie erzwungen würden.
  3. Wiederholung — dieselbe Anweisung mehrfach, oft leicht abweichend.
     Wer eine ändert, hat die andere gegen sich.
  4. Größe — Abschnitte, die zu groß sind, um noch beachtet zu werden.

Ohne Abhängigkeiten, damit das Skript in jeder CI läuft.

    promptinventar.py prompts/assistent.md
    promptinventar.py prompts/*.md --breite 100
    promptinventar.py prompts/assistent.md --bericht inventar.json

Rückgabewert 0, wenn keine Befunde, sonst 1.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Zeichen je Wortmarke — grobe Näherung, nur zur Größenordnung.
ZEICHEN_JE_MARKE = 4

# Verzweigung an natürlicher Sprache. Absichtlich eng gefasst: gesucht wird
# eine Bedingung, die auf dem Wortlaut der Benutzereingabe steht.
SCHLUESSELWORT = [
    (re.compile(r"\bwenn\s+(der|die|das)\s+(benutzer|nutzer|kunde|gast|anwender)\b", re.I),
     "Verzweigung in Prosa"),
    (re.compile(r"\bsagt\s+(der|die|das)\s+(benutzer|nutzer|kunde|gast)\b", re.I),
     "Verzweigung in Prosa"),
    (re.compile(r"\bif\s+the\s+(user|customer|guest|client)\s+(says|writes|asks|mentions|types|wants)\b", re.I),
     "Verzweigung in Prosa"),
    (re.compile(r"\b(enthält|enthaelt)\b.{0,40}?\b(das\s+)?(wort|begriff|schlüsselwort|schluesselwort)\b", re.I),
     "Bedingung auf einem Wort"),
    (re.compile(r"\bcontains?\b.{0,40}?\b(the\s+)?(word|term|keyword|phrase)\b", re.I),
     "Bedingung auf einem Wort"),
    (re.compile(r"\b(schlüsselwörter|schluesselwoerter|keywords?|trigger\s*words?)\b\s*:", re.I),
     "Liste von Schlüsselwörtern"),
    (re.compile(r"\b(bei|for)\s+(den\s+)?(wörtern|woertern|words)\b", re.I),
     "Bedingung auf Wörtern"),
]

# Eine Verzweigung, die zusätzlich einen Wortlaut zitiert, ist der härtere Fall:
# sie bricht garantiert bei der nächsten Sprache.
WORTLAUT = re.compile(r"[\"\u201e\u201c\u00ab\u2018\u2019\']\s*\w{3,}\s*[\"\u201c\u201d\u00bb\u2018\u2019\']")

# Anweisungen, die auf einen Werkzeugaufruf zielen — dienen der Größenmessung.
WERKZEUGHINWEIS = re.compile(
    r"\b(rufe?\s+\w*\s*(das\s+)?werkzeug|use\s+the\s+tool|call\s+the\s+tool|verwende\s+(das\s+)?werkzeug|tool\s*:)\b",
    re.I,
)

VERBOT = re.compile(r"\b(nie|niemals|never|nicht|do\s+not|don't|kein|keine)\b", re.I)
GEBOT = re.compile(r"\b(immer|always|muss|müssen|muessen|must|stets)\b", re.I)


def normalisieren(zeile: str) -> str:
    """Für den Wiederholungsvergleich: Satzzeichen, Fall und Aufzählungsmarken weg."""
    t = zeile.strip().lower()
    t = re.sub(r"^[-*\d.)\s]+", "", t)
    t = re.sub(r"[^\wäöüß ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def abschnitte_schneiden(zeilen: list[str]) -> list[dict]:
    """Teilt an Markdown-Überschriften; ohne Überschriften bleibt ein Abschnitt."""
    abschnitte: list[dict] = []
    aktuell = {"titel": "(ohne Überschrift)", "ab": 1, "zeilen": []}
    for nr, zeile in enumerate(zeilen, 1):
        if re.match(r"^#{1,6}\s+\S", zeile):
            if aktuell["zeilen"]:
                abschnitte.append(aktuell)
            aktuell = {"titel": zeile.strip("# ").strip(), "ab": nr, "zeilen": []}
        aktuell["zeilen"].append(zeile)
    abschnitte.append(aktuell)
    return abschnitte


def datei_messen(pfad: pathlib.Path, breite: int) -> dict:
    text = pfad.read_text(encoding="utf-8")
    zeilen = text.split("\n")
    inhalt = [z for z in zeilen if z.strip()]

    befunde: list[dict] = []

    # 1. Schlüsselwort-Verzweigung.
    for nr, zeile in enumerate(zeilen, 1):
        for muster, was in SCHLUESSELWORT:
            if muster.search(zeile):
                if was == "Verzweigung in Prosa" and WORTLAUT.search(zeile):
                    was = "Verzweigung am zitierten Wortlaut"
                befunde.append({
                    "art": "schluesselwort",
                    "zeile": nr,
                    "was": was,
                    "text": zeile.strip()[:100],
                })
                break

    # 2. Eingebettete Schemata.
    in_block = False
    blockstart = 0
    blocksprache = ""
    for nr, zeile in enumerate(zeilen, 1):
        zaun = re.match(r"^\s*```(\w*)", zeile)
        if zaun and not in_block:
            in_block, blockstart, blocksprache = True, nr, zaun.group(1).lower()
        elif zaun and in_block:
            in_block = False
            if blocksprache in ("json", "jsonc", "yaml", "yml", "ts", "typescript"):
                befunde.append({
                    "art": "schema_im_prompt",
                    "zeile": blockstart,
                    "was": "%s-Block über %s"
                             % (blocksprache.upper(),
                                "1 Zeile" if nr - blockstart - 1 == 1
                                else f"{nr - blockstart - 1} Zeilen"),
                    "text": "gehört ins Werkzeugschema, wo es erzwungen wird",
                })

    # 3. Wiederholung.
    gesehen: dict[str, list[int]] = {}
    for nr, zeile in enumerate(zeilen, 1):
        norm = normalisieren(zeile)
        if len(norm) < 25:          # kurze Zeilen wiederholen sich harmlos
            continue
        gesehen.setdefault(norm, []).append(nr)
    for norm, stellen in gesehen.items():
        if len(stellen) > 1:
            befunde.append({
                "art": "wiederholung",
                "zeile": stellen[0],
                "was": f"{len(stellen)}× wortgleich, auch Zeile "
                       + ", ".join(str(s) for s in stellen[1:]),
                "text": norm[:100],
            })

    # 4. Größe je Abschnitt.
    abschnitte = []
    for a in abschnitte_schneiden(zeilen):
        gefuellt = [z for z in a["zeilen"] if z.strip()]
        abschnitte.append({
            "titel": a["titel"],
            "ab": a["ab"],
            "zeilen": len(gefuellt),
        })
        if len(gefuellt) > breite:
            befunde.append({
                "art": "abschnitt_zu_gross",
                "zeile": a["ab"],
                "was": f"{len(gefuellt)} Zeilen (Grenze {breite})",
                "text": a["titel"],
            })

    return {
        "datei": str(pfad),
        "zeilen": len(zeilen),
        "zeilen_inhalt": len(inhalt),
        "zeichen": len(text),
        "marken_geschaetzt": len(text) // ZEICHEN_JE_MARKE,
        "abschnitte": abschnitte,
        "gebote": sum(1 for z in inhalt if GEBOT.search(z)),
        "verbote": sum(1 for z in inhalt if VERBOT.search(z)),
        "werkzeughinweise": sum(1 for z in inhalt if WERKZEUGHINWEIS.search(z)),
        "befunde": befunde,
    }


ARTNAME = {
    "schluesselwort": "Schlüsselwort-Verzweigung",
    "schema_im_prompt": "Schema in der Prosa",
    "wiederholung": "Wiederholte Anweisung",
    "abschnitt_zu_gross": "Abschnitt zu groß",
}

ARTFOLGE = ["schluesselwort", "schema_im_prompt", "wiederholung", "abschnitt_zu_gross"]


def bericht_drucken(messungen: list[dict], breite: int) -> None:
    for m in messungen:
        print(f"\n{m['datei']}")
        print(
            f"  {m['zeilen']} Zeilen, davon {m['zeilen_inhalt']} mit Inhalt · "
            f"{m['zeichen']} Zeichen · grob {m['marken_geschaetzt']} Wortmarken"
        )
        print(
            f"  {m['gebote']} Zeilen mit Gebot, {m['verbote']} mit Verbot, "
            f"{m['werkzeughinweise']} mit Werkzeughinweis"
        )

        if len(m["abschnitte"]) > 1:
            print("\n  Abschnitte:")
            for a in sorted(m["abschnitte"], key=lambda x: -x["zeilen"]):
                marke = "  <<" if a["zeilen"] > breite else ""
                print(f"    {a['zeilen']:4}  Z{a['ab']:<5} {a['titel'][:56]}{marke}")

        if not m["befunde"]:
            print("\n  Keine Befunde.")
            continue

        print(f"\n  {len(m['befunde'])} Befunde:")
        for art in ARTFOLGE:
            teil = [b for b in m["befunde"] if b["art"] == art]
            if not teil:
                continue
            print(f"\n  {ARTNAME[art]} ({len(teil)}):")
            for b in sorted(teil, key=lambda x: x["zeile"]):
                print(f"    Z{b['zeile']:<5} {b['was']}")
                print(f"           {b['text']}")

    gesamt = sum(len(m["befunde"]) for m in messungen)
    print()
    if gesamt:
        je_art = {
            a: sum(1 for m in messungen for b in m["befunde"] if b["art"] == a)
            for a in ARTFOLGE
        }
        print(
            "Gesamt "
            + ", ".join(f"{je_art[a]}× {ARTNAME[a]}" for a in ARTFOLGE if je_art[a])
            + "."
        )
        if je_art["schluesselwort"]:
            print(
                "Schlüsselwort-Verzweigung ist der schwerste Befund: sie bricht "
                "bei jeder neuen Sprache."
            )
    else:
        print("Keine Befunde.")


def main() -> int:
    zerleger = argparse.ArgumentParser(
        description="Einen Assistenten-Prompt vermessen.",
        epilog="Das Skript zählt und findet Muster. Es urteilt nicht — "
               "was daraus folgt, entscheidet ein Mensch.",
    )
    zerleger.add_argument("dateien", nargs="+", help="Promptdateien")
    zerleger.add_argument("--breite", type=int, default=80,
                          help="Zeilengrenze je Abschnitt (Vorgabe 80)")
    zerleger.add_argument("--bericht", help="Ergebnis zusätzlich als JSON schreiben")
    argumente = zerleger.parse_args()

    messungen = []
    for name in argumente.dateien:
        pfad = pathlib.Path(name)
        if not pfad.is_file():
            print(f"Nicht lesbar: {pfad}", file=sys.stderr)
            return 2
        messungen.append(datei_messen(pfad, argumente.breite))

    bericht_drucken(messungen, argumente.breite)

    if argumente.bericht:
        pathlib.Path(argumente.bericht).write_text(
            json.dumps(messungen, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return 1 if any(m["befunde"] for m in messungen) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
