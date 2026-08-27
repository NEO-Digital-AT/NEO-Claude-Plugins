#!/usr/bin/env python3
"""Adapter für Requesty — führt einen Goldfall gegen den echten Assistenten aus.

Verbindet `goldlauf.py` mit dem Requesty-Router. Nimmt einen Fall als JSON
auf der Standardeingabe, fährt das Gespräch mit dem konfigurierten Modell,
zeichnet **jeden Werkzeugaufruf auf, ohne ihn auszuführen**, und gibt das
Ergebnis in der Form zurück, die `goldlauf.py` erwartet.

Requesty ist OpenAI-kompatibel; der Adapter spricht deshalb
`POST <basis>/chat/completions` ohne SDK und ohne Abhängigkeiten.

    export REQUESTY_API_KEY="…"
    requesty_adapter.py --konfig assistent.json --pruefen
    goldlauf.py goldfaelle.json --adapter "python3 tools/requesty_adapter.py --konfig assistent.json"

Der Schlüssel kommt **ausschließlich** aus der Umgebung. Er steht nie in
der Konfiguration, nie im Repository und nie in einer Ausgabe dieses
Skripts.

Rückgabewert 0 bei Erfolg, 1 bei Aufruffehler, 2 bei Konfigurationsfehler.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

BASIS_EU = "https://router.eu.requesty.ai/v1"
SCHLUESSEL_UMGEBUNG = "REQUESTY_API_KEY"
BASIS_UMGEBUNG = "REQUESTY_BASE_URL"

HOECHSTSCHRITTE = 8
FRIST = 90
VERSUCHE = 3


class Konfigfehler(Exception):
    pass


class Aufruffehler(Exception):
    pass


# --------------------------------------------------------------------------
# Schemaprüfung — knappe Teilmenge von JSON Schema, ohne Abhängigkeiten.
# Sie fängt, was der Anbieter nicht erzwungen hat.
# --------------------------------------------------------------------------

TYPEN = {
    "string": str, "number": (int, float), "integer": int,
    "boolean": bool, "array": list, "object": dict,
}


def schema_pruefen(wert, schema: dict, pfad: str = "") -> list[str]:
    maengel: list[str] = []
    ort = pfad or "(Wurzel)"

    typ = schema.get("type")
    if typ:
        typen = typ if isinstance(typ, list) else [typ]
        if not any(
            isinstance(wert, TYPEN[t]) and not (t != "boolean" and isinstance(wert, bool))
            for t in typen if t in TYPEN
        ):
            return [f"{ort}: erwartet {'/'.join(typen)}, erhalten "
                    f"{type(wert).__name__}"]

    if "enum" in schema and wert not in schema["enum"]:
        maengel.append(f"{ort}: {wert!r} nicht in {schema['enum']!r}")

    if isinstance(wert, str):
        if "pattern" in schema and not re.search(schema["pattern"], wert):
            maengel.append(f"{ort}: {wert!r} passt nicht auf {schema['pattern']!r}")
        if schema.get("format") == "date" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", wert):
            maengel.append(f"{ort}: {wert!r} ist kein Datum JJJJ-MM-TT")
        for grenze, vergleich, wort in (("minLength", len(wert).__lt__, "kürzer als"),
                                        ("maxLength", len(wert).__gt__, "länger als")):
            if grenze in schema and vergleich(schema[grenze]):
                maengel.append(f"{ort}: {wort} {schema[grenze]}")

    if isinstance(wert, (int, float)) and not isinstance(wert, bool):
        if "minimum" in schema and wert < schema["minimum"]:
            maengel.append(f"{ort}: {wert} unter {schema['minimum']}")
        if "maximum" in schema and wert > schema["maximum"]:
            maengel.append(f"{ort}: {wert} über {schema['maximum']}")

    if isinstance(wert, dict):
        eigenschaften = schema.get("properties") or {}
        for pflicht in schema.get("required") or []:
            if pflicht not in wert:
                maengel.append(f"{ort}: Pflichtfeld „{pflicht}“ fehlt")
        if schema.get("additionalProperties") is False:
            for schluessel in wert:
                if schluessel not in eigenschaften:
                    maengel.append(f"{ort}: unbekanntes Feld „{schluessel}“")
        for schluessel, teilschema in eigenschaften.items():
            if schluessel in wert:
                maengel += schema_pruefen(
                    wert[schluessel], teilschema,
                    f"{pfad}.{schluessel}" if pfad else schluessel)

    if isinstance(wert, list) and isinstance(schema.get("items"), dict):
        for i, eintrag in enumerate(wert):
            maengel += schema_pruefen(eintrag, schema["items"], f"{pfad}[{i}]")

    return maengel


# --------------------------------------------------------------------------
# Konfiguration
# --------------------------------------------------------------------------

def konfig_lesen(pfad: pathlib.Path) -> dict:
    try:
        k = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as fehler:
        raise Konfigfehler(f"Konfiguration nicht lesbar: {fehler}")

    for pflicht in ("modell", "systemprompt", "werkzeuge"):
        if not k.get(pflicht):
            raise Konfigfehler(f"In der Konfiguration fehlt „{pflicht}“.")

    for verboten in ("api_key", "apiKey", "schluessel", "token"):
        if verboten in k:
            raise Konfigfehler(
                f"„{verboten}“ steht in der Konfiguration. Der Schlüssel gehört "
                f"ausschließlich in die Umgebungsvariable {SCHLUESSEL_UMGEBUNG}."
            )

    wurzel = pfad.parent
    k["_systemprompt"] = (wurzel / k["systemprompt"]).read_text(encoding="utf-8")
    werkzeuge = json.loads((wurzel / k["werkzeuge"]).read_text(encoding="utf-8"))
    k["_werkzeuge"] = werkzeuge.get("tools", werkzeuge) if isinstance(werkzeuge, dict) else werkzeuge
    k.setdefault("basis", os.environ.get(BASIS_UMGEBUNG) or BASIS_EU)
    k.setdefault("temperatur", 0)
    k.setdefault("hoechstschritte", HOECHSTSCHRITTE)
    k.setdefault("frist", FRIST)
    return k


def schluessel_holen() -> str:
    schluessel = os.environ.get(SCHLUESSEL_UMGEBUNG, "").strip()
    if not schluessel:
        raise Konfigfehler(
            f"{SCHLUESSEL_UMGEBUNG} ist nicht gesetzt. "
            f"Setzen mit: export {SCHLUESSEL_UMGEBUNG}=\"…\""
        )
    return schluessel


# --------------------------------------------------------------------------
# Aufruf
# --------------------------------------------------------------------------

def rufen(konfig: dict, schluessel: str, nachrichten: list[dict]) -> dict:
    rumpf = {
        "model": konfig["modell"],
        "messages": nachrichten,
        "temperature": konfig["temperatur"],
    }
    if konfig["_werkzeuge"]:
        rumpf["tools"] = konfig["_werkzeuge"]
        rumpf["tool_choice"] = konfig.get("werkzeugwahl", "auto")
    if konfig.get("zusatz"):
        rumpf.update(konfig["zusatz"])

    kopfzeilen = {
        "Authorization": f"Bearer {schluessel}",
        "Content-Type": "application/json",
    }
    kopfzeilen.update(konfig.get("kopfzeilen") or {})

    anfrage = urllib.request.Request(
        konfig["basis"].rstrip("/") + "/chat/completions",
        data=json.dumps(rumpf, ensure_ascii=False).encode("utf-8"),
        headers=kopfzeilen,
        method="POST",
    )

    letzter = ""
    for versuch in range(1, VERSUCHE + 1):
        try:
            with urllib.request.urlopen(anfrage, timeout=konfig["frist"]) as antwort:
                return json.loads(antwort.read().decode("utf-8"))
        except urllib.error.HTTPError as fehler:
            text = (fehler.read().decode("utf-8", "replace") or "")[:300]
            if fehler.code == 401:
                raise Konfigfehler(
                    f"401 vom Router — {SCHLUESSEL_UMGEBUNG} ist ungültig oder "
                    f"gilt nicht für {konfig['basis']}."
                )
            if fehler.code == 404:
                raise Konfigfehler(
                    f"404 vom Router — Modell „{konfig['modell']}“ gibt es dort "
                    f"nicht, oder die Basisadresse ist falsch: {konfig['basis']}"
                )
            if fehler.code == 400:
                raise Aufruffehler(f"400 vom Router (Schema oder Parameter): {text}")
            letzter = f"HTTP {fehler.code}: {text}"
            if fehler.code not in (408, 409, 429, 500, 502, 503, 504):
                raise Aufruffehler(letzter)
        except urllib.error.URLError as fehler:
            letzter = f"Netz: {fehler.reason}"
        except TimeoutError:
            letzter = f"Zeitüberschreitung nach {konfig['frist']} s"

        if versuch < VERSUCHE:
            time.sleep(2 ** versuch)

    raise Aufruffehler(f"nach {VERSUCHE} Versuchen: {letzter}")


# --------------------------------------------------------------------------
# Ein Fall
# --------------------------------------------------------------------------

ROLLEN = {"benutzer": "user", "assistent": "assistant", "system": "system",
          "user": "user", "assistant": "assistant"}


def fall_fahren(konfig: dict, schluessel: str, fall: dict) -> dict:
    zustand = fall.get("zustand") or {}
    system = konfig["_systemprompt"]
    if zustand:
        system += (
            "\n\n<zustand>\n"
            + json.dumps(zustand, ensure_ascii=False, indent=2)
            + "\n</zustand>"
        )

    nachrichten = [{"role": "system", "content": system}]
    for schritt in fall.get("verlauf") or []:
        rolle = ROLLEN.get(schritt.get("rolle"), "user")
        nachrichten.append({"role": rolle, "content": schritt.get("text", "")})

    # Feste Werkzeugergebnisse aus dem Fall. Nichts wird wirklich ausgeführt.
    ergebnisse = fall.get("werkzeugergebnisse") or {}
    schemata = {
        w["function"]["name"]: w["function"].get("parameters") or {}
        for w in konfig["_werkzeuge"]
        if isinstance(w, dict) and "function" in w
    }

    aufgezeichnet: list[dict] = []
    schemafehler: list[str] = []
    antwort = ""
    schritte = 0

    while schritte < konfig["hoechstschritte"]:
        schritte += 1
        rueck = rufen(konfig, schluessel, nachrichten)
        wahl = (rueck.get("choices") or [{}])[0]
        nachricht = wahl.get("message") or {}
        aufrufe = nachricht.get("tool_calls") or []

        if not aufrufe:
            antwort = nachricht.get("content") or ""
            break

        nachrichten.append({
            "role": "assistant",
            "content": nachricht.get("content"),
            "tool_calls": aufrufe,
        })

        for aufruf in aufrufe:
            name = (aufruf.get("function") or {}).get("name") or "(ohne Namen)"
            roh = (aufruf.get("function") or {}).get("arguments") or "{}"
            try:
                argumente = json.loads(roh) if isinstance(roh, str) else roh
            except json.JSONDecodeError:
                argumente = {}
                schemafehler.append(f"{name}: Argumente sind kein gültiges JSON")

            if name in schemata:
                schemafehler += [
                    f"{name}: {m}" for m in schema_pruefen(argumente, schemata[name])
                ]
            else:
                schemafehler.append(f"{name}: Werkzeug ist nicht deklariert")

            aufgezeichnet.append({"name": name, "argumente": argumente})

            ergebnis = ergebnisse.get(name, {
                "hinweis": "Für dieses Werkzeug ist im Goldfall kein Ergebnis "
                           "hinterlegt. Nichts wurde ausgeführt."
            })
            nachrichten.append({
                "role": "tool",
                "tool_call_id": aufruf.get("id"),
                "content": json.dumps(ergebnis, ensure_ascii=False),
            })
    else:
        schemafehler.append(
            f"Abbruch nach {konfig['hoechstschritte']} Schritten — "
            f"der Assistent kam zu keiner Antwort"
        )

    return {
        "werkzeuge": aufgezeichnet,
        "antwort": antwort,
        "schritte": schritte,
        "schemafehler": schemafehler,
        "modell": konfig["modell"],
        "basis": konfig["basis"],
    }


# --------------------------------------------------------------------------

def pruefen(konfig: dict, schluessel: str) -> int:
    print(f"Router   {konfig['basis']}")
    print(f"Modell   {konfig['modell']}")
    print(f"Prompt   {len(konfig['_systemprompt'].splitlines())} Zeilen")
    print(f"Werkzeuge {len(konfig['_werkzeuge'])}")
    if not konfig["basis"].startswith("https://router.eu."):
        print("\nHinweis: Das ist nicht der EU-Router. Für EU-Datenhaltung ist "
              f"{BASIS_EU} vorgesehen.")
    if "@" not in konfig["modell"] and not konfig["modell"].startswith("policy/"):
        print("\nAchtung: Das Modell trägt keine Regionsangabe (etwa "
              "„…@eu-central-1“) und ist keine Policy. Der EU-Router allein "
              "hält die Verarbeitung nicht in der EU — siehe requesty.md.")

    ergebnis = fall_fahren(konfig, schluessel, {
        "verlauf": [{"rolle": "benutzer", "text": "Antworte nur mit: bereit"}],
    })
    print(f"\nAntwort  {ergebnis['antwort'][:120]!r}")
    print("Verbindung steht.")
    return 0


def main() -> int:
    zerleger = argparse.ArgumentParser(
        description="Goldfall gegen einen Assistenten hinter Requesty fahren.",
        epilog=f"Der Schlüssel kommt aus {SCHLUESSEL_UMGEBUNG} und aus sonst nichts.",
    )
    zerleger.add_argument("--konfig", required=True, help="Konfigurationsdatei (JSON)")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="nur Verbindung und Konfiguration prüfen")
    zerleger.add_argument("--modell", help="Modell übersteuern (für Vergleiche)")
    argumente = zerleger.parse_args()

    try:
        konfig = konfig_lesen(pathlib.Path(argumente.konfig))
        if argumente.modell:
            konfig["modell"] = argumente.modell
        schluessel = schluessel_holen()
    except (Konfigfehler, OSError, json.JSONDecodeError) as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    try:
        if argumente.pruefen:
            return pruefen(konfig, schluessel)
        fall = json.load(sys.stdin)
        print(json.dumps(fall_fahren(konfig, schluessel, fall), ensure_ascii=False))
        return 0
    except Konfigfehler as fehler:
        print(str(fehler), file=sys.stderr)
        return 2
    except (Aufruffehler, json.JSONDecodeError) as fehler:
        print(str(fehler), file=sys.stderr)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
