# Scrollgebundene Effekte

Lesekonvention siehe `SKILL.md`.

> **Ein Effekt, der nur in der Ruhelage geprüft wurde, gilt als
> ungeprüft.**

Angeheftete Bildflächen, durchlaufender Text, Stationen einer Galerie,
Einblenden beim Scrollen: Diese Effekte haben **keinen** einzigen
Zustand, sondern eine Abfolge. Jeder Fehler darin sitzt in genau einer
Phase — und die Ruhelage ist nie diese Phase. Deshalb wird jede Phase
einzeln gemessen.

## Die Phasen

Je Effekt gibt es mindestens diese sechs, und jede bekommt ihre eigene
Messung:

| Phase | Was dort schiefgeht |
| --- | --- |
| **Einstieg** | Die Fläche heftet sich an, der Inhalt springt |
| **Jede Station** | Die Fläche steht, Inhalt läuft darunter durch |
| **Jeder Übergang** | Zwei Stationen überblenden, beides ist gleichzeitig sichtbar |
| **Ende** | Der letzte Inhalt liegt unter der Fläche |
| **Ausstieg** | Die Fläche löst sich, der Abstand kippt |
| **Auslaufzone** | Der Verlauf wird durchsichtig — **hier scheint Inhalt durch** |

**Die letzte ist die verräterischste.** Wo die Fläche ausläuft, ist sie
nicht mehr deckend: Was darunter liegt, wird sichtbar, und was darüber
liegt, liegt plötzlich auf lesbarem Text.

## Die Prüfbreiten

Nicht die acht Standardbreiten, sondern diese — **alle**:

```
320  360  390  412      hochkant, Telefon
768 x 1024              Tablet
844 x 390               Telefon quer
1500 x 600              niedriges breites Fenster
Desktop im Querformat
```

**Das niedrige breite Fenster ist Pflicht.** Dort ist die angeheftete
Fläche flach und der Randstreifen am größten; gemessen wurden dort 90 px,
wo am Telefon 16 px auffielen.

## Was je Phase gemessen wird

Je Phase **eine Aufnahme** und diese drei Prüfungen, alle mit null
Befunden:

```js
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/surface-edge.js' })
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/text-fit.js' })
await page.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/overflow.js' })

for (const phase of phasen) {
  await page.evaluate((y) => window.scrollTo(0, y), phase)
  for (const w of ['neoSurfaceEdge', 'neoTextFit', 'neoOverflow']) {
    const e = await page.evaluate((n) => window[n].check(), w)
    const text = await page.evaluate(([n, x]) => window[n].report(x), [w, e])
    expect(e.findings, text).toHaveLength(0)
  }
}
```

| Prüfung | Werkzeug | Was sie findet |
| --- | --- | --- |
| Randstreifen | `surface-edge.js` | Die deckende Fläche reicht nicht an den Fensterrand, und Inhalt läuft darunter durch |
| Verdeckter Text | `text-fit.js` (`covered-text`) | Etwas ist über eine Textzeile gezeichnet |
| Überlauf | `overflow.js` | Die Behebung hat einen neuen Befund erzeugt |

**Die Phasen werden benannt, nicht geschätzt.** Die Scrollpositionen
stehen im Test als Liste, damit dieselbe Phase beim nächsten Lauf
dieselbe ist.

## Deckende Flächen reichen bis an beide Fensterränder

Gilt für angeheftete, fixierte und überlagernde Flächen, **unter denen
Inhalt durchläuft**. Der Fehler entsteht nicht an der Fläche, sondern am
Elternelement: dessen `padding-inline` oder `max-width` hält sie vom Rand
weg, und im Streifen dazwischen bleibt der durchlaufende Inhalt sichtbar.

- **Gemessen wird der Streifen zwischen Fläche und Fensterrand**, links
  und rechts, im deckenden **und** im auslaufenden Teil der Fläche.
- **Erlaubt für die Vollbreite ist `border-image` mit `outset`.** Es
  zeichnet außerhalb des Rahmenkastens, ohne Layout zu erzeugen, und
  produziert damit keinen Überlaufbefund.
