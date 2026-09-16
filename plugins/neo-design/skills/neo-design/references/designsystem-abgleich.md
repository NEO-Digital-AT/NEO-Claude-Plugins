# Abgleich mit dem Designsystem

Dieser Text beschreibt **wie gemessen wird**. Wie **gebaut** wird und
wer welche Entscheidung trifft, steht in `claude-design.md` — beim Bau
nach einem Entwurf gilt jener Text und ist zuerst zu lesen.

## Das Problem

Ein Designsystem aus Claude Design liegt als HTML-Artboards vor, oft in
React-Nähe. Gebaut wird in Nuxt mit Vue, in Flutter oder in Contao. Der
Agent liest das System, baut — und es sieht **ähnlich** aus, nicht gleich.

Der Grund: „Ich habe das Designsystem gelesen" ist keine Prüfung. Ohne
Messung fällt die Abweichung erst dem Projektinhaber auf, und dann ist
sie überall.

## Was verglichen wird — und was ausdrücklich nicht

**Verglichen wird das Aussehen und das Verhalten, nicht der Inhalt.**

| Immer verglichen | Nie verglichen |
| --- | --- |
| Breite und Höhe eines Feldes | der Wert **in** einem Feld |
| Wo ein Element steht, relativ zu den anderen | Anzahl und Text der Einträge einer Auswahlliste |
| Abstände, Lücken, Polster, Randstärken | Namen, Zahlen, Datumsangaben, Zählstände |
| Radien, Farben, Schriftgröße, Zeilenhöhe, Laufweite | Daten aus der Datenbank oder aus fremden APIs |
| Verhalten in Hover, Fokus, Deaktiviert, Fehler | — |

Inhalte sind dynamisch. Die Einträge einer Auswahlliste kommen aus der
Anwendung, ein Feldwert aus der Datenbank, eine Liste aus einer fremden
API. Dass dort etwas anderes steht als im Entwurf, ist **kein
Mangel**. Dass das Feld vier Pixel niedriger ist, schon.

### Statische Oberflächentexte: auf Ansage

Zwischen beiden Spalten steht eine dritte Sorte: **Beschriftungen,
Knopftexte, Überschriften, Hilfetexte, Fehlermeldungen und
Leerzustände.** Sie sind kein dynamischer Inhalt, sondern Teil des
Entwurfs — der Entwurf gibt den **Wortlaut** vor, die Sprachdatei ist
nur sein Ort (`oberflaechentexte.md`).

Verglichen werden sie trotzdem **nur auf ausdrückliche Ansage des
Projektinhabers**, weil sie sich im Bau oft noch ändern:

```js
// Standard: Texte bleiben außen vor
neoLayoutDiff.compare(entwurf, gebaut)

// Auf Ansage: Texte werden mitgeprüft — beide Messungen brauchen text: true
neoLayoutDiff.measure({ markedOnly: true, text: true })
neoLayoutDiff.compare(entwurf, gebaut, { text: true })
```

Erfasst wird dabei nur der **eigene** Text eines Elements, also die
unmittelbaren Textknoten. Die Beschriftung eines Feldes und die Aufschrift
eines Knopfes fallen darunter; die Einträge einer Auswahlliste nicht —
die stehen in Kindelementen und bleiben Inhalt. Ein einzelnes Element
lässt sich mit `data-compare-except="text"` ausnehmen.

## Drei Prüfungen, in dieser Reihenfolge

| Prüfung | Werkzeug | Antwort | Inhaltsabhängig |
| --- | --- | --- | --- |
| **1. Layoutabgleich** | `scripts/layout-diff.js` | Sind Maße, Abstände, Positionen und Aussehen gleich? | **nein** |
| **2. Stilabgleich** | `scripts/style-audit.js` | Stammt jeder Wert aus den Tokens? | nein |
| **3. Bildabgleich** | `scripts/image-diff.py` | Sieht die Fläche insgesamt gleich aus? | **ja** |

