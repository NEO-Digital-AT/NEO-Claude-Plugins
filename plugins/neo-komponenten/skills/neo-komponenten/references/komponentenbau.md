# Eine Komponente bauen

Lesekonvention siehe `SKILL.md`.

## Rangfolge beim Bauen

Verbindlich, in dieser Reihenfolge. Jeder Schritt weiter unten braucht
eine Begründung, warum der darüber nicht trägt:

1. **Original-Komponente des Frameworks** — Nuxt UI, Vuetify, Material.
2. **Bestehender Projekt-Wrapper** — eine Komponente der Familie, die es
   schon gibt.
3. **Layout-Werkzeuge des Frameworks.**
4. **Eigenes CSS bzw. Styling** — letzter Ausweg, im Diff begründet.

**Nie nachbauen, was das Framework liefert.** Keine handgebauten Buttons,
Dialoge, Tabellen, Karten, Auswahlfelder. Eigene Widgets nur dort, wo das
Framework keine Entsprechung hat — und auch dort aus Original-Tokens und
Original-Typografierollen zusammengesetzt.

Vor Änderungen an geteilten Primitiven wird die Design-System-Doku des
Projekts gelesen. Existiert ein Dokumentations-MCP oder eine
Offline-Referenz der UI-Bibliothek (llms.txt, Token-Export), werden
**exakte Props, Parameter und Werte nachgeschlagen** — nicht geraten
(Skill `neo-grundregeln`, Belegpflicht).

## Der Vertrag nach außen

Was sichtbar ist, entscheidet, ob ein Frameworkwechsel eine Woche oder
ein Quartal kostet.

| Regel | Folge bei Verstoß |
| --- | --- |
| Eigenschaften im **eigenen Vokabular**: `variant="primary"` ist eine Rolle des Projekts, nicht die Farbe des Frameworks | Blocker |
| **Kein Framework-Typ in der Signatur** | Blocker |
| **Kein Durchreichen unbekannter Attribute** (`v-bind="$attrs"`, Spread) | Blocker — die View kann sonst wieder alles setzen |
| Kein Slot, der rohes Markup erwartet | Blocker |
| Ereignisse in der Sprache der Fachlichkeit: `bestaetigt`, `abgebrochen`, `geaendert` | Muss |
| Höchstens **sechs** Eigenschaften | Sollte — wer mehr braucht, hat zwei Komponenten in einer |
| Ohne die Anwendung darstellbar (Katalog, Klickprototyp, Test) | Muss |

**Die Beschriftung ist kein Pflichtparameter jeder Verwendung.** Trägt
die Komponente ihren Text selbst, kostet eine Umbenennung eine Datei —
sonst alle Views. Ausnahme: Text, der fachlich je Verwendung
unterschiedlich ist.

## Zustände — alle, immer

Jede Komponente baut diese Zustände, und **jeder wird angesehen und
gemessen**:

| Zustand | Verlangt |
| --- | --- |
| Ruhe | Der Ausgangszustand |
| Hover | Verschiebt um **genau eine Stufe**. Der Text nähert sich nie der Fläche an |
| Fokus | Sichtbarer Ring, mindestens 2 px, 3:1 gegen die Umgebung, mit Abstand |
| Gedrückt | Erkennbar, ohne Layoutsprung |
| Aktiv, Ausgewählt | Erkennbar ohne Farbe allein |
| Deaktiviert | Gedämpft, nicht unsichtbar — **und sagt warum** |
| Fehler | Farbe **und** Symbol **und** Text |
| Ladend | Skelett in der Form des echten Inhalts, kein Kreisel |

Fehlt ein Zustand, gilt die Komponente als **nicht fertig**. Kontrast
wird für jeden Zustand gerechnet, nicht geschätzt (Skill `neo-design`,
`references/barrierefreiheit.md`).

## Zugänglichkeit in der Komponente

Sie lebt in der Komponente, damit keine View sie vergessen kann:

- **Zugänglicher Name** für jedes Bedienelement — bei symbolbasierten
  Komponenten Pflichtparameter oder fest eingebaut, nie ableitbar.
- Richtige Rolle und richtiges Element. Ein Knopf ist ein Knopf, kein
  klickbarer Container.
- **Zielgröße mindestens 24 × 24 px**, auf Berührung 44 × 44 px
  angestrebt. Ein kleines Symbol bekommt eine größere Fläche.
- Tastaturbedienung vollständig, Fokusreihenfolge sinnvoll, Escape
  schließt, Dialoge fangen den Fokus und geben ihn zurück.
- `aria-expanded`, `aria-invalid`, `aria-live` dort, wo der Zustand es
  verlangt.
- **Bewegung respektiert `prefers-reduced-motion`.**

## Grenzen, die eine Komponente kennen muss

Statt „Tabellen brauchen Suche und Filter" — hier die Zahlen:

| Element | Ab wann | Was dazukommt |
| --- | --- | --- |
| Liste oder Tabelle | ab **10** Zeilen | Suche |
| Tabelle | ab **25** Zeilen | Seitennavigation oder Nachladen beim Scrollen |
| Tabelle | ab **5** Spalten | Spaltenauswahl, auf schmal reduziert |
| Auswahlfeld | ab **10** Einträgen | Suche im Feld |
| Auswahlfeld | ab **15** Einträgen | Gruppierung, wenn fachlich möglich |
| Jede Liste, Tabelle, Fläche | immer | Leer-Zustand, getrennt nach „nichts angelegt" und „Filter ohne Treffer" |
| Textfeld mit Längengrenze | immer | Zeichenzähler ab 80 % der Grenze sichtbar |
| Vorgang über **10 Sekunden** | immer | Fortschritt mit Auskunft, nicht „Bitte warten" |

Diese Zahlen sind die Untergrenze. Ein Projekt darf sie verschärfen,
nicht aufweichen.

## Tests je Komponente

- **Jedes Bedienelement hat einen Test**, der die Bedienung auslöst und
  das beobachtbare Ergebnis prüft. Ein Bedienelement ohne solchen Test
  gilt als **ungetestet**, auch wenn die Logik dahinter getestet ist
  (Skill `neo-grundregeln`, Tests).
- Getestet wird zusätzlich: jeder Zustand ist erreichbar, der
  deaktivierte Zustand löst nichts aus, der Bestätigungsdialog erscheint
  vor dem Destruktiven, der zugängliche Name ist gesetzt.
- Ein Wächter-Test hält die Kernregel maschinell (`waechter.md`).

## Prüffragen vor dem Commit

1. Steht in einer View eine Farbe, ein Maß, ein Framework-Import? →
   Blocker.
2. Kostet eine Umbenennung mehr als eine Datei? → Vertrag falsch.
3. Fehlt ein Zustand? → nicht fertig.
4. Steht ein Framework-Typ in der Signatur? → Blocker.
5. Gibt es die Komponente schon unter anderem Namen? → zusammenführen,
   nicht duplizieren.
