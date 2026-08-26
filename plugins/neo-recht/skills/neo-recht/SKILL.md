---
name: neo-recht
description: >
  Rechtliche Pflichtbausteine der NEO Digital. Diesen Skill laden bei
  Impressum, Offenlegung, Datenschutzerklärung, Cookie-Auflistung,
  Consent-Dialog und Einwilligungsverwaltung, Barrierefreiheitserklärung,
  Einbindung externer Dienste (Karten, Videos, Schriften, Analyse,
  Newsletter, Chat, Schriftarten-Dienste, eingebettete Rahmen), bei
  Aufbewahrungsfristen, Löschkonzept und Betroffenenrechten, beim
  Aufsetzen einer neuen Website oder Anwendung sowie bei Fragen zum EU
  Cyber Resilience Act, zur technischen Dokumentation und zum Meldeweg.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg; Rechtsstand geprüft 2026-08 (ECG, MedienG, UGB, DSGVO, TKG, BaFG, WZG, CRA)
---

# Rechtliche Pflichten

## Ehrlichkeitsregel zuerst

Dieser Skill ist eine **Bau- und Prüfanleitung, keine Rechtsberatung**.
Er sorgt dafür, dass nichts vergessen wird und dass technisch stimmt, was
rechtlich verlangt ist. Die inhaltliche Endabnahme der Texte macht der
Rechtsbeistand des Kunden — nie der Agent, nie die Agentur allein.

Nie behaupten „DSGVO-konform", „barrierefrei" oder „CRA-konform". Was
gebaut wurde, ist eine an den Vorgaben ausgerichtete Umsetzung; die
Konformität stellt fest, wer sie prüfen darf.

## Drei Pflichtseiten — immer, als eigene Seiten

| Seite | Grundlage | Gilt für |
| --- | --- | --- |
| **Impressum / Offenlegung** | § 5 ECG, §§ 24 und 25 MedienG, § 14 UGB | jede geschäftliche Website |
| **Datenschutzerklärung** | DSGVO Art. 13 und 14, DSG, TKG (Einwilligung für Cookies) | jede Website und Anwendung |
| **Barrierefreiheitserklärung** | BaFG (Markt), WZG (öffentliche Stellen) | jede Website und Anwendung |

Alle drei sind **eigene Seiten**, aus jeder Seite erreichbar (Fußzeile),
nicht hinter einer Einwilligung, nicht in einem Dialog versteckt, ohne
`noindex`, und in jeder ausgelieferten Sprache vorhanden.

- Inhalt des Impressums, einschließlich Rechtevorbehalt, Haftung für
  externe Links und Bildrechte: `references/impressum.md`
- Datenschutzerklärung, Cookie-Auflistung, Widerruf, externe Dienste:
  `references/datenschutz-und-consent.md`
- Barrierefreiheitserklärung und das Barrierefreiheits-Werkzeug:
  `references/barrierefreiheitserklaerung.md`

## Consent: vor der Einwilligung lädt nichts

**Die härteste Regel dieses Skills.** Ohne Einwilligung wird nichts von
einem Dritten geladen — keine Schrift, kein Kartenausschnitt, kein
Video, kein Zählpixel, kein Chat, kein eingebetteter Rahmen.

- **Eingebettete Rahmen (`iframe`) sind Drittzugriffe.** Ein
  YouTube-Video lädt beim Einbetten von Google, bevor jemand auf
  „Abspielen" drückt. Es bleibt bis zur Einwilligung eine Vorschau mit
  Standbild aus dem eigenen Haus und einem Knopf, der erklärt, was beim
  Klick passiert.
- Der Dialog erscheint vor dem ersten Drittzugriff, nicht daneben.
- **„Ablehnen" ist gleichwertig gestaltet** wie „Akzeptieren": gleiche
  Ebene, gleiche Größe, gleiche Erreichbarkeit. Kein grauer Textlink
  neben einem grünen Knopf.
- Kategorien nur für **tatsächlich eingesetzte** Dienste. Eine leere
  Kategorie „Marketing" ist eine unwirksame Vorratseinwilligung.
- Kein vorausgewähltes Kästchen, kein Weiterscrollen als Zustimmung,
  keine Sperre der Seite, bis zugestimmt wurde.
- **Widerruf jederzeit**, über einen festen Punkt in der Fußzeile, so
  einfach wie die Erteilung.