**Der Layoutabgleich ist der wichtigste.** Er misst genau das, was das
Designsystem vorgibt, und ist blind für den Inhalt: er liest den Text in
den Feldern nicht.

**Der Bildabgleich ist der schwächste und der letzte.** Er schlägt an,
sobald irgendwo ein anderer Wert steht — deshalb ist er nur dort
brauchbar, wo der Inhalt von sich aus gleich ist: beim
**Bausteine-Artboard** (Knöpfe, Felder, Abzeichen, Zustände
nebeneinander). Für eine Ansicht mit echten Daten ist er entweder mit
`--ignore` auf die inhaltsfreien Bereiche zu begrenzen oder
wegzulassen. Ein roter Bildabgleich wegen anderer Feldwerte ist kein
Befund, sondern ein falsch angesetztes Werkzeug.

## Liegt ein Gastsystem vor: zwei Vorlagen, keine einzelne Zahl

Manche Produkte werden in ein fremdes System eingebettet oder stehen
unmittelbar daneben — eine Erweiterung, ein eingebundenes Modul, eine
Oberfläche, die sich in die eines Anbieters einfügen soll. Dann
konkurrieren **zwei** Vorlagen: das Designset des eigenen Produkts und
das Gastsystem.

**Das Problem ist die eine Zahl.** Der Bildabgleich gegen das Designset
liefert eine Prozentzahl. Sobald eine Entscheidung zugunsten des
Gastsystems fällt — dessen Typografie, dessen Bedienelemente —, wird
diese Zahl **schlechter**, obwohl das Ergebnis **richtiger** ist. Sie
mischt damit „bewusst anders" mit „versehentlich anders" und verliert
ihre Aussagekraft. Wer sie weiter als Fortschrittsmaß liest, arbeitet
gegen die eigene Entscheidung.

### Die Rangfolge steht vor der ersten Messung

Sobald ein Gastsystem im Spiel ist, wird eine Rangfolge **festgelegt und
schriftlich hinterlegt**, bevor gemessen wird. Bewährt hat sich diese
Aufteilung:

| Frage | Entscheidet |
| --- | --- |
| Was gibt es, wie ist es angeordnet? Aufbau, Reihenfolge, welche Bedienelemente vorkommen, Zustände | das **Designset** |
| Wie liest und bedient es sich? Schriftgrößen, Zeilenhöhen, Schnitte, Maße der Bedienelemente, Trefferflächen | das **Gastsystem** |
| Wofür das Gastsystem kein Gegenstück hat | das **Designset**, aber in der Typografie und mit den Bedienelementen des Gastsystems |
| Beide schweigen | **Rückfrage** — nichts erfinden |

Die Rückfrage in der letzten Zeile läuft wie jede andere: vier Teile,
mit Gegenüberstellungsbild aus `scripts/comparison.js`
(`claude-design.md`).

### Berichtet wird getrennt

- Der Bericht weist Abweichungen **getrennt** aus: solche, die aus einer
  **entschiedenen** Gastsystem-Regel folgen, und solche, die **niemand
  entschieden** hat. Nur die zweite Gruppe ist ein Mangel.
- **Eine Gesamtzahl, die beides vermengt, wird nicht genannt.** Gelingt
  die Trennung an einer Stelle nicht sauber, wird das gesagt, statt eine
  mehrdeutige Zahl zu nennen.

### Die Werte des Gastsystems werden gemessen

Sie werden nicht schätzungsweise übernommen: echte Bildschirme des
Gastsystems rendern und die **gerechneten** Stilwerte auslesen. Aus dem
Stylesheet gelesene Werte reichen nicht, weil Vererbung,
Überschreibungen und Vorgaben des Browsers erst im gerechneten Wert
zusammenkommen.

**Eine verbreitete Falle dabei:** Gastsysteme schreiben Zeilenhöhen oft
**absolut** (etwa in `rem`), nicht als Verhältnis. Wer die Zahl ohne
Einheit übernimmt, setzt den Text je nach Schriftgröße enger oder weiter
als das Gastsystem.

