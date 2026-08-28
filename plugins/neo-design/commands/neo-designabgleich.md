---
description: Gebaute Oberfläche gegen das Designsystem messen — Layout, Stil und Bild, mit Zahlen statt Einschätzung
---

Miss die gebaute Oberfläche gegen das Designsystem. **Verglichen wird
das Aussehen und das Verhalten, nicht der Inhalt.** Ohne Zahlen gilt
nichts als geprüft.

Lade zuerst den Skill `neo-design` und
`references/designsystem-abgleich.md`.

## Vorbereiten

Kläre, falls es nicht im Projekt steht:

1. Wo liegt das Designsystem (Artboards, Tokens, Referenzmessungen)?
2. Welche Ansicht wird abgeglichen, und welches Artboard entspricht ihr?
3. Unter welcher Adresse läuft die gebaute Anwendung?
4. Welche Zustände und Fassungen sind zu prüfen? Vorgabe: Ruhe, Hover,
   Fokus, Deaktiviert, Fehler, je hell und dunkel, dazu die mobile
   Breite.
5. **Sollen die statischen Oberflächentexte mitverglichen werden?**
   Standard ist nein. Nur auf ausdrückliche Ansage des Projektinhabers ja.

Fehlen Marker (`data-abgleich`) auf einer der beiden Seiten, ist das der
erste Befund: ohne sie lässt sich nicht zuordnen, was mit was zu
vergleichen ist. Melde es und schlage die Marker vor, statt über Rolle
und Reihenfolge zu raten.

## Messen

Für **jeden** Zustand und **jede** Fassung, in dieser Reihenfolge:

### 1. Layoutabgleich — der wichtigste

```js
await seite.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/layoutabgleich.js' })
const gebaut = await seite.evaluate(() => neoLayoutabgleich.messen({ nurMarkierte: true }))
const e = neoLayoutabgleich.vergleichen(entwurf, gebaut, { toleranz: 1, nurMarkierte: true })
```

Er misst Breite, Höhe, Position, Polster, Randstärken, Lücken, Radien,
Schriftmaße und Farben — und liest den Text in den Feldern **nicht**.
Erlaubt sind **0 Abweichungen** bei 1 px Toleranz.

Sollen Texte mit: beide Messungen mit `{ texte: true }` erzeugen und
`vergleichen(..., { texte: true })` aufrufen.

### 2. Stilabgleich

```js
await seite.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/style-audit.js' })
const b = await seite.evaluate(() => neoStyleAudit.check())
```

Jeder Fund ist ein erfundener Wert. Erlaubt sind **null Funde**.

### 3. Bildabgleich — nur wo der Inhalt gleich ist

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bildabgleich.py \
  <referenz.png> <gebaut.png> --unterschied <diff.png> --schwelle 0.5
```

Für den **Bausteine-Artboard**. Für eine Ansicht mit echten Daten
entweder die Inhaltsbereiche mit `--ignorieren x,y,b,h` ausnehmen oder
den Bildabgleich weglassen. **Ein roter Bildabgleich wegen abweichender
Feldwerte ist kein Befund**, sondern ein falsch angesetztes Werkzeug —
melde das, statt eine Zahl zu berichten, die nichts aussagt.

Das Unterschiedsbild wird **angesehen**, nicht nur die Zahl gelesen.

## Berichten

Je Zustand und Fassung eine Zeile:

```
Formular hell, Ruhe       Layout 0        Stil 0 Funde    bestanden
Formular hell, Hover      Layout 3        Stil 0 Funde    nicht bestanden
Bausteine dunkel, Ruhe    Layout 0        Stil 2 Funde    Bild 1.84 %   nicht bestanden
```

Für jede nicht bestandene Zeile:

- die Abweichungen aus dem Layoutbericht, gebündelt wie er sie liefert,
- die erfundenen Werte aus dem Stilabgleich, mit Fundstelle,
- die vermutete Ursache nach der Tabelle in
  `references/designsystem-abgleich.md`,
- der Vorschlag zur Behebung.

**Nichts reparieren, solange der Umfang nicht freigegeben ist.** Ist die
Behebung freigegeben: beheben, **erneut messen**, die neuen Zahlen
nennen. So oft, bis alle Zustände und Fassungen bestehen.

Am Ende eine Zeile:

- „Deckungsgleich mit dem Designsystem: ja/nein" — mit den Zahlen, nicht
  mit einer Einschätzung.

Solange auch nur ein Zustand nicht besteht, lautet die Antwort nein. Das
Wort „fertig" fällt erst danach.
