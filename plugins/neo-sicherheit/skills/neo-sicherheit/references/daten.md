# Hochsensible Daten

Lesekonvention siehe `SKILL.md`.

## Was hochsensibel ist

Karten- und Zahlungsdaten, Gesundheitsdaten, Ausweis- und
Meldedaten, biometrische Daten, Zugangsdaten Dritter.

## Die Grundregel

**Hochsensible Daten werden nie persistiert.** Kein Freigabeweg.

Nicht in: Tabellen, Roh-Nutzlasten, Webhook-Protokollen,
Warteschlangen, Auftragsdetails, Fehlerablagen, Protokollen,
Fehlerantworten, Diagnoseausgaben, Exporten, Support-Downloads,
Verwaltungs-Downloads, Zwischenspeichern, Suchindizes, Sicherungen.

**Klardaten existieren ausschließlich transient im Speicher, für genau
einen Aufruf.** Danach sind sie weg — nicht zwischengespeichert, nicht
nachgeschlagen, nicht wiederholt verwendet.

## Was stattdessen gespeichert wird

Nur sichere Kennzeichen, aus denen sich nichts rekonstruieren lässt:

| Erlaubt | Beispiel |
| --- | --- |
| Ein Kennzeichen, dass etwas vorliegt | `hatZahlungsmittel: true` |
| Die Art | `visa`, `virtuell` |
| Die letzten vier Stellen | `•••• 4242` |
| Eine Referenz des Zahlungsdienstleisters | `pm_1a2b3c` |
| Ein Ablaufdatum | `12/2029` |

## Isolierte Verarbeitungspfade

Wo hochsensible Daten unvermeidlich durch das System laufen:

- **Ein eigener Pfad**, getrennt von der übrigen Verarbeitung.
- **Kein öffentlicher Eingang** auf diesen Pfad.
- **Ausgehend nur über eine Positivliste** von Zielen.
- **Ein Standardarbeiter führt niemals Aufträge dieses Pfades aus.**
  Die Trennung ist am Auftrag markiert und wird beim Aufnehmen geprüft
  (Skill `neo-api`, Hintergrundarbeit).
- Der Pfad hat eigene Zugangsdaten, eigene Protokollierung und eine
  eigene Freigabe.

## Redaktionstests vor der Freigabe

**Vor der Freigabe eines solchen Pfades wird über jeden Ausgabekanal
geprüft, dass nichts durchsickert.** Ohne diese Tests gilt der Pfad als
nicht freigegeben — auch wenn er funktioniert.

Geprüfte Kanäle, vollständig:

- [ ] API-Antworten, auch Fehlerantworten
- [ ] Protokolle aller Ebenen, auch `Debug`
- [ ] Warteschlangen- und Auftragsdetails
- [ ] Fehlerablage und Wiederholungseinträge
- [ ] Webhook-Protokolle und Roh-Nutzlasten
- [ ] Exporte, Berichte, Support- und Verwaltungs-Downloads
- [ ] Diagnose- und Statusausgaben
- [ ] Beispiele in der API-Beschreibung
- [ ] Zwischenspeicher und Suchindizes

Der Test speist echte, erkennbare Testwerte ein und sucht sie in jedem
Kanal. Ein Kanal, den niemand geprüft hat, ist der Kanal, über den es
herauskommt.

## Verschlüsselung

- **Übertragung immer verschlüsselt.** Auch intern, auch zwischen
  Containern, sofern das Netz nicht nachweislich getrennt ist.
- **Ruhende Daten verschlüsseln, wo die Plattform es vorsieht** — auf
  Geräten über den Schlüsselspeicher des Systems, in der Datenbank über
  deren Mittel.
- **Der Schlüssel liegt nie neben den Daten.** Eine verschlüsselte
  Sicherung mit dem Schlüssel im selben Ordner ist unverschlüsselt.
- Schlüsselwechsel muss möglich sein, ohne die Daten zu verlieren. Wer
  das nicht vorsieht, wechselt nie.

## Datei-Import und -Export

- **Eine hochgeladene Datei ist fremder Code, bis das Gegenteil geprüft
  ist.** Art an den ersten Bytes prüfen, nicht an der Endung und nicht
  an der Angabe des Browsers.
- Größe und Anzahl begrenzt, vor dem Lesen.
- **Kein serverseitiges Dekodieren fremder Bilder**, wo es sich vermeiden
  lässt (Skill `neo-design`, Nachbearbeitung im Browser).
- Dokumentformate wie SVG werden über eine **Positivliste** gereinigt,
  nicht über eine Verbotsliste — und was entfernt wurde, wird benannt.
- Ausgeliefert wird mit eigener Inhaltsrichtlinie und ohne
  Ausführungsrechte.
- **Exporte tragen dieselben Berechtigungen wie die Ansicht.** Ein
  Export, der mehr Zeilen enthält als die Liste, ist eine Lücke.
- Ein Dateiname aus fremder Hand wird nie als Pfad verwendet.
