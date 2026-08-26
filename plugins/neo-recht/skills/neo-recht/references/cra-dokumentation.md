# CRA: Dokumentenpaket und Meldeweg

Gilt für Anwendungen und Portale — Web, Android, iOS, Windows — also für
alles mit digitalen Elementen, das in den Verkehr gebracht wird. Wie
gebaut wird, regelt der Skill `neo-sicherheit`. Hier steht, **welche
Dokumente existieren müssen**.

## Fristen

| Datum | Was gilt |
| --- | --- |
| 10.12.2024 | Verordnung in Kraft getreten |
| **11.09.2026** | **Meldepflichten nach Artikel 14 gelten** |
| 11.12.2027 | Volle Anwendung, einschließlich der vollständigen technischen Dokumentation und SBOM-Pflichten |

## Der Meldeweg — ab 11.09.2026

Meldepflichtig sind **aktiv ausgenutzte Schwachstellen** und
**schwerwiegende Sicherheitsvorfälle**.

| Stufe | Frist | Inhalt |
| --- | --- | --- |
| Frühwarnung | **24 Stunden** ab Kenntnis | Dass etwas vorliegt, erste Einordnung, betroffene Mitgliedstaaten |
| Ausführliche Meldung | **72 Stunden** ab Kenntnis | Art, Auswirkung, betroffene Versionen, ergriffene und geplante Maßnahmen |
| Abschlussbericht | **14 Tage** nach Verfügbarkeit einer Korrektur (bei aktiv ausgenutzter Schwachstelle) bzw. **1 Monat** nach der ausführlichen Meldung (bei schwerwiegendem Vorfall) | Beschreibung, Ursache, Behebung, Vorbeugung |

- Gemeldet wird über die **einheitliche Meldeplattform der ENISA**; die
  Meldung geht zugleich an die ENISA und an das koordinierende CSIRT des
  Mitgliedstaats der Hauptniederlassung. Welche Stelle das für
  Österreich konkret ist, wird vor dem ersten Ernstfall geklärt und im
  Meldeverfahren festgehalten — nicht im Ernstfall gesucht.
- **Die Fristen laufen ab Kenntnis. Wochenenden und Feiertage zählen.**
  Deshalb braucht der Meldeweg eine Rufbereitschaft und einen
  Stellvertreter, keine Bürozeitenregelung.
- Zusätzlich: Nutzer über die Schwachstelle informieren und, wo
  angebracht, über Abhilfemaßnahmen.

## Das Dokumentenpaket

Ablage: `docs/cra/` — sprachneutral bzw. in der Sprache, in der geliefert
wird. Struktur wie in `NEO-Digital-AT/uptime`:

| Dokument | Inhalt |
| --- | --- |
| `risikobewertung.md` | Produkt, Einsatzumgebung, Bedrohungen, Bewertung, abgeleitete Maßnahmen. Die Grundlage für alles Weitere |
| `anhang-i-abgleich.md` | Zeile für Zeile: welche Anforderung aus Anhang I wie erfüllt ist, mit Fundstelle im Code oder in der Konfiguration |
| `technische-dokumentation.md` | Beschreibung des Produkts, Architektur, Komponenten, SBOM, Entwicklungs- und Auslieferungsprozess, Testnachweise, Unterstützungszeitraum |
| `benutzerinformationen.md` | Was der Betreiber wissen muss: sichere Inbetriebnahme, Konfiguration, Aktualisierung, Ende des Unterstützungszeitraums, Kontakt für Schwachstellenmeldungen |
| `meldeverfahren.md` | Der Weg oben, mit Namen, Vertretung, Erreichbarkeit, Fristen, Vorlagen für die drei Stufen |
| `konformitaetserklaerung.md` | Die Erklärung selbst, mit den herangezogenen Normen |
| `vorfaelle/` | Ein Eintrag je Meldung bzw. je glaubwürdiger Schwachstellenmeldung |

- Jedes Dokument trägt einen Stand und wird bei jeder Änderung am Produkt
  nachgezogen (Skill `neo-doku`).
- Der Unterstützungszeitraum wird ausdrücklich benannt, nicht offen
  gelassen.
- **Ehrlichkeitsregel:** „CRA-konform" nie behaupten. Ohne
  Produkteinstufung, Risikobewertung, technisches Dokumentationspaket,
  SBOM-Automatisierung und Release-Evidenz ist es eine an der Verordnung
  ausgerichtete Umsetzung.

## Was der Agent hier tut und was nicht

- **Tut er:** die Dokumente anlegen und pflegen, den Abgleich mit
  Anhang I führen, Lücken benennen, SBOM und Evidenz aus der Pipeline
  ziehen, den Meldeweg als Ablauf beschreiben und die Vorlagen
  vorbereiten.
- **Tut er nicht:** die Produkteinstufung entscheiden, eine
  Konformitätserklärung unterzeichnen, eine Meldung an eine Behörde
  absetzen oder behaupten, das Produkt sei konform. Das entscheidet und
  verantwortet der Projektinhaber.
