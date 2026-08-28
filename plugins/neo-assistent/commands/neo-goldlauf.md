---
description: Goldfälle eines KI-Assistenten messen — Werkzeugwahl und Argumente, je Sprache und Absicht, mit Zahlen statt Einschätzung
---

Miss den Assistenten gegen seine Goldfälle. **Gemessen wird, welches
Werkzeug mit welchen Argumenten aufgerufen wird** — nicht, ob die Antwort
schön formuliert ist. Ohne Zahlen gilt nichts als geprüft.

Lade zuerst den Skill `neo-assistent` und `references/goldfaelle.md`.

## Vorbereiten

Kläre, falls es nicht im Projekt steht:

1. Wo liegt die Goldfalldatei, wo der Adapter?
2. Welches Modell in welcher Fassung, je Stufe? **Beides gehört in den
   Bericht** — ein Bericht ohne Modellfassung ist nicht vergleichbar.
3. Welche Werkzeuge sind schreibend? Diese Fälle stehen bei 100 %.
4. Wird vor oder nach einer Änderung gemessen? Bei „nachher": wo liegt
   der Bericht von vorher?

Fehlen Goldfälle für eine Absicht oder eine Sprache, ist das der erste
Befund: gemessen wird sonst nur, was ohnehin schon gut lief. Melde die
Lücke und schlage die fehlenden Fälle vor, statt um sie herum zu messen.

Prüfe, dass der Adapter **denselben Weg fährt wie die Anwendung** —
Einordnung, Systemprompt, Absicht, Werkzeugliste, Schemaprüfung,
Vorbedingungen — und dass er schreibende Werkzeuge **nicht** wirklich
ausführt.

## Messen

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/gold-run.py gold-cases.json \
  --adapter "<befehl>" --runs 5 --report report.json
```

| Anlass | Läufe |
| --- | --- |
| Während der Arbeit | 3 |
| Vor jeder Freigabe, in der CI | **5** |
| Umbauschritt, Modellwechsel | **10** |

Ein einzelner grüner Lauf beweist nichts — ein Modell antwortet nicht
deterministisch.

Für einen Ausschnitt: `--language it`, `--intent auftrag_stornieren`,
`--case <kennung>`.

## Deuten

Der Bericht wertet nach Sprache und nach Absicht aus. Lies ihn in dieser
Reihenfolge:

1. **Bricht eine Sprache ein und die andere nicht?** Dann steuern Wörter
   den Ablauf — Schlüsselwort-Routing, ein Beispieldialog in einer
   Sprache oder ein übersetzter Aufzählungswert
   (`references/sprachen.md`).
2. **Bricht eine Absicht ein?** Dann fehlt meist die Abgrenzung in einer
   Werkzeugbeschreibung, oder zwei Absichten überschneiden sich
   (`references/werkzeuge.md`, `references/absichten.md`).
3. **Argumentfehler?** Dann steht die Regel im Prompt statt im Schema.
   `enum`, `pattern`, `required`, `additionalProperties: false`.
4. **Ein schreibendes Werkzeug unter 100 %?** Das ist ein Blocker, keine
   Kennzahl. Es wird sofort behoben, bevor irgendetwas anderes weitergeht.
5. **Fällt ein Fall nur manchmal?** Dann rät das Modell an einer Stelle,
   an der es nicht raten dürfte — meist Datum, Kennung oder Mandant.
   Diese Angaben gehören in den Zustand (`references/architektur.md`).

## Beheben

- **Den Goldfall nicht anpassen.** Ein Fall, der an das Verhalten
  angepasst wird, misst nichts mehr. Geändert wird er nur, wenn sich die
  **Anforderung** geändert hat — mit Vermerk und Grund.
- **Die Ursache benennen, nicht die Wirkung.** „Falsches Werkzeug" ist
  die Wirkung.
- **Eine Änderung**, dann erneut messen. Zwei gleichzeitig, und der Lauf
  sagt nichts mehr aus.
- **Nichts beheben, solange der Umfang nicht freigegeben ist** (Skill
  `neo-grundregeln`).

## Berichten

Je Änderung eine Zeile, mit Modellfassung:

```
Modell <name>@<fassung>, 5 Läufe je Fall

vorher    de 92.0 %   en 61.0 %   schreibend  80.0 %   14 von 22 bestanden
nachher   de 98.0 %   en 97.0 %   schreibend 100.0 %   22 von 22 bestanden
```

Dazu je nicht bestandenem Fall: die häufigsten Mängel aus dem Bericht,
die vermutete Ursache nach der Liste oben und der Vorschlag zur Behebung.

Am Ende ein Satz: „Alle Fälle über der Schwelle: ja/nein" — mit den
Zahlen, nicht mit einer Einschätzung. Solange auch nur ein schreibender
Fall unter 100 % liegt, lautet die Antwort nein. Danach die Abnahmeliste
`references/pruefliste.md`.
