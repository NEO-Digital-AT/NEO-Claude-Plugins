# Von 320 px bis 4K

Eine Ansicht ist fertig, wenn sie auf jedem Gerät ihre Aufgabe erfüllt —
nicht, wenn sie auf dem Bildschirm des Entwicklers gut aussieht.

**Das gilt für Anwendungen und Portale genauso wie für Webseiten.** Eine
Web-Anwendung ist keine Ausnahme, weil sie „am Schreibtisch bedient
wird". Wer sie am Telefon öffnet, bekommt keine Entschuldigung zu sehen,
sondern eine Oberfläche. Der Funktionsumfang darf auf schmalen Geräten
kleiner sein — **das Aussehen nie**. Was weggelassen wird, entscheidet
der Projektinhaber, nicht der Umbruchpunkt.

## Die fünf harten Regeln

1. **Kein waagrechtes Scrollen des Seitenkörpers** — auf keiner Breite,
   auch nicht am Schreibtisch.
2. **Nichts ragt hinaus.** Kein Element steht über dem sichtbaren
   Bereich, auf keiner Breite.
3. **Tabellen füllen die Inhaltsbreite** — 100 %, nie schmaler.
4. **Keine Löcher beim Umbrechen.** Eine umgebrochene Reihe lässt keine
   halbe Reihe frei.
5. **Bedienziele wachsen zum schmalen Gerät hin**, sie schrumpfen nicht.
6. **Kein Text verschwindet** — nicht hinausragend, nicht abgeschnitten,
   nicht auf zwei Zeichen je Zeile gestaucht, nicht mitten im Wort
   umgebrochen.

Alle sechs werden **maschinell geprüft**, auf acht Breiten, mit
`scripts/overflow.js` und `scripts/text-fit.js`. Nicht Gemessenes
gilt als nicht erfüllt.

Die ersten fünf stehen hier. Die sechste hat einen eigenen Text, weil sie
anders funktioniert: sie erzeugt **keinen** Scrollbalken und fällt in
keiner Überlaufprüfung auf — `textpassung.md`.

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

### Nichts ragt hinaus

Der Körper kann still stehen und trotzdem etwas hinausragen: ein Element
in einem Elternteil mit `overflow: hidden`, ein `position: fixed`-Kopf,
ein Menü, das über den Rand schiebt. **Der Seitenüberlauf allein ist
keine ausreichende Prüfung.**

Geprüft wird deshalb je Element: keine rechte Kante über der
Bildschirmbreite, keine linke Kante darunter — außer in einem
ausdrücklichen Scrollbereich.

### Maschinell prüfen

Jede Ansicht bekommt einen Test, der auf **jeder** Prüfbreite alle fünf
harten Regeln prüft:

```js
await page.addScriptTag({ path: 'tools/overflow.js' })
for (const breite of [320, 390, 768, 1024, 1280, 1920, 2560, 3840]) {
  await page.setViewportSize({ width: breite, height: 900 })
  const e = await page.evaluate(() => neoOverflow.check())
  const text = await page.evaluate((x) => neoOverflow.report(x), e)
  expect(e.findings, text).toHaveLength(0)
}
```

Der Prüfer meldet Seitenüberlauf, Elemente über dem Rand, Inhalt breiter
als sein Platz, Tabellen unter der Inhaltsbreite, zu kleine Bedienziele
und **Löcher in umgebrochenen Reihen**. Erlaubt sind **null Befunde**.

Der Test läuft für **jede** Seite der Anwendung, in beiden Themes und in
jeder ausgelieferten Sprache — deutsche Beschriftungen sind länger als
englische, und genau daran bricht das Layout zuerst. Zusätzlich mit
**langen Daten**: ein Name über 60 Zeichen, eine Kennung ohne
Leerzeichen, eine Zahl mit acht Stellen. Ein Layout, das nur mit kurzen
Testdaten hält, hält nicht.

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

## Umbrechen ohne Löcher

**Eine umgebrochene Reihe lässt kein Loch stehen.** Drei Kacheln, die auf
zwei Spalten umbrechen, ergeben in der zweiten Reihe eine halbe leere
Fläche. Das sieht nach einem Fehler aus, weil es einer ist.

Zwei erlaubte Auflösungen, beide bewusst gewählt:

| Weg | Wann | Wie |
| --- | --- | --- |
| **Gleich einspaltig** | wenige, große Kacheln | ein Umbruchpunkt weniger; unter der Schwelle direkt eine Spalte |
| **Das letzte Element füllt** | viele, gleichartige Kacheln | die Kachel, die allein in der letzten Reihe steht, nimmt die volle Breite |

```css
/* Zweispaltig, und das ungerade letzte Element füllt die Reihe */
.kacheln { display: flex; flex-wrap: wrap; gap: var(--neo-luecke); }
.kacheln > * { flex: 0 0 calc(50% - var(--neo-luecke) / 2); min-width: 0; }
.kacheln > :last-child:nth-child(odd) { flex-basis: 100%; }

/* Oder: mitwachsende Spalten, die den Rest von selbst aufteilen */
.kacheln > * { flex: 1 1 280px; min-width: 0; }
```

