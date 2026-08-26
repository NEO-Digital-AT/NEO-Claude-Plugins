# Von 320 px bis 4K

Eine Ansicht ist fertig, wenn sie auf jedem Gerät ihre Aufgabe erfüllt —
nicht, wenn sie auf dem Bildschirm des Entwicklers gut aussieht.

## Die harte Regel: kein horizontales Scrollen

Der Seitenkörper scrollt **nie** waagrecht. Auf keiner Breite, in keiner
Sprache, bei keinem Inhalt. Ein Balken am unteren Rand ist ein Fehler,
kein Kompromiss.

Was breiter ist als der Platz, scrollt **in seinem eigenen Bereich**:
Tabelle, Diagramm, Codeblock, breite Werkzeugleiste. Der Bereich zeigt,
dass er scrollt (Schattenkante am Rand), und ist auch per Tastatur
scrollbar.

Die üblichen Ursachen, in der Reihenfolge, in der sie auftreten:

1. Ein Kind in einem Flex- oder Grid-Bereich schrumpft nicht, weil seine
   Mindestbreite auf „Inhalt" steht. Abhilfe: `min-width: 0` bzw.
   `min-inline-size: 0` am schrumpfenden Kind.
2. Eine lange Zeichenkette ohne Leerzeichen — Kennung, Adresse,
   Prüfsumme, Dateiname. Abhilfe: umbrechen lassen, kürzen mit
   Auslassung und vollem Wert im Titel, oder eine Kopierschaltfläche
   statt der vollen Anzeige.
3. Feste Breiten in Pixeln, wo eine Höchstbreite gemeint war.
4. Bilder, Videos und eingebettete Rahmen ohne Höchstbreite.
5. Negative Außenabstände oder Verschiebungen, die über den Rand ragen.
6. Ein Element mit `position: fixed`, das breiter ist als der Bildschirm.

`overflow-x: hidden` am Körper ist **keine** Lösung. Es versteckt den
Fehler, macht den Inhalt unerreichbar und bricht klebende Elemente.

### Maschinell prüfen

Jede Ansicht bekommt einen Test, der bei jeder Prüfbreite feststellt,
dass nicht waagrecht gescrollt wird:

```js
for (const breite of [320, 390, 768, 1024, 1280, 1920, 2560, 3840]) {
  await page.setViewportSize({ width: breite, height: 900 })
  const ueberstand = await page.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth)
  expect(ueberstand, `Überstand bei ${breite} px`).toBeLessThanOrEqual(0)
}
```

Der Test läuft für jede Seite der Anwendung, in beiden Themes und in
jeder ausgelieferten Sprache — deutsche Beschriftungen sind länger als
englische, und genau daran bricht das Layout zuerst.

## Prüfbreiten

| Breite | Wofür sie steht |
| --- | --- |
| 320 px | Kleinstes Gerät und zugleich WCAG 1.4.10 (400 % Zoom auf 1280) |
| 390 px | Übliches Telefon |
| 768 px | Tablet hochkant, Umbruch von Seitenleiste zu Menü |
| 1024 px | Kleiner Laptop, Tablet quer |
| 1280 px | Arbeitsbreite |
| 1920 px | Üblicher Schreibtischmonitor |
| 2560 px | WQHD |
| 3840 px | 4K |

## Umbruchstufen

| Stufe | Ab | Verhalten |
| --- | --- | --- |
| Kompakt | 0 | Eine Spalte, Navigation eingeklappt hinter einem Knopf, Tabellen werden zu Karten, Dialoge füllen den Bildschirm, Aktionen am unteren Rand |
| Mittel | 640 | Zwei Spalten wo sinnvoll, Navigation weiterhin einklappbar |
| Breit | 1024 | Seitenleiste dauerhaft sichtbar, Tabellen als Tabellen, Dialoge zentriert |
| Weit | 1440 | Inhaltsbreite erreicht ihr Maß, Nebenbereiche werden möglich |
| Sehr weit | 1920 | Kein weiteres Dehnen — der Zuwachs wird verteilt, nicht gestreckt |

