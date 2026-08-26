---
name: neo-komponenten
description: >
  NEO-Komponenten-Grundsatz für Oberflächenarbeit. Diesen Skill laden,
  bevor ein Screen, eine View, ein Dialog, ein Widget oder eine
  UI-Komponente gebaut oder geändert wird — egal ob Nuxt/Vue,
  Flutter/Material oder Angular/Material. Regelt Wrapper-Komponenten
  (Neo*, LeoFlex*), ihre Benennung, den Pflichtkatalog, Größen über eine
  benannte Skala, Farbe und Sprache in der Komponente, Frameworktreue,
  Design-Tokens, Interaktionskonventionen und Wächter-Tests.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, belegt an NEO Uptime (CLAUDE.md Abschnitt 1, ADR 0002, web/admin/test/guard.spec.ts), Stand 2026-08
---

# NEO-Komponenten-Grundsatz

## Kernregel: Views kennen nur die eigenen Komponenten

- Jedes wiederkehrende Oberflächenelement ist eine eigene
  Wrapper-Komponente mit dem Präfix der Produktfamilie: **Neo*** bei
  NEO-Digital-Anwendungen, **LeoFlex*** bei LeoFlex. Das gilt für
  **alles**: jeden Buttonstil, jedes Eingabefeld, jede Tabelle, jeden
  Schalter, jeden Dialog, jeden Inhaltsblock, jede Überschrift, den
  Logobereich, die Werkzeugleiste, die Kopfzeile, die Fußzeile, die
  Seitenleiste, das Navigationsmenü, das Benutzermenü, die
  Meldungsleiste — und die gesamte AppShell.
- **Views kennen das Designframework nicht.** Nuxt UI, Vuetify,
  Material, Angular Material und wie sie heißen kommen in einer View
  nicht vor: kein Import, kein Framework-Element, kein gestaltendes
  HTML-Element, keine Utility-Klasse, kein `style`-Attribut, keine
  Farbkonstante, keine erfundene Maßzahl.
- Erlaubt sind in Views: Komponenten der Familie, Verzweigungen und
  Schleifen, Slots, Bindungen.
- Komponenten dürfen und sollen andere Komponenten der Familie
  verwenden. Eine Buttongruppe nutzt die Buttons, ein Bestätigungsdialog
  die Dialog-Hülle, die AppShell die Kopfzeile.
- Auch das Gesamtlayout gibt eine Komponente vor (AppShell): derselbe
  Block steht nicht in View A links und in View B rechts.
- Gleiche Fläche mit anderen Daten = dieselbe Komponente mit Parametern.
- Fehlt eine Komponente, wird sie gebaut — **kein generischer Ersatz,
  keine lokale Variante.** Eine View, die ein rohes Element braucht,
  deckt eine fehlende Komponente auf.

**Warum:** Eine Designänderung passiert an genau einer Stelle. Ein
Wechsel der Designbasis — Nuxt UI auf Vuetify, Material 3 auf einen
Nachfolger — trifft nur die Komponenten, nie die Views. Ohne diese Regel
sieht jede Seite anders aus, weil Dialog A anders gebaut ist als
Dialog B.

## Was die Komponente selbst trägt

Die Komponente ist der einzige Ort, an dem diese Dinge stehen. Keiner
davon gehört in eine View:

| Gehört in die Komponente | Bleibt Aufgabe der View |
| --- | --- |
| Größe, Abstände, Radien | — |
| Farbe für **Hell- und Dunkelfassung** | — |
| Eigenes CSS bzw. Styling, soweit nötig | — |
| Symbol und Beschriftung samt Übersetzung | — |
| Zustände: Hover, Fokus, Gedrückt, Deaktiviert, Ladend | — |
| Zugänglichkeit: Name, Rolle, Fokusreihenfolge, Zielgröße | — |
| Bestätigungsverhalten bei destruktiven Aktionen | — |
| — | Inhalt, Daten, Ziel, Rückruffunktion |

