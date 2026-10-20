# Betriebsart Webseite

Zwei Betriebsarten, ein Regelwerk. Was in `SKILL.md` steht — Aufbau,
Eingabeführung, Kontrast, Zustände, Responsivität, Texte — gilt für
beide. Was hier steht, gilt nur für Webseiten.

| | Anwendung / Portal | Webseite |
| --- | --- | --- |
| Zweck | arbeiten | überzeugen |
| Dichte | dicht, viele Daten je Fläche | großzügig, Luft zwischen Abschnitten |
| Bewegung | fast keine, nur Zustandswechsel | **erwünscht** — die Seite soll leben |
| Breite | bis zur Arbeitsbreite | Inhaltsspalte plus vollbreite Bühnen |
| Farbe | ausschließlich bedeutungstragend | Marke darf tragen |
| Bilder | selten, nie dekorativ | tragendes Element |
| Wiederholung | Muster sind gut, sie schaffen Sicherheit | Muster sind schlecht, sie schaffen Langeweile |

Welche Betriebsart gilt, steht in der Regeldatei des Projekts. Fehlt der
Eintrag: nachfragen, nicht annehmen.

## Die Seite darf nicht wie eine KI-Seite aussehen

Generierte Seiten sehen einander ähnlich, weil sie aus denselben Mustern
bestehen. Diese Muster sind zu vermeiden oder so umzubauen, dass sie der
Marke gehören und nicht dem Werkzeug:

- **Eyebrow-Zeilen** in Versalien über jeder Überschrift („UNSERE
  LEISTUNGEN"), oft mit Punkt oder Strichlein davor. **Entweder ganz
  weglassen oder etwas Eigenes daraus machen** — eine Nummer, ein
  Datum, ein Kürzel, eine gezeichnete Marke, etwas, das nur zu dieser
  Seite passt. Die Standardform ist verboten.
- Drei gleich große Karten nebeneinander, je mit Symbolkreis,
  Überschrift und drei Zeilen Text.
- Mittig gesetzte Bühne mit Farbverlauf, Schlagzeile und zwei Knöpfen.
- Überschrift mit Farbverlauf im Text.
- Blau-violetter Verlauf als Markenersatz.
- Milchglasflächen über einem Farbverlauf.
- Logo-Leiste in Graustufen mit der Zeile „Vertrauen uns bereits".
- Abschnitte, die alle denselben Rhythmus haben: Überschrift, zwei
  Sätze, Bild rechts, dann Bild links, dann rechts.
- Symbole aus einem Standardsatz in Kreisen, überall gleich groß.
- Emojis als Symbole.

**Der Prüfsatz:** Könnte diese Seite ohne Änderung für ein anderes
Unternehmen stehen? Dann ist sie noch nicht fertig. Typografie, Farbe,
Bildsprache, Rhythmus und die eine ungewöhnliche Idee kommen aus der
Marke, nicht aus dem Trend.

## Dynamik

Eine Webseite darf sich nicht starr anfühlen. Bewegung ist hier kein
Schmuck, sondern Teil der Gestaltung — aber sie hat immer einen Grund.

- **Beim Scrollen erscheinen** (Einblenden mit leichter Verschiebung),
  gestaffelt statt gleichzeitig, einmalig statt bei jedem Vorbeiscrollen.
- **Tiefe durch unterschiedliche Geschwindigkeiten** (Parallax), sparsam
  und nie auf Text, der gelesen werden soll.
- **Bühnen mit Eigenleben:** bewegter Hintergrund, Verlauf in Bewegung,
  Partikel, gezeichnete Formen. Ein Effekt je Seite, nicht drei.
- **Übergänge zwischen Zuständen**: Menü öffnet, Bild vergrößert,
  Abschnitt klappt auf — immer mit Bewegung, nie mit einem Sprung.
- **three.js** dort, wo es etwas zeigt, das flach nicht geht — ein
  Produkt, eine Struktur, eine Bühne. Nicht als Beweis, dass man es kann.

### Grenzen für jede Bewegung

- **`prefers-reduced-motion` wird beachtet.** Reduziert heißt: kein
  Einflug, kein Parallax, keine Dauerschleife. Der Inhalt ist sofort da.
  Das ist keine Nebensache — es ist Barrierefreiheit (`barrierefreiheit.md`).
- **Kein Layoutsprung.** Bewegung nur über `transform` und `opacity`,
  nie über Größe, Position oder Abstand. Jeder Sprung geht in die
  Layoutstabilität und kostet zwei Bewertungen zugleich (`messwerte.md`).
- **Nichts Bewegtes blockiert den Aufbau.** Die Seite ist lesbar, bevor
  der Effekt läuft. Ein Effekt, der das Hauptbild verzögert, wird
  entfernt.
- **Kein Element erscheint erst nach dem Scrollen für Maschinen.** Was
  eingeblendet wird, steht im Markup und ist sichtbar, wenn kein
  JavaScript läuft.
- Dauer 200–600 ms, ruhige Kurve, kein Federn, kein Überschwingen.
- Nichts spielt von selbst mit Ton. Nichts blinkt.

## Wechselnde Wörter und Scroll-Handler

- **Ein wechselndes oder animiertes Wort reserviert den Platz der
  längsten Fassung.** Sonst springt die Zeile bei jedem Wechsel, und der
  Wert für Layoutstabilität (CLS) fällt. Gemessen wird die längste
  ausgelieferte Fassung in **jeder** Sprache, nicht die deutsche.
- **Scroll-Handler lesen keine Geometrie.** Kein
  `getBoundingClientRect`, kein `offsetTop`, kein `scrollHeight` in einem
  Scroll-Ereignis: Jeder Lesezugriff erzwingt Layout, bei jedem
  Bildaufbau. Dafür gibt es `IntersectionObserver`.
- **Was scrollgebunden ist, wird in jeder Phase gemessen**, nicht in der
  Ruhelage: `scrolleffekte.md`.

## Neuladen: die Seite bleibt, wo sie war

Nach dem Neuladen stellt der Browser die Scrollposition wieder her. Zwei
Dinge haben das an `ergotherapie-schumann.at` sichtbar gestört:

- **Bewegte Dekoration als Bezugspunkt.** Chrome merkt sich ein Element
  und stellt die Lage über dieses wieder her (Scroll Anchoring). War das
  eine treibende Form oder die Überschrift der Bühne, stand die Seite
  danach ab 1024 px Breite 9 bis 35 px tiefer — auch ganz oben. Abhilfe:
  `overflow-anchor: none` auf jeder bewegten Dekoration und auf der Bühne
  des ersten Bildschirms. Für die Abschnitte darunter bleibt das
  Verankern an.
- **Weiches Scrollen gilt auch für die Wiederherstellung.** Mit
  `scroll-behavior: smooth` am `html` fuhr die Seite die alte Stelle
  sichtbar von oben an. Abhilfe: weiches Scrollen erst nach dem Laden
  einschalten (ein Attribut am `html`, gesetzt einen Bildaufbau nach
  `load`); bei reduzierter Bewegung und im Modus „Animationen stoppen"
  aus, auch am `html` selbst.

Geprüft wird es: an mehreren Stellen neu laden und die Lage des
sichtbaren Inhalts vorher und nachher vergleichen — Soll 0 px, und die
Wiederherstellung ist ein Sprung, keine Fahrt. Umsetzung und Testablauf:
Skill `neo-contao`, `references/ladezeit.md`, Baustein 7.

## Navigation und Burgermenü

- **Das Burgermenü wird animiert**: das Symbol wandelt sich in ein
  Kreuz, die Fläche fährt ein, die Einträge erscheinen gestaffelt.
- Es bleibt trotzdem ein Bedienelement: `aria-expanded` am Auslöser, der
  Fokus wandert hinein, bleibt gefangen, kehrt beim Schließen zurück,
  Escape schließt.
- Das Menü ist auch bei reduzierter Bewegung vollständig bedienbar — dann
  ohne Übergang, aber mit demselben Ergebnis.
- Eine klebende Kopfzeile verkleinert sich beim Scrollen, ohne den
  Inhalt springen zu lassen, und verdeckt nie das fokussierte Element.
- Der aktive Menüpunkt ist erkennbar, nicht nur beim Überfahren.

## Bilder und Schriften

- Bilder in mehreren Breiten und in modernen Formaten, mit
  `width`/`height` im Markup, damit nichts springt.
- Das Bühnenbild wird bevorzugt geladen, alles darunter nachrangig.
- **Schriften immer selbst ausliefern**, nie von einem fremden Dienst
  laden (Skill `neo-recht`). Beschnitten auf die Zeichen der Seite; nur
  die Schnitte des ersten Bildschirms werden vorgeladen.
- **SVG-Grafiken werden optimiert, bevor sie eingebaut werden.**
  Grafikprogramme schreiben Herkunftsdaten (C2PA) und sieben
  Nachkommastellen hinein; ein Logo kam so auf 25 KB statt 13,5 KB.
  Optimiert wird ohne Kurvennäherung — das SVGO-Standardpaket verschob
  Kanten um bis zu ein Pixel — und belegt mit einem Pixelvergleich bei
  mehreren Breiten (Skill `neo-contao`, `references/ladezeit.md`,
  Baustein 6).

## Referenz

**Ladezeit und Stabilität:** `ergotherapie-schumann.at` (Vorgabe Erich
Nigg, 20.10.2026, mobil Leistung 98, sonst 100, agentisches Browsen
3/3). Die acht Bausteine — eine Skriptdatei je Seite mit `defer`,
eingebettete Stylesheets, beschnittene Schriften, vorgeladenes
Bühnenbild, gemessene Schätzhöhen, optimierte SVG, Neuladen ohne
Versatz, Webserver — gelten für jede Webseite: Skill `neo-contao`,
`references/ladezeit.md`. Die Regeln dort sind in Contao formuliert,
gelten aber sinngemäß für jede Webseite.

**Aufbau von Stil und Bewegung:** `neo-digital.at` und das Repository
`NEO-Digital-AT/website`: `theme/scss/` mit einem Bündel je Bereich,
`theme/js/` mit einem Modul je Effekt (`reveal.js`, `lp-motion.js`,
`neo-bg-fx.js`, `lp-herowall.js`). Aufbau übernehmen, Gestaltung nicht
kopieren — jede Kundenseite bekommt ihre eigene.
