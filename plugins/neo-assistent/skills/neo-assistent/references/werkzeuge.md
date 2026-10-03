# Werkzeuge und MCP-Server

Lesekonvention siehe `SKILL.md`.

> **Ein Werkzeug führt aus und hält die Grenzen. Es entscheidet nichts,
> was im Regelwerk steht, und es schreibt dem Kunden nichts.**

## Woher die Werkzeuge kommen

| Quelle | Wann |
| --- | --- |
| **MCP-Server des Fachsystems**, zum Beispiel des Buchungssystems | immer, wo es einen gibt |
| **Eigene Werkzeuge der Anwendung** | nur für Abläufe, für die es keinen MCP-Server gibt — etwa der Nachweis vor Kundendaten, ein Vorgang über mehrere Systeme, die Übergabe an das Team |

Für das Modell ist beides dasselbe: Name, Beschreibung, Schema, Ergebnis.

## Die Freigabeliste

Ein MCP-Server bringt oft Hunderte Werkzeuge mit. **Ein Assistent bekommt
nur die, die seine Art und seine Aufgabe brauchen** — als Liste in der
Anwendung, nicht als Bitte im Skill.

- **Prozesskritische Werkzeuge bekommt eine Kundenassistenz nie:**
  Stammdaten und Einstellungen (Häuser, Tarife, Einheiten, Richtlinien,
  Konfiguration), Löschungen, Tagesabschluss, das Zusammenführen oder
  Anonymisieren von Personen.
- **Die Abrechnung zwischen Plattform und Mandant** — Verträge, Gebühren,
  Rechnungen der Plattform — erreicht nur die Plattformassistenz. Kein
  Werkzeug einer Mandanten- oder Kundenassistenz kommt daran.
- **Ein Werkzeug außerhalb der Liste wird nicht ausgeführt**, auch wenn
  das Modell es aufruft.
- **Neue Werkzeuge des Servers kommen nicht von selbst dazu.** Die
  Aufnahme in die Liste ist eine Änderung mit Freigabe.

## Der Vertrag eines Werkzeugs

- **Die Definition kommt vom Server, wie er sie liefert:** Name,
  Beschreibung, Schema. Keine eigene Abschrift, die mit der nächsten
  Fassung des Servers auseinanderläuft.
- **Die Angaben des Modells gehen unverändert weiter.** Die Anwendung
  ergänzt nur den Zugriffsrahmen (Mandant, Einheit) und prüft das
  Eigentum; sie wählt keine fachlichen Werte für das Modell.
- **Jeder Vertrag ist belegt, bevor er benutzt wird:** gegen die
  Dokumentation im Repository und gegen einen echten Aufruf in der
  Testumgebung — was geschickt wird, was zurückkommt, welche Fehler es gibt
  (Skill `neo-grundregeln`, `references/belegpflicht.md`).
- **Kennungen kommen aus Ergebnissen**, nie aus dem Gedächtnis des Modells
  und nie aus einem Anzeigenamen.

## Selbstständig nutzen

> **Das Modell nutzt seine Werkzeuge selbst — wie Claude Code.** Dafür
> braucht es keinen Skill; es braucht Werkzeuge, die das zulassen.

- **Die Beschreibung eines Werkzeugs sagt, was es tut, was es braucht und
  was es liefert** — kurz. Sie schreibt dem Modell keinen festen Weg vor.
- **Freigegebene Websites:** Das Werkzeug liest jede Seite der
  freigegebenen Domains — die Startseite, gefundene Links, eine selbst
  gebaute Adresse wie ein Veranstaltungskalender mit Zeitraum. Eine
  `llms.txt` ist eine Abkürzung, wo es sie gibt, keine Voraussetzung.
- **Erst die Werkzeuge, dann das Team.** Ein gescheiterter Abruf beweist
  nicht, dass es die Information nicht gibt.

## Ergebnisse und Fehler

- **Ein Ergebnis sind Tatsachen:** Beträge mit Währung, Kennungen, Stand,
  Verweise. Verweise und Beträge übernimmt das Modell Zeichen für Zeichen.
- **Ein Fehler geht als Tatsache an das Modell zurück**, mit der Meldung
  des Fachsystems. Das Modell korrigiert die Angaben oder wählt einen
  anderen Schritt.
- **Ein schreibender Aufruf wird nie verdeckt wiederholt.** Wiederholt
  wird, was das Modell erneut aufruft; derselbe Aufruf mit demselben Fehler
  ist begrenzt (`aufbau.md`).
- **Ein leeres Ergebnis ist ein Ergebnis.** Ein fehlgeschlagener Aufruf ist
  keines: Er belegt nicht, dass es nichts gibt.
- **Ein Werkzeug gibt nie einen fertigen Satz für den Kunden zurück.**

## Schreiben mit Folgen: vorbereiten, dann ausführen

Für Handlungen mit Geld, Stornierung, Rechnung oder Änderung eines
Vorgangs:

1. **Vorbereiten** liest die aktuellen Fakten, prüft die Angaben und hält
   die genaue Handlung fest, mit einer internen Kennung (Token).
2. **Ausführen** führt genau diese festgehaltene Handlung aus. Hat sich
   etwas geändert oder ist die Frist abgelaufen, wird neu vorbereitet.

- **Die Vorbereitung ist kein Bestätigungsritual.** Ob vor dem Ausführen
  gefragt wird, steht im Skill, nicht im Werkzeug. Deckt der Auftrag des
  Kunden die Handlung, darf im selben Durchlauf ausgeführt werden.
- **Das Token ist intern.** Es wird nie dem Kunden gezeigt und nie von ihm
  abgefragt.

## Nichts doppelt

- **Jeder Schreibvorgang ist vermerkt, bevor er das Fachsystem erreicht.**
  Bricht der Lauf mittendrin ab, steht der Vorgang als „Ergebnis ungewiss"
  da.
- **Idempotenz:** Derselbe Vorgang mit demselben Schlüssel bewirkt beim
  zweiten Mal nichts Neues. Eine Wiederholung nach einem Fehler verwendet
  denselben Schlüssel und denselben Inhalt.
- **Ein ungewisses Ergebnis wird geklärt, nie neu erzeugt.** Zuerst
  nachlesen, ob die Buchung, die Zahlung oder die Rechnung schon besteht.
- **Asynchrone Ergebnisse**, etwa ein Zahlungslink, der erst später
  bereitsteht: Das Werkzeug gibt die Kennung des Vorgangs zurück, ein
  Lesewerkzeug fragt denselben Vorgang ab. Nie einen zweiten anlegen, um
  schneller zu sein.

## Sprache

- **Werkzeugnamen, Argumentnamen und Aufzählungswerte sind englisch und
  kanonisch** und werden nie übersetzt. Was der Kunde liest, formuliert
  das Modell in seiner Sprache.
- **Telefonnummern, Daten und Beträge** gehen in der Form an das Werkzeug,
  die das Schema verlangt — Telefonnummern international mit `+` und
  Landesvorwahl, Datum nach ISO 8601 —, nie in der Schreibweise des Kunden.

## Hintergrundarbeit im Werkzeug

Ein Werkzeug darf eine Handlung, die das Modell ausgelöst hat, dauerhaft
zu Ende führen — etwa erst stornieren, wenn die Gebühr bezahlt ist. Es
beginnt **keine** Handlung, die das Modell nicht ausgelöst hat, und sein
Ergebnis geht an das Modell zurück (`aufbau.md`).
