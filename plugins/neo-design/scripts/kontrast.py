#!/usr/bin/env python3
"""Kontrastrechner nach WCAG 2.2 für die NEO-Gestaltungsregeln.

Rechnet das Kontrastverhältnis zweier Farben und prüft es gegen die
Anforderung der jeweiligen Verwendung. Durchsichtige Farben werden vorher
über einen Grund zusammengesetzt — genau so, wie der Browser es tut, denn
eine Hover-Fläche mit Alphawert ist der häufigste Grund für einen
unlesbaren Knopf.

Ohne Abhängigkeiten, damit das Skript in jeder CI läuft.

    kontrast.py "#5C5470" "#FFFFFF"
    kontrast.py "#FFFFFF" "#2A025F1F" --grund "#0F0524" --art element
    kontrast.py --paare design/kontrastpaare.json
    kontrast.py --beispiel > design/kontrastpaare.json

Rückgabewert 0, wenn alles besteht, sonst 1 — damit als Tor verwendbar.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Anforderung je Verwendung: (AA, AAA). AAA ist für Nicht-Text nicht
# definiert; dort bleibt es bei 3:1 (WCAG 1.4.11).
ARTEN: dict[str, tuple[float, float, str]] = {
    "text": (4.5, 7.0, "Fließtext, Beschriftung, Hilfetext (1.4.3/1.4.6)"),
    "grosstext": (3.0, 4.5, "ab 24 px, oder ab 18,66 px fett (1.4.3/1.4.6)"),
    "element": (3.0, 3.0, "Rand, Symbol, Zustand, Diagramm, Fokus (1.4.11)"),
}

NAMEN = {
    "white": "#FFFFFF", "black": "#000000", "transparent": "#00000000",
}


class Farbfehler(ValueError):
    pass


def farbe(wert: str) -> tuple[float, float, float, float]:
    """Liest #RGB, #RGBA, #RRGGBB, #RRGGBBAA, rgb() und rgba() als RGBA 0..1."""
    text = wert.strip().lower()
    text = NAMEN.get(text, text)

    treffer = re.fullmatch(r"rgba?\(([^)]*)\)", text)
    if treffer:
        teile = [t.strip() for t in treffer.group(1).replace("/", " ").replace(",", " ").split()]
        if len(teile) not in (3, 4):
            raise Farbfehler(f"„{wert}“ ist keine gültige rgb()-Angabe")
        zahlen = []
        for i, teil in enumerate(teile):
            if teil.endswith("%"):
                zahlen.append(float(teil[:-1]) / 100 * (1 if i == 3 else 1))
            else:
                zahlen.append(float(teil) / (255 if i < 3 else 1))
        while len(zahlen) < 4:
            zahlen.append(1.0)
        return tuple(min(1.0, max(0.0, z)) for z in zahlen)  # type: ignore[return-value]

    roh = text.lstrip("#")
    if len(roh) in (3, 4):
        roh = "".join(z * 2 for z in roh)
    if len(roh) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", roh):
        raise Farbfehler(f"„{wert}“ ist keine Farbe (erwartet #RGB, #RRGGBB, #RRGGBBAA oder rgb())")
    werte = [int(roh[i:i + 2], 16) / 255 for i in range(0, len(roh), 2)]
    if len(werte) == 3:
        werte.append(1.0)
    return tuple(werte)  # type: ignore[return-value]


