# Der Prozess im Detail

Lesekonvention siehe `SKILL.md`.

## Die neun Schritte

### 1. Analysieren

Was wird gebaut — und **was ausdrücklich nicht**. Der zweite Teil fehlt
fast immer und ist der wichtigere: er verhindert, dass der Umfang
während der Arbeit wächst.

**Zuerst die Regelwerke des Projekts lesen**, in dieser Reihenfolge:

1. `CLAUDE.md` bzw. `AGENTS.md` im Wurzelverzeichnis
2. Das Architekturdokument
3. Das bereichsspezifische Konzeptdokument
4. Die Entscheidungsakten, die den Bereich betreffen

**Wissen allein aus der README reicht nie.** Wer nur die README gelesen
hat, hat nicht analysiert.

### 2. Abhängigkeiten prüfen

Welche bestehenden Funktionen, Verträge, Tests und Dokumente kann die
Änderung treffen? **Vor** der Umsetzung, nicht danach.

Realistische Was-wäre-wenn-Fälle durchdenken und benennen. Die Liste
aus diesem Schritt wird in Schritt 7 wieder gebraucht — wer sie nicht
schreibt, kann sie später nicht prüfen.

### 3. Begründen und belegen

Jede Feststellung mit Quelle: Fundstelle im Code, offizielle
Dokumentation, offizielle Spezifikation (`belegpflicht.md`). Risiken
benennen, auch unbequeme.

### 4. Zusammenfassen und Freigabe abwarten

**Der Schritt, der am häufigsten übersprungen wird.**

Die Zusammenfassung enthält:

- Was gebaut wird, in Sätzen, die der Projektinhaber prüfen kann
- Was ausdrücklich nicht dabei ist
- Welche Dateien und Bereiche betroffen sind
- Welche Risiken bestehen
- Was offen ist und eine Entscheidung braucht

**Was eine Freigabe ist:**

| Ist eine Freigabe | Ist keine Freigabe |
| --- | --- |
| „Ja, mach das so" | „Leg los" **vor** der Zusammenfassung |
| „Ja, aber Punkt 3 anders" (dann gilt die Korrektur) | „Klingt gut" auf eine Frage, die zwei Optionen enthielt |
| Eine ausdrückliche Auswahl aus vorgelegten Optionen | Schweigen |
| „Wie besprochen" mit klarem Bezug | Eine Freigabe für etwas anderes |

**„Leg los" hebt diesen Schritt nicht auf.** Auch dann wird erst
zusammengefasst und die Bestätigung abgewartet. Wer ohne Freigabe baut,
baut auf eigenes Risiko und hat die Regel verletzt, auch wenn das
Ergebnis gefällt.

**Bei Oberflächen kommt ein Schritt davor:** mehrere Vorschläge, als
Skizze oder Screenshot vorgelegt, Änderungsrunden, ausdrückliche
Freigabe (Skill `neo-design`, `references/entwurfsverfahren.md`).

**Liegt bereits ein Entwurf aus Claude Design vor**, entfällt dieser
Schritt — die Gestaltung ist entschieden. Dann gilt: der Entwurf gibt
vor, umgesetzt wird nach Inventar Element für Element, und **jede**
Abweichung ist eine Rückfrage, keine Entscheidung (Skill `neo-design`,
`references/claude-design.md`).

### 5. Umsetzen

**Nur den freigegebenen Umfang.** Fällt beim Bauen etwas auf, das
darüber hinausgeht:

- Harte Sicherheitslücke → sofort beheben, unverzüglich melden.
- Alles andere → **notieren und melden, nicht mitmachen.** Auch wenn es
  eine Zeile wäre. Auch wenn es offensichtlich falsch ist.

### 6. Testen und reparieren

Neue Tests für neues Verhalten (`tests.md`). **Rote Tests werden behoben,
nie umgangen, nie abgeschwächt, nie übersprungen, nie quarantäniert.**

### 7. Nachbarfunktionen mitprüfen

Die Liste aus Schritt 2 wird abgearbeitet — jeder Punkt einzeln, mit
Ergebnis. „Habe ich mir angesehen" ist kein Ergebnis.

### 8. Dokumentieren im selben Schritt

Systemdoku, Änderungsprotokoll, betroffene Handbuch- und Regelseiten
(Skill `neo-doku`). **Nicht im nächsten Commit, nicht morgen.**

### 9. Fertigmelden

Ehrlich:

- Was sichtbar ist und wie man es sieht
- Was offen blieb und warum
- Was als Nächstes ansteht
- **Rote Tests heißen rot.** Zahlen statt Einschätzungen.

## Der Umsetzungsplan bei großen Aufgaben

Bei großen Aufgaben entsteht **vor** der Arbeit ein Plan als Markdown.
„Groß" heißt: mehr als ein Tag, mehr als ein Bereich, oder etwas
Tragendes wird angefasst.

Der Plan enthält:

| Abschnitt | Inhalt |
| --- | --- |
| Reihenfolge | Welcher Schritt vor welchem, und warum |
| Betroffene Bereiche | Module, Dienste, Verträge, Oberflächen |
| Benötigte Dokumentationen | Welche fremden Spezifikationen gebraucht werden, und ob sie vorliegen |
| Mögliche Live-Tests | Was sich am laufenden System prüfen lässt |
| Fehlende Zugangsdaten | Was angefordert werden muss, bevor es weitergeht |
| Nur theoretisch prüfbar | Was nicht getestet werden kann, und warum |
| Risiken | Was schiefgehen kann, mit Auswirkung |
| Rückweg | Wie der Zustand vorher wiederhergestellt wird |

**Erst nach Freigabe des Plans beginnt die Arbeit.**

Der Plan liegt unter `/plan` bzw. `/plans`, nie unter `/docs`
(Skill `neo-doku`).

## Wenn der Umfang während der Arbeit wächst

Das passiert. Der Umgang damit ist festgelegt:

1. **Anhalten**, nicht weiterbauen.
2. Benennen, was dazukommt und warum.
3. Aufwand und Auswirkung schätzen.
4. Vorlegen: mitmachen, verschieben oder weglassen.
5. **Die Entscheidung abwarten.**

Ein gewachsener Umfang ohne Freigabe ist ein Regelverstoß, auch wenn er
gut gemeint war. Er macht den Diff unprüfbar und die Fertigmeldung
wertlos.

## Was der Agent nie tut

- Ohne Freigabe bauen.
- Eine Freigabe für X als Freigabe für Y lesen.
- Den Umfang stillschweigend erweitern.
- Eine Entscheidung treffen, die dem Projektinhaber zusteht.
- „Fertig" melden, solange etwas rot ist oder ungeprüft blieb.
