# Löschkonzept und Aufbewahrungsfristen

Die Datenschutzerklärung nennt Speicherdauern. **Ein Löschkonzept sorgt
dafür, dass sie stimmen.** Ohne es ist die Erklärung eine Behauptung.

Auch hier gilt: Bau- und Prüfanleitung, keine Rechtsberatung. Die
Fristen bestätigt der Rechtsbeistand des Kunden — sie ergeben sich aus
Datenschutz-, Steuer- und Unternehmensrecht und widersprechen einander
gelegentlich.

## Das Verzeichnis

Je Projekt eine Tabelle in der Entwicklerdoku, die für **jede** Datenart
beantwortet:

| Spalte | Inhalt |
| --- | --- |
| Datenart | Was es ist, in Worten, nicht als Tabellenname |
| Wo | Tabelle, Dateiablage, Protokoll, Sicherung, Drittdienst |
| Zweck | Wozu die Daten da sind |
| Rechtsgrundlage | Vertrag, Einwilligung, berechtigtes Interesse, gesetzliche Pflicht |
| Frist | Ab wann gerechnet wird, und wie lange |
| Danach | Löschen oder anonymisieren |
| Wie | Der Mechanismus, der es tut |

**Der Auslöser gehört dazu.** „Sieben Jahre" reicht nicht — sieben Jahre
ab Rechnungsdatum, ab Vertragsende oder ab letzter Nutzung sind drei
verschiedene Daten.

## Typische Konflikte

- **Aufbewahrungspflicht schlägt Löschpflicht.** Was gesetzlich
  aufzubewahren ist, wird nicht gelöscht, sondern **gesperrt**: aus dem
  laufenden Betrieb heraus, für den regulären Zugriff unerreichbar,
  bis die Frist abläuft.
- **Einwilligung widerrufen heißt löschen** — aber nicht das, was auf
  einer anderen Grundlage weiterhin gebraucht wird.
- **Ein Bestelldatensatz ist nicht der Newsletter-Eintrag**, auch wenn
  dieselbe Adresse darin steht. Getrennte Zwecke, getrennte Fristen.

## Automatisch, nicht von Hand

- **Was von Hand gelöscht werden müsste, wird nie gelöscht.** Ein
  wiederkehrender Auftrag erledigt es, protokolliert, wie viel er
  gelöscht hat, und meldet sich, wenn er nichts tut.
- Der Lauf ist idempotent und verträgt einen Abbruch.
- Er läuft zuerst im Trockenlauf: zählen, berichten, nichts löschen —
  bis die Zahlen plausibel sind.
- Ein Löschlauf, der plötzlich um ein Vielfaches mehr trifft als sonst,
  bricht ab und meldet. Das ist die Bremse gegen einen Fehler im Filter.

## Technisch

- **Weiches Löschen ist kein Löschen.** Ein Kennzeichen genügt der
  Rechtslage nicht; nach Fristablauf wird hart gelöscht oder anonymisiert
  (Skill `neo-code`, `references/datenmodell.md`).
- **Kaskaden bewusst festlegen.** Ein gelöschter Kunde hinterlässt sonst
  Bestellungen ohne Besitzer — oder reißt eine Buchhaltung mit, die
  bleiben muss.
- **Anonymisieren heißt: der Bezug ist nicht wiederherstellbar.** Ein
  Ersetzen des Namens bei erhaltener Kundennummer ist Pseudonymisierung,
  kein Löschen. Wer Auswertungen behalten will, plant die Anonymisierung
  von Anfang an ein.
- Vergessene Orte, an denen Daten liegen: Protokolle, Zwischenspeicher,
  Suchindizes, Warteschlangen, Exporte, hochgeladene Dateien,
  Mailversand-Dienstleister, Analysewerkzeuge, Sicherungen.
- **Sicherungen sind kein Freibrief.** Aus einer Sicherung wird nicht
  einzeln gelöscht; stattdessen läuft die Sicherung nach ihrer eigenen,
  begrenzten Aufbewahrung aus — und wer eine Sicherung zurückspielt,
  lässt den Löschlauf danach erneut laufen (Skill `neo-betrieb`).

## Betroffenenrechte technisch bedienbar

Die Rechte stehen in der Datenschutzerklärung. Sie müssen auch
**erfüllbar** sein, innerhalb der gesetzlichen Frist:

| Recht | Was die Anwendung können muss |
| --- | --- |
| Auskunft | Alle Daten einer Person über alle Tabellen hinweg einsammeln und ausgeben |
| Berichtigung | Ändern, auch dort, wo Daten gespiegelt wurden |
| Löschung | Der Ablauf oben, auf Zuruf statt auf Frist |
| Einschränkung | Sperren, ohne zu löschen |
| Datenübertragbarkeit | Ausgabe in einem gängigen, maschinenlesbaren Format |
| Widerspruch, Widerruf | Verarbeitung beenden, Einwilligung zurücknehmen |

**Ein Auskunftsersuchen, das drei Tage Handarbeit kostet, ist ein
Baumangel.** Der Weg wird einmal gebaut und getestet — mit einem echten
Testdatensatz, nicht theoretisch.

## Prüfung

- [ ] Verzeichnis vollständig: jede Datenart, jeder Ort, jede Frist.
- [ ] Fristen stimmen mit der Datenschutzerklärung überein.
- [ ] Löschlauf vorhanden, automatisch, protokolliert, mit Bremse.
- [ ] Trockenlauf gemacht, Zahlen plausibel.
- [ ] Anonymisierung prüft nachweislich, dass kein Bezug bleibt.
- [ ] Protokolle, Zwischenspeicher, Suchindizes und Drittdienste bedacht.
- [ ] Auskunft, Löschung und Übertragbarkeit einmal echt durchgespielt.
