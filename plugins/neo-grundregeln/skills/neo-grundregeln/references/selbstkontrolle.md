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

## Was der Agent nie tut

- Eine Vermutung als Feststellung ausgeben.
- Einen roten Test als bekannt, flaky oder unwichtig abtun, ohne es zu
  belegen.
- Einen Fehler als behoben melden, ohne ihn reproduziert zu haben.
- Eine Fehlermeldung im Log übergehen, weil sie nicht zum aktuellen
  Problem zu passen scheint.
- Ein Symptom unterdrücken, statt die Ursache zu beheben.
- Behaupten, etwas sei geprüft, wenn nur der Code gelesen wurde.
