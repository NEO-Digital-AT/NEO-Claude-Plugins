---
name: neo-komponenten
description: >
  NEO-Komponenten-Grundsatz für Oberflächenarbeit. Diesen Skill laden,
  bevor ein Screen, eine View, ein Dialog, ein Widget oder eine
  UI-Komponente gebaut oder geändert wird — egal ob Nuxt/Vue,
  Flutter/Material oder Angular/Material. Regelt Wrapper-Komponenten
  (Neo*, LeoFlex*), ihre Benennung, den Pflichtkatalog, den Vertrag einer
  Komponente, Größen über eine benannte Skala, Farbe und Sprache in der
  Komponente, Frameworktreue, den Umgang mit bestehenden Bibliotheken,
  Interaktionskonventionen und den Wächter-Test, der das maschinell
  durchsetzt.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, belegt an NEO Uptime (CLAUDE.md Abschnitt 1, ADR 0002, web/admin/test/guard.spec.ts), Stand 2026-08
---

# NEO-Komponenten-Grundsatz

## Wie diese Regeln zu lesen sind

| Wort | Bedeutung |
| --- | --- |
| **Nie**, **immer**, **muss** | Verbindlich. Ein Verstoß ist ein **Blocker**: der Wächter-Test schlägt fehl, der Merge wird zurückgewiesen. |
| **Ausnahme** | Nur als Eintrag in der Positivliste des Wächters, mit Begründung, freigegeben vom Projektinhaber. **Es gibt keine Ausnahme, die nicht im Wächter steht** — genau das macht sie im Diff sichtbar. |
| **Sollte** | Begründet abweichbar, die Abweichung wird gemeldet. |

## Die Kernregel

> **Views kennen nur die eigenen Komponenten.**

Jedes wiederkehrende Oberflächenelement ist eine eigene
Wrapper-Komponente mit dem Präfix der Produktfamilie: **Neo*** bei
NEO-Digital-Anwendungen, **LeoFlex*** bei LeoFlex.

Das gilt für **alles**, ohne Ausnahme: jeden Buttonstil, jedes
Eingabefeld, jede Tabelle, jeden Schalter, jeden Dialog, jeden
Inhaltsblock, jede Überschrift, den Logobereich, die Werkzeugleiste, die
Kopfzeile, die Fußzeile, die Seitenleiste, das Navigationsmenü, das
Benutzermenü, die Meldungsleiste — und die gesamte AppShell.

**Views kennen das Designframework nicht.** In einer View kommen nicht
vor:

| Nie in einer View | Warum |
| --- | --- |
| Ein Import aus Nuxt UI, Vuetify, Material, Angular Material | Der Framework-Wechsel wandert sonst in jede View |
| Ein gestaltendes HTML-Element: `div`, `span`, `section`, `button`, `input`, `table`, `ul`, `p`, `h1`–`h6` | Es trägt Gestaltung, die niemand zentral ändern kann |
| Ein `class`- oder `style`-Attribut | Dasselbe |
| Eine Farbkonstante: `#rgb`, `rgb(`, `hsl(`, benannte Farben | Farbe lebt im Token, nicht in der View |
| Eine Maßzahl mit Einheit außerhalb einer Token-Referenz | Maße leben in der Skala |

Erlaubt sind in Views: Komponenten der Familie, Verzweigungen und
Schleifen, Slots, Bindungen — sonst nichts.

**Fehlt eine Komponente, wird sie gebaut.** Kein generischer Ersatz,
keine lokale Variante, kein „nur dieses eine Mal".

**Warum:** Eine Designänderung passiert an genau einer Stelle. Ein
Wechsel der Designbasis — Nuxt UI auf Vuetify, Material 3 auf einen
Nachfolger — trifft nur die Komponenten, nie die Views. Ohne diese Regel
sieht jede Seite anders aus, weil Dialog A anders gebaut ist als
Dialog B.

