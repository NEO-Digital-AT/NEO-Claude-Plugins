# Komponentenkatalog

## Bereiche

Der Bereich im Namen ist zugleich der Ordner. Die Liste ist der Rahmen;
Projekte ergänzen fachliche Bereiche (etwa `Contract`, `Account`,
`Invoice`), sie erfinden aber keine zweiten Namen für dasselbe.

| Bereich | Was darin liegt |
| --- | --- |
| `Shell` | Alles, was um den Inhalt herum steht: AppShell, Kopf, Fuß, Seitenleiste, Werkzeugleiste, Benutzermenü, Brotkrume, Seitenkopf |
| `Nav` | Navigation im Inhalt: Reiter, Menü, Seitennavigation, Schrittanzeige |
| `Form` | Alles, was Eingaben entgegennimmt, samt Buttons und Formularaktionen |
| `Data` | Alles, was Daten zeigt: Tabelle, Liste, Kennzahl, Abzeichen, Beschreibungsliste, Diagramm |
| `Feedback` | Dialog, Bestätigung, Kurzmeldung, Meldungsleiste, Hinweisblock, Leer-Zustand, Skelett, Fortschritt |
| `Layout` | Seite, Abschnitt, Karte, Raster, Trennlinie — die Gefäße für Inhalt |
| `Text` | Überschrift, Fließtext, Link, Zahl, Datum, Codeanzeige |
| `Brand` | Wortmarke, Bildmarke, Symbol, Avatar |

## Pflichtkatalog

Diese Komponenten hat jede NEO-Anwendung, bevor die erste View entsteht.
Fehlt eine, wird sie gebaut — nicht ersetzt.

**Shell.** AppShell · Header · Sidebar · SidebarItem · UserMenu ·
Breadcrumb · PageHeader · Footer · ThemeToggle · LanguageSwitch

**Nav.** Tabs · Tab · Menu · MenuItem · Pagination

**Form.** ButtonPrimary · ButtonSecondary · ButtonGhost ·
ButtonDelete · ButtonEdit · ButtonAdd · ButtonSave · ButtonCancel ·
IconButton · Field · Input · Textarea · Select · Combobox · Checkbox ·
RadioGroup · Switch · Segmented · DateField · TimeField · NumberField ·
FileDrop · SearchField · FormActions

**Data.** Table · TableToolbar · TablePagination · Badge · Tag ·
KpiTile · DescriptionList

**Feedback.** Dialog · ConfirmDialog · Toast · ToastRegion ·
NotificationBar · Callout · EmptyState · Skeleton

**Layout.** Page · Section · Card · Divider · Toolbar

**Text.** Heading · Text · Link · Number · DateTime

**Brand.** Icon · Wordmark · Brandmark · Avatar

Der Katalog ist die Untergrenze, nicht die Obergrenze. Was ein Projekt
zusätzlich braucht, kommt dazu — nach demselben Muster benannt.

## Wann eine neue Komponente entsteht

Eine neue Komponente entsteht, wenn **eine** dieser Bedingungen zutrifft:

- Dasselbe Element erscheint zum zweiten Mal.
- Eine View bräuchte ein rohes Element, um weiterzukommen.
- Eine bestehende Komponente müsste einen weiteren Schalter bekommen, der
  ihr Aussehen grundlegend ändert.
- Eine wiederkehrende Handlung (Löschen, Anlegen, Exportieren) hat noch
  keine eigene Komponente.

Sie entsteht **nicht**, weil eine einzelne View eine Sonderform hübsch
fände. Das ist der Weg, auf dem jede Seite anders aussieht.

## Der Vertrag einer Komponente

Was nach außen sichtbar ist, entscheidet darüber, ob ein
Frameworkwechsel später eine Woche oder ein Quartal kostet.

- **Eigenschaften im eigenen Vokabular.** `variant="primary"` ist eine
  Rolle des Projekts, nicht die Farbe des Frameworks. Nie einen
  Framework-Wert durchreichen und nie einen Framework-Typ in der
  Signatur führen.
