# Tests

Lesekonvention siehe `SKILL.md`.

**Tests sind Pflicht** für neue Funktionen, Bugfixes und geänderte
Logik. **Kein Abschluss ohne Abdeckung** — eine Fertigmeldung ohne Test
ist keine.

## Oberflächen-Funktionstests

**Jedes Bedienelement hat einen Test**, der die Bedienung auslöst und
das **beobachtbare Ergebnis** prüft. Jeder Knopf, jeder Schalter, jeder
Menüpunkt, jede Dialogaktion, jedes Feld.

**Ein Bedienelement ohne solchen Test gilt als ungetestet** — auch wenn
die dahinterliegende Logik vollständig getestet ist. Das ist die Regel,
die am häufigsten übergangen wird, und sie ist ein Blocker.

**Und zwar an jeder Stelle, an der es vorkommt.** Dieselbe Tabelle mit
demselben Knopf auf zwei Seiten sind **zwei** Prüfungen. Ein Element, das
auf Seite A getestet ist und auf Seite B nicht, gilt auf Seite B als
ungetestet — dort bricht es. Inventar, Durchlauf und Rauchtest:
`durchlauf.md`.

| Stack | Womit |
| --- | --- |
| Vue, Nuxt | Komponententests, dazu Ende-zu-Ende für die Abläufe |
| Flutter | Widget-Tests, dazu Integrationstests |
| Angular | Komponententests, dazu Ende-zu-Ende |
| Contao | Funktionale Tests gegen die gerenderte Seite und das Backend |

Zusätzlich geprüft wird je Bedienelement:

- [ ] Der deaktivierte Zustand löst nachweislich nichts aus.
- [ ] Der Bestätigungsdialog erscheint **vor** dem Destruktiven.
- [ ] Nach der Aktion erscheint die sichtbare Rückmeldung.
- [ ] Der zugängliche Name ist gesetzt.
- [ ] Die Bedienung geht per Tastatur.

## Keine fake-grünen Tests

Ein Test, der immer grün ist, ist schlimmer als keiner: er erzeugt
Vertrauen ohne Grundlage.

| Fake-grün | Stattdessen |
| --- | --- |
| Nur den Statuscode prüfen | Struktur **und** Bedeutung der Antwort prüfen |
| Prüfen, dass nichts geworfen wurde | Prüfen, was herauskommt |
| Eine mutierende Operation aufrufen, ohne die Wirkung zu prüfen | Die beobachtbare Zustandsänderung prüfen |
| Gegen den eigenen Mock prüfen, der dasselbe tut wie der Code | Gegen die Erwartung prüfen, nicht gegen die Umsetzung |
| Zusicherungen abschwächen, bis der Test grün ist | Den Fehler beheben |
| Einen Test überspringen, quarantänieren oder auskommentieren | Beheben oder mit Freigabe entfernen |

**Eine abgeschwächte Zusicherung ist ein Regelverstoß**, kein
Zwischenschritt. Sie fällt im Diff auf und wird zurückgewiesen.

## Kein Test zu einer selbst erfundenen Anforderung

> **Ein Test über Erfundenes ist schlimmer als die Erfindung.**

Die Erfindung allein ist ein Fehler, den jemand beim Lesen bemerkt. Der
Test darüber macht sie zum **Soll**: Er ist grün, er steht im Bericht,
und ab da gilt das erfundene Verhalten als geprüft. Wer es später
korrigiert, macht den Test rot und sieht aus, als hätte er etwas kaputt
gemacht. So wird aus einem Satz, den niemand verlangt hat, eine
Eigenschaft des Produkts, die niemand mehr anzweifelt.

**Vor jedem Test wird die Anforderung benannt** — nicht beschrieben,
benannt:

| Zulässige Herkunft | Beispiel |
| --- | --- |
| Der freigegebene Entwurf | Artboard, Zustand, Beschriftung |
| Eine Anweisung des Projektinhabers | Nachricht, Ticket, Akte |
| Ein Vertrag | OpenAPI, Schema, Gesetzestext, Fiskalvorschrift |
| Ein real aufgetretener Fehler | Regressionstest, siehe unten |

**Findet sich keine dieser Herkünfte, wird kein Test geschrieben,
sondern gefragt.** Ein Test ist kein Ort, an dem eine offene Frage
entschieden wird.

