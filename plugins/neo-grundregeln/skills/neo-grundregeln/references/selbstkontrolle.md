# Selbstkontrolle, Auswirkungsanalyse, Debugging

Lesekonvention siehe `SKILL.md`.

## Nach jeder Änderung, vor dem nächsten Schritt

**Den eigenen Code noch einmal lesen und gegen den freigegebenen Umfang
prüfen — BEVOR der nächste Schritt beginnt.** Nicht am Ende, nicht vor
dem Commit, sondern nach jeder Änderung.

Gelesen wird der **Diff**, nicht die Erinnerung an das, was man tun
wollte. Die häufigsten Funde dabei: eine vergessene Debug-Ausgabe, eine
Datei, die versehentlich mit drin ist, eine Zeile, die man „nur schnell"
mitgeändert hat.

## Auswirkungsanalyse

Pflicht, und zwar schriftlich. Benannt wird, **was betroffen ist**:

| Bereich | Frage |
| --- | --- |
| Programmteile | Wer ruft das auf? Wer wird davon aufgerufen? |
| Verträge | Ändert sich etwas an einer API, einem Schema, einem Ereignis? |
| Tests | Welche Tests decken das ab? Welche müssen mit? |
| Dokumente | Welche Doku, welches Handbuch, welche Regeldatei? |
| Datenbank | Migration nötig? Bestehende Daten betroffen? |
| Betrieb | Startvorgang, Konfiguration, Ausrollung, Überwachung? |
| Sicherheit | Autorisierung, Daten, Protokolle, Angriffsfläche? |
| Oberfläche | Weicht etwas vom Designsystem ab? |

Ein Punkt ohne Antwort ist nicht geprüft. **„Nicht betroffen" ist eine
gültige Antwort, „weiß nicht" nicht.**

## Debugging: Logs zuerst, dann Hypothese

**Vor jeder Ursachentheorie werden die Laufzeit-Logs gelesen.** Wer
zuerst rät und dann sucht, findet Belege für die falsche Theorie.

Reihenfolge:

1. **Das Symptom genau benennen.** Was passiert, was sollte passieren,
   ab wann, wie oft, bei wem.
2. **Die Logs lesen** — die des betroffenen Laufs, nicht die von gestern.
3. **Sichtbare Fehlermeldungen sofort im Code verfolgen.** Eine Meldung,
   die man für einen Nebeneffekt hält, ist meistens die Ursache.
4. **Reproduzieren.** Ein Fehler, der sich nicht reproduzieren lässt, ist
   nicht verstanden.
5. **Erst dann eine Hypothese** — und die wird geprüft, nicht geglaubt.
6. **Beheben, an der Ursache.** Nicht am Symptom, nicht mit einem
   Sonderfall, nicht mit einem `try/catch` darum.
7. **Regressionstest schreiben**, bevor der Fehler als erledigt gilt
   (`tests.md`).

## „Das wird es beheben" — drei Bedingungen

Dieser Satz fällt nie, solange nicht **alle drei** zutreffen:

1. **Das Log bestätigt den exakten Fehlerweg.** Nicht ein ähnlicher Weg,
   nicht ein plausibler.
2. **Der Fix adressiert genau diesen Weg.**
3. **Der Nutzer hat das Ergebnis verifiziert.**

Solange eine davon fehlt, heißt es: „Vermutung, noch nicht verifiziert" —
mit der Angabe, welcher Beleg fehlt.

## Grüne Tests sind keine Laufzeitverifikation

**Berührt eine Änderung eines dieser Dinge, wird das ausgelieferte
Verhalten geprüft — nicht nur die Tests:**

- Laufzeitverhalten und Startvorgang
- Migrationen
- Routing
- Authentifizierung und Autorisierung
- Konfiguration und Umgebungswerte
- Extern sichtbares Verhalten
- Alles, was mit einem Container, einem Build oder einer Ausrollung zu
  tun hat

Geprüft heißt: **Neustart, Build, Probelauf** — und das Ergebnis
angesehen. Nicht „sollte gehen".

Aus der Praxis belegt: die EF-Falle beim Anlegen über die Navigation ist
in einem Projekt dreimal aufgetreten und jedes Mal **erst im
Laufzeitlauf** aufgefallen, nie im Test (Skill `neo-code`,
`references/dotnet.md`).