Die Zahlen sind der Vorschlag; führend ist die Skala des Projekts. Neue
Umbruchpunkte werden nicht erfunden — wer einen braucht, begründet ihn.

Umgebrochen wird nach **verfügbarem Platz**, nicht nach Gerätetyp. Wo das
Framework Container-Abfragen unterstützt, werden sie den
Bildschirmabfragen vorgezogen: eine Karte in einer schmalen Spalte ist
schmal, auch auf einem 4K-Monitor.

## Tabellen auf schmalen Geräten

Rangfolge, in dieser Reihenfolge zu prüfen:

1. **Spalten weglassen.** Die meisten Tabellen haben zwei wichtige
   Spalten und sechs für später. Auf schmal bleiben die zwei.
2. **Zeile zu Karte.** Jede Zeile wird ein Block mit Beschriftung und
   Wert untereinander, die Hauptaktion sichtbar.
3. **Waagrecht scrollen im Tabellenbereich**, erste Spalte klebt.
   Zulässig, aber die schlechteste der drei — nur bei echten
   Datenmengen.

Nie: die Tabelle so schrumpfen, dass Zahlen umbrechen oder Text auf zwei
Buchstaben abgeschnitten wird.

## Weitere Muster

- **Dialoge** füllen unter 640 px die ganze Fläche und schließen mit
  einem Knopf oben links oder rechts, nicht nur mit einem Klick daneben.
- **Formularaktionen** stehen auf schmalen Geräten am unteren Rand, in
  Daumenreichweite, und verdecken dabei kein Feld.
- **Seitenleisten** klappen zu einer Symbolleiste ein, bevor sie
  verschwinden. Der eingeklappte Zustand behält die Beschriftung als
  Namen für Vorlesegeräte.
- **Klebende Köpfe** sind auf schmalen Geräten flach: ein Kopf, der ein
  Drittel der Höhe frisst, ist auf 390 × 660 px unbrauchbar.
- **Zahlen und Zeiten** kürzen ihre Darstellung, nicht ihre Bedeutung:
  aus „14. September 2026, 09:31" wird „14.09.26, 09:31", nie „14.09."

## Große Bildschirme

Ein 4K-Monitor ist kein gedehnter Laptop.

- **Lesbare Zeile begrenzen.** Fließtext bleibt bei 60 bis 90 Zeichen.
  Eine über 3840 px gezogene Textzeile liest niemand.
- **Den Zuwachs verteilen, nicht strecken.** Mehr Platz wird zu: einer
  zweiten Spalte, einem dauerhaft sichtbaren Detailbereich, mehr Zeilen
  ohne Blättern, einem breiteren Diagramm. Nicht zu breiteren Knöpfen und
  nicht zu einer Formularspalte über die halbe Wand.
- **Die Dichte bleibt.** Zeilenhöhen, Polster und Schriftgrößen werden
  nicht mitskaliert; sonst wirkt die Anwendung auf großen Geräten wie ein
  Kinderspielzeug.
- **Nichts steht allein in der Mitte.** Ein Formular mit vier Feldern,
  zentriert auf 3840 px, mit leeren Flächen links und rechts, ist ein
  unfertiger Entwurf. Entweder es bekommt einen Begleitbereich, oder die
  Fläche wird bewusst und sichtbar gerahmt.
- **Grafiken in doppelter Auflösung** oder als Vektor. Ein unscharfes
  Logo fällt auf 4K sofort auf.
- Zeilenlängen und Höchstbreiten kommen aus Tokens, nicht aus Zahlen in
  der View.

## Was auf jedem Gerät gleich bleibt

Aufgabe, Reihenfolge der Schritte, Beschriftungen und die Stelle, an der
eine Aktion sitzt. Mobil ist kein anderes Produkt und kein Restposten —
dieselbe Anwendung, andere Anordnung. Eine Funktion, die auf dem Telefon
fehlt, ist eine Entscheidung des Projektinhabers, keine Folge der Breite.
