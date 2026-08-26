#!/usr/bin/env python3
"""Bildabgleich fuer den Vergleich Designsystem gegen gebaute Oberflaeche.

Vergleicht zwei PNG-Aufnahmen Bildpunkt fuer Bildpunkt, nennt die Abweichung
als Zahl und schreibt ein Unterschiedsbild, in dem jede abweichende Stelle
magenta markiert ist. Damit laesst sich "sieht aus wie im Entwurf" belegen
statt behaupten.

Ohne Abhaengigkeiten: PNG wird mit der Standardbibliothek gelesen und
geschrieben, damit das Skript in jeder CI laeuft.

    bildabgleich.py entwurf.png gebaut.png
    bildabgleich.py entwurf.png gebaut.png --unterschied diff.png --schwelle 0.5
    bildabgleich.py entwurf.png gebaut.png --ignorieren 20,600,400,40

Rueckgabewert 0, wenn die Abweichung unter der Schwelle liegt, sonst 1.
"""
from __future__ import annotations

import argparse
import pathlib
import struct
import sys
import zlib

SIGNATUR = b"\x89PNG\r\n\x1a\n"
KANAELE = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


class Bildfehler(ValueError):
    pass


def _entfiltern(roh: bytes, breite: int, hoehe: int, kanaele: int) -> bytearray:
    """Macht die PNG-Zeilenfilter rueckgaengig und liefert rohe Bildpunkte."""
    zeilenlaenge = breite * kanaele
    aus = bytearray(zeilenlaenge * hoehe)
    vorher = bytearray(zeilenlaenge)
    pos = 0
    for y in range(hoehe):
        filter_typ = roh[pos]
        pos += 1
        zeile = bytearray(roh[pos:pos + zeilenlaenge])
        pos += zeilenlaenge
        if filter_typ == 1:      # Sub
            for i in range(kanaele, zeilenlaenge):
                zeile[i] = (zeile[i] + zeile[i - kanaele]) & 0xFF
        elif filter_typ == 2:    # Up
            for i in range(zeilenlaenge):
                zeile[i] = (zeile[i] + vorher[i]) & 0xFF
        elif filter_typ == 3:    # Average
            for i in range(zeilenlaenge):
                links = zeile[i - kanaele] if i >= kanaele else 0
                zeile[i] = (zeile[i] + ((links + vorher[i]) >> 1)) & 0xFF
        elif filter_typ == 4:    # Paeth
            for i in range(zeilenlaenge):
                a = zeile[i - kanaele] if i >= kanaele else 0
                b = vorher[i]
                c = vorher[i - kanaele] if i >= kanaele else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                vorhersage = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                zeile[i] = (zeile[i] + vorhersage) & 0xFF
        elif filter_typ != 0:
            raise Bildfehler(f"Unbekannter Zeilenfilter {filter_typ}")
        aus[y * zeilenlaenge:(y + 1) * zeilenlaenge] = zeile
        vorher = zeile
    return aus