## Validierungsreihenfolge

Fest, nach jeder substanziellen Änderung:

```
1  Abhängigkeiten installieren
2  Lint und statische Analyse
3  Tests
4  Build
```

**Rote Tests und Analysefehler sind Blocker.** Kein Weiterarbeiten, kein
Commit, keine Fertigmeldung. Ein Schritt wird nicht übersprungen, weil
der vorige „schon gestern lief".

## Ein Befund ist eine Klasse — aber kein Auftrag

> **Suchen ist Information. Beheben ist Auftrag. Einen Agenten starten ist
> eine Handlung. Nur das Erste geschieht von sich aus.**

Wer nur die genannte Stelle behebt, liefert dieselbe Meldung in einer Woche
erneut, für die Seite daneben. Deshalb wird nach jedem gemeldeten Mangel
**dieselbe Ursache gesucht** — gesucht, nicht behoben:

| Wo noch gesucht wird | Warum |
| --- | --- |
| **Das andere Ende** | Links gefunden heißt rechts ungeprüft — oben heißt unten |
| **Andere Breiten und Größen** | 16 px am Telefon sind 90 px im niedrigen breiten Fenster |
| **Jede Seite mit derselben Komponente** | Die Ursache sitzt in der Komponente, nicht auf der Seite |
| **Derselbe Zustand woanders** | Hover, Fokus, leer, ladend, Fehler |
| **Dieselbe Ursache in anderer Form** | Ein vergessener Wert ist selten einmal vergessen |

**Und dann hört es auf.** Das Suchen darf die Arbeit nicht erweitern:

- **Behoben wird nur das gemeldete Problem** (Kernregel 3). Die weiteren
  Fundstellen werden **aufgelistet und zu Punkten**, nicht mitbehoben —
  auch nicht, wenn die Behebung „dieselbe Zeile" wäre.
- **Kein Fachagent für einen Befund.** Ein Agent wird für den Auftrag
  gestartet, nicht je Fundstelle und nicht je Testbefund. Höchstens einer
  je Punkt (`orchestrierung.md`).
- **Ein Testbefund ist kein Auftrag.** Dass eine Prüfung etwas findet,
  macht es nicht zur Aufgabe dieser Sitzung. Es macht es zu einem Punkt
  auf der Liste, den der Projektinhaber freigibt oder streicht.
- **Die Suche selbst bleibt klein.** Sie beantwortet „wo noch?", nicht
  „was ist hier sonst nicht in Ordnung?". Eine Suche, die in eine
  allgemeine Prüfung des Projekts übergeht, ist aus dem Ruder gelaufen.
- **Die Zahl gehört in die Antwort**: „gemeldet: 1, behoben: 1, weitere
  Fundstellen als Punkte notiert: 6".

**Der Fall, aus dem diese Fassung entstanden ist:** Ein gemeldetes Problem
löste eine Prüfung aus, die Prüfung fand weitere Befunde, und für die
Befunde wurden Agenten gestartet — Arbeit an Dingen, die niemand
beauftragt hatte, während das gemeldete Problem darin unterging.

## Der Reparaturvoranschlag

> **Ein Prüfbericht endet mit einem Voranschlag, nicht mit einer
> Reparatur.**

Ein Review, ein Testlauf, ein Prüfwerkzeug findet Befunde. Was davon
behoben wird, entscheidet der Projektinhaber — und er kann es nur
entscheiden, wenn er weiß, was es kostet. Deshalb steht am Ende jeder
Prüfung diese Tabelle, und **nichts läuft, bevor sie freigegeben ist**:

```
Nr  Befund                            Notwendigkeit  Agenten  Dauer
 1  Kontrast 1,08:1 im dunklen Block   Blocker           1     ~25 min
 2  Randstreifen 16 px auf 3 Seiten    Blocker           1     ~40 min
 3  Zwei Begriffe für dieselbe Sache   sollte            0     ~10 min
 4  Abstand 14 statt 16 px             kosmetisch        0     ~5 min
 5  „Fehlender Alternativtext"         kein Befund       0       —
                                       Summe: 2 Agenten, ~75 min
```

### Die vier Stufen der Notwendigkeit

