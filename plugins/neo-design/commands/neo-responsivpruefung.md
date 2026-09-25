---
description: Eine Oberfläche auf allen Breiten und in allen Scrollphasen messen — kein Überlauf, nichts ragt hinaus, deckende Flächen reichen an den Rand, keine Deko über Text, Tabellen füllen, keine Löcher, Bedienziele groß genug
---

Miss die Oberfläche auf allen Prüfbreiten. **Gemessen wird, nicht
angesehen.** Erlaubt sind null Befunde.

Lade zuerst den Skill `neo-design` und `references/responsiv.md`. Gibt es
angeheftete Flächen, durchlaufenden Inhalt oder Stationen, zusätzlich
`references/scrolleffekte.md`.

## Vorbereiten

Kläre, falls es nicht im Projekt steht:

1. Welche Seiten und Dialoge gehören dazu? **Alle**, nicht die
   wichtigen — der Fehler sitzt auf der unwichtigen Seite.
2. Welche Sprachen werden ausgeliefert? Deutsche Beschriftungen sind
   länger als englische; daran bricht das Layout zuerst.
3. Hell und dunkel, und welche Zustände: gefüllt, leer, ladend, Fehler.
4. Gibt es **lange Testdaten**? Ein Name über 60 Zeichen, eine Kennung
   ohne Leerzeichen, eine achtstellige Zahl. Ein Layout, das nur mit
   kurzen Daten hält, hält nicht.
5. Welche Bereiche dürfen ausdrücklich waagrecht scrollen? Sie tragen
   `data-table-area` und `overflow-x: auto`.
6. **Gibt es scrollgebundene Effekte?** Angeheftete Bildflächen,
   durchlaufender Text, Stationen einer Galerie, Einblenden beim
   Scrollen. Wenn ja: Welche **Phasen** hat jeder Effekt, und bei welcher
   Scrollposition beginnt jede? Die Liste wird festgehalten, nicht
   geschätzt.
7. **Übernimmt die Bühne des Prüfstands die Prüfbreite?** Eine auf 1440 px
   festgenagelte Bühne nimmt den Umbruchpunkt der Anwendung nicht mit —
   dann sind die Zahlen unterhalb des Umbruchpunkts nur untereinander
   vergleichbar und keine Aussage über die Anwendung. Läuft die Uhr des
   Prüfstands? Beendet sich das Aufnahmeskript von selbst?
   `references/pruefstand.md`.

## Messen

Für **jede** Seite, jede Sprache, jede Fassung, jeden Zustand:

```js
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/overflow.js' })
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/text-fit.js' })
for (const breite of [320, 390, 768, 1024, 1280, 1920, 2560, 3840]) {
  await page.setViewportSize({ width: breite, height: 900 })
  for (const w of ['neoOverflow', 'neoTextFit']) {
    const e = await page.evaluate((n) => window[n].check(), w)
    const text = await page.evaluate(([n, x]) => window[n].report(x), [w, e])
    expect(e.findings, text).toHaveLength(0)
  }
}
```

**Beide Prüfer gehören zusammen.** Der eine misst, was hinausragt, der
andere, was innen nicht passt — und nur der erste erzeugt einen
Scrollbalken. Ein Layout, das nur den ersten besteht, kann abgeschnittenen
Text, zweizeichenbreite Spalten und Brüche mitten im Wort enthalten.

### Überlagerungen einzeln öffnen

Der Durchlauf oben misst die Seite, wie sie daliegt. **Über eine Auswahl,
ein Menü oder einen Datumswähler beweist er nichts** — die sind zu.
Deshalb je Überlagerung ein eigener Durchgang:

```js
for (const ausloeser of await page.getByRole('button', { expanded: false }).all()) {
  await ausloeser.scrollIntoViewIfNeeded()
  await ausloeser.click()
  const e = await page.evaluate(() => neoOverflow.check())
  expect(e.findings, await page.evaluate((x) => neoOverflow.report(x), e))
    .toHaveLength(0)
  await page.keyboard.press('Escape')
}
```

**Vorher in den sichtbaren Bereich scrollen**, sonst misst man die
Bildlaufstellung statt der Aufklapprichtung. Zusätzlich bei **kleiner
Höhe** (400 px, Telefon quer) — dort klappt fast alles falsch auf, was am
Schreibtisch passt.

