---
description: Eine Oberfläche nach einem Entwurf aus Claude Design bauen — Inventar, Element für Element, nach jedem Element gemessen
---

Baue die Ansicht nach dem vorliegenden Entwurf. **Der Entwurf gibt vor,
du setzt um. Du gestaltest nicht.** Jede Abweichung ist eine Rückfrage,
keine Entscheidung.

Lade zuerst den Skill `neo-design` und **vollständig**
`references/claude-design.md`. Ohne diesen Text wird nicht gebaut.

## Schritt 0 — Klären

Kläre, falls es nicht im Projekt steht:

1. Welches Artboard entspricht der zu bauenden Ansicht?
2. Welche Fassungen liegen vor — hell, dunkel, mobil?
3. Welche Zustände zeigt der Entwurf, welche fehlen?
4. Welche Felder, Werte und Verhaltensweisen kommen aus der Fachlichkeit
   und nicht aus dem Entwurf?
5. Gibt es die Ansicht bereits? Dann **nicht bauen**, sondern nach
   `references/claude-design.md`, Abschnitt „Wenn die Seite schon
   existiert", Wege vorlegen und warten.

Fehlt eine Fassung oder ein Zustand im Entwurf: **fragen**, nicht
ableiten.

## Schritt 1 — Inventar, vor der ersten Zeile Code

Miss das Artboard und liste **jedes** Element von oben nach unten:

```js
await seite.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/layoutabgleich.js' })
const entwurf = await seite.evaluate(() => neoLayoutabgleich.messen({ nurMarkierte: true }))
```

Format und Beispiel stehen in `references/claude-design.md`. Es gilt:

- jedes Element, nicht die wichtigen;
- Maße **gemessen**, nicht geschätzt;
- je Element ein Marker (`data-abgleich`), der später auf beiden Seiten
  steht;
- was die Aufgabe braucht und der Entwurf nicht zeigt, steht als **offene
  Frage** im Inventar.

**Lege das Inventar vor.** Enthält es offene Fragen, warte auf die
Antworten, bevor du baust.

## Schritt 2 — Element für Element bauen

Für **jedes** Element des Inventars, in der Reihenfolge des Inventars:

1. Zeile im Inventar lesen, Element im Entwurf ansehen.
2. Bauen — ausschließlich mit Komponenten der Produktfamilie (`Neo*`,
   `LeoFlex*`, Skill `neo-komponenten`), ausschließlich mit Tokens.
3. Messen: Layoutabgleich für dieses Element gegen das Artboard,
   Toleranz 1 px.
4. **0 Abweichungen** — sonst korrigieren und erneut messen. Nicht
   weiterbauen.
5. Nächstes Element.

Ein Element ist fertig, wenn es **gemessen bestanden** hat, nicht wenn es
fertig aussieht.

Fehlt im Entwurf ein Vorbild für ein fachlich nötiges Bauteil: **halte
an und frage** (Schritt 4). Erfinde nichts.

## Schritt 3 — Die ganze Seite

Erst wenn jedes Element einzeln besteht:

1. Layoutabgleich über die **vollständige** Seite, je Fassung hell,
   dunkel, mobil.
2. Stilabgleich: null erfundene Werte.
3. Bildabgleich gegen das Artboard, mit Unterschiedsbild — und das Bild
   **ansehen**.
4. Die Seite **im Ganzen** neben dem Artboard betrachten: Rhythmus,
   Gewichtung, Eindruck. Jedes Einzelmaß kann stimmen und die Seite
   trotzdem falsch wirken.
5. Alle Zustände: Ruhe, Hover, Fokus, Deaktiviert, Fehler, Ladend, Leer.

## Schritt 4 — Rückfrage bei jeder Abweichung

Sobald eine Abweichung nötig scheint: **anhalten**. Vier Teile, keiner
davon optional:

1. **Zwei Bilder nebeneinander** — links die Vorgabe, rechts der
   Vorschlag, erzeugt mit `scripts/gegenueberstellung.js`. Meldet das
   Werkzeug `brauchbar: false`, wird die Rückfrage nicht abgeschickt.
2. **Was abweicht, in Maßen**: Vorgabe, Vorschlag, Differenz.
3. **Warum** es nötig ist — fachlich, nicht geschmacklich.
4. **Mindestens zwei Möglichkeiten** mit Vor- und Nachteilen, eine
   **Empfehlung**, und der Satz, dass die Entscheidung beim
   Projektinhaber liegt.

Dann **warten**. Nicht vorbereiten, nicht anfangen, nicht die eigene
Empfehlung umsetzen, weil keine Antwort kam.

## Schritt 5 — Berichten

Je Fassung und Zustand eine Zeile:

```
Formular hell, Ruhe     Layout 0   Stil 0   Bild 0.12 %   bestanden
Formular dunkel, Hover  Layout 2   Stil 0   —             nicht bestanden
```

Dazu die Selbstprüfung aus `references/claude-design.md`, alle sechs
Sätze mit Zahlen:

- „Inventar: <n> Elemente aus dem Artboard, alle gemessen."
- „Gebaut und einzeln geprüft: <n> von <n> Elementen, je 0 Abweichungen."
- „Gesamtdurchgang: Layout <n>, Stil <n>, Bild <x> %."
- „Zustände geprüft: <Liste>, je hell und dunkel."
- „Abweichungen vom Entwurf: <n> — alle vorgelegt und entschieden."
- „Eigene Gestaltungsentscheidungen: **0**."

Steht in der letzten Zeile etwas anderes als null, ist die Arbeit nicht
abnahmefähig — unabhängig davon, wie gut das Ergebnis aussieht. Danach
die Abnahmeliste `references/pruefliste.md`.