- Drittlandübermittlung (etwa USA) wird im Dialog benannt.
- Der Dialog selbst ist barrierefrei: Tastatur, Fokusfalle, Kontrast.

## Schriften

**Schriften werden immer selbst ausgeliefert.** Nie von einem fremden
Dienst laden — auch nicht „nur die eine". Der Abruf überträgt die
IP-Adresse des Besuchers, bevor irgendjemand zugestimmt hat.

Ist Selbstauslieferung im Einzelfall nicht möglich, ist **bunny.net** die
abgestimmte Ausweichlösung. Alles andere braucht eine Freigabe.

## Externe Dienste

Für **jeden** eingesetzten Fremddienst muss vorliegen: Zweck,
Anbieter mit Sitz, übertragene Daten, Rechtsgrundlage, Speicherdauer,
Drittlandübermittlung, Link auf dessen Datenschutzerklärung — und, wo
nötig, ein Auftragsverarbeitungsvertrag.

Fehlt eines davon, wird der Dienst nicht eingebaut. Der Vorschlag zum
Einsatz eines Dienstes enthält diese Angaben; die Entscheidung fällt der
Projektinhaber.

## Löschen, nicht nur erklären

Die Datenschutzerklärung nennt Speicherdauern — ein **Löschkonzept**
sorgt dafür, dass sie stimmen. Je Datenart eine Frist mit Auslöser,
danach automatisch löschen oder anonymisieren. Was von Hand gelöscht
werden müsste, wird nie gelöscht. Betroffenenrechte müssen technisch
bedienbar sein, nicht nur beschrieben.

Verzeichnis, Konflikte mit Aufbewahrungspflichten, vergessene Orte und
die Prüfliste: `references/loeschkonzept.md`.

## KI im Produkt

Setzt das Produkt KI ein, kommen die Pflichten der EU-KI-Verordnung dazu
— die Transparenzpflichten aus Artikel 50 gelten seit **02.08.2026**.
Einstufung, Offenlegung, Kennzeichnung und die Weitergabe von Daten an
ein Modell: Skill `neo-ki`.

## Anwendungen und Portale: EU Cyber Resilience Act

Zusätzlich zu den drei Pflichtseiten gilt für Web-, Android-, iOS- und
Windows-Anwendungen der **CRA**. Er verlangt nicht nur sichere Technik,
sondern ein **Dokumentenpaket**: Produkteinstufung, Risikobewertung,
technische Dokumentation, Benutzerinformationen, Meldeverfahren,
Konformitätserklärung.

- Welche Dokumente das sind und was hineingehört:
  `references/cra-dokumentation.md`
- Wie gebaut wird, damit die Dokumente etwas beschreiben können:
  Skill `neo-sicherheit`.

## Prüfung vor der Abnahme

- [ ] Impressum, Datenschutzerklärung und Barrierefreiheitserklärung
      erreichbar, vollständig, in jeder Sprache.
- [ ] Kein Hinweis auf die EU-Streitbeilegungsplattform mehr im
      Impressum (seit 20.07.2025 abgeschaltet).
- [ ] Netzwerkmitschnitt beim ersten Aufruf: **kein** Aufruf an einen
      fremden Host vor der Einwilligung — Schriften, Karten, Videos,
      Analyse eingeschlossen.
- [ ] „Ablehnen" gleichwertig, keine Vorauswahl, Widerruf in der
      Fußzeile.
- [ ] Cookie-Auflistung in der Datenschutzerklärung stimmt mit dem
      überein, was tatsächlich gesetzt wird.
- [ ] Für jeden Fremddienst liegen die Angaben oben vor.
- [ ] Schriften kommen von der eigenen Domain.
- [ ] Bei Anwendungen: CRA-Dokumentenpaket angelegt und aktuell.
- [ ] Löschkonzept vorhanden, Fristen decken sich mit der
      Datenschutzerklärung, der Löschlauf läuft automatisch.
- [ ] Bei KI-Funktionen: Offenlegung nach Artikel 50 vorhanden
      (Skill `neo-ki`).

Zugehörige Skills: `neo-design` (Barrierefreiheit im Bau, Messwerte),
`neo-sicherheit` (CRA-Technik, Secrets, Release-Evidenz), `neo-contao`
(Umsetzung in Contao), `neo-doku` (Ablage und Pflege der Dokumente).