def ueber(vorne: tuple[float, float, float, float],
          hinten: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Setzt eine durchsichtige Farbe über eine andere (Quelle über Ziel, sRGB)."""
    a = vorne[3]
    if a >= 1.0:
        return vorne
    b = hinten[3]
    aus = a + b * (1 - a)
    if aus == 0:
        return (0.0, 0.0, 0.0, 0.0)
    kanal = tuple((vorne[i] * a + hinten[i] * b * (1 - a)) / aus for i in range(3))
    return (*kanal, aus)  # type: ignore[return-value]


def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def leuchtdichte(f: tuple[float, float, float, float]) -> float:
    r, g, b = (_linear(c) for c in f[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def verhaeltnis(vorne: tuple[float, float, float, float],
                hinten: tuple[float, float, float, float]) -> float:
    a, b = leuchtdichte(vorne), leuchtdichte(hinten)
    hell, dunkel = (a, b) if a >= b else (b, a)
    return (hell + 0.05) / (dunkel + 0.05)


def hex_von(f: tuple[float, float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in f[:3])


def rechne(vorne_roh: str, hinten_roh: str, grund_roh: str | None,
           art: str) -> dict:
    """Setzt zusammen, rechnet und bewertet ein Paar."""
    if art not in ARTEN:
        raise Farbfehler(f"Unbekannte Art „{art}“ (erlaubt: {', '.join(ARTEN)})")
    grund = farbe(grund_roh) if grund_roh else None
    hinten = farbe(hinten_roh)
    if hinten[3] < 1.0:
        if grund is None:
            raise Farbfehler(
                f"Der Hintergrund „{hinten_roh}“ ist durchsichtig. "
                "Ohne --grund lässt sich nicht rechnen, was der Anwender sieht.")
        hinten = ueber(hinten, grund)
    vorne = farbe(vorne_roh)
    if vorne[3] < 1.0:
        vorne = ueber(vorne, hinten)

    wert = verhaeltnis(vorne, hinten)
    aa, aaa, _ = ARTEN[art]
    return {
        "vorne": vorne_roh, "hinten": hinten_roh, "grund": grund_roh, "art": art,
        "gerechnet_vorne": hex_von(vorne), "gerechnet_hinten": hex_von(hinten),
        "wert": wert, "aa": aa, "aaa": aaa,
        "besteht_aa": wert >= aa, "besteht_aaa": wert >= aaa,
    }


BEISPIEL = {
    "_hinweis": (
        "Kontrastpaare des Projekts. Jede Farbkombination, die ein Anwender "
        "sieht, steht hier — auch die Hover-Fassung. Prüfen mit: "
        "kontrast.py --paare <diese Datei>. Die Werte stammen aus NEO Uptime "
        "und dienen als Muster; sie sind durch die eigenen zu ersetzen. "
        "„Rand eines Feldes“ fällt absichtlich durch: ein Rand, der ein "
        "Bedienelement überhaupt erst erkennbar macht, braucht 3:1. Eine rein "
        "trennende Linie ohne diese Aufgabe braucht das nicht und gehört "
        "nicht in diese Liste."
    ),
    "grund": "#FFFFFF",
    "stufe": "aa",
    "paare": [
        {"name": "Hell · Fließtext auf Fläche", "vorne": "#0C0025", "hinten": "#FFFFFF"},
        {"name": "Hell · Nebentext auf Fläche", "vorne": "#5C5470", "hinten": "#FFFFFF"},
        {"name": "Hell · Primärknopf, Ruhe", "vorne": "#FFFFFF", "hinten": "#2A025F"},
        {"name": "Hell · Primärknopf, Hover", "vorne": "#FFFFFF", "hinten": "#3A0B7F"},
        {"name": "Hell · Rand eines Feldes", "vorne": "#D5D0E4", "hinten": "#FFFFFF", "art": "element"},
        {"name": "Hell · Geistknopf, Hover mit Alpha", "vorne": "#2A025F", "hinten": "#2A025F14", "grund": "#FFFFFF"},
        {"name": "Dunkel · Fließtext auf Fläche", "vorne": "#F5F2FC", "hinten": "#121214", "grund": "#0A0A0B"},
        {"name": "Dunkel · Primärknopf, Ruhe", "vorne": "#14101F", "hinten": "#A8F20D"},
        {"name": "Dunkel · Fokusring", "vorne": "#A8F20D", "hinten": "#121214", "art": "element"},
    ],
}


def lauf_datei(pfad: pathlib.Path, stufe_arg: str | None) -> int:
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as fehler:
        print(f"Paardatei nicht lesbar: {fehler}", file=sys.stderr)
        return 2

    paare = daten.get("paare")
    if not isinstance(paare, list) or not paare:
        print("Die Paardatei enthält keine Liste „paare“.", file=sys.stderr)
        return 2

    stufe = (stufe_arg or daten.get("stufe") or "aa").lower()
    grund_gesamt = daten.get("grund")

    ergebnisse, fehler_liste = [], []
    for nummer, paar in enumerate(paare, start=1):
        name = paar.get("name") or f"Paar {nummer}"
        try:
            ergebnis = rechne(
                paar["vorne"], paar["hinten"],
                paar.get("grund", grund_gesamt), paar.get("art", "text"))
        except (Farbfehler, KeyError) as fehler:
            fehler_liste.append(f"{name}: {fehler}")
            continue
        ergebnis["name"] = name
        ergebnisse.append(ergebnis)

    breite = max((len(e["name"]) for e in ergebnisse), default=10)
    durchgefallen = 0
    print(f"Kontrastprüfung nach WCAG 2.2, Stufe {stufe.upper()} — {pfad}\n")
    for e in ergebnisse:
        soll = e["aaa"] if stufe == "aaa" else e["aa"]
        ok = e["wert"] >= soll
        durchgefallen += 0 if ok else 1
        marke = "OK  " if ok else "FEHL"
        print(f"  {marke}  {e['name']:<{breite}}  {e['wert']:6.2f}:1"
              f"  (Soll {soll}:1, {e['art']})")

    print()
    if fehler_liste:
        print("Nicht rechenbar:")
        for zeile in fehler_liste:
            print(f"  - {zeile}")
        print()
    if durchgefallen or fehler_liste:
        print(f"{durchgefallen} von {len(ergebnisse)} Paaren unter der Anforderung"
              f"{f', {len(fehler_liste)} nicht rechenbar' if fehler_liste else ''}.")
        return 1
    print(f"Alle {len(ergebnisse)} Paare bestehen Stufe {stufe.upper()}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Kontrastverhältnis nach WCAG 2.2 rechnen und prüfen.",
        epilog="Ohne Angabe von --art gilt „text“ (4,5:1 auf Stufe AA).")
    zerleger.add_argument("vorne", nargs="?", help="Vordergrundfarbe, z. B. \"#0C0025\"")
    zerleger.add_argument("hinten", nargs="?", help="Hintergrundfarbe, z. B. \"#FFFFFF\"")
    zerleger.add_argument("--grund", help="Undurchsichtiger Grund unter durchsichtigen Farben")
    zerleger.add_argument("--art", default="text", choices=sorted(ARTEN),
                          help="Verwendung des Vordergrunds")
    zerleger.add_argument("--stufe", choices=["aa", "aaa"], help="Geforderte Stufe")
    zerleger.add_argument("--paare", type=pathlib.Path, help="JSON-Datei mit Farbpaaren")
    zerleger.add_argument("--beispiel", action="store_true",
                          help="Beispiel einer Paardatei ausgeben")
    argumente = zerleger.parse_args(argv)

    if argumente.beispiel:
        print(json.dumps(BEISPIEL, ensure_ascii=False, indent=2))
        return 0

    if argumente.paare:
        return lauf_datei(argumente.paare, argumente.stufe)

    if not argumente.vorne or not argumente.hinten:
        zerleger.print_help()
        return 2

    try:
        e = rechne(argumente.vorne, argumente.hinten, argumente.grund, argumente.art)
    except Farbfehler as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    stufe = argumente.stufe or "aa"
    soll = e["aaa"] if stufe == "aaa" else e["aa"]
    print(f"Verhältnis   {e['wert']:.2f}:1")
    print(f"Vordergrund  {e['gerechnet_vorne']}"
          f"{'  (zusammengesetzt aus ' + e['vorne'] + ')' if e['gerechnet_vorne'].lower() != e['vorne'].lower().rstrip() else ''}")
    print(f"Hintergrund  {e['gerechnet_hinten']}"
          f"{'  (zusammengesetzt aus ' + e['hinten'] + ')' if e['gerechnet_hinten'].lower() != e['hinten'].lower().rstrip() else ''}")
    print(f"Verwendung   {argumente.art} — {ARTEN[argumente.art][2]}")
    print(f"Anforderung  {soll}:1 (Stufe {stufe.upper()})")
    print()
    if e["wert"] >= soll:
        rest = "" if stufe == "aaa" or e["besteht_aaa"] else "  (AAA mit 7:1 nicht erreicht)"
        print(f"Bestanden.{rest}")
        return 0
    print(f"Nicht bestanden. Es fehlen {soll - e['wert']:.2f} Punkte auf {soll}:1.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
