# Notfall und Bereitschaft

## Das Betriebshandbuch

Je Projekt eine Seite in der Entwicklerdoku (Skill `neo-doku`), die
folgende Fragen beantwortet — kurz, aktuell, ohne Prosa:

| Frage | Inhalt |
| --- | --- |
| Was tut der Dienst? | Zwei Sätze, für jemanden, der ihn nachts zum ersten Mal sieht |
| Wovon hängt er ab? | Datenbank, fremde APIs, Zahlungsdienst, Mailversand, DNS |
| Wie startet er neu? | Der genaue Befehl, in der richtigen Reihenfolge |
| Wo stehen die Protokolle? | Ort, Zugang, was normal aussieht |
| Wie sieht gesund aus? | Statusendpunkt, Kennzahlen, Erwartungswerte (Skill `neo-api`) |
| Wer ist zuständig? | Namen, Erreichbarkeit, Vertretung |
| Was sind die bekannten Störungsbilder? | Symptom, Ursache, Abhilfe — gewachsen aus echten Vorfällen |

Das Handbuch wird **beim Vorfall gelesen und danach ergänzt.** Was
gefehlt hat, kommt hinein.

## Eskalationsstufen

| Stufe | Lage | Reaktion |
| --- | --- | --- |
| 1 | Auffälligkeit ohne Auswirkung auf Anwender | im nächsten Arbeitsschritt |
| 2 | Teil der Funktion gestört, Arbeit noch möglich | am selben Tag, Kunde informiert |
| 3 | Dienst nicht nutzbar, Daten unversehrt | sofort, Bereitschaft, Kunde informiert |
| 4 | Datenverlust, Datenabfluss, Sicherheitsvorfall | sofort, Projektinhaber unverzüglich, Meldewege prüfen (Skill `neo-recht`) |

Die Einstufung nimmt vor, wer den Vorfall entdeckt. **Im Zweifel höher
einstufen** — eine zu hohe Stufe kostet einen Anruf, eine zu niedrige
kostet den Kunden.

## Während der Störung

1. **Zuerst Wirkung begrenzen, dann Ursache suchen.** Ein Rückbau auf
   den letzten funktionierenden Stand ist keine Niederlage.
2. **Protokolle lesen, bevor eine Theorie entsteht** (Skill
   `neo-grundregeln`).
3. Jeder Eingriff wird mitgeschrieben, mit Uhrzeit. Wer später
   rekonstruieren will, was passiert ist, hat sonst nur Erinnerung.
4. Nichts wird gelöscht, was Beweis sein könnte — Protokolle,
   Warteschlangen, fehlgeschlagene Aufträge.
5. Kunden werden informiert, solange die Störung läuft, nicht erst
   danach. Eine Statusseite ist dafür da.
6. **Kein „wir schauen mal".** Wer nach einer festgelegten Zeit keine
   Spur hat, eskaliert.

## Nach der Störung

Nachbereitung innerhalb weniger Tage, schriftlich, im Repo:

- Was ist passiert, in einer Zeitleiste mit Uhrzeiten.
- Wie viele Anwender waren wie lange betroffen.
- Warum ist es passiert — die technische Ursache, nicht der Name eines
  Menschen.
- Warum ist es nicht früher aufgefallen.
- Was verhindert die Wiederholung: **eine Maßnahme mit einem
  Zuständigen und einem Datum.**
- Für jeden real aufgetretenen Fehler entsteht ein Regressionstest,
  bevor er als erledigt gilt (Skill `neo-grundregeln`).

**Ohne Schuldzuweisung.** Wer bestraft wird, meldet beim nächsten Mal
später.

## Wartungsfenster

- Angekündigt, mit Zeitraum und erwarteter Auswirkung.
- Außerhalb der Hauptnutzungszeit des Kunden, nicht der eigenen.
- Mit Rückweg: was passiert, wenn es nicht klappt, steht vorher fest.
- Nach dem Fenster eine kurze Bestätigung, dass alles läuft — geprüft,
  nicht vermutet.
