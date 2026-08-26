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
  laden (Skill `neo-recht`).

## Referenz

`neo-digital.at` und das Repository `NEO-Digital-AT/website`. Dort steht
der Aufbau, der gemeint ist: `theme/scss/` mit einem Bündel je Bereich,
`theme/js/` mit einem Modul je Effekt (`reveal.js`, `lp-motion.js`,
`neo-bg-fx.js`, `lp-herowall.js`). Aufbau übernehmen, Gestaltung nicht
kopieren — jede Kundenseite bekommt ihre eigene.