**Prüffrage vor jedem Commit:** Wenn morgen aus dem Löschsymbol das Wort
„Löschen" werden soll, mehrsprachig — muss dann mehr als eine Datei
angefasst werden? Wenn ja, ist die Regel verletzt.

## Handlungsspezifische Komponenten

Eine allgemeine Buttonkomponente reicht nicht. Wiederkehrende
**Handlungen** bekommen eine eigene Komponente, die alles über diese
Handlung weiß.

Beispiel `NeoFormButtonDelete`:

- Besteht nur aus dem Löschsymbol, Seitenverhältnis 1:1.
- Standardgröße `xl`, über die Eigenschaft `size` auf `md` oder eine
  andere Stufe der Skala verkleinerbar — nie über CSS in der View.
- Trägt die Fehlerfarbe für Hell und Dunkel selbst.
- Trägt ihren zugänglichen Namen selbst; die View liefert höchstens noch,
  **was** gelöscht wird.
- Löst den Bestätigungsdialog selbst aus, statt ihn jeder View zu
  überlassen.

Die View schreibt damit nur noch, dass hier gelöscht wird — nicht wie das
aussieht, wie es heißt, welche Farbe es hat und ob nachgefragt wird.

Dieselbe Bauart gilt für die anderen wiederkehrenden Handlungen:
Anlegen, Bearbeiten, Speichern, Abbrechen, Duplizieren, Exportieren.

## Eine kleine Auswahl statt jeder Framework-Variante

Nicht jede Buttonvariante des Frameworks bekommt eine Komponente. Es gibt
eine **festgelegte, kleine Auswahl** — und für jede davon eine getrennte
Komponente.

- Der Kanon wird einmal festgelegt und in der Regeldatei des Projekts
  benannt: die Rollen (etwa primär, sekundär, geist, gefährlich) plus die
  handlungsspezifischen Komponenten.
- Eine neue Variante ist eine Entscheidung des Projektinhabers, keine
  Nebenwirkung einer View. Wer eine braucht, legt sie vor und begründet
  sie.
- Getrennte Komponenten statt einer Komponente mit vielen Schaltern: eine
  Komponente mit acht Wahrheitswerten ist ein Framework im Framework und
  läuft genauso auseinander wie rohe Elemente.

## Größen über eine benannte Skala

- Größen heißen `xs`, `sm`, `md`, `lg`, `xl` — nicht 34, nicht `2rem`.
- Die Komponente legt ihre **Standardgröße** fest. Die View darf sie über
  die Eigenschaft `size` auf eine andere Stufe der Skala setzen, sonst
  nichts.
- Die Stufen sind projektweit dieselben und kommen aus den Tokens. Eine
  Komponente, die eigene Zahlen erfindet, bricht das System.
- Kein `width`, kein `height`, kein `margin` von außen. Wer eine
  Komponente von außen zurechtschiebt, hat die falsche Komponente.

## Benennung

`{Präfix}{Bereich}{Element}{Ausprägung}` — englische Bezeichner, wie im
Code üblich; die sichtbaren Texte bleiben deutsch.

```
NeoFormButtonDelete      Neo · Form · Button · Delete
NeoDataTable             Neo · Data · Table
NeoShellSidebar          Neo · Shell · Sidebar
LeoFlexFeedbackToast     LeoFlex · Feedback · Toast
```

Der Bereich ist zugleich der Ordner. Gleiches liegt beieinander, und der
Name verrät ohne Suche, wo die Datei liegt. Pflichtkatalog, Bereiche und
die Frage, wann eine neue Komponente entsteht: `references/katalog.md`.

## Bestehende Komponentenbibliotheken

- Eine bestehende, produktive Wrapper-Bibliothek (z. B. LeoFlex*) NIE
  ohne vorherige, ausdrückliche Freigabe des Projektinhabers
  umschreiben. Erlaubt ist höchstens: Regeln verschärfen und optimieren —
  mit Begründung und Freigabe.
- In jungen, noch nicht weit fortgeschrittenen Anwendungen darf Claude
  nach Freigabe umbauen, was für den Grundsatz nötig ist.
