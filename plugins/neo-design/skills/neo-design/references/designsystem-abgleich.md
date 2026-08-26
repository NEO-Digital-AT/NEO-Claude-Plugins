# Abgleich mit dem Designsystem

## Das Problem

Ein Designsystem aus Claude Design liegt als HTML-Artboards vor, oft in
React-Nähe. Gebaut wird in Nuxt mit Vue, in Flutter oder in Contao. Der
Agent liest das System, baut — und es sieht **ähnlich** aus, nicht gleich.

Der Grund: „Ich habe das Designsystem gelesen" ist keine Prüfung. Ohne
Messung fällt die Abweichung erst dem Projektinhaber auf, und dann ist
sie überall.

## Die Regel

**Fertig heißt gemessen.** Eine Ansicht, die gegen ein Designsystem
gebaut wurde, gilt erst als fertig, wenn **beide** Prüfungen bestanden
sind und die Zahlen berichtet wurden:

| Prüfung | Werkzeug | Was sie beantwortet |
| --- | --- | --- |
| **Bildabgleich** | `scripts/bildabgleich.py` | Sieht es aus wie im Entwurf? |
| **Stilabgleich** | `scripts/stilabgleich.js` | Stammt jeder Wert aus den Tokens? |

Der Bildabgleich sagt **dass** etwas anders ist, der Stilabgleich sagt
**warum**. Einer allein reicht nicht: eine Ansicht kann pixelnah
aussehen und trotzdem erfundene Werte tragen, und sie kann jeden Token
verwenden und trotzdem falsch angeordnet sein.

„Sieht gut aus" ist keine Zahl. Wer keine Zahl nennt, hat nicht geprüft.

## Das Verfahren

### 1. Referenzaufnahme aus dem Designsystem

Das Artboard im Browser öffnen und mit festen Bedingungen aufnehmen:

```js
const kontext = await browser.newContext({
  viewport: { width: 1440, height: 900 },   // Maß des Artboards
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
  colorScheme: 'light',
})
const seite = await kontext.newPage()
await seite.goto(artboardAdresse)
await seite.evaluate(() => document.fonts.ready)
await seite.screenshot({ path: 'design/referenz/knoepfe.png' })
```

Die Referenzaufnahmen werden **ins Repository eingecheckt**, unter
`design/referenz/`. Sie sind die Abnahmegrundlage und müssen bei einer
Änderung des Designsystems neu erzeugt werden.

### 2. Dieselbe Ansicht in der gebauten Anwendung

**Identisches Sichtfeld, identischer Bildmaßstab, dieselben Bedingungen.**
Weicht eines davon ab, vergleicht man zwei verschiedene Dinge, und das
Werkzeug weist es mit einer Meldung ab.

### 3. Bildabgleich

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bildabgleich.py \
  design/referenz/knoepfe.png .abgleich/knoepfe.png \
  --unterschied .abgleich/knoepfe-diff.png --schwelle 0.5
