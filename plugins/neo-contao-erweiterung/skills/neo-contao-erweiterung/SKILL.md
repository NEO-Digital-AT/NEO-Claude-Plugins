---
name: neo-contao-erweiterung
description: >
  Verbindliche Regeln für den Bau einer eigenen Contao-Erweiterung (Bundle,
  Plugin, Modul) zum Weitergeben oder Verkaufen. Diesen Skill laden, sobald
  eine Contao-Erweiterung angelegt, erweitert, umbenannt, dokumentiert,
  übersetzt oder veröffentlicht wird — auch wenn sie zuerst nur in einem
  Kundenprojekt gespiegelt liegt. Ebenso bei Beispielwerten, Hilfstexten,
  Platzhaltern, README, CHANGELOG, Sprachdateien, Standardgestaltung von
  Web-Komponente, PDF und E-Mail, API-Schlüsseln und Einstellungen einer
  Erweiterung. Ergänzt den Skill neo-contao (Websites, Rangfolge,
  Migrationen, Theme); bei Widerspruch gilt für Erweiterungen dieser hier.
metadata:
  herkunft: Vorgaben des Inhabers vom 11. und 12.10.2026, belegt an den vier ausgelieferten Erweiterungen (NEO-Contao-Websitecheck, NEO-Contao-Brevo, NEO-Contao-SuperAgent, NEO-Contao-LLMS)
---

# Contao-Erweiterungen bauen

Eine Erweiterung wird **verkauft und weitergegeben**. Sie läuft bei
fremden Agenturen und deren Kunden, in deren Design, in deren Sprache.
Daraus folgen die Regeln unten — sie gelten ohne Ausnahme und müssen
nicht bei jeder neuen Erweiterung erneut gesagt werden.

## 1. Vollständig neutral

**In der Erweiterung steht nichts, das auf den Hersteller oder auf ein
Kundenprojekt zeigt** — außer dem Namen der Erweiterung selbst.

- **Keine Personennamen.** Nicht der des Inhabers, nicht der eines
  Mitarbeiters, nicht der eines Kunden — weder in Hilfstexten noch in
  Beispielen, Kommentaren, Doku, Testdaten oder Commit-fähigen Fixtures.
  Beispielperson: „Max Mustermann" bzw. die landesübliche Entsprechung
  (`references/neutralitaet.md`).
