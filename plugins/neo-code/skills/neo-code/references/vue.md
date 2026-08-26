# Vue 3

Maßgeblich ist der **offizielle Vue-Stilleitfaden** mit seinen
Prioritäten A (unbedingt) bis D (mit Vorsicht). Priorität A und B gelten
ohne Diskussion.

## Grundentscheidungen

- **Composition API mit `<script setup>`**, TypeScript. Keine Options
  API in neuem Code.
- **Zustand in Pinia**, nicht in einem globalen Objekt und nicht in einem
  Ereignisbus.
- Ein Store je Fachbereich, mit klarem Zuschnitt. Kein Store, der alles
  hält.
- Kein `provide`/`inject` als heimlicher globaler Zustand — nur für
  echte Baumkontexte, dokumentiert.

## Komponenten

- **Mehrwortige Komponentennamen**, `PascalCase` in Datei und Vorlage.
  Bei NEO trägt jede Komponente das Präfix der Produktfamilie und folgt
  dem Katalog (Skill `neo-komponenten`).
- **Props ausführlich deklariert:** Typ, Pflicht oder Vorgabe, bei
  begrenzten Wertemengen ein Aufzählungstyp. Kein `props: ['x']`.
- **Ereignisse deklariert** (`defineEmits`) und fachlich benannt
  (`bestaetigt`, `geaendert`), nicht `click` aus einem inneren Element
  durchgereicht.
- **`v-for` immer mit stabilem `key`** — nie der Index, wenn sich die
  Liste ändern kann.
- **`v-if` und `v-for` nie am selben Element.** Erst filtern, dann
  ausgeben.
- Kein Durchreichen unbekannter Attribute in Wrapper-Komponenten: das
  hebt die Kapselung auf (Skill `neo-komponenten`).

## Reaktivität

- `ref` als Voreinstellung, `reactive` nur, wenn ein Objekt wirklich als
  Ganzes reaktiv sein muss.
- `computed` für Ableitungen. Ein `watch`, der nur einen Wert setzt,
  ist ein `computed`, das falsch geschrieben wurde.
- `watch` mit klarer Quelle und, wo nötig, `{ immediate: true }` statt
  einer zusätzlichen Zeile beim Aufbau.
- Keine Nebenwirkungen im Aufbau der Komponente, die eine Anfrage
  auslösen, ohne dass Abbruch und Fehlerfall behandelt sind.
- Aufräumen ist Pflicht: Zeitgeber, Ereignisbehandler, Beobachter und
  offene Ströme werden beim Abbau entfernt.

## Aufbau einer Datei

Reihenfolge in der Einzeldatei-Komponente: `<script setup>`,
`<template>`, `<style scoped>`. Stile sind **immer** `scoped` — ein
globaler Stil aus einer Komponente heraus trifft irgendwann etwas
anderes.

## Ordner

```
app/
  components/<familie>/<bereich>/   Wrapper-Komponenten (Neo*, LeoFlex*)
  composables/                      wiederverwendbare Logik, useX()
  stores/                           Pinia
  pages/ bzw. views/                Ansichten — nur Komponenten der Familie
  utils/                            reine Funktionen, ohne Framework
  types/                            geteilte Typen
```

Eine Ansicht enthält keine Gestaltung und keinen Framework-Import
(Skill `neo-komponenten`, Wächter-Test).

## Wiederverwendbare Logik

- Als `useX()`-Funktion, nicht als Mixin.
- Sie gibt zurück, was der Aufrufer braucht, und räumt selbst auf.
- Keine versteckte Abhängigkeit auf einen bestimmten Ort im Baum.

## Werkzeuge

- ESLint mit dem Vue-3-Regelsatz und TypeScript-Regeln, `--max-warnings 0`.
- Formatierung maschinell, Konfiguration im Repo.
- `vue-tsc` bzw. die Typprüfung des Projekts als CI-Blocker.
- Tests: Komponententests für jedes Bedienelement, dazu Ende-zu-Ende für
  die Abläufe (Skill `neo-grundregeln`, Abschnitt Tests).