```

Das Unterschiedsbild markiert jede abweichende Stelle magenta und lässt
den Rest blass stehen. **Es wird angesehen, nicht nur die Zahl gelesen** —
0,4 % an der falschen Stelle können ein falscher Primärknopf sein.

Bereiche mit veränderlichem Inhalt (Uhrzeit, Zähler) werden ausgenommen:
`--ignorieren x,y,breite,hoehe`, mehrfach angebbar.

### 4. Stilabgleich

```js
await seite.addScriptTag({ path: '<plugin>/scripts/stilabgleich.js' })
const bericht = await seite.evaluate(() => neoStilabgleich.pruefen())
console.log(await seite.evaluate((b) => neoStilabgleich.bericht(b), bericht))
```

Er liest die **berechneten** Stile jedes Elements und meldet jede Farbe,
jeden Radius, jede Schriftgröße und jeden Schatten, der nicht aus den
Tokens stammt. Er arbeitet am fertigen DOM und ist deshalb unabhängig
vom Framework.

Ohne Angabe liest er die Tokens aus den CSS-Eigenschaften der Wurzel
(`--neo-*`, `--leoflex-*`). Wer eine `tokens.json` hat, übergibt sie:
`neoStilabgleich.pruefen({ tokens: … })`. Mit `{ abstaende: true }`
werden zusätzlich Polster, Außenabstände und Lücken geprüft.

### 5. Wiederholen, bis es stimmt

Nicht einmal messen und dann behaupten. Nach jeder Korrektur erneut
messen, bis beide Prüfungen bestehen. Erst dann fällt das Wort „fertig".

## Was womit verglichen wird

| Gegenstand | Prüfung | Schwelle |
| --- | --- | --- |
| Bausteine-Artboard (Knöpfe, Felder, Abzeichen, Zustände nebeneinander) | Bild **und** Stil | **0,5 %** — hier ist Pixelnähe erreichbar und verlangt |
| Ganze Ansicht mit echten Daten | Bild **und** Stil | **2 %** — Inhalte weichen ab, Anordnung nicht |
| Hell- und Dunkelfassung | beide, je Fassung | wie oben |
| Mobile Fassung | beide, je Breite | wie oben |
| **Stilabgleich, immer** | Stil | **0 Funde.** Ein erfundener Wert ist kein Rundungsfehler |

Der Bausteine-Artboard ist der wichtigste Vergleich: stimmen die
Bausteine, stimmen die Seiten fast von selbst. Wer nur ganze Seiten
vergleicht, sucht Fehler an der falschen Stelle.

## Framework-Übersetzung

**Das Designsystem ist die Quelle für Werte und Aussehen, nicht für
Code.**

- Claude Design liefert HTML und CSS, oft in React-Nähe. **Dieser Code
  wird nie in ein Vue-, Nuxt-, Flutter- oder Contao-Projekt kopiert.**
- Übernommen werden: die **Tokens** (unverändert, nicht nachgebaut), die
  Maße, die Zustände, die Anordnung.
- Gebaut wird in den Wrapper-Komponenten der Produktfamilie mit den
  Mitteln des Zielframeworks (Skill `neo-komponenten`).
- Gemessen wird gegen das Artboard. Der Weg dorthin ist frei, das
  Ergebnis nicht.
- **Die Tokens werden übernommen, nicht abgetippt.** Ein von Hand
  übertragener Farbwert ist der erste Ort, an dem das System auseinander
  läuft.

## Häufige Ursachen einer Abweichung

Wenn der Bildabgleich anschlägt, in dieser Reihenfolge suchen:

| Ursache | Woran man sie erkennt |
| --- | --- |
| Schrift nicht geladen oder nicht selbst ausgeliefert | Text an allen Stellen leicht versetzt, gleiche Farbe |
| Andere Zeilenhöhe oder Laufweite | Text stimmt am Anfang, wandert nach unten auseinander |
| UA-Stylesheet nicht zurückgesetzt | Knöpfe, Felder und Listen weichen ab, Text nicht |
| `box-sizing` unterschiedlich | Alles mit Rahmen und Polster ist ein paar Pixel zu groß |
| Token abgetippt statt übernommen | Eine einzelne Farbe weicht ab — der Stilabgleich nennt sie |
| Radius aus der falschen Stufe | Nur die Ecken sind magenta |
| Unterschiedlicher Bildmaßstab | Alles ist unscharf abweichend, nichts stimmt genau |
| Animation lief noch | Abweichung wandert zwischen zwei Läufen |

## In der Pipeline

Beide Prüfungen laufen als Tor (Skill `neo-deployment`,
`references/workflows.md`). Der Bildabgleich liefert einen
Rückgabewert; der Stilabgleich wird in einem Testlauf ausgewertet und
schlägt bei einem Fund fehl.

Referenzaufnahmen und Unterschiedsbilder gehören ins Repository, die
Unterschiedsbilder als Erzeugnis in einen ignorierten Ordner — sie sind
Beleg für einen Lauf, nicht Bestand.
