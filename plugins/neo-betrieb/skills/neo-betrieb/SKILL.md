---
name: neo-betrieb
description: >
  NEO-Betriebsregeln. Diesen Skill laden bei Sicherung und
  Wiederherstellung, Datenverlust, Wiederanlauf, Notfall und
  Bereitschaft, Störungsmeldung und Nachbereitung, Wartungsfenstern,
  E-Mail-Zustellbarkeit (SPF, DKIM, DMARC, Bounces, Spam), sowie beim
  Umzug oder der Neuauflage einer Website mit alten Adressen,
  Weiterleitungen, Sitemap und 404-Strategie. Ebenso beim Aufsetzen
  eines Betriebshandbuchs für ein Projekt.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# NEO-Betriebsregeln

## Sicherung: erst echt, wenn sie zurückgespielt wurde

**Ein Backup, das nie wiederhergestellt wurde, ist kein Backup, sondern
eine Vermutung.**

- Je Projekt stehen zwei Zahlen fest, bevor es live geht:
  **wie viel Datenverlust hinnehmbar ist** und **wie schnell wieder
  gearbeitet werden kann**. Ohne diese Zahlen ist jeder Sicherungsplan
  geraten.
- **Mindestens einmal je Quartal eine echte Wiederherstellung**, auf ein
  getrenntes System, mit Protokoll: wann, welcher Stand, wie lange, was
  fehlte.
- Sicherungen liegen **nicht auf demselben System** wie die Daten und
  nicht unter denselben Zugangsdaten. Wer die Produktion übernimmt, darf
  die Sicherung nicht mit übernehmen.
- Verschlüsselt, mit dem Schlüssel getrennt aufbewahrt — und der
  Schlüssel selbst gesichert. Ein unlesbares Backup ist keines.
- Auch Dateien, hochgeladene Medien und Konfiguration werden gesichert,
  nicht nur die Datenbank.

Einzelheiten, Aufbewahrung und der Ablauf einer Wiederherstellung:
`references/sicherung.md`.

## Notfall

- Je Projekt ein **Betriebshandbuch**: was der Dienst tut, wovon er
  abhängt, wie er neu startet, wo die Protokolle liegen, wer zuständig
  ist, wie eskaliert wird.
- **Wer wen wann anruft**, steht vorher fest — nicht im Ernstfall.
  Dasselbe gilt für die Vertretung.
- Störungen werden **nachbereitet**: was ist passiert, warum, was hat es
  gekostet, was verhindert die Wiederholung. Ohne Schuldzuweisung, mit
  einer Maßnahme, die jemand übernimmt.
- Wartungsfenster werden angekündigt, nicht angekündigte Ausfälle
  entschuldigt.
- Meldepflichten nach CRA laufen parallel und haben eigene Fristen
  (Skill `neo-recht`).

Aufbau des Handbuchs, Eskalationsstufen und Nachbereitung:
`references/notfall.md`.

## E-Mail: ankommen, nicht nur absenden

Eine Anwendung, deren Kennwort-Zurücksetzen im Spam landet, ist kaputt —
auch wenn der Versand erfolgreich meldet.

- **SPF, DKIM und DMARC** sind eingerichtet, bevor die erste Mail
  hinausgeht. DMARC beginnt beobachtend und wird dann verschärft.
- **Transaktionspost und Werbepost sind getrennt**: getrennte Absender
  bzw. Subdomains, damit eine abgemeldete Werbemail die Rechnung nicht
  mitreißt.
- Rückläufer und Beschwerden werden **behandelt**, nicht ignoriert. Eine
  Adresse, die dauerhaft ablehnt, wird nicht weiter angeschrieben.
- Jede Mail hat einen Textteil, nicht nur HTML. Kein Bild als einziger
  Inhalt.
- Zustellbarkeit wird **gemessen**, bevor es live geht, und danach
  stichprobenartig.

Einrichtung, Prüfung und Fallstricke: `references/email.md`.

## Umzug und Neuauflage

Der teuerste Fehler bei einer Website-Neuauflage ist der, den niemand
sieht: **die alten Adressen verschwinden.** Rankings, Verweise und
Lesezeichen laufen ins Leere, und es dauert Monate, bis das zurückkommt.

- **Vor dem Umbau** werden die alten Adressen erhoben — aus Sitemap,
  Serverprotokollen, Suchkonsole und Analysewerkzeug. Nicht geschätzt.
- Jede alte Adresse bekommt ein Ziel: **301**, nicht 302, nicht auf die
  Startseite gesammelt.
- Sitemap, interne Verweise, Canonicals und strukturierte Daten werden
  mitgezogen.
- Nach dem Umschalten wird **gemessen**: 404-Aufkommen,
  Weiterleitungsketten, Indexierung, Sichtbarkeit.

Ablauf, Prüfliste und was nach dem Umschalten beobachtet wird:
`references/relaunch.md`.

Zugehörige Skills: `neo-deployment` (Zweige, Ausrollung),
`neo-sicherheit` (Härtung, Secrets, Release-Evidenz), `neo-recht`
(Meldepflichten, Löschfristen), `neo-api` (Überwachung, Statusendpunkt),
`neo-design` (Messwerte).
