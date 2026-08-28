# Text im Layout

Lesekonvention siehe `SKILL.md`. Formulierung und Wortwahl:
`oberflaechentexte.md`. Breiten, Umbruch und Lücken: `responsiv.md`.

> **Kein Text verschwindet, und wo er nicht ganz passt, ist entschieden,
> wie er nicht passt.**

Ein Layout kann jede Größenregel erfüllen und trotzdem falsch aussehen:
Der Kasten steht richtig, nur ist der Text darin abgeschnitten, zwei
Buchstaben breit oder mitten im Wort umgebrochen. **Das erzeugt keinen
Scrollbalken und fällt in keiner Überlaufprüfung auf.**

## Die fünf Arten, wie Text nicht passt

| Art | Was man sieht | Wo es auffällt |
| --- | --- | --- |
| **Ragt hinaus** | Der Kasten wird zu breit, die Seite scrollt | `ueberlauf.js` |
| **Waagrecht abgeschnitten** | Text verschwindet hinter der Kante | `textpassung.js` |
| **Senkrecht abgeschnitten** | Unten fehlt etwas, ohne Hinweis | `textpassung.js` |
| **Bereich zu schmal** | Eine Spalte mit zwei Zeichen je Zeile | `textpassung.js` |
| **Falsch umgebrochen** | Bruch mitten im Wort statt an der Silbe | `textpassung.js` |

Nur die erste erzeugt einen Balken. Die anderen vier sehen aus wie
Absicht — deshalb werden sie gemessen.

## Umbrechen: die Rangfolge

**Automatisch umbrechen heißt nicht: irgendwo umbrechen.** Für welchen
Inhalt welche Regel gilt:

| Inhalt | Regel | Warum |
| --- | --- | --- |
| **Fließtext, Beschriftungen, Überschriften** | `hyphens: auto` **plus** `lang` am Dokument | trennt an Silbengrenzen, wie ein Setzer es täte |
| **Zusammengesetzte Wörter, die oft brechen** | zusätzlich `&shy;` oder `<wbr>` an der gewünschten Stelle | die Trennstelle wird bestimmt, nicht geraten |
| **Kennungen, URLs, Prüfsummen, Dateinamen** | `overflow-wrap: anywhere` | hier gibt es keine Silbe; ein Bruch irgendwo ist richtig |
| **Alles andere** | `overflow-wrap: break-word` als Rückfall | bricht erst, wenn das Wort sonst hinausragen würde |
| **Nie für Fließtext** | `word-break: break-all` | bricht grundsätzlich mitten im Wort |

> **`hyphens: auto` ohne `lang` tut nichts.** Der Browser braucht die
> Sprache, um sein Trennwörterbuch zu wählen. Fehlt sie, wird nicht
> getrennt — und niemand merkt, warum die Regel wirkungslos ist. Das ist
> der häufigste stille Fehler in diesem Bereich.

```html
<html lang="de">
```

```css
/* Fließtext: an Silbengrenzen */
.text { hyphens: auto; overflow-wrap: break-word; }

/* Kennungen: an beliebiger Stelle, weil es keine bessere gibt */
.kennung { overflow-wrap: anywhere; }
```

Bei mehreren Sprachen trägt der jeweilige Abschnitt sein eigenes `lang` —
ein deutscher Text wird nicht nach englischen Regeln getrennt.

## Kürzen mit Anstand

Kürzen ist erlaubt. **Information verlieren nicht.**

- Wer kürzt, bietet den vollen Text an: `title`, `aria-label`, ein
  Tooltip, ein Detailbereich oder die Zeile im Aufklappzustand.
- **Eine Auslassung ohne Volltext ist Datenverlust.** Der Anwender sieht,
  dass da etwas stand, und kommt nicht heran.
- Ohne `text-overflow` verschwindet der Text **ohne Zeichen** — schlimmer
  als die Auslassung, weil man es nicht einmal merkt.
- Eine Zeilenklemme (`-webkit-line-clamp`) über mehreren Zeilen braucht
  denselben Weg zum vollen Text.
- **Nie kürzen**: Beträge, Zeiten, Zustände, Fehlermeldungen und alles,
  wonach jemand sucht. Lieber umbrechen oder die Spalte weglassen.

## Bereiche, die zu klein geworden sind

Der Gegenspieler zum Überlauf, und er wird selten geprüft: ein Bereich
schrumpft so weit, dass sein Inhalt unleserlich wird.

