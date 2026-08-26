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
| Autorisierung | Jeder Endpoint: erlaubt, verboten, fremdes Objekt |
| Oberflächengrößen | Kein horizontales Scrollen auf acht Breiten (Skill `neo-design`) |
| Komponenten-Grundsatz | Der Wächter-Test (Skill `neo-komponenten`) |
| Designsystem | Layout- und Stilabgleich (Skill `neo-design`) |
| Migrationen | Lauf gegen eine Kopie des Bestands |

## Was der Agent nie tut

- Einen Test überspringen, deaktivieren oder quarantänieren, um grün zu
  werden.
- Eine Zusicherung abschwächen.
- Einen roten Test als Flakiness abtun, ohne es zu belegen.
- „Getestet" melden, wenn nur die Logik getestet ist und die Bedienung
  nicht.
- Testzahlen schätzen. Sie werden genannt: wie viele liefen, wie viele
  sind grün.
