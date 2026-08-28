# Screenshots für die Dokumentation

## Grundsatz

Ein Screenshot **belegt**, was der Text sagt. Er ersetzt ihn nie. Was nur
im Bild steht, ist für Vorlesegeräte, für die Suche und für generative
Agenten nicht vorhanden.

Jedes Bild in der Doku ist:

- **im Repository eingecheckt** und von dort verlinkt — nie von einem
  fremden Server geladen,
- **reproduzierbar erzeugt**, nicht von Hand abfotografiert,
- **markiert**, wo eine bestimmte Stelle gemeint ist,
- **frei von echten Daten**: keine Kundennamen, keine Adressen, keine
  Kennungen, keine Tokens, keine E-Mail-Adressen.

## Wann ein Screenshot gebraucht wird

| Fall | Bild |
| --- | --- |
| Eine Ansicht wird zum ersten Mal erklärt | Gesamtaufnahme, Elemente nummeriert |
| Ein einzelner Schritt eines Ablaufs | Detailaufnahme mit Rahmen um das Bedienelement |
| Ein Zustand, den man erkennen muss (Fehler, Warnung, Leer) | Aufnahme genau dieses Zustands |
| Ein Wert, dessen Wirkung man sehen muss | Vorher und nachher nebeneinander |
| Reine Fließtext-Erklärung, Begriffsklärung, Architektur | kein Screenshot |

Kein Bild „zur Auflockerung". Jedes Bild kostet Pflege bei jeder
Designänderung.

## Aufnahme

Erzeugt wird mit Playwright, gegen die laufende Anwendung oder einen
Klickprototyp. Reproduzierbar heißt: dieselbe Eingabe ergibt dasselbe
Bild.

```js
const kontext = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  deviceScaleFactor: 2,          // scharf auf großen Bildschirmen
  reducedMotion: 'reduce',       // keine halb gelaufene Animation im Bild
  locale: 'de-AT',
  timezoneId: 'Europe/Vienna',
  colorScheme: 'light',
})
const page = await kontext.newPage()
await page.goto(adresse)
await page.evaluate(() => document.fonts.ready)   // sonst springt die Schrift
await page.waitForSelector('[data-test="fertig"]')
```

- **Feste Demodaten.** Ein Screenshot mit „vor 3 Minuten" ändert sich bei
  jedem Lauf und erzeugt bei jedem Doku-Commit einen Diff. Uhrzeit,
  Zufallswerte und Zählstände festnageln.
- **Ein Bildmaß je Art:** Gesamtaufnahmen 1280 px breit, Mobilaufnahmen
  390 px, Detailaufnahmen über den Ausschnitt. Nicht bei jedem Bild neu
  entscheiden.
- **Hell ist die Voreinstellung.** Unterscheidet sich eine Funktion in
  der Dunkelfassung, kommen beide Bilder nebeneinander.
- **Was doch personenbezogen ist, wird maskiert** (`mask:` in
  `page.screenshot`), nicht nachträglich übermalt.

## Markieren

Die Markierungen werden **vor der Aufnahme in die Seite eingeblendet**
und mitfotografiert. Sie sind damit vektorscharf, folgen exakt den
Elementen und sind auf hellem wie dunklem Grund lesbar (weiße Fassung
unter dem Rot).

```js
await page.addScriptTag({ path: '<plugin>/scripts/annotate.js' })
await page.evaluate(() => {
  neoAnnotate
    .frame('[data-test="typ"]', { number: 1 })
    .frame('[data-test="intervall"]', { number: 2 })
    .arrow('[data-test="speichern"]', { text: 'Erst danach wird geprüft', direction: 'top' })
    .highlight('h1')
    .note({ text: 'Der Typ legt fest, welche Felder erscheinen.', at: '[data-test="typ"]' })
})
await page.screenshot({ path: 'docs/frontend/de/bedienung/bilder/auftrag-anlegen.png', fullPage: true })
```

| Aufruf | Wofür |
| --- | --- |
| `frame(ziel, {number, text, padding, all})` | Roter Rahmen, wahlweise mit Nummernmarke |
| `arrow(ziel, {direction, text, length})` | Roter Pfeil auf ein Element, `direction`: `left`, `right`, `top`, `bottom` |
| `number(ziel, n)` | Nummernmarke ohne Rahmen |
| `note({text, at, position, width})` | Kasten mit Erklärtext, an einem Element ausgerichtet |
| `highlight(ziel)` | Textmarker über den Textzeilen |
| `spotlight(ziel, {dim, padding})` | Alles außer dem Ziel abdunkeln — für Detailaufnahmen |
| `clip(ziel, padding)` | Liefert den `clip`-Bereich für eine Detailaufnahme |
| `clear()` | Entfernt alle Markierungen |

Für eine Detailaufnahme: `spotlight` setzen, `clip` holen, mit
`page.screenshot({ clip })` aufnehmen.

Regeln zur Markierung:

- **Höchstens fünf Marken je Bild.** Mehr braucht zwei Bilder.
- Nummern folgen der Reihenfolge im Text, nicht der Lage im Bild.
- Der Infokasten trägt einen kurzen Satz, keinen Absatz. Der Absatz steht
  im Text.
- Nichts überdecken, was der Leser sehen soll.
- Die Bedeutung der Marke steht im Text daneben — eine „1" im Bild ohne
  „1." im Text ist wertlos.

## Ablage und Benennung

```
docs/frontend/de/bedienung/auftraege/
  anlegen.md
  bilder/
    auftrag-anlegen.png
    auftrag-anlegen-typ-detail.png
    auftrag-anlegen-fehler.png
```

- Bilder liegen in `bilder/` **neben** der Datei, die sie verwendet.
- Name: `<gegenstand>-<zustand>[-detail].png`, klein, mit Bindestrich,
  ohne Umlaute.
- **Sprachgebunden.** Zeigt ein Bild Oberflächentext, gibt es je
  Sprachbaum ein eigenes mit demselben Dateinamen. Sprachneutrale
  Diagramme liegen unter `docs/assets/`.
- Format PNG. Große Gesamtaufnahmen dürfen WebP sein, wenn das Projekt es
  vorsieht. Keine Bilder über etwa 500 kB — sonst zuerst den Ausschnitt
  prüfen, nicht die Qualität senken.

## Einbinden

```markdown
![Das Formular „Auftrag anlegen“. Rahmen 1 markiert das Auswahlfeld
„Typ“, Rahmen 2 das Auswahlfeld „Intervall“.](bilder/auftrag-anlegen.png)
```

- **Der Alternativtext beschreibt, was zu sehen ist**, nicht „Screenshot".
  Er ist Pflicht — für Vorlesegeräte und für Agenten.
- Relative Pfade, nie absolute Adressen.
- Das Bild steht **nach** dem Schritt, den es zeigt, nicht davor.

## Pflege

- Ändert sich die Oberfläche, werden die betroffenen Bilder im **selben
  Schritt** neu erzeugt. Ein alter Screenshot ist eine falsche Doku.
- Wo das Projekt die Aufnahme automatisiert, läuft sie in der CI und der
  Diff zeigt geänderte Bilder — dann fällt Vergessen auf.
- Bilder, die keine Doku mehr verwendet, werden gelöscht. Verwaiste
  Binärdateien bleiben sonst für immer im Verlauf.
