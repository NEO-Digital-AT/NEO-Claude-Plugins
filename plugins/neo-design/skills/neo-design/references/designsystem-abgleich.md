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
neoLayoutabgleich.vergleichen(entwurf, gebaut)

// Auf Ansage: Texte werden mitgeprüft — beide Messungen brauchen texte: true
neoLayoutabgleich.messen({ nurMarkierte: true, texte: true })
neoLayoutabgleich.vergleichen(entwurf, gebaut, { texte: true })
```

Erfasst wird dabei nur der **eigene** Text eines Elements, also die
unmittelbaren Textknoten. Die Beschriftung eines Feldes und die Aufschrift
eines Knopfes fallen darunter; die Einträge einer Auswahlliste nicht —
die stehen in Kindelementen und bleiben Inhalt. Ein einzelnes Element
lässt sich mit `data-abgleich-ohne="text"` ausnehmen.

## Drei Prüfungen, in dieser Reihenfolge

| Prüfung | Werkzeug | Antwort | Inhaltsabhängig |
| --- | --- | --- | --- |
| **1. Layoutabgleich** | `scripts/layoutabgleich.js` | Sind Maße, Abstände, Positionen und Aussehen gleich? | **nein** |
| **2. Stilabgleich** | `scripts/style-audit.js` | Stammt jeder Wert aus den Tokens? | nein |
| **3. Bildabgleich** | `scripts/bildabgleich.py` | Sieht die Fläche insgesamt gleich aus? | **ja** |

**Der Layoutabgleich ist der wichtigste.** Er misst genau das, was das
Designsystem vorgibt, und ist blind für den Inhalt: er liest den Text in
den Feldern nicht.

**Der Bildabgleich ist der schwächste und der letzte.** Er schlägt an,
sobald irgendwo ein anderer Wert steht — deshalb ist er nur dort
brauchbar, wo der Inhalt von sich aus gleich ist: beim
**Bausteine-Artboard** (Knöpfe, Felder, Abzeichen, Zustände
nebeneinander). Für eine Ansicht mit echten Daten ist er entweder mit
`--ignorieren` auf die inhaltsfreien Bereiche zu begrenzen oder
wegzulassen. Ein roter Bildabgleich wegen anderer Feldwerte ist kein
Befund, sondern ein falsch angesetztes Werkzeug.

## Marker: was mit was verglichen wird

Der Layoutabgleich muss wissen, welches Element im Entwurf welchem im
Gebauten entspricht. Das Markup unterscheidet sich zwangsläufig — ein
`<div>` im Artboard, eine `NeoField`-Komponente in der Anwendung.

**Beide Seiten tragen denselben Marker:**

```html
<!-- im Artboard -->
<select data-abgleich="feld-typ">…</select>

<!-- in der Anwendung, anderes Framework, anderes Markup -->
<NeoSelect data-abgleich="feld-typ" … />
```

- Der Marker benennt die **Rolle** des Elements, nicht seinen Inhalt:
  `feld-typ`, `knopf-speichern`, `kopfzeile`, nicht
  `select-2`.
- Markiert wird, was gemessen werden soll: Felder, Knöpfe, Karten,
  Abschnitte, Kopf- und Fußbereiche. Nicht jedes Element.
- Ohne Marker ordnet das Werkzeug über Rolle und Reihenfolge zu
  (`textfeld#1`, `knopf#2`). Das trägt für einen ersten Blick, bricht
  aber, sobald sich die Struktur unterscheidet. **Für die Abnahme werden
  Marker gesetzt** und mit `{ nurMarkierte: true }` gemessen.
- Wo der Inhalt die Größe bestimmen **soll** — ein Knopf, der mit seiner
  Beschriftung wächst —, wird das Feld einzeln ausgenommen:
  `data-abgleich-ohne="breite"`. Die Ausnahme ist sichtbar und
  begründbar, statt still hingenommen.

Marker im Artboard zu setzen kostet fünf Minuten und ist die Bedingung
dafür, dass sich das Ergebnis überhaupt messen lässt.

## Zustände: „verhält es sich gleich"

Ein Feld, das im Ruhezustand stimmt und beim Fokus einen anderen Ring
zeigt, ist nicht fertig. Gemessen wird je Zustand — der Zustand wird
ausgelöst, dann gemessen:

```js
await seite.hover('[data-abgleich="knopf-speichern"]')
const hover = await seite.evaluate(() => neoLayoutabgleich.messen({ zustand: 'hover' }))

await seite.focus('[data-abgleich="feld-adresse"]')
const fokus = await seite.evaluate(() => neoLayoutabgleich.messen({ zustand: 'fokus' }))
```

Pflichtzustände: **Ruhe, Hover, Fokus, Deaktiviert, Fehler** — und jeder
davon in Hell und Dunkel. Der Entwurf muss dieselben Zustände zeigen;
fehlen sie im Artboard, ist das der erste Befund, nicht der letzte.

## Das Verfahren

1. **Marker setzen**, im Artboard und in der Anwendung.
2. **Referenz messen und aufnehmen.** Festes Sichtfeld, fester
   Bildmaßstab, `reducedMotion: 'reduce'`, Farbschema, Sprache,
   Zeitzone, Schriften geladen. Die Messung wird als JSON unter
   `design/referenz/` eingecheckt, die Aufnahme als PNG daneben.
3. **Gebaute Ansicht messen** — identische Bedingungen. Weicht eine ab,
   vergleicht man zwei verschiedene Dinge.
4. **Layoutabgleich** je Zustand und je Fassung:

   ```js
   const e = neoLayoutabgleich.vergleichen(entwurf, gebaut, { toleranz: 1, nurMarkierte: true })
   console.log(neoLayoutabgleich.bericht(e))
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
| Breite eines Knopfes weicht ab | der Knopf wächst mit seiner Beschriftung — entweder dieselbe Beschriftung messen oder `data-abgleich-ohne="breite"` |
| Schriftart weicht ab | Schrift nicht selbst ausgeliefert oder nicht geladen |
| Text weicht ab (nur bei zugeschaltetem Textvergleich) | Wortlaut aus dem Entwurf nicht übernommen, oder der Entwurf ist neuer als die Sprachdatei |

## In der Pipeline

Layoutabgleich und Stilabgleich laufen als Testfall, der bei einem Fund
fehlschlägt; der Bildabgleich liefert einen Rückgabewert (Skill
`neo-deployment`, `references/workflows.md`).

Referenzmessungen und Referenzaufnahmen gehören ins Repository — sie
sind die Abnahmegrundlage. Unterschiedsbilder sind Erzeugnisse eines
Laufs und gehören in einen ignorierten Ordner.