Der Überlaufprüfer meldet zehn Arten:

| Art | Bedeutung |
| --- | --- |
| Seite scrollt waagrecht | Der Körper hat einen Balken — nie zulässig |
| Ragt über den Rand | Ein Element steht außerhalb des Bildschirms |
| Überlauf versteckt | `overflow-x: hidden` am Körper verdeckt den Fehler |
| Inhalt breiter als der Platz | Ein Element kann seinen Inhalt nicht fassen |
| Tabelle nutzt die Breite nicht / zu breit | Tabellen füllen den Inhaltsbereich |
| Loch in der umgebrochenen Reihe | Eine halbe Reihe steht leer |
| Bedienziel zu klein | Unter 44 px auf schmal, unter 24 px darüber |
| Überlagerung ragt hinaus | Hätte in die andere Richtung aufklappen müssen; der Befund nennt den freien Platz dort |
| Überlagerung abgeschnitten | Ein Vorfahre schneidet sie ab — Umklappen hilft nicht, sie gehört in eine eigene Ebene |
| Überlagerung höher als der Bildschirm | Ohne eigenen Scrollbereich ist der untere Teil unerreichbar |

Der Textpassungsprüfer meldet acht Arten:

| Art | Bedeutung |
| --- | --- |
| Text verschwindet hinter der Kante | abgeschnitten, ohne Kürzungszeichen |
| Text unten abgeschnitten | feste Höhe, mehr Text als Platz |
| Gekürzt ohne Volltext | Auslassung, und das Ganze steht nirgends |
| Texte überlappen | zwei Texte liegen übereinander — immer ein Fehler |
| Bereich zu schmal für seinen Text | unter acht Zeichen je Zeile |
| Umbruch mitten im Wort | `break-all` oder `anywhere` im Fließtext |
| Silbentrennung ohne Sprachangabe | `hyphens: auto` ohne `lang` — wirkungslos |
| Schrift zu klein | unter 12 px, auf schmal unter 14 px |
| Etwas ist über den Text gezeichnet | Deko, Abzeichen oder Verlauf auf einer Zeile — in **jeder** Phase ein Fehler |

**Auch Dialoge und geöffnete Menüs messen.** Ein geschlossenes Menü ragt
nie hinaus; ein geöffnetes schon. Also: öffnen, messen, schließen.

**Zusätzlich bei 200 % Textvergrößerung messen.** Dort fällt ein Layout
mit fester Kartenhöhe zuerst um: der Text wächst, die Karte nicht.

### Scrollphasen einzeln messen

**Die Ruhelage beweist über einen scrollgebundenen Effekt nichts.** Je
Effekt und je Phase — Einstieg, jede Station, jeder Übergang, Ende,
Ausstieg und die Auslaufzone, in der die Fläche durchsichtig wird:

```js
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/surface-edge.js' })
for (const phase of phasen) {
  await page.evaluate((y) => window.scrollTo(0, y), phase)
  await page.screenshot({ path: `phase-${phase}.png` })
  for (const w of ['neoSurfaceEdge', 'neoTextFit', 'neoOverflow']) {
    const e = await page.evaluate((n) => window[n].check(), w)
    const text = await page.evaluate(([n, x]) => window[n].report(x), [w, e])
    expect(e.findings, text).toHaveLength(0)
  }
}
```

Die Prüfbreiten sind hier andere, und **alle** sind Pflicht: 320, 360,
390 und 412 hochkant, 768 × 1024, 844 × 390 quer, Desktop quer und
**1500 × 600** — das niedrige breite Fenster, in dem der Randstreifen am
größten wird.

`surface-edge.js` meldet zwei Arten:

| Art | Bedeutung |
| --- | --- |
| Fläche reicht nicht an den Rand, Inhalt läuft darunter | Befund. Der Bericht nennt die Größe des Spalts und das Elternelement, dessen `padding-inline` oder `max-width` ihn verursacht |
| Fläche reicht nicht an den Rand, nichts läuft darunter | Hinweis, kein Befund — aber eine andere Phase kann Inhalt dorthin schieben |

