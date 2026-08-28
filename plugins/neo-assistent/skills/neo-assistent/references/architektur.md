# Aufbau eines Assistenten

Lesekonvention siehe `SKILL.md`.

## Warum ein großer Prompt scheitert

Ein Systemprompt ist ein einziger Namensraum. Jede Anweisung gilt für
jede Anfrage. Zwei Folgen, beide unvermeidlich:

- **Es gibt keine Kapselung.** Eine Zeile, die für Absicht A geschrieben
  wurde, wird bei Absicht B mitgelesen. Deshalb bricht B, wenn man A
  ändert. Kein Modell und kein besserer Wortlaut behebt das.
- **Die Aufmerksamkeit verteilt sich.** Je mehr gleichrangige
  Anweisungen, desto geringer das Gewicht jeder einzelnen. Ab einer
  gewissen Größe ist eine zusätzliche Regel wirkungslos oder verdrängt
  eine andere.

Die Antwort ist nicht ein kürzerer Prompt, sondern **weniger Prompt je
Anfrage**. Das Modell soll nur sehen, was für diese eine Anfrage gilt.

## Die fünf Schichten

```
┌ Systemprompt ────────────────────────────────────────────┐
│ Rolle, Ton, Grenzen, Eskalation. Gilt immer.             │  < 150 Zeilen
│ Enthält keine Werkzeugauswahl und kein Fachwissen.       │  sprachneutral
└──────────────────────────────────────────────────────────┘
┌ Absicht (genau eine je Anfrage) ─────────────────────────┐
│ Zweck · erlaubte Werkzeuge · Zusatzanweisung             │  < 40 Zeilen
└──────────────────────────────────────────────────────────┘
┌ Werkzeuge (nur die dieser Absicht) ──────────────────────┐
│ Name · Beschreibung mit Abgrenzung · striktes Schema     │
└──────────────────────────────────────────────────────────┘
┌ Zustand ─────────────────────────────────────────────────┐
│ Mandant, heutiges Datum, Auswahl, Ergebnis des letzten   │  Daten,
│ Werkzeugaufrufs. Als Daten übergeben, nie als Prosa.     │  kein Text
└──────────────────────────────────────────────────────────┘
┌ Ablauf ──────────────────────────────────────────────────┐
│ Vorbedingung · Schemaprüfung · Bestätigung · Wiederholung │  Code
│ · Abbruch · Rechte. Im Code, nicht im Prompt.            │
└──────────────────────────────────────────────────────────┘
```

**Die Grenze zwischen Prompt und Code ist die wichtigste Grenze:** Was
verlässlich sein muss, gehört in den Code. Ein Prompt bittet, ein Schema
erzwingt, eine Vorbedingung im Code entscheidet.

| Gehört in den Prompt | Gehört in den Code |
| --- | --- |
| Rolle, Ton, Anrede | Reihenfolge zwingender Schritte |
| Was der Assistent nicht tut | Rechteprüfung |
| Wie er nachfragt, wenn etwas fehlt | Bestätigung vor schreibender Handlung |
| Wie er ein Ergebnis formuliert | Gültigkeit der Argumente |
| Wann eine Absicht zutrifft | Wiederholung und Abbruch |
| — | Kennungen, Datum, Zeitzone, Mandant |

Ein Satz wie „Storniere nie ohne Bestätigung" gehört **zusätzlich** in
den Prompt, aber er ist keine Absicherung. Die Absicherung ist die
Vorbedingung im Code, die einen Aufruf ohne vorherige Bestätigung
zurückweist.

## Eine Stufe oder zwei

**Eine Stufe** — das Modell bekommt Systemprompt und alle Werkzeuge, die
Werkzeugauswahl macht es selbst. Richtig, solange die Werkzeuge wenige
sind und einander nicht ähneln.

**Zwei Stufen** — ein vorgeschalteter Aufruf ordnet die Anfrage einer
Absicht zu, danach bekommt das Bearbeitungsmodell nur die Anweisungen und
Werkzeuge dieser Absicht.

