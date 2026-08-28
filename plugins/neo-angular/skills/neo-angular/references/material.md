# Angular Material und Material Design 3

Lesekonvention siehe `SKILL.md`.

> **Für Angular Material gibt es keine `llms.txt`.** Gelesen wird die
> offizielle Dokumentation **der eingesetzten Fassung** — nicht die einer
> anderen. Angular Material hat mehrfach seine Theming-Schnittstelle
> verändert; eine erinnerte Mixin-Signatur ist fast immer die alte.

## Material Design 3 ist ein System

Nicht eine Farbe, nicht ein Schatten, nicht ein Radius. Übernommen wird
**das Gefüge**:

| Ebene | Was übernommen wird |
| --- | --- |
| **Farbrollen** | Primär, Sekundär, Tertiär, Fehler, Oberflächen und die zugehörigen „on"-Rollen — als Rollen, nicht als Einzelfarben |
| **Typografie** | Die Stufen des Systems, durchgängig; keine erfundene Zwischengröße |
| **Form** | Die Radiusstufen; nicht je Komponente ein eigener Wert |
| **Höhe** | Die Schattenstufen; Höhe bedeutet Bedeutung, nicht Dekoration |
| **Zustände** | Die Deckschichten für Hover, Fokus, Gedrückt — nicht selbst gemischt |

**Einzelne Werte herauszupicken ergibt kein Material Design**, sondern
eine Oberfläche, die stellenweise so aussieht.

**Und: wo das Designsystem des Projekts von Material abweicht, gewinnt
das Designsystem.** Die Abweichung ist eine Rückfrage mit
Gegenüberstellung, keine Eigenkonstruktion (Skill `neo-design`,
`references/claude-design.md`).

## Theming

- **Ein Theme, aus Tokens**, hell und dunkel, an einer Stelle definiert.
- **Kein `::ng-deep`.** Es ist abgekündigt, wirkt global und bricht bei
  jeder Fassungsänderung. In NEO-Projekten ist es **verboten**.
- **Kein `!important`**, kein Überschreiben von Material-Klassen in einer
  View.
- **Dichte über die vorgesehene Einstellung**, nicht über Höhen und
  Polster an der einzelnen Komponente.
- Wo ein Wert fehlt, wird das **Theme** ergänzt — nicht die Komponente
  überschrieben.

## Hinter den Wrappern

- **Keine `mat-`-Komponente in einer View** (Skill `neo-komponenten`).
- Der Wrapper **verengt**: nur die Props, die im Projekt vorgesehen sind.
  Eine durchgereichte Prop, die niemand gewollt hat, ist die nächste
  Abweichung vom Designsystem.
- Ein Bibliothekswechsel darf keine View anfassen.

## Was trotz Bibliothek geprüft wird

Angular Material ist zugänglich gebaut — und **nicht automatisch
zugänglich konfiguriert**:

- **Kontraste gerechnet**, auch für Theme-Farben und besonders in
  Hover- und Deaktiviert-Zuständen (`kontrast.py`, Skill `neo-design`).
  Eine Farbrolle, die dem System entspricht, kann im eigenen Theme
  trotzdem durchfallen.
- **Bedienziele**: Symbolknöpfe in Tabellenzeilen sind der häufigste
  Verstoß gegen 44 × 44 px auf schmalen Geräten.
- **Tabellen** füllen die Inhaltsbreite und folgen auf schmal der
  Rangfolge — Spalten weglassen, Zeile zu Karte, erst dann scrollen.
- **Dialoge**: Fokus hinein, gefangen, zurück; Escape schließt; auf
  schmalen Geräten füllend.
- **Textpassung**: Material-Komponenten mit fester Höhe schneiden bei
  langen Beschriftungen ab — in der längsten Sprache prüfen (Skill
  `neo-design`, `references/textpassung.md`).
- **Bewegung** beachtet `prefers-reduced-motion`.

## Symbole

- **Selbst ausgeliefert**, nicht von einem fremden Dienst geladen (Skill
  `neo-recht`).
- **Nur der benötigte Satz**, nicht die ganze Sammlung — sonst wächst das
  Bündel um ein Vielfaches.
- Jedes Symbol trägt einen **Namen** für Vorlesegeräte; ein Symbol ohne
  Text ist ein Knopf ohne Beschriftung.
