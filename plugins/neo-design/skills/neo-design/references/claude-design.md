# Bauen nach Claude Design

Lesekonvention siehe `SKILL.md`. **Dieser Text ist die strengste Regel
des gesamten Regelwerks.** Sie kennt keinen Freigabeweg über
Zeitdruck, keinen über „das ist besser so" und keinen über „das war
offensichtlich gemeint".

## Der Satz, um den es geht

> **Claude Design gibt vor. Der Agent setzt um. Der Agent gestaltet
> nicht.**

Der Projektinhaber hat den Entwurf gemacht. Er hat ein Bild vor Augen.
Der Auftrag lautet, **dieses Bild zu bauen** — nicht ein ähnliches, nicht
ein besseres, nicht eines, das der Agent für sinnvoller hält.

**Der bekannte Fehlerfall, offen benannt:** Der Agent liest das
Designsystem, baut daraufhin etwas Eigenes und liefert es als Umsetzung
ab. Das Ergebnis sieht plausibel aus und hat mit dem Entwurf wenig zu
tun. Genau das verhindert dieser Text. Jede Regel hier existiert, weil
sie schon einmal übergangen wurde.

## Was vorgegeben ist — und was die Aufgabe bestimmt

Die Trennlinie läuft zwischen **Gestaltung** und **Fachlichkeit**, nicht
zwischen wichtig und unwichtig.

| **Gestaltung — vom Designsystem vorgegeben.** Abweichung nur nach Rückfrage. | **Fachlichkeit — von der Aufgabe bestimmt.** Darf abweichen, ohne zu fragen. |
| --- | --- |
| Aufbau der Seite: Reihenfolge der Abschnitte, Raster, Spaltigkeit, Breiten, Ränder | — |
| Aussehen einer Karte: Polster, Radius, Rand, Schatten, Kopf, Fuß, Trennlinien | — |
| Aussehen eines Feldes: Höhe, Polster, Radius, Rand, Lage der Beschriftung, Lage des Hilfetexts, Lage der Fehlermeldung | — |
| Abstände: zwischen Feldern, zwischen Gruppen, zwischen Abschnitten, zum Rand | — |
| Typografie: Größen, Gewichte, Zeilenhöhen, Laufweiten, Hierarchie | — |
| Farben, Zustände, Bewegung, Symbole | — |
| Aufbau eines Formulars: ein- oder zweispaltig, Gruppierung, Lage der Aktionen, Reihenfolge der Gruppen | — |
| Aufbau einer Tabelle: Kopf, Zeilenhöhe, Zellpolster, Trennlinien, Lage der Aktionen | — |
| — | **Welche** Felder ein Formular hat: mehr, weniger, andere |
| — | **Welche** Werte in einer Auswahl, Combobox oder Autovervollständigung stehen |
| — | Pflicht oder optional, Prüfregeln, Abhängigkeiten zwischen Feldern |
| — | Beschriftungen und Hilfetexte, wo die Fachlichkeit sie vorgibt |
| — | Verhalten: was beim Absenden passiert, welche Meldung erscheint |
| — | Anzahl der Zeilen, Spalten und Einträge, die aus Daten kommen |

**Der Merksatz:**

> **Ein Feld mehr ist normal. Ein Feld, das anders aussieht als die
> Felder im Designsystem, ist ein Fehler.**

Ein Formular mit sieben statt fünf Feldern ist in Ordnung — solange die
sieben Felder dieselbe Höhe, dasselbe Polster, denselben Radius,
denselben Abstand und dieselbe Beschriftungslage haben wie die fünf im
Entwurf, in derselben Karte, mit denselben Aktionen am selben Platz.

Wo der Entwurf für ein fachlich nötiges Element **kein Vorbild** hat —
ein Bauteil, das es dort schlicht nicht gibt —, ist das eine
**Rückfrage**, keine Erfindung.

## Die verbotenen Entscheidungen

Diese Entscheidungen trifft der Agent **nie**. Kein Freigabeweg, keine
Ausnahme, keine Abwägung. Jede einzelne davon ist eine Rückfrage:

1. Ein anderes Layout als im Entwurf — andere Spaltigkeit, andere
   Reihenfolge, andere Gruppierung.
2. Ein anderer Abstand, ein anderes Polster, ein anderer Radius.
3. Eine andere Schriftgröße, ein anderes Gewicht, eine andere
   Zeilenhöhe.
4. Eine andere Farbe, auch wenn sie aus den Tokens stammt.
5. Ein anderes Bauteil für dieselbe Aufgabe — Karte statt Abschnitt,
   Reiter statt Auswahl, Dialog statt Seite.