`text-fit.js` meldet zusätzlich `covered-text`: etwas ist über eine
Textzeile gezeichnet. Eine angeheftete Fläche über der halben
Fensterbreite gilt als Seitenrahmen und wird dort nicht gemeldet; für sie
gilt die Randstreifenprüfung.

**Jede Phase bekommt eine Aufnahme, und jede Aufnahme wird abgesucht** —
Ränder, Ecken, Übergänge, Überlagerungen (`references/pruefstand.md`).

## Deuten

**Zuerst den Prüfstand ausschließen.** Koppeln die gemeldeten Paare
ausnahmslos ein Element der einen Spalte mit einem der anderen, und
überlappt **innerhalb** einer Spalte nichts, ist die Bühne zu breit und
nicht die Anwendung zu eng (`references/pruefstand.md`). Ein Befund, der
nur im Prüfstand auftritt, wird nicht gemeldet.

Danach in dieser Reihenfolge, weil jede Ursache die folgenden erzeugt:

1. **Ragt über den Rand** — die Wurzelursache. Meist eine feste
   Pixelbreite, eine lange Kennung ohne Umbruch, oder ein fehlendes
   `min-width: 0` an einem Flex-Kind.
2. **Seitenüberlauf** — meist nur die Folge von 1. Erst 1 beheben.
3. **Inhalt breiter als der Platz** — dasselbe eine Ebene tiefer.
4. **Abgeschnittener Text** — dort ist Information weg, das wiegt
   schwerer als alles Folgende. Feste Höhe oder feste Breite an einem
   Kasten, der mitwachsen müsste.
5. **Loch in der Reihe** — die Kacheln brechen um, ohne dass das letzte
   Element füllt. Zwei erlaubte Auflösungen stehen in
   `references/responsiv.md`.
6. **Tabelle zu schmal** — feste Breite statt `width: 100%`.
7. **Bereich zu schmal für seinen Text** — die Spalte wird weggelassen
   oder zur Karte, nicht schmaler gemacht (`references/textpassung.md`).
8. **Umbruch mitten im Wort** — `hyphens: auto` **plus** `lang` für
   Fließtext, `overflow-wrap: anywhere` nur für Kennungen.
9. **Bedienziel zu klein** — meist Symbolknöpfe in Tabellenzeilen.

`overflow-x: hidden` am Körper ist **nie** die Behebung. Es versteckt den
Befund und macht den Inhalt unerreichbar.

## Berichten

Je Seite eine Zeile, je Breite eine Spalte:

```
Seite            320  390  768 1024 1280 1920 2560 3840
/uebersicht       0    0    0    0    0    0    0    0   bestanden
/auftraege        3    3    1    0    0    0    0    2   nicht bestanden
/auftraege/:id    0    0    0    0    0    0    0    0   bestanden
```

Für jede nicht bestandene Zelle: die Befunde aus dem Bericht, mit
Fundstelle, die vermutete Ursache nach der Liste oben und der Vorschlag
zur Behebung.

**Nichts reparieren, solange der Umfang nicht freigegeben ist.** Nach der
Freigabe: beheben, **erneut messen**, die neuen Zahlen nennen.

**Der Befundvergleich entscheidet, nicht der Eindruck.** Vorher und
nachher laufen `overflow.js` und `text-fit.js` auf allen acht Breiten, und
der Vergleich zeigt **null neue Befunde**. Eine Behebung, die einen
anderen Befund erzeugt — etwa ein Pseudo-Element mit `100vw`, das
`content-too-wide` auslöst —, wird umgebaut, bevor sie gemergt wird.

**Ein gemeldeter Mangel ist eine Befundklasse.** Dieselbe Ursache wird
überall gesucht: andere Seite, anderes Ende, andere Breiten, jede Seite
mit derselben Komponente. Alle Fundstellen werden genannt.

**Jede sichtbare Korrektur wird mit einem Vorher-nachher-Bild gemeldet**,
die Stelle markiert (`scripts/comparison.js`).

Am Ende eine Zeile mit Zahlen, nicht mit einer Einschätzung: wie viele
Seiten × Breiten × Sprachen geprüft, wie viele bestanden. Solange eine
Zelle Befunde hat, lautet die Antwort nein. Danach die Abnahmeliste
`references/pruefliste.md`.