- Definiert ein bestehender Screen das Muster schon: Struktur und Aufbau
  übernehmen, keine lokale Variante erfinden. Fehlt eine
  Komponenten-Definition: keinen generischen Ersatz erfinden —
  nachfragen.

## Frameworktreue innerhalb der Komponenten

- Rangfolge beim Bauen einer Komponente: Original-Komponente des
  Frameworks → bestehender Projekt-Wrapper → Layout-Utilities → eigenes
  CSS/Styling nur als letzter, begründeter Ausweg.
- Nie nachbauen, was das Framework liefert: keine handgebauten Buttons,
  Dialoge, Tabellen, Karten. Eigene Widgets nur dort, wo das Framework
  keine Komponente hat — und auch dort nur aus Original-Tokens und
  Original-Typografierollen zusammengesetzt.
- Keine erfundenen Werte: Farben ausschließlich über Design-Tokens bzw.
  Theme-Rollen (keine Hex-Werte, kein rgba, keine Opacity-Tricks),
  Radien, Abstände und Schriftgrößen nur aus der Skala des
  Design-Systems.
- Keine dekorativen Verläufe, Schattensysteme oder Animationssysteme,
  keine Ad-hoc-Designexperimente.
- Vor Änderungen an geteilten Primitiven die Design-System-Doku des
  Projekts lesen. Existiert ein Dokumentations-MCP oder eine
  Offline-Referenz der UI-Library (llms.txt, Token-Export): exakte Props,
  Parameter und Werte nachschlagen, dann bauen — nicht raten.
- Liegt eine Design-Referenz vor (Design-Set, Klickprototyp, Screenshot):
  sie pixelnah umsetzen statt improvisieren — aber nur mit
  Original-Werten des Design-Systems.

## Interaktionskonventionen

- **Destruktive Aktionen nie still:** Löschen, Entfernen, Stornieren
  verlangen immer einen Bestätigungsdialog, der die Folge benennt.
  Auslösender und bestätigender Knopf tragen die Fehlerfarbe; die
  Fehlerfarbe ist für Zerstörendes reserviert.
- **Jede Aktion sagt, dass sie stattgefunden hat.** Ein Formular, das auf
  Speichern hin still bleibt, sieht aus wie ein defektes.
- Harte Fehler = blockierender Dialog. Toasts/Snackbars nur für Erfolg
  und Information. Kein Auto-Dismiss für Inhalte, die der Nutzer lesen
  muss.
- Zustand nie nur über Farbe anzeigen — immer Symbol plus Wort.
- Tabellen brauchen Suche, Filter, Seitennavigation und einen
  Leer-Zustand.
- Sentence case, keine Emojis in der Oberfläche.

Gestaltung, Eingabeführung, Barrierefreiheit und Verhalten auf allen
Bildschirmgrößen regelt der Skill `neo-design`.

## Durchsetzung

- Wo das Projekt es erlaubt, erzwingt ein Wächter-Test oder eine
  Lint-Regel die Kernregel maschinell: der Wächter schlägt fehl, wenn
  eine View ein rohes Framework-Widget, ein gestaltendes HTML-Element,
  ein `class`- oder `style`-Attribut, eine Farbkonstante, eine erfundene
  Maßzahl oder einen Import außerhalb der eigenen Komponenten enthält.
  Vorbild: `web/admin/test/guard.spec.ts` in NEO Uptime.
- Ausnahmen stehen als Positivliste **im Wächter selbst**, je Eintrag mit
  Begründung. Ein neuer Eintrag ist eine Änderung am Wächter und damit
  sichtbar im Diff — genau das ist der Zweck. Neue Ausnahmen brauchen
  eine Freigabe.
- Jede Komponente und jede View bringt Oberflächen-Funktionstests mit:
  jedes Bedienelement per Test auslösen und das beobachtbare Ergebnis
  prüfen (Details: Skill `neo-grundregeln`, Abschnitt Tests).
- Der Komponenten-Grundsatz gehört als Entscheidungsakte (ADR) und als
  Abschnitt in die Regeldatei des Projekts, mit Verweis auf den Wächter.
