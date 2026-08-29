# Leistung

Lesekonvention siehe `SKILL.md`.

> **Leistung ohne Zahl ist eine Meinung.**

Schnell ist keine Eigenschaft, die man einem Code ansieht. Sie ist ein
Messwert mit einer Grenze daneben. Ohne Grenze gibt es kein „zu langsam",
und ohne Messung gibt es keinen Beweis — nur den Anruf des Kunden.

## Jeder Endpunkt hat ein Zeitbudget

- **Das Budget steht vor dem Bau fest**, nicht danach: p95 in
  Millisekunden, unter benannter Last, mit benannter Datenmenge. Ein
  Budget, das erst nach der Messung festgelegt wird, ist die Messung.
- **Gemessen wird am fertigen Pfad**, mit echter Datenbank und echter
  Datenmenge — nicht gegen zehn Zeilen in einem Testbestand.
- **Die Zahl steht in der Abnahme**, mit Datum und Bedingungen.
- **Ein Rückgang ist ein Befund**, kein Rauschen. Wer eine Grenze
  überschreitet, legt vor, warum, und der Projektinhaber entscheidet.

| Was | Übliche Grenze | Wo sie herkommt |
| --- | --- | --- |
| Lesender Endpunkt | p95 unter 300 ms | Der Anwender bemerkt darunter nichts |
| Schreibender Endpunkt | p95 unter 800 ms | Ein Klick, der länger dauert, wird zweimal geklickt |
| Hintergrundarbeit | benannt je Auftrag | Sonst wächst sie unbemerkt |

Die Zahlen sind ein **Ausgangswert**, kein Gesetz. Was gilt, entscheidet
der Projektinhaber je Anwendungsfall — aber es gilt eine Zahl.

## Die Datenbank ist fast immer die Ursache

Einzelheiten: `references/efcore.md`. Was hier zählt:

- **Die Abfragezahl je Endpunkt wird gemessen** und als Erwartung im Test
  festgehalten. Eine Zahl, die niemand kennt, wächst — und N+1 fällt erst
  im Betrieb auf, wenn der Bestand groß genug ist.
- **Keine Abfrage ohne Obergrenze.** Jede Liste ist paginiert oder
  begrenzt. Eine unbegrenzte Abfrage ist ein Ausfall mit Ansage: Sie
  läuft zwei Jahre gut und fällt an dem Tag um, an dem der Bestand wächst.
- **Projektion statt Entität**, Lesen ohne Verfolgung.
- **Indizes werden mit dem Abfrageplan begründet**, nicht mit Gefühl. Ein
  Index ohne Messung ist Schreiblast ohne Nutzen.
- **Große Mengen werden gestreamt**, nicht materialisiert:
  `IAsyncEnumerable` statt einer Liste mit hunderttausend Einträgen im
  Speicher.
- **Kein LINQ über eine Menge, die aus der Datenbank hätte gefiltert
  werden können.** Der Filter gehört in die Abfrage, nicht in den
  Speicher.

## Ausgehende Aufrufe

- **`IHttpClientFactory`, immer.** Ein selbst erzeugter `HttpClient` je
  Aufruf erschöpft die Steckplätze; einer als Feld erkennt keinen
  DNS-Wechsel. Beides fällt erst unter Last oder nach einer Umstellung
  auf, und dann schwer.
- **Jeder ausgehende Aufruf hat eine Zeitgrenze.** Ohne sie wartet die
  Anfrage, bis der Aufrufer aufgibt — und der Server hält den Platz
  weiter. Es gibt keinen Aufruf „ohne Zeitgrenze, weil er schnell ist".
- **Wiederholung nur bei wiederholbaren Fehlern**, mit wachsendem Abstand
  und Obergrenze, und nur bei Aufrufen, die sich wiederholen lassen
  (Skill `neo-code`, `references/querschnitt.md`).
- **Ein fremder Dienst darf ausfallen, ohne die eigene Anwendung
  mitzunehmen**: Zeitgrenze, Wiederholung, Abschaltung — und ein
  benanntes Verhalten, wenn er endgültig nicht antwortet.

## Zwischenspeicher

- **Bewusst oder gar nicht.** Ein Zwischenspeicher ohne Schlüsselschema
  und ohne Verfallszeit ist ein Fehler, der später als Datenschutzfrage
  wiederkommt.
- **Nichts Geschütztes im gemeinsamen Zwischenspeicher**, ohne dass der
  Mandant und der Aufrufer im Schlüssel stehen (Skill `neo-sicherheit`).
- **`Cache-Control: no-store`** bei geschützten Antworten.
- **Zuerst die Abfrage reparieren, dann zwischenspeichern.** Ein
  Zwischenspeicher vor einer schlechten Abfrage verbirgt sie nur, bis er
  kalt ist — und kalt ist er genau dann, wenn viel los ist.

## Speicher und Zuteilung

- **Erst messen, dann feilen.** Zuteilungen zu jagen, bevor eine Messung
  sie als Ursache benennt, ist verlorene Zeit und macht den Code
  schlechter lesbar (Kernregel 23).
- Wo eine Messung es verlangt: keine unnötige Zwischenliste, keine
  Zeichenkettenverkettung in einer Schleife, kein Doppelaufzählen einer
  `IEnumerable`.
- **Ein Hintergrunddienst, der nie aufräumt, ist ein Leck mit Verzögerung.**

## Der Lasttest

- **Vor der ersten Ausrollung** und danach vor jeder Änderung, die den
  Datenzugriff berührt.
- **Gegen einen Bestand in der Größenordnung der Wirklichkeit**, nicht
  gegen einen leeren.
- **Berichtet werden p50, p95, Fehlerquote und die Abfragezahl** — nicht
  „lief gut".
- **Ein Lasttest ohne Grenze daneben ist ein Datenpunkt, keine Prüfung.**

## Abnahme

- [ ] Je Endpunkt ein **Zeitbudget** benannt, gemessen, mit Zahl
      berichtet.
- [ ] Abfragezahl je Endpunkt gemessen und im Test festgehalten.
- [ ] Keine unbegrenzte Abfrage; Paginierung überall, wo die Menge
      wachsen kann.
- [ ] Ausgehende Aufrufe über `IHttpClientFactory`, jeder mit Zeitgrenze.
- [ ] Wiederholung mit Obergrenze, Verhalten beim endgültigen Fehlschlag
      benannt.
- [ ] Zwischenspeicher mit Schlüsselschema und Verfallszeit, nichts
      Geschütztes ungeschützt.
- [ ] Lasttest gegen einen realistischen Bestand gelaufen, p50, p95,
      Fehlerquote und Abfragezahl berichtet.