**Nie**: eine leere Platzhalterkachel einsetzen, um die Reihe zu füllen.
Sie ist für Vorlesegeräte ein Element ohne Inhalt und beim nächsten
Datensatz an der falschen Stelle.

Die Regel gilt für **jede** umbrechende Reihe: Kacheln, Karten,
Kennzahlen, Filterknöpfe, Bildergitter, Formularspalten. Der Prüfer misst
sie, indem er die Kinder nach Reihen gruppiert und die letzte Reihe mit
den vorherigen vergleicht.

## Tabellen

**Eine Tabelle nutzt immer die volle Breite ihres Inhaltsbereichs.** Eine
Tabelle mit 600 px in einem 1248 px breiten Bereich ist ein Fehler: sie
lässt Fläche frei, und die freie Fläche wirkt wie ein Ladefehler.

- `width: 100%`, nie eine feste Pixelbreite.
- Spaltenbreiten in Prozent oder über `table-layout: fixed`, nicht in
  Pixeln.
- Lange Inhalte in Zellen brechen um (`overflow-wrap: anywhere`) oder
  werden gekürzt — sie schieben die Tabelle nicht auf.
- Eine Tabelle **breiter** als der Inhaltsbereich ist nur in einem
  ausdrücklichen Scrollbereich zulässig (`data-table-area` mit
  `overflow-x: auto`). Auch dort ist sie nie **schmaler** als der
  sichtbare Bereich.

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
Buchstaben abgeschnitten wird. **Untergrenze sind im Mittel acht Zeichen
je Zeile** — darunter ist eine Spalte ein senkrechter Buchstabenstapel und
wird weggelassen, nicht schmaler gemacht (`textpassung.md`).

## Bedienziele wachsen nach unten hin

Ein Finger ist kein Mauszeiger. **Auf schmalen Geräten werden
Bedienelemente größer als am Schreibtisch, nicht kleiner.**

| Breite | Kleinstes Bedienziel |
| --- | --- |
| bis 768 px | **44 × 44 px** |
| darüber | 24 × 24 px (WCAG 2.2, 2.5.8) |

- Das gilt für die **Trefferfläche**, nicht für das Symbol. Ein 20 px
  großes Symbol in einem 44 px großen Knopf ist richtig.
- Zwischen zwei Zielen mindestens 8 px Abstand — sonst trifft der Finger
  beide.
- **Symbolknöpfe in Tabellenzeilen** sind der häufigste Verstoß: am
  Schreibtisch 24 px, am Telefon unbedienbar. Auf schmal werden sie zu
  einer Zeilenaktion mit Text oder zu einem Menü.
- Werkzeugleisten in Editoren werden auf schmal **größer und weniger**,
  nicht kleiner und mehr. Was nicht in eine Reihe passt, geht in ein
  Überlaufmenü — nicht in eine zweite, halbleere Reihe.
- Ein Textlink im Fließtext ist ausgenommen; ein Link, der wie ein Knopf
  aussieht, nicht.

## Navigation auf schmalen Geräten

- **Unter dem Umbruchpunkt ist das Hauptmenü nicht dauerhaft sichtbar.**
  Es liegt hinter einem Knopf — Burger, Symbolleiste, Schublade —, und
  der Knopf ist selbst ein Bedienziel nach der Tabelle oben.
- **Nichts davon ragt hinaus.** Eine geöffnete Schublade bleibt im
  sichtbaren Bereich; ein Menü, das rechts hinausschiebt, erzeugt genau
  den waagrechten Balken, den es nicht geben darf.
- `aria-expanded` am Knopf, Fokus in das geöffnete Menü, Fokusfalle,
  Escape schließt, Fokus zurück auf den Knopf (Skill `neo-design`,
  `references/barrierefreiheit.md`).
- Der **geschlossene** Zustand ist der Ausgangszustand. Ein Menü, das
  beim Laden offen steht und dann zuklappt, springt.

## Höchstbreiten

Auf großen Bildschirmen sind Höchstbreiten kein Feinschliff, sondern
Voraussetzung dafür, dass eine Anwendung nicht auseinanderfällt.

| Was | Höchstbreite |
| --- | --- |
| Inhaltsbereich | aus dem Token, meist 1280 bis 1600 px |
| Fließtextspalte | 60 bis 90 Zeichen |
| Formularspalte | so breit wie das breiteste sinnvolle Feld, nicht wie der Bildschirm |
| Einzelnes Textfeld | nach Inhalt: Postleitzahl kurz, Kennung mittel, Freitext voll |

- **Ein Textfeld, das über die halbe Wand läuft, ist ein Fehler**, auch
  wenn technisch nichts kaputt ist. Ein Eingabefeld zeigt durch seine
  Breite, wie viel erwartet wird.
- Höchstbreiten stehen in **Tokens**, nicht als Zahl in der View.
- Der Inhaltsbereich wird zentriert, nicht linksbündig an die Wand
  geheftet.

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
