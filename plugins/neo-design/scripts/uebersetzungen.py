#!/usr/bin/env python3
"""Vollständigkeit der Übersetzungen prüfen.

Vergleicht die Sprachdateien eines Projekts gegen die Leitsprache und
meldet, was fehlt, leer ist, unübersetzt geblieben ist oder in den
Platzhaltern abweicht. Der letzte Fall ist der gefährlichste: ein
Platzhalter, der in einer Sprache fehlt, ist kein Schönheitsfehler,
sondern ein Laufzeitfehler oder eine Meldung mit einer Lücke darin.

Gelesen werden:

    JSON und ARB     .json, .arb            verschachtelt oder flach
    PHP-Rückgabe     .php                   return [ 'a' => 'b', ... ]
    Flaches YAML     .yaml, .yml            key: wert, über Einrückung

Ohne Abhängigkeiten, damit das Skript in jeder CI läuft.

    uebersetzungen.py lang/ --leitsprache en
    uebersetzungen.py app/locales --leitsprache en --sprachen de,fr,it
    uebersetzungen.py lang/ --leitsprache en --quellen app/,resources/
    uebersetzungen.py lang/ --leitsprache en --bericht bericht.json

Rückgabewert 0, wenn keine Befunde, 1 bei Befunden, 2 bei Lesefehlern.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Platzhalter der gebräuchlichen Rahmenwerke. Sie müssen in jeder Sprache
# gleich vorkommen — sonst fehlt im Satz ein Wert oder die Formatierung bricht.
PLATZHALTER = re.compile(
    r"\{\{\s*[\w.]+\s*\}\}"          # {{ name }}       Vue, Angular, Blade
    r"|\{[\w.]+\}"                    # {name}           ICU, Flutter, .NET
    r"|:[a-zA-Z_]\w*"                 # :name            Laravel
    r"|%\d+\$[sd]"                    # %1$s             positionell
    r"|%[sd]"                         # %s               C-Stil
    r"|#\{[\w.]+\}"                   # #{name}
)

# Werte, die in mehreren Sprachen zu Recht gleich lauten.
GLEICH_ERLAUBT = {
    "ok", "e-mail", "email", "info", "status", "url", "id", "pdf", "csv",
    "json", "xml", "api", "web", "app", "server", "client", "login",
    "logout", "import", "export", "start", "stop", "reset", "admin",
    "n/a", "-", "…", "%", "€", "$",
}

ICU_PLURAL = re.compile(r"\{\s*\w+\s*,\s*(plural|select|selectordinal)\s*,", re.I)


class Lesefehler(Exception):
    pass


# --------------------------------------------------------------------------
# Lesen
# --------------------------------------------------------------------------

def flach(baum, praefix: str = "") -> dict[str, str]:
    """Verschachtelte Struktur in Punktschlüssel überführen."""
    flachliste: dict[str, str] = {}
    if isinstance(baum, dict):
        for schluessel, wert in baum.items():
            if schluessel.startswith("@"):      # ARB-Meta, kein Text
                continue
            neu = f"{praefix}.{schluessel}" if praefix else str(schluessel)
            flachliste.update(flach(wert, neu))
    elif isinstance(baum, list):
        for i, wert in enumerate(baum):
            flachliste.update(flach(wert, f"{praefix}[{i}]"))
    else:
        flachliste[praefix] = "" if baum is None else str(baum)
    return flachliste


def json_lesen(pfad: pathlib.Path) -> dict[str, str]:
    try:
        return flach(json.loads(pfad.read_text(encoding="utf-8")))
    except json.JSONDecodeError as fehler:
        raise Lesefehler(f"{pfad}: kein gültiges JSON — {fehler}")


PHP_EINTRAG = re.compile(
    r"""(['"])(?P<schluessel>(?:\\.|(?!\1).)*)\1\s*=>\s*"""
    r"""(?:(['"])(?P<wert>(?:\\.|(?!\3).)*)\3|(?P<offen>\[))""",
    re.S,
)


def php_lesen(pfad: pathlib.Path) -> dict[str, str]:
    """Liest ein PHP-Sprachfile der Form return [ 'a' => 'b', 'c' => [ ... ] ].

    Bewusst einfach gehalten. Was nicht sicher gelesen werden kann, wird
    gemeldet — nicht geraten.
    """
    text = pfad.read_text(encoding="utf-8")
    if "return" not in text:
        raise Lesefehler(f"{pfad}: kein `return`-Array gefunden")

    ergebnis: dict[str, str] = {}
    pfadteile: list[str] = []
    tiefe_bei: list[int] = []
    tiefe = 0
    i = 0
    while i < len(text):
        treffer = PHP_EINTRAG.search(text, i)
        klammer_zu = text.find("]", i)
        if treffer and (klammer_zu == -1 or treffer.start() < klammer_zu):
            schluessel = treffer.group("schluessel")
            if treffer.group("offen"):
                pfadteile.append(schluessel)
                tiefe += 1
                tiefe_bei.append(tiefe)
            else:
                voll = ".".join(pfadteile + [schluessel])
                ergebnis[voll] = (treffer.group("wert") or "").replace("\\'", "'")
            i = treffer.end()
        elif klammer_zu != -1:
            if tiefe_bei and tiefe == tiefe_bei[-1]:
                tiefe_bei.pop()
                if pfadteile:
                    pfadteile.pop()
                tiefe -= 1
            i = klammer_zu + 1
        else:
            break

    if not ergebnis:
        raise Lesefehler(f"{pfad}: keine Einträge lesbar")
    return ergebnis


def yaml_lesen(pfad: pathlib.Path) -> dict[str, str]:
    """Flaches YAML über Einrückung. Anker, Listen und Blöcke kann es nicht."""
    ergebnis: dict[str, str] = {}
    stapel: list[tuple[int, str]] = []
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8").split("\n"), 1):
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        if zeile.lstrip().startswith("-") or "<<:" in zeile or "&" in zeile.split(":")[0]:
            raise Lesefehler(
                f"{pfad}:{nr}: Listen und Anker kann dieser Leser nicht — "
                f"bitte als JSON prüfen"
            )
        einzug = len(zeile) - len(zeile.lstrip())
        if ":" not in zeile:
            continue
        schluessel, _, wert = zeile.strip().partition(":")
        wert = wert.strip().strip('"').strip("'")
        while stapel and stapel[-1][0] >= einzug:
            stapel.pop()
        voll = ".".join([t[1] for t in stapel] + [schluessel.strip()])
        if wert == "":
            stapel.append((einzug, schluessel.strip()))
        else:
            ergebnis[voll] = wert
    return ergebnis


LESER = {".json": json_lesen, ".arb": json_lesen, ".php": php_lesen,
         ".yaml": yaml_lesen, ".yml": yaml_lesen}


def sprache_lesen(wurzel: pathlib.Path, sprache: str) -> tuple[dict[str, str], list[str]]:
    """Sammelt alle Sprachdateien einer Sprache — als Datei oder als Ordner."""
    eintraege: dict[str, str] = {}
    fehler: list[str] = []
    kandidaten: list[pathlib.Path] = []

    ordner = wurzel / sprache
    if ordner.is_dir():
        kandidaten = sorted(p for p in ordner.rglob("*") if p.suffix in LESER)
        praefix_ab = ordner
    else:
        kandidaten = sorted(p for p in wurzel.glob(sprache + ".*") if p.suffix in LESER)
        kandidaten += sorted(p for p in wurzel.rglob("*")
                             if p.suffix in LESER and p.stem == sprache)
        praefix_ab = None

    for pfad in dict.fromkeys(kandidaten):
        try:
            teil = LESER[pfad.suffix](pfad)
        except Lesefehler as f:
            fehler.append(str(f))
            continue
        if praefix_ab is not None:
            rel = pfad.relative_to(praefix_ab).with_suffix("")
            gruppe = ".".join(rel.parts)
            teil = {f"{gruppe}.{k}": v for k, v in teil.items()}
        eintraege.update(teil)

    return eintraege, fehler


# --------------------------------------------------------------------------
# Vergleichen
# --------------------------------------------------------------------------

def platzhalter(text: str) -> list[str]:
    return sorted(m.group(0) for m in PLATZHALTER.finditer(text))


def vergleichen(leit: dict[str, str], leitname: str,
                andere: dict[str, dict[str, str]]) -> list[dict]:
    befunde: list[dict] = []

    for sprache, eintraege in andere.items():
        for schluessel, leitwert in leit.items():
            wert = eintraege.get(schluessel)

            if wert is None:
                befunde.append({"art": "fehlt", "sprache": sprache,
                                "schluessel": schluessel, "was": "Schlüssel fehlt",
                                "text": leitwert[:60]})
                continue

            if not wert.strip():
                befunde.append({"art": "leer", "sprache": sprache,
                                "schluessel": schluessel, "was": "Wert ist leer",
                                "text": leitwert[:60]})
                continue

            if (wert.strip() == leitwert.strip()
                    and wert.strip().lower() not in GLEICH_ERLAUBT
                    and len(wert.strip()) > 3
                    and not wert.strip().isdigit()):
                befunde.append({"art": "unuebersetzt", "sprache": sprache,
                                "schluessel": schluessel,
                                "was": f"gleich wie {leitname}",
                                "text": wert[:60]})

            a, b = platzhalter(leitwert), platzhalter(wert)
            if a != b:
                fehlend = [p for p in a if p not in b]
                zuviel = [p for p in b if p not in a]
                teile = []
                if fehlend:
                    teile.append("fehlt " + ", ".join(fehlend))
                if zuviel:
                    teile.append("zu viel " + ", ".join(zuviel))
                befunde.append({"art": "platzhalter", "sprache": sprache,
                                "schluessel": schluessel,
                                "was": "; ".join(teile), "text": wert[:60]})

            if ICU_PLURAL.search(leitwert) and not ICU_PLURAL.search(wert):
                befunde.append({"art": "plural", "sprache": sprache,
                                "schluessel": schluessel,
                                "was": f"{leitname} hat eine Pluralform, diese Sprache nicht",
                                "text": wert[:60]})

        for schluessel in eintraege:
            if schluessel not in leit:
                befunde.append({"art": "verwaist", "sprache": sprache,
                                "schluessel": schluessel,
                                "was": f"nicht in {leitname} vorhanden",
                                "text": eintraege[schluessel][:60]})

    return befunde


SCHLUESSEL_IM_CODE = re.compile(r"""['"`]([a-zA-Z][\w.\-]*(?:\.[\w\-]+)+)['"`]""")


def tote_schluessel(leit: dict[str, str], quellen: list[pathlib.Path]) -> list[dict]:
    """Schlüssel, die nirgends im Quelltext auftauchen. Heuristisch."""
    benutzt: set[str] = set()
    endungen = {".vue", ".ts", ".js", ".tsx", ".jsx", ".php", ".dart", ".cs",
                ".html", ".twig", ".blade.php"}
    for wurzel in quellen:
        for pfad in wurzel.rglob("*"):
            if not pfad.is_file() or pfad.suffix not in endungen:
                continue
            try:
                text = pfad.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            benutzt.update(SCHLUESSEL_IM_CODE.findall(text))

    befunde = []
    for schluessel in leit:
        if schluessel in benutzt:
            continue
        # Auch als Teilpfad zulassen: Gruppen werden oft dynamisch gebildet.
        if any(schluessel.startswith(b + ".") or b.startswith(schluessel + ".")
               for b in benutzt):
            continue
        befunde.append({"art": "tot", "sprache": "—", "schluessel": schluessel,
                        "was": "im Quelltext nicht gefunden (Verdacht)",
                        "text": leit[schluessel][:60]})
    return befunde


# --------------------------------------------------------------------------
# Bericht
# --------------------------------------------------------------------------

ARTNAME = {
    "fehlt": "Schlüssel fehlt",
    "leer": "Wert ist leer",
    "platzhalter": "Platzhalter weicht ab",
    "plural": "Pluralform fehlt",
    "unuebersetzt": "Unübersetzt geblieben",
    "verwaist": "Verwaister Schlüssel",
    "tot": "Schlüssel ohne Fundstelle (Verdacht)",
}
FOLGE = ["fehlt", "platzhalter", "leer", "plural", "unuebersetzt", "verwaist", "tot"]


def bericht_drucken(befunde: list[dict], leit: dict[str, str], leitname: str,
                    andere: dict[str, dict[str, str]], grenze: int) -> None:
    print(f"Übersetzungsprüfung — Leitsprache {leitname} mit {len(leit)} Schlüsseln\n")

    for sprache in sorted(andere):
        eigene = [b for b in befunde if b["sprache"] == sprache]
        fehlt = sum(1 for b in eigene if b["art"] in ("fehlt", "leer"))
        abdeckung = 100.0 * (len(leit) - fehlt) / len(leit) if leit else 100.0
        marke = "OK  " if not eigene else "FEHL"
        print(f"  {marke}  {sprache:<6} {len(andere[sprache]):>5} Schlüssel"
              f"   Abdeckung {abdeckung:5.1f} %   {len(eigene)} Befunde")

    if not befunde:
        print("\nBestanden. Jeder Schlüssel in jeder Sprache, Platzhalter passen.")
        return

    print(f"\n{len(befunde)} Befunde:")
    for art in FOLGE:
        teil = [b for b in befunde if b["art"] == art]
        if not teil:
            continue
        print(f"\n  {ARTNAME[art]} ({len(teil)}):")
        for b in teil[:grenze]:
            print(f"    [{b['sprache']}] {b['schluessel']}")
            print(f"           {b['was']}" + (f"  „{b['text']}\"" if b["text"] else ""))
        if len(teil) > grenze:
            print(f"    … und {len(teil) - grenze} weitere")

    hart = [b for b in befunde if b["art"] in ("fehlt", "leer", "platzhalter", "plural")]
    print(f"\n{len(hart)} davon sind Blocker (fehlend, leer, Platzhalter, Plural).")
    if any(b["art"] == "platzhalter" for b in befunde):
        print("Abweichende Platzhalter zuerst: sie brechen zur Laufzeit oder "
              "lassen eine Lücke im Satz.")


def main() -> int:
    zerleger = argparse.ArgumentParser(
        description="Vollständigkeit der Übersetzungen prüfen.",
        epilog="Liest JSON, ARB, PHP-Rückgabe-Arrays und flaches YAML.",
    )
    zerleger.add_argument("wurzel", help="Ordner mit den Sprachdateien")
    zerleger.add_argument("--leitsprache", required=True, help="etwa en")
    zerleger.add_argument("--sprachen", help="Kommaliste; ohne Angabe automatisch")
    zerleger.add_argument("--quellen", help="Kommaliste von Ordnern, für tote Schlüssel")
    zerleger.add_argument("--grenze", type=int, default=15, help="Zeilen je Befundart")
    zerleger.add_argument("--bericht", help="Ergebnis zusätzlich als JSON schreiben")
    argumente = zerleger.parse_args()

    wurzel = pathlib.Path(argumente.wurzel)
    if not wurzel.is_dir():
        print(f"Kein Ordner: {wurzel}", file=sys.stderr)
        return 2

    if argumente.sprachen:
        sprachen = [s.strip() for s in argumente.sprachen.split(",") if s.strip()]
    else:
        sprachen = sorted({p.name for p in wurzel.iterdir() if p.is_dir()}
                          | {p.stem for p in wurzel.glob("*") if p.suffix in LESER})
    sprachen = [s for s in sprachen if s != argumente.leitsprache]

    leit, fehler = sprache_lesen(wurzel, argumente.leitsprache)
    if not leit:
        print(f"Keine Einträge für die Leitsprache {argumente.leitsprache} in {wurzel}.",
              file=sys.stderr)
        for f in fehler:
            print("  " + f, file=sys.stderr)
        return 2
    if not sprachen:
        print(f"Keine weiteren Sprachen neben {argumente.leitsprache} gefunden.",
              file=sys.stderr)
        return 2

    andere: dict[str, dict[str, str]] = {}
    for sprache in sprachen:
        andere[sprache], teil = sprache_lesen(wurzel, sprache)
        fehler += teil

    for f in fehler:
        print("Lesefehler: " + f, file=sys.stderr)

    befunde = vergleichen(leit, argumente.leitsprache, andere)
    if argumente.quellen:
        quellen = [pathlib.Path(q.strip()) for q in argumente.quellen.split(",")]
        befunde += tote_schluessel(leit, [q for q in quellen if q.is_dir()])

    bericht_drucken(befunde, leit, argumente.leitsprache, andere, argumente.grenze)

    if argumente.bericht:
        pathlib.Path(argumente.bericht).write_text(
            json.dumps({"leitsprache": argumente.leitsprache,
                        "schluessel": len(leit), "befunde": befunde},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if (befunde or fehler) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