| Stufe | Was hineingehört |
| --- | --- |
| **Blocker** | Fehlfunktion, Datenverlust, Sicherheitslücke, rechtliche Pflicht, Verstoß gegen eine Regel mit „nie", „immer" oder „muss" |
| **sollte** | Ein echter Mangel, an dem nichts bricht: Wortwahl, doppelte Begriffe, fehlender Test, unsaubere Struktur |
| **kosmetisch** | Sichtbar, aber ohne Folge. Kann bleiben |
| **kein Befund** | Der Prüfer hat sich geirrt. **Wird trotzdem genannt**, mit Begründung, sonst taucht er beim nächsten Lauf wieder auf |

**Die Stufe wird begründet, nicht behauptet.** „Blocker" braucht den Satz,
was bricht; „kosmetisch" den Satz, warum nichts davon abhängt.

### Die Dauer ist eine Schätzung und heißt so

- **Grundlage benennen**: Zahl der berührten Dateien, ob gemessen werden
  muss, ob ein Fremdsystem beteiligt ist. Eine Zahl ohne Grundlage ist
  geraten.
- **Nach der Arbeit wird die tatsächliche Dauer genannt**, neben der
  geschätzten. Nur so werden die Schätzungen besser.
- **Zwei Stunden sind keine Schätzung, sondern ein Schnitt.** Was länger
  dauert, wird in Punkte zerlegt und einzeln vorgelegt.

### Vor der Freigabe läuft nichts

- **Kein Fachagent**, auch keiner „zur Vorbereitung" oder „nur zum
  Nachsehen".
- **Keine Datei geändert**, auch nicht die eine Zeile, die „sowieso klar"
  ist.
- **Keine Teilfreigabe von selbst.** Gibt der Projektinhaber Befund 1 und
  3 frei, bleiben 2 und 4 offene Punkte auf der Liste — nicht
  „naheliegend mitgemacht".
- **Einzige Ausnahme: eine harte Sicherheitslücke.** Die wird sofort
  behoben und unverzüglich gemeldet (Kernregel 27). Alles andere wartet.

## Die eigene Aufnahme ist Prüfgegenstand

**Jeder Screenshot, jede Aufnahme, jede Ausgabe, die der Agent selbst
erzeugt, wird angesehen, bevor sie in eine Antwort kommt** — vollständig,
nicht an der Stelle, um die es ging.

- **Jeder sichtbare Mangel wird in derselben Antwort gemeldet**, auch wenn
  er nicht zur Aufgabe gehört.
- **Ein Mangel, der in einer eigenen Aufnahme sichtbar war und nicht
  gemeldet wurde, ist ein Verstoß.** „Nicht aufgefallen" ist keine
  Auskunft: Die Aufnahme lag vor.
- Bei Oberflächen im Einzelnen: Skill `neo-design`,
  `references/pruefstand.md`.

## Keine Behebung erzeugt einen neuen Befund

**Vorher und nachher wird mit demselben Werkzeug gemessen, und die
Befundlisten werden verglichen.** Null neue Befunde.

Eine Behebung, die einen anderen Befund erzeugt, wird **umgebaut, bevor
sie gemergt wird** — nicht danach gemeldet und nicht als Folgeaufgabe
notiert. Das gilt auch, wenn der neue Befund „kleiner" wirkt als der
alte: Ob er kleiner ist, entscheidet der Projektinhaber.

## Was der Agent nie tut

- Eine Vermutung als Feststellung ausgeben.
- Einen roten Test als bekannt, flaky oder unwichtig abtun, ohne es zu
  belegen.
- Einen Fehler als behoben melden, ohne ihn reproduziert zu haben.
- Eine Fehlermeldung im Log übergehen, weil sie nicht zum aktuellen
  Problem zu passen scheint.
- Ein Symptom unterdrücken, statt die Ursache zu beheben.
- Behaupten, etwas sei geprüft, wenn nur der Code gelesen wurde.
- **Einen Mangel in einer eigenen Aufnahme übergehen.**
- **Nur die gemeldete Stelle beheben**, ohne dieselbe Ursache anderswo
  gesucht zu haben.
- **Eine Behebung mergen, die einen neuen Prüfbefund erzeugt.**
- **Nach einer Prüfung mit dem Reparieren anfangen**, ohne Voranschlag und
  ohne Freigabe.
- **Eine Dauer nennen, ohne ihre Grundlage zu nennen** — oder die
  tatsächliche Dauer danach verschweigen.
