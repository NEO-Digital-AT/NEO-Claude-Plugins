---
description: Eine Oberfläche auf allen Breiten messen — kein Überlauf, nichts ragt hinaus, Tabellen füllen, keine Löcher, Bedienziele groß genug
---

Miss die Oberfläche auf allen Prüfbreiten. **Gemessen wird, nicht
angesehen.** Erlaubt sind null Befunde.

Lade zuerst den Skill `neo-design` und `references/responsiv.md`.

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
   `data-tabellenbereich` und `overflow-x: auto`.

## Messen

Für **jede** Seite, jede Sprache, jede Fassung, jeden Zustand:

```js
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/ueberlauf.js' })
for (const breite of [320, 390, 768, 1024, 1280, 1920, 2560, 3840]) {
  await page.setViewportSize({ width: breite, height: 900 })
  const e = await page.evaluate(() => neoUeberlauf.pruefen())
  const text = await page.evaluate((x) => neoUeberlauf.bericht(x), e)
  expect(e.befunde, text).toHaveLength(0)
}
```

Der Prüfer meldet sechs Arten:

| Art | Bedeutung |
| --- | --- |
| Seite scrollt waagrecht | Der Körper hat einen Balken — nie zulässig |
| Ragt über den Rand | Ein Element steht außerhalb des Bildschirms |
| Überlauf versteckt | `overflow-x: hidden` am Körper verdeckt den Fehler |
| Inhalt breiter als der Platz | Ein Element kann seinen Inhalt nicht fassen |
| Tabelle nutzt die Breite nicht / zu breit | Tabellen füllen den Inhaltsbereich |
| Loch in der umgebrochenen Reihe | Eine halbe Reihe steht leer |
| Bedienziel zu klein | Unter 44 px auf schmal, unter 24 px darüber |

**Auch Dialoge und geöffnete Menüs messen.** Ein geschlossenes Menü ragt
nie hinaus; ein geöffnetes schon. Also: öffnen, messen, schließen.

## Deuten

In dieser Reihenfolge, weil jede Ursache die folgenden erzeugt:

1. **Ragt über den Rand** — die Wurzelursache. Meist eine feste
   Pixelbreite, eine lange Kennung ohne Umbruch, oder ein fehlendes
   `min-width: 0` an einem Flex-Kind.
2. **Seitenüberlauf** — meist nur die Folge von 1. Erst 1 beheben.
3. **Inhalt breiter als der Platz** — dasselbe eine Ebene tiefer.
4. **Loch in der Reihe** — die Kacheln brechen um, ohne dass das letzte
   Element füllt. Zwei erlaubte Auflösungen stehen in
   `references/responsiv.md`.
5. **Tabelle zu schmal** — feste Breite statt `width: 100%`.
6. **Bedienziel zu klein** — meist Symbolknöpfe in Tabellenzeilen.

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

Am Ende eine Zeile mit Zahlen, nicht mit einer Einschätzung: wie viele
Seiten × Breiten × Sprachen geprüft, wie viele bestanden. Solange eine
Zelle Befunde hat, lautet die Antwort nein. Danach die Abnahmeliste
`references/pruefliste.md`.
