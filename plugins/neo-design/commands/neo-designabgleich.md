---
description: Gebaute Oberfläche gegen das Designsystem messen — Bildabgleich und Stilabgleich, mit Zahlen statt Einschätzung
---

Miss die gebaute Oberfläche gegen das Designsystem. **Zwei Prüfungen,
beide müssen bestehen.** Ohne Zahlen gilt nichts als geprüft.

Lade zuerst den Skill `neo-design` und
`references/designsystem-abgleich.md`.

## Vorbereiten

Kläre, falls es nicht im Projekt steht:

1. Wo liegt das Designsystem (Artboards, Tokens, Referenzaufnahmen)?
2. Welche Ansicht wird abgeglichen, und welches Artboard entspricht ihr?
3. Unter welcher Adresse läuft die gebaute Anwendung?
4. Welche Fassungen sind zu prüfen — hell, dunkel, mobil?

Fehlen Referenzaufnahmen unter `design/referenz/`, erzeuge sie aus den
Artboards und melde das: sie sind ab jetzt die Abnahmegrundlage und
gehören ins Repository.

## Messen

Für **jede** zu prüfende Fassung:

1. Referenz und gebaute Ansicht mit **identischem Sichtfeld, identischem
   Bildmaßstab und identischen Bedingungen** aufnehmen
   (`deviceScaleFactor`, `reducedMotion: 'reduce'`, Farbschema, Sprache,
   Zeitzone, Schriften geladen). Weicht eines ab, vergleichst du zwei
   verschiedene Dinge.

2. **Bildabgleich** mit Unterschiedsbild:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bildabgleich.py \
     <referenz.png> <gebaut.png> --unterschied <diff.png> --schwelle <wert>
   ```

   Schwelle: **0.5** für einen Bausteine-Artboard, **2.0** für eine ganze
   Ansicht mit echten Daten. Bereiche mit veränderlichem Inhalt mit
   `--ignorieren x,y,b,h` ausnehmen und die Ausnahme benennen.

3. **Das Unterschiedsbild ansehen**, nicht nur die Zahl lesen. Benenne,
   *welche* Bauteile magenta sind — ein halbes Prozent an der falschen
   Stelle kann der Primärknopf sein.

4. **Stilabgleich** gegen die laufende Ansicht:

   ```js
   await seite.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/stilabgleich.js' })
   const b = await seite.evaluate(() => neoStilabgleich.pruefen())
   ```

   Jeder Fund ist ein erfundener Wert. **Erlaubt sind null Funde.**

## Berichten

Je Fassung eine Zeile mit den gemessenen Zahlen:

```
Bausteine hell    Bild 0.31 %  (Schwelle 0.5)   Stil 0 Funde    bestanden
Bausteine dunkel  Bild 1.84 %  (Schwelle 0.5)   Stil 3 Funde    nicht bestanden
```

Für jede nicht bestandene Fassung:

- welche Bauteile im Unterschiedsbild markiert sind,
- welche erfundenen Werte der Stilabgleich nennt, mit Fundstelle,
- die vermutete Ursache nach der Tabelle in
  `references/designsystem-abgleich.md`,
- der Vorschlag zur Behebung.

**Nichts reparieren, solange der Umfang nicht freigegeben ist.** Ist die
Behebung freigegeben: beheben, **erneut messen**, die neuen Zahlen
nennen. So oft, bis alle Fassungen bestehen.

Am Ende eine Zeile:

- „Deckungsgleich mit dem Designsystem: ja/nein" — mit den Zahlen, nicht
  mit einer Einschätzung.

Solange auch nur eine Fassung nicht besteht, lautet die Antwort nein.
Das Wort „fertig" fällt erst danach.