## Marker: was mit was verglichen wird

Der Layoutabgleich muss wissen, welches Element im Entwurf welchem im
Gebauten entspricht. Das Markup unterscheidet sich zwangsläufig — ein
`<div>` im Artboard, eine `NeoField`-Komponente in der Anwendung.

**Beide Seiten tragen denselben Marker:**

```html
<!-- im Artboard -->
<select data-compare="feld-typ">…</select>

<!-- in der Anwendung, anderes Framework, anderes Markup -->
<NeoSelect data-compare="feld-typ" … />
```

- Der Marker benennt die **Rolle** des Elements, nicht seinen Inhalt:
  `feld-typ`, `knopf-speichern`, `kopfzeile`, nicht
  `select-2`.
- Markiert wird, was gemessen werden soll: Felder, Knöpfe, Karten,
  Abschnitte, Kopf- und Fußbereiche. Nicht jedes Element.
- Ohne Marker ordnet das Werkzeug über Rolle und Reihenfolge zu
  (`textfeld#1`, `knopf#2`). Das trägt für einen ersten Blick, bricht
  aber, sobald sich die Struktur unterscheidet. **Für die Abnahme werden
  Marker gesetzt** und mit `{ markedOnly: true }` gemessen.
- Wo der Inhalt die Größe bestimmen **soll** — ein Knopf, der mit seiner
  Beschriftung wächst —, wird das Feld einzeln ausgenommen:
  `data-compare-except="breite"`. Die Ausnahme ist sichtbar und
  begründbar, statt still hingenommen.

Marker im Artboard zu setzen kostet fünf Minuten und ist die Bedingung
dafür, dass sich das Ergebnis überhaupt messen lässt.

## Zustände: „verhält es sich gleich"

Ein Feld, das im Ruhezustand stimmt und beim Fokus einen anderen Ring
zeigt, ist nicht fertig. Gemessen wird je Zustand — der Zustand wird
ausgelöst, dann gemessen:

```js
await seite.hover('[data-compare="knopf-speichern"]')
const hover = await seite.evaluate(() => neoLayoutDiff.measure({ state: 'hover' }))

await seite.focus('[data-compare="feld-adresse"]')
const fokus = await seite.evaluate(() => neoLayoutDiff.measure({ state: 'focus' }))
```

Pflichtzustände: **Ruhe, Hover, Fokus, Deaktiviert, Fehler** — und jeder
davon in Hell und Dunkel. Der Entwurf muss dieselben Zustände zeigen;
fehlen sie im Artboard, ist das der erste Befund, nicht der letzte.

## Das Verfahren

**Vor Schritt 1:** Liegt ein Gastsystem vor, steht dessen Rangfolge
schriftlich fest — sonst misst man gegen eine Vorlage, die gar nicht
gilt. Und der Prüfstand, in dem gemessen wird, ist selbst geprüft:
laufende Uhr, mitwachsende Bühne, Aufnahmeskript, das sich beendet
(`pruefstand.md`).

1. **Marker setzen**, im Artboard und in der Anwendung.
2. **Referenz messen und aufnehmen.** Festes Sichtfeld, fester
   Bildmaßstab, `reducedMotion: 'reduce'`, Farbschema, Sprache,
   Zeitzone, Schriften geladen. Die Messung wird als JSON unter
   `design/referenz/` eingecheckt, die Aufnahme als PNG daneben.
3. **Gebaute Ansicht messen** — identische Bedingungen. Weicht eine ab,
   vergleicht man zwei verschiedene Dinge.
4. **Layoutabgleich** je Zustand und je Fassung:

   ```js
   const e = neoLayoutDiff.compare(entwurf, gebaut, { tolerance: 1, markedOnly: true })
   console.log(neoLayoutDiff.report(e))
   ```

   Der Bericht bündelt dieselbe Abweichung über mehrere Elemente zu
   einem Fund — ein falscher Radius-Token erzeugt eine Zeile, nicht
   sechzehn. Ein gleichmäßiger Versatz aller Elemente wird als ein
   Befund gemeldet, nicht als hundert.