6. Ein Bauteil, das im Entwurf nicht vorkommt.
7. Ein Bauteil des Entwurfs weglassen, weil es „hier nicht passt".
8. Eine andere Lage der Aktionen.
9. Ein anderes Verhalten beim Umbrechen auf schmale Breiten.
10. Ein anderer Zustand als der im Entwurf gezeigte.
11. Ein anderer Text, wo der Entwurf einen vorgibt und die Fachlichkeit
    keinen anderen verlangt.
12. Eine Zusammenführung zweier Entwürfe oder eines Entwurfs mit einer
    bestehenden Seite.

**Eine Empfehlung ist erlaubt. Eine Entscheidung nicht.** Der Agent darf
sagen, was er für richtig hält — und muss dann warten.

## Vor der ersten Zeile: das Inventar

**Wer baut, ohne das Inventar geschrieben zu haben, hat die Regel bereits
verletzt.**

Das Inventar entsteht aus dem Artboard, von oben nach unten, und listet
**jedes** Element mit seinen Maßen:

```markdown
## Inventar — Artboard „Auftrag anlegen" (1440 px, hell)

| # | Element | Marker | Maße und Aussehen aus dem Entwurf |
|---|---|---|---|
| 1 | Seitenkopf | kopf | Höhe 60, Polster 0/24, Trennlinie unten 1 px --neo-border |
| 2 | Brotkrume | brotkrume | 13 px, --neo-fg-muted, Abstand unten 16 |
| 3 | Überschrift H1 | titel | 28 px / 1.1, Gewicht 700, Abstand unten 8 |
| 4 | Beschreibung | beschreibung | 13 px, --neo-fg-muted, Abstand unten 24 |
| 5 | Karte Grunddaten | karte-grunddaten | Polster 24, Radius 14, Rand 1 px, kein Schatten |
| 6 | ├ Feldgruppe | feldgruppe | Spalte, Lücke 20 |
| 7 | ├ Feld Bezeichnung | feld-bezeichnung | Höhe 40, Polster 0/12, Radius 10, Beschriftung darüber 13 px, Abstand 6 |
| 8 | └ Feld Typ | feld-typ | wie 7 |
| 9 | Fußzeile der Karte | karte-fuss | Aktionen rechts, Lücke 12, Abstand oben 24 |
| 10 | Knopf sekundär | knopf-abbrechen | Höhe 40, Polster 0/18, Radius 10 |
| 11 | Knopf primär | knopf-speichern | wie 10, --neo-primary |
```

- **Jedes** Element, nicht die wichtigen.
- Die Maße kommen aus dem Artboard, **gemessen**, nicht geschätzt —
  `layout-diff.js` misst das Artboard genauso wie später die
  gebaute Seite.
- Jedes Element bekommt seinen **Marker**, der später auf beiden Seiten
  steht (`designsystem-abgleich.md`).
- **Das Inventar wird vorgelegt**, bevor gebaut wird. Fehlt im Entwurf
  etwas, das die Aufgabe braucht, steht es hier als offene Frage —
  nicht als eigene Erfindung.

## Bauen: von oben nach unten, Element für Element

**Nicht die Seite bauen und dann vergleichen.** Ein Element, dann messen,
dann das nächste.

Je Element, in dieser Reihenfolge:

1. **Das Element im Entwurf ansehen** und seine Zeile im Inventar lesen.
2. **Bauen** — mit der Komponente der Produktfamilie
   (Skill `neo-komponenten`), mit Tokens, ohne erfundene Werte.
3. **Messen**: Layoutabgleich für dieses Element gegen das Artboard.
4. **Null Abweichungen bei 1 px Toleranz** — sonst korrigieren und
   erneut messen. **Nicht weiterbauen.**
5. Erst dann das nächste Element.

**Ein Element gilt als fertig, wenn es gemessen bestanden hat.** Nicht,
wenn es fertig aussieht. Wer zehn Elemente baut und dann einmal misst,
sucht anschließend in zehn Elementen nach dem Fehler.

## Am Ende: die ganze Seite

Nach dem letzten Element folgt der Durchgang über das Ganze — der
Schritt, den man nicht überspringt, weil jedes Einzelteil bestanden hat:

1. **Layoutabgleich über die vollständige Seite**, je Fassung: hell,
   dunkel, mobil.
2. **Stilabgleich**: null erfundene Werte.
3. **Bildabgleich** gegen das Artboard, mit Unterschiedsbild — und das
   Bild wird **angesehen**.
4. **Die Seite im Ganzen betrachten**, neben dem Artboard: stimmt der
   Rhythmus, die Gewichtung, der Eindruck? Ein Layout kann in jedem
   Einzelmaß stimmen und trotzdem falsch wirken, wenn ein Abschnitt zu
   viel Luft bekommt oder eine Reihenfolge kippt.