```
Anfrage
   │
   ├─ Stufe 1: Einordnung ──────────────────────────────────┐
   │   kleines, schnelles Modell, kein Werkzeugzugriff      │
   │   Ausgabe streng: { absicht, sprache, sicher }         │
   │   absicht stammt aus der geschlossenen Liste           │
   └────────────────────────────────────────────────────────┘
   │
   ├─ Stufe 2: Bearbeitung ─────────────────────────────────┐
   │   starkes Modell                                       │
   │   Systemprompt + NUR diese Absicht + NUR ihre Werkzeuge│
   └────────────────────────────────────────────────────────┘
   │
   └─ Ablauf: Schema prüfen → Vorbedingung → ausführen → antworten
```

**Was die zweite Stufe wirklich bringt:** eine Änderung an Absicht A
kann Absicht B nicht mehr erreichen, weil B den Text von A nie sieht. Das
ist die Antwort auf „ich ändere etwas und woanders geht etwas kaputt" —
nicht Disziplin, sondern Bauweise.

**Wann die zweite Stufe nötig wird.** Nicht nach Gefühl und nicht nach
einer Zahl, sondern nach der Messung: Wenn die Trefferquote der
Werkzeugwahl mit jedem zusätzlichen Werkzeug sinkt, ist die Grenze
erreicht. Als Orientierung liegt sie oft bei etwa 15 bis 20 Werkzeugen —
bei ähnlichen Werkzeugen deutlich früher. **Die Zahl ist keine Regel,
die Messung ist die Regel** (`goldfaelle.md`).

**Die Einordnung ist kein Textabgleich.** Sie liefert ein Feld aus einer
geschlossenen Liste, über strukturierte Ausgabe erzwungen. Kommt etwas
zurück, das nicht in der Liste steht, gilt die Rückfallabsicht — nie der
ähnlichste Wert.

## Der Zustand

Alles, was der Assistent schon weiß, wird ihm **als Daten** übergeben und
nicht in Prosa erzählt:

```json
{
  "heute": "2026-08-27",
  "zeitzone": "Europe/Vienna",
  "mandant": "M1",
  "benutzer": { "rolle": "sachbearbeitung" },
  "auswahl": { "auftragsnummer": "A-4711" },
  "letztes_ergebnis": { "tool": "auftrag_suchen", "treffer": 1 }
}
```

Damit erledigen sich drei wiederkehrende Fehler:

- **Datumsrechnung.** „Morgen" wird aus `heute` bestimmt, nicht geraten.
  Ohne `heute` rechnet das Modell mit einem erfundenen Tag — der Fehler
  ist selten reproduzierbar und deshalb besonders teuer.
- **Erfundene Kennungen.** Was im Zustand steht, muss nicht erraten
  werden; was nicht darin steht, holt ein Suchschritt.
- **Mandantentrennung.** Der Mandant kommt aus der Sitzung, nie aus dem
  Text der Anfrage (Skill `neo-sicherheit`).

## Der Adapter

Zwischen Anwendung und Modell steht **eine** Stelle, die den Aufruf
zusammensetzt: Systemprompt, Absicht, Werkzeuge, Zustand, Verlauf. Sie
ist zugleich der Punkt, an dem die Goldfälle ansetzen.

```
tools/assistant_adapter.py   Fall (JSON) auf stdin  →  Ergebnis (JSON) auf stdout
```

Der Adapter fährt denselben Weg wie die Anwendung — nicht einen
verkürzten. Ein Prüfweg, der etwas anderes tut als der Betriebsweg, misst
nichts (`goldfaelle.md`).

## Was in den Prompt nie gehört

- Werkzeugschemata als JSON-Block. Sie gehören in die Werkzeugdefinition,
  wo sie erzwungen werden.
- Fachdaten: Listen von Codes, Preisen, Häusern, Zuständen. Sie veralten,
  blähen jeden Aufruf und gehören in ein Nachschlagewerkzeug.
- Beispieldialoge in einer einzigen Sprache. Sie verzerren alle anderen
  (`sprachen.md`).
- Anweisungen, die schon im Schema stehen. Doppelt gepflegt heißt
  irgendwann widersprüchlich.
- Entschuldigungen, Höflichkeitsformeln und Wiederholungen derselben
  Regel in anderen Worten.