5. **Stilabgleich** gegen die laufende Ansicht.
6. **Bildabgleich** für den Bausteine-Artboard, mit Unterschiedsbild.
7. **Beheben, erneut messen, Zahlen nennen.** So oft, bis alles besteht.

## Schwellen

| Prüfung | Gegenstand | Schwelle |
| --- | --- | --- |
| Layoutabgleich | jede Ansicht, jeder Zustand, jede Fassung | **0 Abweichungen** bei Toleranz 1 px |
| Layoutabgleich mit Texten | nur auf Ansage des Projektinhabers | **0 Abweichungen** |
| Stilabgleich | jede Ansicht | **0 Funde** |
| Bildabgleich | Bausteine-Artboard | **0,5 %** |
| Bildabgleich | Ansicht mit echten Daten | nur mit ausgenommenen Inhaltsbereichen, sonst weglassen |
| Bildabgleich | Ansicht neben einem Gastsystem | **keine Gesamtzahl** — getrennt nach entschieden und unentschieden |

Die Toleranz von 1 px deckt Rundung ab, nicht Nachlässigkeit. Wer sie
höher setzt, begründet es an Ort und Stelle.

## Framework-Übersetzung

**Das Designsystem ist die Quelle für Werte und Aussehen, nicht für
Code.**

- Claude Design liefert HTML und CSS, oft in React-Nähe. **Dieser Code
  wird nie in ein Vue-, Nuxt-, Flutter- oder Contao-Projekt kopiert.**
- Übernommen werden: die **Tokens** (unverändert, nicht abgetippt), die
  Maße, die Abstände, die Zustände, die Anordnung.
- Gebaut wird in den Wrapper-Komponenten der Produktfamilie mit den
  Mitteln des Zielframeworks (Skill `neo-komponenten`).
- Gemessen wird gegen das Artboard. Der Weg dorthin ist frei, das
  Ergebnis nicht.

## Ursachen einer Abweichung

| Befund im Layoutabgleich | Übliche Ursache |
| --- | --- |
| Höhe eines Feldes weicht ab | andere Feldhöhe im Token, oder `box-sizing` nicht gesetzt |
| Polster weicht ab, Höhe stimmt | Polster hart geschrieben statt aus der Skala |
| Lücke zwischen Feldern weicht ab | Abstand über Außenabstand statt über `gap`, oder falsche Stufe |
| Alle Radien weichen gleich ab | ein Token abgetippt statt übernommen |
| Zeilenhöhe weicht ab, Schriftgröße stimmt | Zeilenhöhe als Zahl gegen Zeilenhöhe in Pixeln |
| Gleichmäßiger Versatz aller Elemente | anderer Außenabstand oder anderes Polster an der Wurzel |
| Nur ein Element sitzt falsch | fehlender Umbruch, falsche Ausrichtung im Flex-Bereich |
| Breite eines Knopfes weicht ab | der Knopf wächst mit seiner Beschriftung — entweder dieselbe Beschriftung messen oder `data-compare-except="breite"` |
| Schriftart weicht ab | Schrift nicht selbst ausgeliefert oder nicht geladen |
| Text weicht ab (nur bei zugeschaltetem Textvergleich) | Wortlaut aus dem Entwurf nicht übernommen, oder der Entwurf ist neuer als die Sprachdatei |

## In der Pipeline

Layoutabgleich und Stilabgleich laufen als Testfall, der bei einem Fund
fehlschlägt; der Bildabgleich liefert einen Rückgabewert (Skill
`neo-deployment`, `references/workflows.md`).

Referenzmessungen und Referenzaufnahmen gehören ins Repository — sie
sind die Abnahmegrundlage. Unterschiedsbilder sind Erzeugnisse eines
Laufs und gehören in einen ignorierten Ordner.