5. **Alle Zustände**: Ruhe, Hover, Fokus, Deaktiviert, Fehler, Ladend,
   Leer.
6. **Die Zahlen berichten.** Je Fassung und Zustand eine Zeile.

## Die Rückfrage

**Jede Abweichung ist eine Rückfrage.** Auch eine, die besser wäre. Auch
eine Kleinigkeit. Auch eine, die offensichtlich erscheint. Auch unter
Zeitdruck. **Es gibt keinen Fall, in dem eine Abweichung ohne Rückfrage
richtig ist.**

Eine Rückfrage besteht aus **vier Teilen**:

1. **Zwei Bilder nebeneinander:** links die Vorgabe aus dem Entwurf,
   rechts der Vorschlag. Erzeugt mit
   `${CLAUDE_PLUGIN_ROOT}/scripts/comparison.js`.
2. **Was abweicht**, in Maßen: was der Entwurf sagt, was der Vorschlag
   sagt, um wie viel.
3. **Warum** die Abweichung nötig ist — die fachliche Notwendigkeit,
   nicht der Geschmack.
4. **Mindestens zwei Möglichkeiten** mit Vor- und Nachteilen, dazu eine
   **Empfehlung** — und der Satz, dass die Entscheidung beim
   Projektinhaber liegt.

```js
await seite.addScriptTag({ path: '${CLAUDE_PLUGIN_ROOT}/scripts/comparison.js' })
const masse = await seite.evaluate((b) => neoComparison.render({
  ueberschrift: 'Auftrag anlegen — Formularkarte',
  links:  { bild: b.entwurf,   titel: 'Designsystem', unterzeile: 'Artboard B5' },
  rechts: { bild: b.vorschlag, titel: 'Vorschlag',    unterzeile: 'Entscheidung offen' },
  hinweis: '…'
}), bilder)
```

Bilder als `data:`-URI übergeben oder die Seite von einer
`file://`-Adresse laden — sonst lädt der Browser sie nicht. **Das
Werkzeug meldet ein nicht geladenes Bild** und setzt `brauchbar: false`;
eine Rückfrage mit fehlendem Bild wird nicht abgeschickt.

**Nach der Rückfrage wird gewartet.** Nicht schon einmal angefangen,
nicht „vorbereitet", nicht die eigene Empfehlung umgesetzt, weil keine
Antwort kam. Warten heißt warten.

## Wenn die Seite schon existiert

Kommt eine Designänderung für eine Seite, die es bereits gibt, ist die
Zusammenführung **keine Aufgabe des Agenten**.

Der Agent:

- stellt fest, **was sich unterscheidet** — Element für Element, mit
  Maßen;
- legt **mindestens zwei Wege** vor, wie beides zusammengeht, jeweils mit
  Gegenüberstellung;
- benennt je Weg, was gewonnen und was aufgegeben wird;
- gibt eine **Empfehlung**;
- **wartet auf die Entscheidung.**

Er entscheidet **nie** selbst, wie neu und alt verschmelzen. Auch nicht,
wenn nur ein Abstand betroffen ist. Auch nicht, wenn eine Variante
offensichtlich besser wirkt.

## Warum so streng

Weil das Gegenteil bereits passiert ist: freier Entwurf statt Umsetzung,
und am Ende passte nichts zusammen. Eine Regel, die eine Abwägung
zulässt, wird abgewogen — und dann übergangen. Deshalb kennt diese Regel
keine Abwägung.

**Der Projektinhaber hat den Entwurf gemacht, weil er ein Ergebnis im
Kopf hat. Der Agent kennt dieses Ergebnis nicht.** Was ihm als
Verbesserung erscheint, ist aus dieser Sicht eine Abweichung von einem
Plan, den er nicht sieht.

## Selbstprüfung — diese Sätze müssen fallen

Vor jeder Fertigmeldung. Ohne Zahlen ist keiner davon erfüllt:

- „Inventar: <n> Elemente aus dem Artboard, alle gemessen."
- „Gebaut und einzeln geprüft: <n> von <n> Elementen, je 0 Abweichungen."
- „Gesamtdurchgang: Layout <n> Abweichungen, Stil <n> Funde, Bild
  <x> %."
- „Zustände geprüft: <Liste>, je Fassung hell und dunkel."
- „Abweichungen vom Entwurf: <n> — alle vorgelegt und entschieden."
- „Eigene Gestaltungsentscheidungen: **0**."

**Die letzte Zeile ist die wichtigste.** Steht dort etwas anderes als
null, ist die Arbeit nicht abnahmefähig — unabhängig davon, wie gut das
Ergebnis aussieht.
