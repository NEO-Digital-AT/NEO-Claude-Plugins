---
description: Herkunftsgrenzen eines Projekts prüfen — Quelltext und laufende Quellen, mit Zahlen statt Vermutung
---

Prüfe, was dieses Projekt über eine Herkunftsgrenze lädt. **Gemessen
wird, nicht angenommen.** Erlaubt sind null Blocker.

Lade zuerst den Skill `neo-cors`.

## Schritt 1 — Die Quellen aufzählen

Kläre, falls es nicht im Projekt steht:

1. Unter welcher **Herkunft** läuft die Oberfläche, je Umgebung?
2. Welche Quellen lädt sie über die Grenze — API, Medienspeicher, CDN,
   Schriften, Karten, Module, Texturen?
3. Welche davon werden **ausgewertet** statt nur angezeigt: Canvas,
   WebGL, three.js, Web-Audio, Aufnahmen?
4. Wo reisen **Anmeldedaten** mit?
5. Läuft die Entwicklung über einen Proxy? Dann ist dort nichts geprüft
   (`references/entwicklung.md`).

Fehlt die Liste der Herkünfte je Umgebung, ist das der **erste Befund**:
Ohne sie lässt sich weder konfigurieren noch messen.

## Schritt 2 — Quelltext lesen

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cors-scan.py src/
```

Zwei Gruppen, und der Unterschied zählt:

- **Befund** — sicher falsch: abgeschaltete Browsersicherheit,
  öffentlicher Weiterleitungsdienst, `*` neben Anmeldedaten, ungeprüft
  gespiegelte Herkunft, fremdes Worker-Skript, `file://`. Erlaubt sind
  **null**.
- **Nachsehen** — hängt an etwas, das der Quelltext nicht zeigt. **Das
  ist kein Mangel.** Jeder Punkt wird angesehen und das Ergebnis
  berichtet; als Befund gemeldet wird er nur, wenn das Nachsehen einen
  ergibt.

## Schritt 3 — Laufende Quellen messen

Je Quelle **und je Umgebung**, mit der echten Herkunft:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cors-check.py <adresse> \
        --origin <herkunft> [--method POST] [--header content-type:application/json] \
        [--header authorization] [--credentials] [--expect-header content-disposition] \
        [--media]
```

- `--media` für alles, was in eine Zeichenfläche, nach WebGL oder in den
  Audiographen geht.
- `--expect-header` für jede Antwortkopfzeile, die der Code liest.
- Eine Methode außer GET, HEAD und OPTIONS wird **nicht** abgeschickt;
  das Werkzeug misst die Vorabfrage und sagt, was es ausgelassen hat.
  `--send-actual` nur, wo ein Schreibvorgang unschädlich ist.

## Schritt 4 — Deuten

In dieser Reihenfolge, weil die obere Ursache die unteren erzeugt:

1. **Keine Freigabe** — nichts anderes zählt, solange die fehlt.
2. **Vorabfrage nicht beantwortet** (401, 403, 405, Umleitung) — der
   Klassiker: `OPTIONS` läuft durch die Anmeldeprüfung.
3. **`*` mit Anmeldedaten** — geht gar nicht, nicht „manchmal".
4. **Methode oder Kopfzeile fehlt in der Vorabfrage.**
5. **Doppelte Freigabe** — Anwendung und Proxy setzen beide.
6. **`Vary: Origin` fehlt** — erklärt „geht mal, geht mal nicht".
7. **Kopfzeile nicht freigegeben** — erklärt `null` im Code bei
   sichtbarem Wert in den Werkzeugen.
8. **Medien**: Freigabe vorhanden, aber `crossorigin` fehlt in der
   Auszeichnung — die Messung sieht nur die eine Hälfte.

## Schritt 5 — Berichten

Je Quelle eine Zeile:

```
Quelle                              Herkunft                 Blocker  Warnungen
https://api.example.at/v1/auftraege https://app.example.at         0          0   bestanden
https://medien.example.at/*         https://app.example.at         1          1   nicht bestanden
```

Für jede nicht bestandene Zeile: die Blocker im Wortlaut, die vermutete
Ursache nach der Liste oben, der Vorschlag zur Behebung — und die Stufe
aus der Rangfolge des Skills: Lässt sich die Grenze **vermeiden**,
statt sie zu öffnen?

**Nichts reparieren, solange der Umfang nicht freigegeben ist.** Nach
der Freigabe: beheben, **erneut messen**, die neuen Zahlen nennen.

Am Ende die Abnahmeliste `references/pruefliste.md`. Solange eine Quelle
einen Blocker hat, lautet die Antwort nein.
