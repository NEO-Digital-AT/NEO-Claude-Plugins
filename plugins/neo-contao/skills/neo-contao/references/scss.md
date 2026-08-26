# SCSS in Contao

## Ausnahmslos SCSS

Styles werden **nur** in SCSS geschrieben — kein handgeschriebenes CSS,
keine Stile im Template, kein `style`-Attribut. SCSS wird dabei auch
benutzt und nicht nur als Dateiendung geführt: Verschachtelung,
Variablen, Mixins, Funktionen, Schleifen und Berechnungen sind der
Grund, warum die Datei so heißt.

- **Schleifen** statt zwanzig fast gleicher Blöcke: Abstandsklassen,
  Spaltenbreiten, Farbvarianten, Rasterstufen entstehen aus einer Liste.
- **Berechnungen** statt abgetippter Zahlen: Zeilenhöhen, Abstände und
  Größen leiten sich aus der Skala ab.
- **Mixins** für Wiederkehrendes: Umbruchpunkte, Fokusring, sichtbar nur
  für Vorlesegeräte, Textabschnitt mit Auslassung.
- **Verschachtelung** bildet die Zugehörigkeit ab — aber höchstens drei
  Ebenen tief. Wer tiefer verschachtelt, erzeugt Selektoren, die niemand
  mehr übersteuern kann.

## Ebenen

Programmiert wird in Ebenen, und die Reihenfolge der Einbindung **ist**
die Kaskadenreihenfolge:

```
1  tokens/      Farben, Schriften, Typografie, Abstände, Effekte
2  base/        Zurücksetzung, Grundelemente, Typografie-Grundlage
3  components/  wiederverwendbare Bausteine (Knopf, Karte, Feld, Abzeichen)
4  bereiche/    Kopf, Fuß, Navigation, Abschnitte, Formulare, Blog
5  seiten/      was nur eine Seitengattung braucht
6  largescreen  Anpassungen für sehr große Flächen zuletzt
```

- **Tokens sind CSS-Eigenschaften (`--neo-…`), nicht nur
  SCSS-Variablen.** Nur so lässt sich zur Laufzeit umschalten — Hell und
  Dunkel, Markenfarbe je Mandant. SCSS-Variablen sind zur Bauzeit weg.
- Eine Ebene greift nie auf eine höhere zu. Eine Komponente kennt keine
  Seite.

## Ein SCSS je Bereich, je Komponente

Jeder Bereich und jede Komponente bekommt eine eigene Datei als Partial
(`_kopfzeile.scss`, `_karte.scss`, `_blog.scss`). Eine Sammeldatei, in
der alles steht, ist der Zustand, den diese Regel verhindert.

Vorbild ist `NEO-Digital-AT/website`, `theme/scss/`: ein Partial je
Bereich (`_chrome`, `_footer`, `_forms`, `_blog`, `_richtext`,
`_timeline`, `_a11y` …), dazu ein Ordner `tokens/`.

## Welcher Renderer läuft — das entscheidet die Syntax

**Vor der ersten Zeile feststellen, wer das SCSS übersetzt.** Beide Wege
kommen vor, und sie vertragen unterschiedliche Syntax.

| Weg | Syntax | Einbindung |
| --- | --- | --- |
| **Contaos eigener Renderer** (Combiner) | **Nur die alte Syntax:** `@import`, globale `$variablen`, `@mixin` und `@include` in der alten Form. **Kein** `@use`, **kein** `@forward`, keine Modulnamensräume wie `math.div`, `map.get`, `color.adjust` | Die `.scss`-Datei wird direkt im Contao-Layout gewählt |
| **Dart Sass im Build** | Volle moderne Syntax, `@use` und `@forward` erlaubt | Das erzeugte `.css` wird im Contao-Layout gewählt |

**Nie annehmen, welcher Weg gilt.** Wird über Contao gerendert, gilt die
alte Syntax ausnahmslos — moderne Modulaufrufe brechen den Aufbau, und
zwar erst beim Ausliefern, nicht beim Schreiben.

**Kompiliertest ist Pflicht:** einmal gegen den Renderer übersetzen, der
später läuft, bevor eine neue Sprachform großflächig verwendet wird.
Ein grüner Editor ist kein Beleg.

Beobachteter Stand: `NEO-Digital-AT/website` übersetzt mit **Dart Sass im
Build** nach `files/theme/neo/*.css` und nutzt deshalb `@use`; Contao
kombiniert und minifiziert das Ergebnis nur noch. Das ist der IST-Zustand
jenes Projekts, keine Vorgabe für neue.

## Einbindung im Layout

- **Stylesheets werden im Contao-Layout gewählt, genau wie JavaScript.**
  Nicht im Template eingehängt, nicht im Kopf hartkodiert.
- Kopf- und Fußzeile sind Layout-Module. Ihre Stile hängen deshalb am
  **Layout**, nicht an einem Inhaltselement — sonst fehlen sie, sobald
  eine Seite das Element nicht enthält.
- Stile, die nur ein bestimmtes Inhaltselement braucht, dürfen am
  Element bzw. im zuständigen Controller registriert werden.

## Jede Seite liefert nur, was sie braucht

**Kein großes Gesamt-CSS.** Der Grundsatz: so groß wie nötig, so klein
wie möglich.

- Ein Einstiegsbündel je Seitengattung: Grundbündel für alle Seiten,
  eigene Bündel für Sonderfälle (Landingpages, Fallstudien, Schauraum).
- Ein Bündel wird ausgelagert, sobald es spürbar Gewicht hat und nur auf
  wenigen Seiten wirkt. In `NEO-Digital-AT/website` waren das 88 KB
  Quelltext, die jede Seite mitschleppte, obwohl sie auf fünf Seiten
  gebraucht wurden.
- Nach jeder Auslagerung wird gemessen, nicht geschätzt (Skill
  `neo-design`, `references/messwerte.md`).

### Zwei Fallen beim Auslagern

1. **Namenskollision.** Ein Partial `_lp.scss` und ein Einstiegsbündel
   `lp.scss` sind für Dart Sass mehrdeutig und brechen den Aufbau. Das
   Bündel bekommt einen anderen Namen (`lp-base.scss`).
2. **Verlorene Übersteuerung.** Eine ausgelagerte Datei kann Regeln
   enthalten, die bisher global etwas übertrumpft haben — in
   `NEO-Digital-AT/website` setzte `_leoflexcase.scss` eine
   Einblenddauer, die auf **jeder** Seite die kürzere aus `_site.scss`
   überstimmte. Nach dem Auslagern gilt woanders plötzlich ein anderer
   Wert. Vor dem Auslagern prüfen, was die Datei global definiert, und
   die Änderung bewusst entscheiden und im Kommentar festhalten.

## Verboten

- Rohes CSS neben dem SCSS.
- Farbliterale außerhalb der Token-Dateien.
- Maßzahlen, die nicht aus der Skala kommen.
- `!important` ohne Kommentar mit Begründung.
- Verschachtelung tiefer als drei Ebenen.
- `@extend` über Dateigrenzen hinweg — es zieht Selektoren an Stellen,
  die niemand erwartet. Stattdessen ein Mixin.
- Eine Datei, die mehr als einen Bereich bedient.
