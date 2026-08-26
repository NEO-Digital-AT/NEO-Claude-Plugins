# Der Wächter-Test

Lesekonvention siehe `SKILL.md`.

**Ohne Wächter zerfällt der Komponenten-Grundsatz beim ersten
Termindruck.** Er ist deshalb keine Kür, sondern Teil des Grundsatzes:
ein Projekt mit Oberflächen und ohne Wächter erfüllt die Regel nicht,
auch wenn der Code heute sauber aussieht.

Vorbild und Beleg: `web/admin/test/guard.spec.ts` in NEO Uptime, dazu
`docs/adr/0002-komponenten-grundsatz.md`.

## Was er prüft

Er liest **jede Datei unter den Views** — bei Nuxt `app/pages/**` und
`app/layouts/**`, bei Flutter die Screens, bei Angular die Seiten-
Komponenten — und schlägt fehl bei:

| Nr. | Regel | Beispiel eines Verstoßes |
| --- | --- | --- |
| 1 | Ein gestaltendes HTML-Element im Template | `<div class="row">`, `<button>`, `<input>`, `<table>`, `<ul>`, `<p>`, `<h1>`–`<h6>`, `<span>`, `<section>` |
| 2 | Ein `class`- oder `style`-Attribut | `class="mt-4"`, `style="color:red"` |
| 3 | Ein Farbliteral | `#fff`, `#a8f20d`, `rgb(`, `rgba(`, `hsl(`, `red`, `white` |
| 4 | Eine Maßzahl mit Einheit außerhalb einer Token-Referenz | `12px`, `1.5rem`, `50%`, `2em` |
| 5 | Ein Import außerhalb der erlaubten Quellen | alles außer `~/components/<familie>/`, `~/composables/`, `vue`, `#app` |

**Strukturelle Elemente sind erlaubt**, weil sie keine Gestaltung tragen:
`template`, `slot`, `component`, `transition`, `keep-alive`, `teleport`,
`suspense`, sowie die Seiten- und Layout-Platzhalter des Frameworks.

Geprüft wird **nur der Vorlagenteil**. Skript- und Stilblöcke einer
View werden ausgeschnitten, bevor die Regeln greifen — ein Stilblock in
einer View ist ohnehin über Regel 2 hinaus verboten und wird gesondert
gemeldet.

## Wie die Ausnahmen geführt werden

**Ausnahmen stehen als Positivliste im Wächter selbst**, je Eintrag mit
Begründung:

```ts
const ERLAUBT: { datei: string; grund: string }[] = [
  // Heute keine Ausnahmen. Jeder Eintrag braucht einen Grund und eine Freigabe.
]
```

- **Ein neuer Eintrag ist eine Änderung am Wächter** und damit sichtbar
  im Diff. Genau das ist der Zweck.
- Ein Eintrag ohne Grund ist ungültig.
- Ein Eintrag braucht die Freigabe des Projektinhabers.
- **Eine View, die ein rohes Element braucht, deckt eine fehlende
  Komponente auf.** Dann wird die Komponente gebaut, nicht die Ausnahme
  eingetragen. Ein Eintrag ist die Antwort auf einen echten Sonderfall,
  nicht auf Zeitdruck.

## Wie er meldet

Ein Fund nennt: **Datei, Zeile, verletzte Regel, gefundener Ausdruck**.
Eine Meldung wie „Verstoß in pages/monitore.vue" ist nutzlos.

```
app/pages/monitore/[id].vue:42   Regel 1   gestaltendes Element <div>
app/pages/monitore/[id].vue:47   Regel 3   Farbliteral #2A025F
app/layouts/default.vue:12       Regel 5   Import aus 'vuetify/components'
```

Am Ende die Anzahl und ein klarer Fehlschlag. **Kein „Warnung"** — der
Wächter ist ein Blocker oder er ist wirkungslos.

## Wo er läuft

- **In der CI als Blocker**, bei jedem Pull Request (Skill
  `neo-deployment`).
- Lokal über denselben Befehl wie die übrigen Tests, damit ihn niemand
  erst in der CI trifft.
- Er läuft ohne Browser und ohne Anwendung: er liest Dateien, mehr
  nicht. Deshalb ist er schnell und kann bei jedem Lauf mit.

## Was er nicht kann

Ehrlich benannt, damit niemand sich auf ihn verlässt, wo er blind ist:

- Er sieht **nicht**, ob eine Komponente gut gebaut ist — nur, dass die
  View keine rohen Mittel verwendet.
- Er sieht **nicht**, ob eine Komponente einen Framework-Typ in der
  Signatur führt. Das wird bei der Durchsicht geprüft
  (`komponentenbau.md`).
- Er sieht **nicht**, ob das Ergebnis dem Designsystem entspricht. Dafür
  gibt es Layout- und Stilabgleich (Skill `neo-design`).
- Er sieht **nicht**, ob eine Komponente doppelt existiert.

## Ein Wächter für andere Stacks

Das Muster überträgt sich, die Regeln bleiben:

| Stack | Was gelesen wird | Erlaubte Importquellen |
| --- | --- | --- |
| Nuxt, Vue | `app/pages/**`, `app/layouts/**` (nur `<template>`) | `~/components/<familie>/`, `~/composables/`, `vue`, `#app` |
| Flutter | die Screens unter `presentation/` | `shared/widgets/`, `domain/`, Dart-Kern |
| Angular | die Seiten-Komponenten samt Vorlage | die eigene Komponentenbibliothek, `@angular/core` |
| Contao | die Templates | keine — dort gilt zusätzlich: kein fester Text (Skill `neo-contao`) |

Fehlt für einen Stack ein Wächter, ist das ein Befund und wird gemeldet —
nicht stillschweigend übergangen.