- **Kein Durchreichen unbekannter Attribute.** Wer alle Attribute
  weiterleitet, hat die Kapselung aufgegeben: dann steht die Farbe eben
  doch in der View.
- **Was aufklappt, klappt in der Komponente um.** Auswahl, Menü,
  Datumswähler und Tooltip entscheiden **selbst** beim Öffnen, ob nach
  oben oder unten, nach links oder rechts Platz ist, und sie tragen ihren
  eigenen Scrollbereich, wenn keine Richtung reicht. Die View gibt nur
  Inhalt und Ziel. Steht die Richtung in der View, gibt es sie so oft, wie
  die Komponente benutzt wird — und falsch ist sie dann überall dort, wo
  niemand hingesehen hat (Skill `neo-design`, `references/responsiv.md`).
- **Kein Slot, der rohes Markup erwartet.** Slots nehmen Inhalt oder
  andere Komponenten der Familie.
- **Ereignisse in der Sprache der Fachlichkeit**: `bestaetigt`,
  `abgebrochen`, `geaendert` — nicht `click` auf einem inneren Element.
- Feste, kleine Menge von Eigenschaften. Wer mehr als etwa sechs braucht,
  hat zwei Komponenten in einer.
- Jede Komponente ist ohne die Anwendung darstellbar — für den
  Klickprototyp, den Katalog und die Tests.

## Frameworkwechsel

Das Ziel ist überprüfbar: **Beim Wechsel des Frameworks ändert sich
nichts unterhalb von `components/`.**

Prüfbar mit zwei Fragen:

1. Kommt der Name des Frameworks irgendwo außerhalb des
   Komponentenordners vor — in einer View, einem Store, einem Test, einer
   Route? Jedes Vorkommen ist eine Fessel.
2. Steht in der Signatur einer Komponente ein Typ, ein Wertebereich oder
   eine Aufzählung des Frameworks? Dann wandert der Wechsel in die Views.

Der Wächter-Test prüft Frage 1 maschinell. Frage 2 wird bei der
Durchsicht geprüft.

## Anti-Muster

| Muster | Warum es scheitert |
| --- | --- |
| `NeoBox` mit freien Abstands- und Farb-Eigenschaften | Ein `div` mit anderem Namen. Die Regel ist damit umgangen, nicht erfüllt. |
| Eine Komponente mit acht Wahrheitswerten | Ein Framework im Framework; niemand weiß mehr, welche Kombination geprüft ist. |
| `v-bind="$attrs"` bzw. Spread aller Eigenschaften | Die View kann wieder alles setzen, auch Farbe und Maß. |
| Beschriftung als Pflichtparameter jeder Verwendung | Beim Umbenennen sind alle Views betroffen — genau das, was verhindert werden soll. |
| Eine Kopie der Komponente „nur für diese eine Seite" | Zwei Wahrheiten, die auseinanderlaufen. |
| Größe als Zahl von außen | Bricht die Skala und damit die Einheitlichkeit. |

## Prüfliste für eine neue Komponente

- [ ] Name nach `{Präfix}{Bereich}{Element}{Ausprägung}`, im passenden
      Ordner.
- [ ] Baut auf der Original-Komponente des Frameworks auf; eigenes
      Styling nur, wo begründet.
- [ ] Farbe, Größe, Radius, Abstand ausschließlich aus Tokens.
- [ ] Hell- und Dunkelfassung gebaut und angesehen.
- [ ] Standardgröße gesetzt, Skala über `size` erreichbar.
- [ ] Alle Zustände gebaut: Ruhe, Hover, Fokus, Gedrückt, Aktiv,
      Deaktiviert, Fehler, Ladend.
- [ ] Kontrast gerechnet, auch für Hover (Skill `neo-design`).
- [ ] Zugänglicher Name, Rolle, Tastaturbedienung, Zielgröße ≥ 24 px.
- [ ] Sichtbare Texte aus der Sprachdatei, in der Komponente.
- [ ] Oberflächen-Funktionstest je Bedienelement.
- [ ] Im Komponentenkatalog bzw. Klickprototyp des Projekts eingetragen.
- [ ] Keine Framework-Typen in der Signatur.