- **Der Test darf nicht die Umsetzung abschreiben.** Er prüft, was
  verlangt wurde, nicht, was der Code gerade tut. Wer den Test aus dem
  eigenen Code ableitet, hat bewiesen, dass der Code tut, was er tut.
- **Ein Test, der einen Oberflächentext festhält**, hält damit auch die
  **Zusage** fest, die in diesem Text steht. Er ist nur zulässig, wenn
  der Text eine Herkunft hat (Kernregel 2).
- **Wird eine Erfindung entdeckt, geht der Test mit.** Der Text wird
  entfernt und der Test, der ihn festhielt, ebenfalls — nicht
  angepasst, bis er wieder grün ist. Und beides wird gemeldet, nicht
  stillschweigend berichtigt.

## Regressionstests

**Für jeden real aufgetretenen Fehler existiert ein Regressionstest,
bevor er als erledigt gilt.** Ohne Ausnahme.

Der Test wird **zuerst** geschrieben, so dass er den Fehler zeigt — dann
wird behoben. Ein Test, der nach dem Fix geschrieben wird, prüft
oft die Umsetzung statt das Verhalten.

Der Test trägt einen Hinweis auf den Vorfall, damit niemand ihn später
als überflüssig entfernt.

## Fremde Anbieter

- **In Tests gefälscht.** Kein Test ruft einen echten Fremddienst — er
  wäre langsam, teuer, unzuverlässig und nicht reproduzierbar.
- **Keine Abhängigkeit von interaktiven Anmeldungen in der CI.** Kein
  Test, der einen zweiten Faktor braucht. Ein echter Anmeldelauf ist ein
  **manueller Rauchtest**, keine Teststrategie.
- **Mock- und Demoschichten werden mitgepflegt:** jede neue
  Schnittstellenfunktion bekommt ihre Mock-Entsprechung im selben
  Commit. Eine Mock-Schicht, die hinterherhinkt, macht die Tests
  wertlos.
- Der Mock bildet auch **Fehlerfälle** ab, nicht nur den Erfolgsfall:
  Zeitüberschreitung, 429, 500, ungültige Antwort.

## Testdaten

- **Isoliert oder aufgeräumt.** Nie im Produktivbestand.
- **Keine echten Kundendaten in Test und Entwicklung.** Wird ein
  Produktivstand für eine Fehlersuche gebraucht, wird er vorher
  anonymisiert; der Vorgang ist freigegeben und dokumentiert
  (Skill `neo-code`, `references/datenmodell.md`).
- Jeder Test legt an, was er braucht, und räumt auf. Ein Test, der von
  einem anderen abhängt, ist zwei Tests zu viel.
- Zeit, Zufall und Kennungen kommen aus einspritzbaren Quellen, damit
  Läufe reproduzierbar sind (Skill `neo-code`,
  `references/querschnitt.md`).

## Was zusätzlich getestet wird

| Bereich | Was |
| --- | --- |
| Mandantentrennung | Für jede neue mandantenbezogene Tabelle: A sieht B nicht (Skill `neo-sicherheit`) |
| Schnittstellen | Je Endpunkt sechs Pflichtfälle, Antwort gegen den Vertrag (Skill `neo-api`, `references/tests.md`) |
| Oberflächendurchlauf | Jedes Bedienelement an jeder Stelle, Rauchtest je Route (`durchlauf.md`) |
| Oberflächengrößen | Acht Breiten: kein Überlauf, nichts ragt hinaus, keine Löcher, Bedienziele (Skill `neo-design`) |
| Komponenten-Grundsatz | Der Wächter-Test (Skill `neo-komponenten`) |
| Designsystem | Layout- und Stilabgleich (Skill `neo-design`) |
| Migrationen | Lauf gegen eine Kopie des Bestands |

## Was der Agent nie tut

- **Einen Test zu etwas schreiben, das er sich selbst ausgedacht hat.**
- **Einen Oberflächentext prüfen, dessen Herkunft er nicht nennen kann.**
- Einen Test überspringen, deaktivieren oder quarantänieren, um grün zu
  werden.
- Eine Zusicherung abschwächen.
- Einen roten Test als Flakiness abtun, ohne es zu belegen.
- „Getestet" melden, wenn nur die Logik getestet ist und die Bedienung
  nicht.
- Testzahlen schätzen. Sie werden genannt: wie viele liefen, wie viele
  sind grün.