def png_lesen(pfad: pathlib.Path) -> tuple[int, int, bytearray]:
    """Liest ein PNG und liefert Breite, Hoehe und die Bildpunkte als RGB."""
    daten = pfad.read_bytes()
    if not daten.startswith(SIGNATUR):
        raise Bildfehler(f"{pfad} ist keine PNG-Datei")
    pos = len(SIGNATUR)
    breite = hoehe = farbtyp = bittiefe = 0
    idat = bytearray()
    palette = b""
    while pos < len(daten):
        laenge = struct.unpack(">I", daten[pos:pos + 4])[0]
        art = daten[pos + 4:pos + 8]
        inhalt = daten[pos + 8:pos + 8 + laenge]
        pos += 12 + laenge
        if art == b"IHDR":
            breite, hoehe, bittiefe, farbtyp, _, _, verschraenkt = struct.unpack(">IIBBBBB", inhalt)
            if bittiefe != 8:
                raise Bildfehler(f"{pfad}: nur 8 Bit je Kanal, gefunden {bittiefe}")
            if verschraenkt:
                raise Bildfehler(f"{pfad}: verschraenkte PNG werden nicht gelesen")
            if farbtyp not in KANAELE:
                raise Bildfehler(f"{pfad}: Farbtyp {farbtyp} wird nicht gelesen")
        elif art == b"PLTE":
            palette = inhalt
        elif art == b"IDAT":
            idat += inhalt
        elif art == b"IEND":
            break

    kanaele = KANAELE[farbtyp]
    punkte = _entfiltern(zlib.decompress(bytes(idat)), breite, hoehe, kanaele)

    # Alles auf RGB bringen; Alpha wird ueber Weiss zusammengesetzt.
    rgb = bytearray(breite * hoehe * 3)
    for i in range(breite * hoehe):
        q = i * kanaele
        if farbtyp == 0:
            r = g = b = punkte[q]
        elif farbtyp == 2:
            r, g, b = punkte[q], punkte[q + 1], punkte[q + 2]
        elif farbtyp == 3:
            k = punkte[q] * 3
            r, g, b = palette[k], palette[k + 1], palette[k + 2]
        elif farbtyp == 4:
            a = punkte[q + 1] / 255
            r = g = b = round(punkte[q] * a + 255 * (1 - a))
        else:
            a = punkte[q + 3] / 255
            r = round(punkte[q] * a + 255 * (1 - a))
            g = round(punkte[q + 1] * a + 255 * (1 - a))
            b = round(punkte[q + 2] * a + 255 * (1 - a))
        rgb[i * 3], rgb[i * 3 + 1], rgb[i * 3 + 2] = r, g, b
    return breite, hoehe, rgb


def png_schreiben(pfad: pathlib.Path, breite: int, hoehe: int, rgb: bytearray) -> None:
    roh = bytearray()
    for y in range(hoehe):
        roh.append(0)                                   # Filter "None"
        roh += rgb[y * breite * 3:(y + 1) * breite * 3]

    def block(art: bytes, inhalt: bytes) -> bytes:
        return (struct.pack(">I", len(inhalt)) + art + inhalt
                + struct.pack(">I", zlib.crc32(art + inhalt) & 0xFFFFFFFF))

    pfad.write_bytes(
        SIGNATUR
        + block(b"IHDR", struct.pack(">IIBBBBB", breite, hoehe, 8, 2, 0, 0, 0))
        + block(b"IDAT", zlib.compress(bytes(roh), 6))
        + block(b"IEND", b""))


def vergleichen(a: tuple[int, int, bytearray], b: tuple[int, int, bytearray],
                toleranz: int, ignorieren: list[tuple[int, int, int, int]]):
    breite, hoehe, links = a
    _, _, rechts = b
    unterschied = bytearray(breite * hoehe * 3)
    abweichend = maximal = 0
    summe = 0
    uebersprungen = 0

    def ignoriert(x: int, y: int) -> bool:
        return any(rx <= x < rx + rb and ry <= y < ry + rh for rx, ry, rb, rh in ignorieren)

    for y in range(hoehe):
        for x in range(breite):
            i = (y * breite + x) * 3
            if ignoriert(x, y):
                uebersprungen += 1
                unterschied[i:i + 3] = bytes((230, 230, 235))
                continue
            d = max(abs(links[i] - rechts[i]),
                    abs(links[i + 1] - rechts[i + 1]),
                    abs(links[i + 2] - rechts[i + 2]))
            maximal = max(maximal, d)
            summe += d
            if d > toleranz:
                abweichend += 1
                unterschied[i:i + 3] = bytes((255, 0, 200))     # Magenta
            else:
                # Uebereinstimmendes bleibt sichtbar, aber blass.
                hell = 255 - (255 - links[i]) // 5
                unterschied[i], unterschied[i + 1], unterschied[i + 2] = hell, hell, hell
    gesamt = breite * hoehe
    geprueft = gesamt - uebersprungen
    return {
        "breite": breite, "hoehe": hoehe, "gesamt": gesamt, "geprueft": geprueft,
        "uebersprungen": uebersprungen, "abweichend": abweichend,
        "anteil": (abweichend / geprueft * 100) if geprueft else 0.0,
        "maximal": maximal, "mittel": (summe / geprueft) if geprueft else 0.0,
        "bild": unterschied,
    }


