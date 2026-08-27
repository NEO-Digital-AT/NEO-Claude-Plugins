---
name: neo-code
description: >
  NEO-Regeln für Codeaufbau und Codestruktur. Diesen Skill laden, bevor
  eine neue Datei, Klasse, Komponente, ein Modul, ein Dienst oder ein
  Projekt angelegt wird, und bei jeder Frage nach Ordnerstruktur,
  Schichten, Benennung, Formatierung, Lint- und Analyseregeln,
  Zustandsverwaltung, Abhängigkeitsinjektion, Nebenläufigkeit oder
  Fehlerbehandlung. Ebenso beim Entwurf eines Datenmodells: Tabellen,
  Spalten, Schemata, Mandantentrennung, Indizes, Löschart, Migrationen. Deckt .NET und C#, Vue 3 und Flutter/Dart ab, dazu
  Querschnittsregeln für Zeit, Geld, Kennungen, Protokollierung und
  Konfiguration.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg; Stackkonventionen nach den offiziellen Leitfäden, Schichtung belegt an bestehenden NEO-Projekten (src/<Produkt>.Api|Domain|Infrastructure|Tests), Stand 2026-08
---

# NEO-Codeaufbau

## Grundsatz: die Vorgaben des Stacks gelten

NEO erfindet keinen Hausstil für Code. Es gilt, was der jeweilige Stack
offiziell vorgibt — **damit sich ein fremder Entwickler sofort
zurechtfindet** und nicht erst eine Hausordnung lernen muss.

| Stack | Maßgeblich |
| --- | --- |
| .NET, C# | Die C#-Codierungskonventionen und die Framework Design Guidelines von Microsoft, durchgesetzt über `.editorconfig` und Analyzer |
| Vue 3 | Der offizielle Vue-Stilleitfaden (Prioritäten A bis D), Composition API mit `<script setup>`, durchgesetzt über ESLint mit dem Vue-Regelsatz |
| Flutter, Dart | Effective Dart (Style, Documentation, Usage, Design) und `flutter_lints`, durchgesetzt über `analysis_options.yaml` |

Einzelheiten je Stack: `references/dotnet.md`, `references/vue.md`,
`references/flutter.md`.

## Rangfolge bei Widersprüchen

1. **Das bestehende Muster des Projekts.** Konsistenz schlägt Reinheit.
   Wer ein Projekt zur Hälfte umstellt, macht es schlechter als es war.
2. **Die offizielle Konvention des Stacks.**
3. **Diese Regeln**, wo der Stack nichts sagt.
4. Persönlicher Geschmack — nie.

Soll ein bestehendes Projekt auf die Konvention gebracht werden, ist das
ein eigener, freigegebener Schritt mit eigenem Commit, nicht ein
Nebenprodukt einer Fehlerbehebung.

## Schichten und Importrichtung

- **Schichtgrenzen sind festgelegt, und die Importrichtung ist eine
  Einbahnstraße.** Innen kennt außen nicht: die Fachlogik weiß nichts von
  der Datenbank, nichts vom Web und nichts von der Oberfläche.
- Bewährter Schnitt, wie in bestehenden NEO-Projekten (`src/<Produkt>.*`):

  ```
  Domain          Fachlichkeit, Regeln, Verträge — kennt nichts
  Infrastructure  Datenbank, fremde APIs, Dateien — kennt Domain
  Api / App       Endpoints, Oberfläche — kennt Domain und Infrastructure
  Tests           kennt alles
  ```

- Ein Verstoß gegen die Richtung wird maschinell abgewiesen, wo das
  Projekt es hergibt (Architekturtest, Lint-Regel, Projektverweis).
- **Die Oberfläche ruft nur eigene Komponenten** — der
  Komponenten-Grundsatz ist Teil der Schichtung (Skill
  `neo-komponenten`).

## Eine Verantwortung je Einheit

- Eine Datei, eine Sache. Wächst eine Datei über das, was auf zwei
  Bildschirmhöhen überblickbar ist, wird sie geteilt — nicht mit einer
  Region kaschiert.
- Eine Funktion tut eine Sache. Braucht sie ein „und" im Namen, sind es
  zwei.
- Keine Sammelbecken: keine `Helper`-, `Utils`-, `Common`- oder
  `Misc`-Datei, in der Unzusammenhängendes landet. Ein Name, der nichts
  aussagt, zieht alles an.
- Kein toter Code, keine auskommentierten Pfade, keine TODOs im
  committeten Stand.

## Benennung

- **Bezeichner sind englisch** — Klassen, Methoden, Variablen, Dateien,
  Tabellen, Spalten, Routen, Zweige.
- **Sichtbare Texte sind deutsch** und kommen aus der Sprachdatei, nie
  aus dem Code (Skill `neo-design`).
- **Kommentare und Dokumentation sind deutsch**, mit echten Umlauten
  (Skill `neo-doku`). Ausnahme: die Doku einer Contao-Erweiterung ist
  englisch (Skill `neo-contao`).
- Ein Begriff je Sache, im ganzen System. Heißt es im Backend `property`,
  heißt es nicht im Frontend `location`.
- Namen sagen, was etwas **ist** oder **tut** — nicht, wie es gebaut ist.
  Keine Typkürzel, keine Ungarische Notation.
- Abkürzungen nur, wenn sie im Fachgebiet üblicher sind als das Wort.

## Kommentare

Der Kommentar erklärt das **Warum**, nie das Was. Was der Code tut, sagt
der Code. Ein Kommentar gehört dorthin, wo jemand später fragen wird
„warum so und nicht anders" — eine Eigenheit einer fremden API, eine
bewusst gewählte Reihenfolge, ein Fehler, der schon einmal passiert ist.

Ein Kommentar, der beim Ändern des Codes nicht mitgeändert wird, ist eine
Lüge im Repository. Beim Ändern mitlesen.

## Maschinell erzwingen

Ohne Werkzeug zerfällt jede Konvention beim ersten Termindruck.

- Formatierung, Lint und Analyse laufen als **CI-Blocker**, nicht als
  Empfehlung.
- Die Konfiguration liegt im Repo (`.editorconfig`, ESLint-Konfiguration,
  `analysis_options.yaml`) und gilt für alle — Editor, Konsole, CI.
- **Warnungen sind Fehler**, wo der Stack das zulässt. Eine geduldete
  Warnung wird zu tausend.
- Eine Ausnahme steht als Eintrag mit Begründung in der
  Werkzeugkonfiguration, nicht als Unterdrückung mitten im Code — im
  Diff sichtbar und freigabepflichtig.
- Formatierung wird nie von Hand nachgezogen und nie in einem
  Fachcommit vermischt.

## Datenmodell

Benennung, Schemata je Modul, Mandantentrennung, Schlüssel und Indizes,
weiches gegen hartes Löschen, Historie, Migrationen ohne Ausfall und
Testdaten ohne echte Kundendaten: `references/datenmodell.md`.

## Querschnitt

Zeit und Zeitzonen, Geld und Rundung, Kennungen, Nullwerte,
Fehlerbehandlung, Protokollierung, Konfiguration und Nebenläufigkeit:
`references/querschnitt.md`. Diese Punkte sind stackübergreifend und
verursachen erfahrungsgemäß die teuersten Fehler.

Zugehörige Skills: `neo-grundregeln` (Prozess, Qualität, Tests),
`neo-api` (Schnittstellen), `neo-komponenten` (Oberflächenkomponenten),
`neo-sicherheit` (Sicherheit im Code), `neo-doku` (Dokumentation).