## Was die Komponente selbst trägt

Die Komponente ist der **einzige** Ort für diese Dinge. Keiner davon
gehört in eine View:

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
  andere Stufe der Skala verkleinerbar — **nie über CSS in der View**.
- Trägt die Fehlerfarbe für Hell und Dunkel selbst.
- Trägt ihren zugänglichen Namen selbst; die View liefert höchstens noch,
  **was** gelöscht wird.
- Löst den Bestätigungsdialog selbst aus, statt ihn jeder View zu
  überlassen.

Die View schreibt damit nur noch, dass hier gelöscht wird — nicht wie das
aussieht, wie es heißt, welche Farbe es hat und ob nachgefragt wird.

Dieselbe Bauart für die anderen wiederkehrenden Handlungen: Anlegen,
Bearbeiten, Speichern, Abbrechen, Duplizieren, Exportieren.

## Eine kleine Auswahl statt jeder Framework-Variante

Nicht jede Buttonvariante des Frameworks bekommt eine Komponente. Es gibt
eine **festgelegte, kleine Auswahl** — und für jede davon eine getrennte
Komponente.

- Der Kanon wird einmal festgelegt und in der Regeldatei des Projekts
  benannt: die Rollen (primär, sekundär, geist, gefährlich) plus die
  handlungsspezifischen Komponenten.
- **Eine neue Variante ist eine Entscheidung des Projektinhabers**, keine
  Nebenwirkung einer View.
- Getrennte Komponenten statt einer Komponente mit vielen Schaltern: eine
  Komponente mit acht Wahrheitswerten ist ein Framework im Framework.

## Größen über eine benannte Skala

- Größen heißen `xs`, `sm`, `md`, `lg`, `xl` — **nie** 34, nie `2rem`.
- Die Komponente legt ihre **Standardgröße** fest. Die View darf sie über
  `size` auf eine andere Stufe der Skala setzen, sonst nichts.
- Die Stufen sind projektweit dieselben und kommen aus den Tokens.
- **Kein `width`, kein `height`, kein `margin` von außen.** Wer eine
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

Der Bereich ist zugleich der Ordner.

## Interaktionskonventionen

- **Destruktive Aktionen nie still.** Löschen, Entfernen, Stornieren
  verlangen einen Bestätigungsdialog, der die Folge benennt. Auslösender
  und bestätigender Knopf tragen die Fehlerfarbe; **die Fehlerfarbe ist
  für Zerstörendes reserviert**.
- **Jede Aktion sagt, dass sie stattgefunden hat.** Ein Formular, das auf
  Speichern hin still bleibt, sieht aus wie ein defektes.
- Harte Fehler = blockierender Dialog. Kurzmeldungen nur für Erfolg und
  Information. Kein Selbstschließen für Inhalte, die gelesen werden
  müssen.
- **Zustand nie nur über Farbe** — immer Symbol plus Wort.
- Tabellen brauchen Suche, Filter, Seitennavigation und einen
  Leer-Zustand (Grenzen in `references/komponentenbau.md`).
- Sentence case, keine Emojis in der Oberfläche.

## Die Bereiche

| Bereich | Referenz |
| --- | --- |
| Pflichtkatalog, Bereiche, wann eine Komponente entsteht, Anti-Muster | `references/katalog.md` |
| Der Vertrag einer Komponente: Eigenschaften, Slots, Ereignisse, Zustände, Zugänglichkeit, Tests | `references/komponentenbau.md` |
| Der Wächter-Test: Regelliste, Algorithmus, Ausnahmeführung, CI | `references/waechter.md` |
| Bestehende Bibliotheken, Migration, Frameworkwechsel | `references/bestandsbibliothek.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

Gestaltung, Eingabeführung, Barrierefreiheit, Verhalten auf allen
Bildschirmgrößen und der Abgleich mit dem Designsystem: Skill
`neo-design`.