def bereich(text: str) -> tuple[int, int, int, int]:
    teile = text.split(",")
    if len(teile) != 4:
        raise argparse.ArgumentTypeError("Bereich als x,y,breite,hoehe angeben")
    return tuple(int(t) for t in teile)  # type: ignore[return-value]


def main(argv: list[str] | None = None) -> int:
    z = argparse.ArgumentParser(
        description="Zwei PNG-Aufnahmen vergleichen und die Abweichung als Zahl nennen.",
        epilog="Gedacht fuer den Abgleich einer Entwurfsvorlage mit der gebauten Oberflaeche.")
    z.add_argument("entwurf", type=pathlib.Path, help="Aufnahme aus dem Designsystem")
    z.add_argument("gebaut", type=pathlib.Path, help="Aufnahme der gebauten Oberflaeche")
    z.add_argument("--unterschied", type=pathlib.Path, help="Pfad fuer das Unterschiedsbild")
    z.add_argument("--toleranz", type=int, default=8,
                   help="Erlaubte Abweichung je Farbkanal, 0 bis 255 (Vorgabe 8, deckt Kantenglaettung ab)")
    z.add_argument("--schwelle", type=float, default=1.0,
                   help="Erlaubter Anteil abweichender Bildpunkte in Prozent (Vorgabe 1.0)")
    z.add_argument("--ignorieren", type=bereich, action="append", default=[],
                   metavar="X,Y,B,H", help="Bereich ausnehmen, mehrfach angebbar")
    a = z.parse_args(argv)

    try:
        links = png_lesen(a.entwurf)
        rechts = png_lesen(a.gebaut)
    except (Bildfehler, OSError, zlib.error) as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    if links[0] != rechts[0] or links[1] != rechts[1]:
        print(f"Die Bilder haben verschiedene Masse: "
              f"Entwurf {links[0]}x{links[1]}, gebaut {rechts[0]}x{rechts[1]}.\n"
              f"Beide Aufnahmen mit demselben Sichtfeld und demselben Bildmassstab erzeugen.",
              file=sys.stderr)
        return 2

    e = vergleichen(links, rechts, a.toleranz, a.ignorieren)
    if a.unterschied:
        png_schreiben(a.unterschied, e["breite"], e["hoehe"], e["bild"])

    print(f"Bildmasse        {e['breite']} x {e['hoehe']} ({e['gesamt']} Bildpunkte)")
    if e["uebersprungen"]:
        print(f"Ausgenommen      {e['uebersprungen']} Bildpunkte in {len(a.ignorieren)} Bereich(en)")
    print(f"Abweichend       {e['abweichend']} von {e['geprueft']}  =  {e['anteil']:.3f} %")
    print(f"Groesste Abweichung je Kanal   {e['maximal']}")
    print(f"Mittlere Abweichung je Kanal   {e['mittel']:.2f}")
    print(f"Toleranz {a.toleranz}, Schwelle {a.schwelle} %")
    if a.unterschied:
        print(f"Unterschiedsbild {a.unterschied}")
    print()
    if e["anteil"] <= a.schwelle:
        print("Bestanden. Die gebaute Oberflaeche deckt sich mit dem Entwurf.")
        return 0
    print(f"Nicht bestanden. {e['anteil']:.3f} % weichen ab, erlaubt sind {a.schwelle} %.")
    if a.unterschied:
        print("Die magenta markierten Stellen im Unterschiedsbild ansehen und angleichen.")
    else:
        print("Mit --unterschied ein Unterschiedsbild schreiben lassen, um die Stellen zu sehen.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