- **Keine Firmennamen, Domains, Adressen, Telefonnummern, Städte** des
  Herstellers oder eines Kunden. Beispiele nutzen die reservierten Domains
  `example.com`, `example.org`, `example.net` und erfundene Orte
  („Musterstadt").
- **Kein Hersteller-Branding in Beschreibungen.** Der Erweiterungsname
  darf die Marke tragen; Texte, Hilfen, Beispielwerte und Doku nicht.
  Kein „Entwickelt von …", kein Verweis auf die eigene Website.
- **Kein Hersteller-Design.** Keine Hausfarben, Hausschriften, Hausklassen,
  kein Logo im Paket. Web-Komponente, PDF und E-Mail kommen im
  **neutralen Grunddesign**; gestaltet wird in der Website des Kunden über
  CSS-Variablen, Template-Überschreibungen und Backend-Einstellungen.
- **Keine Projektreste.** Keine Kommentare wie „für Kunde X ergänzt",
  „Befund von Y", keine Datumsnotizen aus einem Projekt.

**Belegt wird das mit dem Prüfwerkzeug**, nicht mit Durchsehen:

```
python3 plugins/neo-contao-erweiterung/scripts/bundle-check.py <bundle> \
  --forbid "<Vorname>" --forbid "<Nachname>" --forbid "<Firma>" \
  --forbid "<firmen-domain.tld>" --forbid "<Produktname eines Kunden>"
```

Ergebnis null Befunde, sonst ist die Erweiterung nicht fertig. Die
Begriffe für `--forbid` sind die Namen des Inhabers, seiner Firma, ihrer
Domain und aller Kunden, deren Projekt die Erweiterung berührt hat.

## 2. Aufbau nach den bestehenden Erweiterungen

Nicht neu erfinden — die vier ausgelieferten Erweiterungen geben den
Aufbau vor. Namen, Ordner, `composer.json`, Einstellungen im Backend,
Übernahme alter Werte, lokaler Prüfstand: `references/aufbau.md`.

Kurzform: eigenes Repository `NEO-Contao-<Name>`, Paket
`neo-digital/contao-<name>-bundle`, `type: contao-bundle`, Lizenz MIT,
Namensraum `Neo\<Name>Bundle`, Tabellen `tl_neo_*`, Spiegel im Projekt
unter `bundles/<ordner>/` per `rsync`, Änderungen nur im eigenen
Repository.

## 3. Einstellungen gehören ins Backend, nicht in die Umgebung

Ein Kunde ohne Serverzugang muss die Erweiterung vollständig einrichten
können.

- **API-Schlüssel, Modelle, Absender, Empfänger, Grenzen** sind Felder im
  Backend. Schlüssel werden verschlüsselt gespeichert (mit dem
  App-Secret), nie wieder angezeigt, **exakt** so gespeichert wie
  eingegeben (Contao kodiert `=`, `&`, `<` beim Speichern — `decodeEntities`
  setzen und beim Lesen dekodieren).
- `config.yaml` und Umgebungsvariablen sind nur **Rückfall für leere
  Felder**. Eine Migration übernimmt vorhandene Werte einmalig ins Backend.
- **Werte, die ein Fremdsystem kennt** (Modelle, Verteiler, Vorlagen),
  kommen als Auswahl live von dessen API — mit Textfeld als Rückfall ohne
  Schlüssel und dem gespeicherten Wert immer in der Liste.
- **Ein Knopf „Verbindung prüfen"** zeigt, ob jeder Dienst vom Server aus
  erreichbar ist und den Schlüssel annimmt — mit der genauen Antwort,
  Schlüssel maskiert.
- **Kostet die Erweiterung Geld pro Aufruf** (KI, bezahlte API), gibt es
  eine Obergrenze für alle Besucher zusammen, im Backend einstellbar, und
  einen unsichtbaren Spam-Schutz (ALTCHA, Honeypot). Fehlt ein nötiger
  Schlüssel, lehnt sie offen ab, statt ein leeres Ergebnis zu liefern.

Einzelheiten: `references/aufbau.md`, Abschnitt Einstellungen.

## 4. Elf Sprachen im Backend, fest

Jede Erweiterung liefert die Backend-Oberfläche und alle Standardtexte in
**elf Sprachen**: Englisch, Deutsch, Französisch, Niederländisch,
Italienisch, Polnisch, Tschechisch, Ungarisch, Slowenisch, Kroatisch,
Spanisch (`en de fr nl it pl cs hu sl hr es`).

- `contao/languages/<sprache>/` für jede der elf, mit denselben Dateien
  und Schlüsseln wie Englisch.
- Texte für Besucher (Frontend, PDF, E-Mail) in
  `translations/<domain>.<sprache>.yaml`, ebenfalls elf.
- Neue Schlüssel entstehen **in allen elf Dateien im selben Schritt**.
  Eine Sprache später nachziehen gibt es nicht.
- Beispielwerte werden mitübersetzt und bleiben neutral (Abschnitt 1).

Vollständigkeit belegt `bundle-check.py`; Regeln und Wortwahl:
`references/sprachen.md`.

## 5. Dokumentation: erst Englisch, dann Deutsch

- `README.md` enthält **zuerst den englischen Teil, dann den deutschen**
  (`# … (Deutsch)`), beide vollständig.
- Jeder Teil erklärt mindestens: was die Erweiterung tut, Voraussetzungen,
  **Installation** (Contao Manager und Composer), Einrichtung im Backend,
  Bedienung mit Verweis auf die ausführliche Doku, Anpassen des Designs,
  Rechte für Redakteure, Datenschutz, Sprachen, Lizenz.
- `CHANGELOG.md` je Fassung, aus Sicht dessen, der aktualisiert.
- Ausführliche Doku über mehrere Seiten nach Skill `neo-doku`.

Aufbau des README und Vorlage: `references/doku.md`.

## 6. Aktualisieren ohne Schaden

Unverändert aus Skill `neo-contao`, `references/erweiterungsbau.md`:
neue Felder optional mit Standardwert, nichts umbenannt oder entfernt,
keine nachträgliche Pflicht, Migrationen defensiv und wiederholbar,
semantische Versionierung.

## Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und die
Zahlen nennen — vor allem das Ergebnis von `bundle-check.py`.

Zugehörige Skills: `neo-contao` (Websites, Rangfolge, Migrationen),
`neo-doku` (Doku), `neo-design` (Barrierefreiheit der Web-Komponente),
`neo-sicherheit` (Schlüssel, Härtung), `neo-recht` (Datenschutz-Hinweise
in der Doku).
