# Endpunkte testen

Lesekonvention siehe `SKILL.md`. Allgemeine Testregeln, fake-grüne Tests
und Regressionstests: Skill `neo-grundregeln`, `references/tests.md`.

> **Jeder Endpunkt wird getestet, und zwar auf das, was er liefert —
> nicht darauf, dass er antwortet.**

Ein Test, der nur den Statuscode prüft, sagt: der Server lebt. Er sagt
nichts darüber, ob im Feld `betrag` der Betrag steht.

## Die Pflichtfälle je Endpunkt

Kein Endpunkt gilt als getestet, solange nicht alle sechs Zeilen
existieren. Das ist eine Liste, keine Auswahl.

| # | Fall | Was geprüft wird |
| --- | --- | --- |
| 1 | **Gutfall** | Statuscode, **Gestalt** der Antwort, **Bedeutung** jedes Feldes |
| 2 | **Ungültige Eingabe** | 400 mit Fehlerhülle, das **fehlerhafte Feld benannt** |
| 3 | **Nicht angemeldet** | 401, kein Datenleck in der Meldung |
| 4 | **Angemeldet, nicht berechtigt** | 403 — und zwar auch für ein **fremdes Objekt**, das es gibt |
| 5 | **Nicht vorhanden** | 404, nicht 500, und nicht 403 für etwas, das es nicht gibt |
| 6 | **Wirkung** | Bei schreibenden Endpunkten: der Zustand **danach** wird gelesen und geprüft |

Dazu, wo zutreffend: Konflikt (409), Ratenbegrenzung (429), zu große
Nutzlast (413), falscher Inhaltstyp (415).

**Fall 4 ist der wichtigste und wird am häufigsten vergessen.** Ein
Endpunkt, der ein fremdes Objekt ausliefert, weil niemand geprüft hat,
ob es dem Anfragenden gehört, ist die häufigste ernste Lücke (Skill
`neo-sicherheit`).

**Fall 6 ist der, der Fall 1 rettet.** Ein `POST`, das 201 liefert und
nichts speichert, besteht Fall 1. Erst der anschließende `GET` zeigt es.

## Die Antwort wird ganz geprüft

„Gestalt und Bedeutung" heißt konkret:

- **Jedes Feld des Vertrags ist vorhanden**, mit dem richtigen Typ.
- **Kein Feld zu viel.** Ein Feld, das nicht im Vertrag steht, ist ein
  Befund — es ist entweder undokumentiert oder ein Datenleck.
- **Die Werte stimmen fachlich**, nicht nur formal: der Betrag ist der
  gebuchte Betrag, das Datum das gespeicherte, der Status der erwartete.
- **Verschachtelte Objekte und Listen** werden mitgeprüft, nicht nur die
  oberste Ebene.
- **Leere Liste ist ein eigener Fall**, mit korrekter Hülle und
  korrekter Gesamtzahl.
- **Sortierung und Blätterung**: erste Seite, letzte Seite, Seite über
  dem Ende, Gesamtzahl.
- **Zahlen als Zahlen**, Datumsangaben im vereinbarten Format mit
  Zeitzone.

**Kein Test gegen ein aufgezeichnetes Antwortdokument im Ganzen.** Ein
Vergleich mit einem gespeicherten Abbild ist grün, bis jemand das Abbild
neu erzeugt — und dann ist er grün mit dem Fehler darin. Geprüft werden
Felder und Bedeutungen.

## Gegen den Vertrag, nicht nur gegen den Code

Swagger und OpenAPI sind Pflicht (`SKILL.md`) — und damit prüfbar:

- **Jede Antwort wird gegen das Schema aus dem Dokument geprüft.** Weicht
  sie ab, ist entweder die Umsetzung oder das Dokument falsch; beides ist
  ein Befund.
- **Jeder Endpunkt des Dokuments hat mindestens einen Test.** Ein
  dokumentierter Endpunkt ohne Test ist ein Versprechen ohne Deckung.
- **Jeder Endpunkt im Code steht im Dokument.** Ein undokumentierter
  Endpunkt ist ein Befund, auch wenn er funktioniert.
- Die Abdeckung wird **gezählt und berichtet**: wie viele Endpunkte im
  Dokument, wie viele getestet.

Damit fällt eine ganze Fehlerklasse weg: der Vertrag, der sich still von
der Umsetzung entfernt hat.

## Was zusätzlich geprüft wird

| Bereich | Was |
| --- | --- |
| Mandantentrennung | A sieht B nicht — je mandantenbezogenem Endpunkt (Skill `neo-sicherheit`) |
| Idempotenz | Zweimal derselbe Aufruf mit demselben Schlüssel ergibt einen Vorgang |
| Nebenläufigkeit | Zwei gleichzeitige Änderungen am selben Objekt enden vorhersehbar |
| Fehlerhülle | Alle Fehler haben dieselbe Gestalt, mit Korrelationskennung |
| Versionierung | Die alte Fassung antwortet weiter wie zugesagt |
| Grenzwerte | Feldlängen, Zahlengrenzen, leere Zeichenkette, Umlaute, Emoji |
| Zeit | Zeitzonen, Sommerzeitwechsel, Datum an der Monatsgrenze |

## Der Vollständigkeitsnachweis

Am Ende steht eine Zahl, keine Einschätzung:

```
Endpunkte im OpenAPI-Dokument      42
davon mit Gutfall-Test             42
davon mit allen sechs Pflichtfällen 39   ← 3 offen
Endpunkte im Code ohne Dokument     0
Antworten gegen das Schema geprüft  42
```

**Jede Zeile unter 100 % wird benannt**, mit dem Namen der Endpunkte.
„Weitgehend abgedeckt" ist keine Aussage.
