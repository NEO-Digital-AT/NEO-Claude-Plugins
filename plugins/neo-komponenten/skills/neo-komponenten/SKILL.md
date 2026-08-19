---
name: neo-komponenten
description: >
  NEO-Komponenten-Grundsatz für Oberflächenarbeit. Diesen Skill laden,
  bevor ein Screen, eine View, ein Dialog, ein Widget oder eine
  UI-Komponente gebaut oder geändert wird — egal ob Flutter/Material,
  Vue/Vuetify oder Angular/Material. Regelt Wrapper-Komponenten
  (Neo*, LeoFlex*), Frameworktreue, Design-Tokens,
  Interaktionskonventionen und Wächter-Tests.
metadata:
  herkunft: NEO Digital — aus Vue/Vuetify-Projekten übernommen, übertragen auf Flutter/M3 und Angular, Stand 2026-08
---

# NEO-Komponenten-Grundsatz

## Kernregel: Views kennen nur die eigenen Komponenten

- Jedes wiederkehrende Oberflächenelement ist eine eigene
  Wrapper-Komponente mit dem Präfix der Produktfamilie: **Neo*** bei
  NEO-Digital-Anwendungen (z. B. NEOcash), **LeoFlex*** bei LeoFlex.
  Das gilt für ALLES: jeden Buttonstil, jede Tabelle, jeden Schalter,
  Nummernblock, Geldschein- und Münzblock, Kopfzeile, Fußzeile,
  Navigationsmenü, Sidebar, jeden Dialog — und die gesamte AppShell.
- Views und Screens rufen ausschließlich diese Komponenten auf. Sie
  kennen die Design-Komponenten des Frameworks (Material, Vuetify, …)
  nicht und importieren sie nicht direkt.
- Auch das Gesamtlayout gibt eine Komponente vor (AppShell): der
  Nummernblock steht nicht in View A links und in View B rechts.
- Komponenten dürfen andere Komponenten der Familie verwenden — eine
  Buttongruppen-Komponente nutzt die Button-Komponenten, ein Dialog die
  Dialog-Shell.
- Größe, Farbe und Stil gibt die Komponente vor. Dynamisch sind nur
  Inhalt, Ziel und Funktion (Texte, Daten, Callbacks).
- Gleiche Fläche mit anderen Daten = dieselbe Komponente mit Parametern.
  Ein wiederkehrender Dialog (z. B. Trinkgeld) sieht überall gleich aus,
  weil überall dieselbe Komponente läuft.

**Warum:** Eine Design-Änderung passiert an genau einer Stelle. Ein
Wechsel der Designbasis (etwa Material 3 auf einen Nachfolger) trifft nur
die Komponenten, nie die Views. Ohne diese Regel entsteht kein
einheitliches Konzept — Dialog A sieht anders aus als Dialog B.

## Bestehende Komponentenbibliotheken

- Eine bestehende, produktive Wrapper-Bibliothek (z. B. LeoFlex*) NIE
  ohne vorherige, ausdrückliche Freigabe des Projektinhabers
  umschreiben. Erlaubt ist höchstens: Regeln verschärfen und
  optimieren — mit Begründung und Freigabe.
- In jungen, noch nicht weit fortgeschrittenen Anwendungen darf Claude
  nach Freigabe umbauen, was für den Grundsatz nötig ist.
- Definiert ein bestehender Screen das Muster schon: Struktur und
  Aufbau übernehmen, keine lokale Variante erfinden. Fehlt eine
  Komponenten-Definition: keinen generischen Ersatz erfinden —
  nachfragen.

## Frameworktreue innerhalb der Komponenten

- Rangfolge beim Bauen einer Komponente: Original-Komponente des
  Frameworks → bestehender Projekt-Wrapper → Layout-Utilities →
  eigenes CSS/Styling nur als letzter, begründeter Ausweg.
- Nie nachbauen, was das Framework liefert: keine handgebauten Buttons,
  Dialoge, Tabellen, Karten. Eigene Widgets nur dort, wo das Framework
  keine Komponente hat — und auch dort nur aus Original-Tokens und
  Original-Typografierollen zusammengesetzt.
- Keine erfundenen Werte: Farben ausschließlich über Design-Tokens bzw.
  Theme-Rollen (keine Hex-Werte, kein rgba, keine Opacity-Tricks in
  Views), Radien, Abstände und Schriftgrößen nur aus der Skala des
  Design-Systems. Kein fontSize, keine Farbkonstante und keine erfundene
  Maßzahl in einer View.
- Keine dekorativen Verläufe, Schattensysteme oder Animationssysteme,
  keine Ad-hoc-Designexperimente.
- Vor Änderungen an geteilten Primitiven die Design-System-Doku des
  Projekts lesen. Existiert ein Dokumentations-MCP oder eine
  Offline-Referenz der UI-Library (llms.txt, Token-Export): exakte
  Props, Parameter und Werte nachschlagen, dann bauen — nicht raten.
- Liegt eine Design-Referenz vor (Design-Set, Screenshot): sie pixelnah
  umsetzen statt improvisieren — aber nur mit Original-Werten des
  Design-Systems.

## Interaktionskonventionen

- **Destruktive Aktionen nie still:** Löschen, Entfernen, Stornieren
  verlangen immer einen Bestätigungsdialog, der die Folge benennt.
  Auslösender und bestätigender Knopf tragen die Fehlerfarbe; die
  Fehlerfarbe ist für Zerstörendes reserviert.
- Harte Fehler = blockierender Dialog. Toasts/Snackbars nur für Erfolg
  und Information. Kein Auto-Dismiss für Inhalte, die der Nutzer lesen
  muss.
- Zustand nie nur über Farbe anzeigen — immer Symbol plus Wort.
- Tabellen brauchen Suche, Filter, Seitennavigation und einen
  Leer-Zustand.
- Sentence case, keine Emojis in der Oberfläche.

## Durchsetzung

- Wo das Projekt es erlaubt, erzwingt ein Wächter-Test oder eine
  Lint-Regel die Kernregel maschinell: der Wächter schlägt fehl, wenn
  eine View ein rohes Framework-Widget, eine Farbkonstante oder eine
  erfundene Maßzahl verwendet. Neue Ausnahmen brauchen eine Freigabe.
- Jede Komponente und jede View bringt Oberflächen-Funktionstests mit:
  jedes Bedienelement per Test auslösen und das beobachtbare Ergebnis
  prüfen (Details: Skill `neo-grundregeln`, Abschnitt Tests).
- Der Komponenten-Grundsatz gehört als Entscheidungsakte (ADR) und als
  Abschnitt in die Regeldatei des Projekts, mit Verweis auf den Wächter.