**Untergrenze: im Mittel acht Zeichen je Zeile.** Darunter ist eine
Spalte keine Spalte mehr, sondern ein senkrechter Buchstabenstapel.

Rangfolge, wenn eine Spalte unter die Grenze fällt — dieselbe wie bei
Tabellen (`responsiv.md`):

1. **Die Spalte weglassen.** Auf schmal bleiben die zwei wichtigen.
2. **Zeile zu Karte**, Beschriftung und Wert untereinander.
3. **Waagrecht scrollen im Tabellenbereich**, erste Spalte klebt.

**Nie**: die Spalte stehen lassen und hoffen. Eine Spaltenbreite in
Prozent, die auf 320 px 34 px ergibt, ist auf 320 px eine falsche
Entscheidung — nicht ein Rundungsproblem.

Dasselbe gilt für Knöpfe mit Text, Kennzahlkacheln, Reiter und
Auswahlfelder: was seinen eigenen Text nicht mehr fassen kann, wird
weggelassen, umgebaut oder bekommt Platz.

## Schriftgrößen

- **Untergrenze 12 px**, auf schmalen Geräten **14 px**. Darunter wird
  nicht gestaltet, sondern gespart.
- **Text wird auf dem Telefon nicht kleiner.** Der Bildschirm ist kleiner,
  das Auge nicht. Sekundärtext, der am Schreibtisch 13 px hat, hat am
  Telefon 14 px — nicht 11.
- **Mitwachsen statt springen**, aus Tokens, mit Boden und Decke:

  ```css
  --neo-schrift-h1: clamp(1.75rem, 1.2rem + 2vw, 2.75rem);
  ```

  Ohne Boden wird die Überschrift auf 320 px unlesbar, ohne Decke auf
  4K albern. Beide Werte kommen aus der Skala des Systems, nicht aus dem
  Gefühl.
- **`vw` allein ist kein Schriftmaß.** Es ignoriert die Zoomstufe des
  Anwenders und bricht WCAG 1.4.4. Immer in `clamp()` mit einem `rem`-Anteil.
- Zeilenhöhe wächst mit: enge Zeilen bei großer Schrift sind so unlesbar
  wie zu kleine Schrift.

## Zoom und Vergrößerung

Was hier gilt, gilt auch, wenn der Anwender vergrößert
(`barrierefreiheit.md`):

- **200 % reine Textvergrößerung** ohne Verlust von Inhalt oder Funktion.
- **400 % Zoom** auf 1280 px — das entspricht 320 px Breite.
- Danach ist **nichts abgeschnitten**, nichts überlappt, nichts
  verschwunden. Der Textpassungsprüfer läuft auch in diesem Zustand.

Ein Layout mit fester Höhe pro Karte fällt hier zuerst um: der Text
wächst, die Karte nicht.

## Überlappen

**Zwei Texte liegen nie übereinander.** Das ist kein Grenzfall, sondern
immer ein Fehler.

Die üblichen Ursachen: eine feste Höhe für eine Zeile, die zweizeilig
wird; ein negativer Außenabstand, der auf einer anderen Breite nicht mehr
passt; absolut positionierter Text über fließendem; eine Beschriftung,
die in einer anderen Sprache länger ist.

## Messen

```js
await page.addScriptTag({ path: 'tools/textpassung.js' })
const e = await page.evaluate(() => neoTextpassung.pruefen())
expect(e.befunde, await page.evaluate((x) => neoTextpassung.bericht(x), e))
  .toHaveLength(0)
```

Erlaubt sind **null Befunde**. Gemessen wird zusammen mit `ueberlauf.js`,
auf denselben acht Breiten, je Sprache, in Hell und Dunkel — und
zusätzlich:

- **Mit langen Daten.** Ein Name über 60 Zeichen, ein zusammengesetztes
  Wort ohne Leerzeichen, eine Kennung ohne Trennstelle, eine achtstellige
  Zahl.
- **In der längsten Sprache.** Deutsche Beschriftungen sind rund 30 %
  länger als englische; französische ähnlich. Wer nur in Englisch prüft,
  prüft den einfachsten Fall.
- **Bei 200 % Textvergrößerung.**

Der Prüfer meldet neun Arten; die Reihenfolge im Bericht ist die
Reihenfolge der Behebung. **Zuerst das Abgeschnittene** — dort ist
Information weg. Danach Überlappung, dann zu schmale Bereiche, dann
Umbruch und Schriftgröße.
