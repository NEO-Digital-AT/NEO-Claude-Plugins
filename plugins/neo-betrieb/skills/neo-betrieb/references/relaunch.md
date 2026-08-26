# Umzug und Neuauflage

Der teuerste Fehler einer Website-Neuauflage ist unsichtbar: die alten
Adressen verschwinden. Verweise von außen, Lesezeichen und Platzierungen
in Suchmaschinen laufen ins Leere. Es dauert Monate, bis das zurückkommt
— wenn es zurückkommt.

## Vor dem Umbau: die alten Adressen erheben

Nicht schätzen. Aus **allen** Quellen zusammentragen und entdoppeln:

- Sitemap der alten Seite
- Serverprotokolle der letzten Monate — dort stehen auch die Adressen,
  die keine Sitemap kennt
- Suchkonsole: was ist indexiert, was bekommt Aufrufe
- Analysewerkzeug: welche Seiten werden tatsächlich besucht
- Eingehende Verweise: welche Adressen verlinkt jemand von außen
- Dateien: PDF, Bilder, Downloads. Ein verlinktes Preisblatt ist eine
  Adresse wie jede andere

Ergebnis ist eine Liste, die im Repo liegt, nicht im Kopf.

## Die Zuordnung

Jede alte Adresse bekommt genau ein Ziel:

| Fall | Ziel |
| --- | --- |
| Inhalt existiert weiter | die neue Adresse desselben Inhalts, **301** |
| Inhalt wurde aufgeteilt | die passendste neue Seite, nicht die Übersicht |
| Inhalt wurde zusammengelegt | die neue Sammelseite |
| Inhalt entfällt ersatzlos | die nächstliegende thematische Seite — oder bewusst **410** |
| Adresse war ein Fehler | **404**, ausdrücklich so entschieden |

Verboten:

- **302 statt 301.** Eine vorübergehende Weiterleitung überträgt nichts.
- **Alles auf die Startseite.** Das wertet die Suchmaschine als Fehler
  und behandelt die Ziele wie 404.
- **Ketten.** Alt zu Zwischenstand zu Neu verliert bei jedem Schritt und
  bricht, sobald jemand einen Zwischenschritt aufräumt. Immer direkt auf
  das Endziel.
- **Schleifen.** Klingt absurd, passiert bei jeder zweiten Neuauflage.

## Mitziehen, was an den Adressen hängt

- Sitemap neu erzeugen, alte Adressen entfernen
- Interne Verweise auf die **neuen** Adressen setzen, nicht auf die
  Weiterleitung
- Canonicals prüfen: keine Seite zeigt auf eine alte Adresse
- Strukturierte Daten, Sprachverknüpfungen und Feeds
- Robots-Angaben: keine Seite bleibt versehentlich gesperrt, keine
  gesperrte Seite steht in der Sitemap
- Verweise außerhalb der Website: Signaturen, Visitenkarten, Anzeigen,
  Profile in Verzeichnissen, QR-Codes auf gedrucktem Material

## Umschalten

1. Weiterleitungen **vor** dem Umschalten auf einem Testsystem prüfen —
   die ganze Liste, maschinell, nicht stichprobenartig.
2. Alte Seite erreichbar halten, bis die neue steht.
3. Umschalten, dann sofort die Liste erneut gegen die Live-Seite prüfen.
4. Sitemap bei den Suchmaschinen neu einreichen.
5. Messwerte aufnehmen (Skill `neo-design`, `references/messwerte.md`) —
   der Zustand direkt nach dem Umschalten ist der Vergleichspunkt.

## Danach beobachten

In den ersten Wochen regelmäßig:

- **404-Aufkommen** in den Serverprotokollen. Jede Adresse, die
  auftaucht und nicht in der Liste stand, wird nachgetragen.
- Indexierung und Sichtbarkeit in der Suchkonsole.
- Weiterleitungsketten, die durch spätere Änderungen entstanden sind.
- Antwortzeiten und Kernwerte — eine neue Seite ist nicht automatisch
  schneller.

## 404-Strategie

Eine 404-Seite ist Teil der Gestaltung, kein Serverstandard:

- Sagt, was passiert ist, in einem Satz ohne Schuldzuweisung.
- Bietet Suche und die wichtigsten Einstiege an.
- Behält Kopf und Fuß der Seite — der Besucher soll nicht das Gefühl
  haben, die Website verlassen zu haben.
- Antwortet mit dem Statuscode **404**, nicht mit 200. Eine „weiche 404"
  hält die tote Adresse im Index.
- 404-Aufkommen wird beobachtet, nicht nur gestaltet.

## Prüfliste

- [ ] Adressliste aus allen sechs Quellen erhoben und im Repo abgelegt.
- [ ] Jede alte Adresse hat genau ein Ziel und eine bewusste Entscheidung.
- [ ] Nur 301, keine Ketten, keine Sammelweiterleitung auf die Startseite.
- [ ] Sitemap, interne Verweise, Canonicals, Feeds und Sprachverknüpfungen
      gezogen.
- [ ] Weiterleitungen maschinell geprüft — vor und nach dem Umschalten.
- [ ] 404-Seite gestaltet, antwortet mit 404.
- [ ] Messwerte vor und nach dem Umschalten festgehalten.
- [ ] 404-Aufkommen und Indexierung in den ersten Wochen beobachtet.
