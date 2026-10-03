# Abnahme, Testdaten, Fehlersuche

Lesekonvention siehe `SKILL.md`.

> **Ein grüner Test beweist die Anwendung, nicht das Modell.** Ob das
> Modell die Skills befolgt, zeigt nur ein Lauf mit dem echten Modell.

## Zwei Belegarten — getrennt berichtet

| Belegart | Was sie beweist | Was sie nicht beweist |
| --- | --- | --- |
| **1. Tests der Werkzeuggrenzen**, mit gestelltem Modell | dass die Anwendung ihre Grenzen hält | dass das echte Modell richtig handelt |
| **2. Lauf im Staging** mit echtem Modell, echter Anwendung und Testdaten | dass ein Anliegen von der Nachricht bis zum Ergebnis funktioniert | dass es in jeder Sprache und jeder Lage funktioniert |

**Eine Belegart ersetzt keine andere.** Fehlt eine, steht in der
Fertigmeldung „nicht geprüft", nie „bestanden".

**Keine Prüfskripte um das Modell.** Kein Messgerüst wertet Antworten oder
Werkzeugwahl des Modells aus: Ob das Modell richtig handelt, zeigt der
echte Lauf.

### 1. Tests der Werkzeuggrenzen

Pflicht, bei jeder Änderung, in der CI:

- **Mandantentrennung:** Ein Aufruf aus Mandant A erreicht nichts von B.
- **Nachweis:** Ohne übereinstimmende Merkmale gibt das Werkzeug nichts
  heraus und verrät nicht, ob es den Vorgang gibt; die Sperre greift.
- **Schalter:** Abgeschaltet heißt nicht ausführbar.
- **Freigabeliste:** Ein Werkzeug außerhalb der Liste wird nicht
  ausgeführt.
- **Doppelausführung:** Derselbe Schreibvorgang zweimal bewirkt einmal
  etwas; ein ungewisses Ergebnis wird geklärt, nicht wiederholt.
- **Neue Nachrichten:** Eine Nachricht während der Arbeit geht in den Lauf
  ein; ein laufender Schreibvorgang wird festgehalten.
- **Zustellung:** KI-Hinweis und Signatur stehen an jeder Antwort; ein
  wiederholter Versand wiederholt keine Handlung.
- **Das Skill-Paket:** vollständig, gültig, im ersten Aufruf ganz im
  Kontext, unter der Größengrenze.

Ein gestelltes Modell ruft nur Werkzeuge auf, die im jeweiligen Aufruf
tatsächlich angeboten werden — sonst prüft der Test einen Assistenten, den
es nicht gibt.

### 2. Lauf im Staging

Vor jeder Freigabe einer Änderung an Skill, Werkzeug, Kontext oder
Modell: die betroffenen Abläufe, von der Nachricht bis zum Ergebnis im
Fachsystem.

- **Testumgebung, Testdaten.** Keine Schreibvorgänge mit echten
  Kundendaten, keine echten Zahlungen.
- **Jede ausgelieferte Sprache für sich.** Die Übersetzung eines deutschen
  Laufs ist kein Lauf.
- **Je Lauf festgehalten:** Ablauf, Sprache, Modell (angefragt und
  geliefert), Stand des Codes, Fassung des Skill-Pakets, Werkzeugaufrufe
  mit Ergebnis, Wirkung im Fachsystem, die zugestellte Antwort, was offen
  blieb.
- **Bewertet wird die Wirkung, nicht der Wortlaut.** „Gebucht" ohne
  Buchung im Fachsystem ist durchgefallen; eine schöne Bestätigung ohne den
  nötigen Zahlungslink ebenso.
- Geheimnisse und Kundendaten stehen nicht in gewöhnlichen Protokollen.

## Wenn der Assistent falsch handelt

1. **Den Lauf lesen, bevor etwas geändert wird:** was im Kontext stand,
   welche Werkzeuge mit welchen Angaben aufgerufen wurden, was zurückkam,
   was geantwortet wurde (Skill `neo-grundregeln`,
   `references/selbstkontrolle.md`).
2. **Die Ursache zuordnen:**

| Befund im Lauf | Ursache | Behoben in |
| --- | --- | --- |
| Die Regel fehlt, ist unklar oder widerspricht einer anderen | Regelwerk | dem Skill, dem der Bereich gehört |
| Das Werkzeug lieferte Falsches oder Unklares oder ließ eine Grenze offen | Werkzeug | dem Werkzeug, mit Test |
| Die Anweisung des Betreibers fehlt oder ist falsch | Einstellung | den Einstellungen — durch den Betreiber |
| Die Regel stand klar im Kontext, und das Modell handelte anders | Modell | zuerst Wortlaut und Ort der Regel prüfen, erst dann die Modellfrage (`modell.md`) |

3. **Nie** eine Prüfung, einen Filter, einen Ersatztext, einen Router oder
   ein zweites Modell als Reparatur (`verbote.md`).
4. **Denselben Fall erneut laufen lassen**, mit dem echten Modell, und das
   Ergebnis berichten.