- **Nicht erlaubt: ein Pseudo-Element mit `100vw`** und **keine negativen
  Ränder**, die einen Überlaufbefund erzeugen. Beides wurde versucht und
  war die Ursache eines neuen Befunds `content-too-wide` am Raster.
- **Eine Fläche, die absichtlich nur die Inhaltsspalte breit ist**, trägt
  `data-inset-ok` mit Grund. Ohne Vermerk gilt der Spalt als Fehler.

`surface-edge.js` nennt die Größe des Spalts, das Elternelement, das ihn
verursacht, und was darunter durchläuft. Ein Spalt ohne Inhalt darunter
ist ein **Hinweis**, kein Befund — aber kein Freibrief: Eine andere Phase
schiebt Inhalt dorthin.

## Nichts Dekoratives über Text, in keinem Zustand

Deko ist: Fortschrittsstriche, Punkte, Abzeichen, Symbole, Schatten,
Glanz, Verläufe.

- **Das gilt in Übergangs- und Auslaufzonen genauso** — dort scheint der
  Text durch die Fläche, und die Deko liegt darauf.
- **Das gilt während Animationen**, nicht nur danach.
- **Kann das Layout es auf schmalen Breiten nicht garantieren, fällt die
  Deko dort weg.** Diese Entscheidung trifft der Projektinhaber; der
  Agent legt sie mit Bild vor (Kernregel 1).
- Eine Überdeckung, die gewollt ist, trägt `data-covers-ok`. Eine
  angeheftete Fläche über der Breite des halben Fensters gilt als
  Seitenrahmen und wird nicht gemeldet — für sie gilt der Abschnitt
  darüber.

`text-fit.js` findet das mit `document.elementsFromPoint` an mehreren
Punkten je Zeile — waagrecht **und** senkrecht, weil ein 6 px hoher
Strich auf einer 20 px hohen Zeile die Mitte nicht trifft.

## Kein Fix erzeugt einen neuen Prüfbefund

**Vorher und nachher** laufen `overflow.js` und `text-fit.js` auf allen
acht Breiten, und die Befundlisten werden **verglichen**:

```
vorher:   3 Befunde   (edge-gap 2, covered-text 1)
nachher:  0 Befunde   — null neue
```

**Null neue Befunde.** Eine Behebung, die einen anderen Befund erzeugt,
wird umgebaut, bevor sie gemergt wird — nicht danach gemeldet.

## Bewegung und Leistung

- **Scroll-Handler lesen keine Geometrie.** Kein `getBoundingClientRect`
  in einem Scroll-Ereignis: das erzwingt Layout bei jedem Bildaufbau.
  Dafür gibt es `IntersectionObserver`.
- **Bei abgeschalteter Bewegung werden auch `animation-delay` und
  `transition-delay` zurückgesetzt.** Sonst bleibt Inhalt unsichtbar
  stehen, der auf ein Ereignis gewartet hätte, das nie kommt.
- **Wechselnde oder animierte Wörter reservieren den Platz der längsten
  Fassung.** Sonst verschiebt sich die Seite bei jedem Wechsel.

## Abnahme

- [ ] Je Effekt sind die Phasen **benannt** und als Scrollpositionen im
      Test festgehalten.
- [ ] Je Phase eine Aufnahme, und die Aufnahme wurde **abgesucht**
      (`pruefstand.md`).
- [ ] Je Phase: `surface-edge.js`, `text-fit.js`, `overflow.js` — **null
      Befunde**.
- [ ] Gemessen auf 320, 360, 390, 412 hochkant, 768 × 1024, 844 × 390
      quer, Desktop quer und **1500 × 600**.
- [ ] Keine Deko über Text, auch nicht in der Auslaufzone.
- [ ] Vollbreite über `border-image` mit `outset`; kein `100vw`, kein
      negativer Rand.
- [ ] Befundvergleich vorher/nachher: **null neue Befunde**.
- [ ] Jede sichtbare Korrektur mit Vorher-nachher-Bild gemeldet
      (`comparison.js`).
