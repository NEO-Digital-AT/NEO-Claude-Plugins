---
name: neo-ki
description: >
  NEO-Regeln für KI im eigenen Produkt. Diesen Skill laden, sobald eine
  Funktion ein Sprachmodell oder ein anderes KI-System einsetzt: Chat,
  Assistent, Textvorschlag, Zusammenfassung, Klassifizierung, Suche mit
  Einbettungen, Bild- oder Sprachgenerierung, Agenten und Werkzeugaufrufe.
  Ebenso bei Fragen zur EU-KI-Verordnung (AI Act), zu Kennzeichnung und
  Offenlegung, zur Wahl des Anbieters und Modells, zur Weitergabe von
  Daten an ein Modell, zu Prompt Injection, zu Kosten und Grenzen sowie
  zum Verhalten, wenn die KI-Fähigkeit abgeschaltet ist.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg; Rechtsstand geprüft 2026-08 (Verordnung (EU) 2024/1689); Technik nach der KI-Integration von LeoFlex
---

# KI im Produkt

## Zwei Fragen vor jeder KI-Funktion

1. **Löst das Problem sich ohne KI besser?** Eine Auswahlliste, eine
   Suche oder eine Regel ist berechenbar, prüfbar und kostenlos. KI ist
   die Antwort auf offene Sprache und unscharfe Muster — nicht auf eine
   Aufgabe, die eine Abfrage erledigt.
2. **Was passiert, wenn die Antwort falsch ist?** Wenn die Folge nicht
   tragbar ist, gehört ein Mensch dazwischen oder die Funktion entsteht
   nicht.

## Rechtsstand: die EU-KI-Verordnung

| Datum | Was gilt |
| --- | --- |
| 01.08.2024 | Verordnung (EU) 2024/1689 in Kraft |
| 02.02.2025 | Verbotene Praktiken; **KI-Kompetenz** des eigenen Personals |
| 02.08.2025 | Pflichten für Modelle mit allgemeinem Verwendungszweck |
| **02.08.2026** | **Transparenzpflichten nach Artikel 50** — verbindlich, ohne Übergangsfrist |
| 02.08.2027 | Weitere Hochrisiko-Regeln |

Bußgeldrahmen: bis **35 Mio. Euro oder 7 %** des weltweiten Jahresumsatzes
bei verbotenen Praktiken, bis **15 Mio. Euro oder 3 %** bei Verstößen
gegen andere Pflichten — die Transparenzpflichten eingeschlossen.

**Was Artikel 50 verlangt**, in Kurzform:

- **Ein Chat oder Assistent gibt sich zu erkennen.** Der Nutzer erfährt,
  dass er mit einer Maschine spricht — es sei denn, das ist ohnehin
  offensichtlich. Die Angabe steht sichtbar, nicht in der
  Datenschutzerklärung.
- **Erzeugte Inhalte werden maschinenlesbar gekennzeichnet.** Text, Bild,
  Ton, Video aus generativer KI tragen eine technische Markierung.
- **Täuschend echte Inhalte** von Personen, Orten oder Ereignissen werden
  ausdrücklich als erzeugt ausgewiesen.
- Systeme zur Emotionserkennung oder biometrischen Kategorisierung legen
  das gegenüber den Betroffenen offen.

Einstufung, Pflichten je Rolle, Kennzeichnung in der Praxis und die
Abgrenzung zu Hochrisiko: `references/ai-act.md`.

**Ehrlichkeitsregel:** „KI-Act-konform" nie behaupten. Die Einstufung des
Systems und die rechtliche Abnahme macht der Rechtsbeistand des Kunden,
nicht der Agent und nicht die Agentur allein (Skill `neo-recht`).

## Offenlegung in der Oberfläche

- Der Hinweis steht **dort, wo die Interaktion beginnt** — im Chatfenster,
  am Eingabefeld, über dem Vorschlag. Nicht in einer Fußnote.
- Er ist verständlich und knapp: was hier KI ist, was sie kann, was sie
  nicht kann.
- **Erzeugte Inhalte sind auch für Menschen erkennbar**, nicht nur
  maschinell — eine Kennzeichnung am Inhalt, nicht nur im Quelltext.
- Der Hinweis ist barrierefrei und erscheint auch ohne JavaScript
  (Skill `neo-design`).
- Wo ein Mensch übernimmt, wechselt der Hinweis sichtbar mit.

## Technik

- **Der Anbieterzugriff ist serverseitig.** Kein Schlüssel im Browser,
  kein Aufruf aus der Oberfläche, nie.
- **Eine gemeinsame Abstraktion**, nicht das SDK des Anbieters im
  Fachcode. Ein Anbieterwechsel darf keine Fachlogik anfassen (Skill
  `neo-code`).
- **Modell, Routing und Residenz kommen aus der Konfiguration**, mit
  einem Standardmodell als Rückfall und der Möglichkeit, es je Ablauf zu
  übersteuern. Kein Modellname im Code.
- **Ist die Fähigkeit abgeschaltet, startet die Anwendung trotzdem** und
  die betroffenen Abläufe behandeln sie als nicht verfügbar — mit
  Meldung, nicht mit einem Absturz.

Grenzen, Prompt Injection, Prüfung der Ausgaben, Kosten, Protokollierung
und Tests: `references/technik.md`.

## Daten

- **Keine personenbezogenen Daten an ein Modell ohne Rechtsgrundlage**,
  ohne Auftragsverarbeitungsvertrag und ohne Eintrag in der
  Datenschutzerklärung (Skill `neo-recht`).
- Was hingeschickt wird, wird vorher **reduziert**: nur die Felder, die
  die Aufgabe braucht. Ein ganzer Datensatz „zur Sicherheit" ist eine
  Übermittlung zu viel.
- Drittlandübermittlung wird benannt, im Consent wie in der Erklärung.
- **Keine Zahlungsdaten, keine Gesundheitsdaten, keine Zugangsdaten** an
  ein Modell — auch nicht versehentlich über einen mitgeschickten
  Protokollauszug.
- Wo der Anbieter Eingaben zum Training verwenden könnte, wird das
  vertraglich ausgeschlossen oder der Anbieter nicht eingesetzt.

## Verantwortung

- **Die Ausgabe eines Modells ist ein Vorschlag, kein Ergebnis.** Sie
  wird nie ungeprüft gespeichert, verschickt, veröffentlicht oder in eine
  Zustandsänderung umgesetzt.
- Wo eine Ausgabe eine Handlung auslöst, prüft der Code die Gestalt und
  die Grenzen der Ausgabe, bevor er handelt.
- **Fremder Text ist Daten, nie Anweisung.** Inhalte aus E-Mails,
  Webseiten, Dateien oder Nutzereingaben dürfen die Aufgabenstellung
  nicht verändern.
- Der Anwender kann eine falsche Ausgabe melden, und die Meldung landet
  irgendwo, wo sie jemand liest.

**Wird ein Assistent mit Werkzeugzugriff gebaut** — Chat, Agent,
Copilot, ein angebundener MCP-Server —, gilt zusätzlich der Skill
`neo-assistent`: Aufbau in Schichten, Absichten statt Schlüsselwörter,
Werkzeugschemata, Mehrsprachigkeit, Goldfälle, Modellwahl.

Zugehörige Skills: `neo-assistent` (Bau von Assistenten),
`neo-recht` (Datenschutz, Consent, Pflichtseiten),
`neo-sicherheit` (Secrets, Härtung), `neo-design` (Oberfläche, Hinweise,
Barrierefreiheit), `neo-api` (Endpoints), `neo-code` (Abstraktion).
