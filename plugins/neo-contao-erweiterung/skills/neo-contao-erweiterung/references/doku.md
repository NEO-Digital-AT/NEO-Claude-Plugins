# Dokumentation einer Erweiterung

Jede Erweiterung liefert ihre Dokumentation **im Paket** mit: wie man sie
installiert, einrichtet und die Rechte setzt, wie man sie bedient und was
man tut, wenn etwas nicht geht. Sie liegt unter `docs/` und geht mit jeder
Fassung mit. Wer die Erweiterung kauft, braucht keine Rückfrage beim
Hersteller (Vorgabe des Inhabers vom 11.11.2026).

Das README ist kurz: was die Erweiterung ist, wie man sie installiert, und
der Verweis auf die Dokumentation.

## Sprachen

**Erst Englisch, dann Deutsch.** Englisch ist Leitsprache, Deutsch ist
ebenfalls Pflicht (Skill `neo-doku`, Abschnitt Sprachen).

- Das README enthält beide Teile, der englische steht oben. Der deutsche
  Teil beginnt mit einer Überschrift erster Ebene, die „(Deutsch)" trägt,
  z. B. `# Website-Check für Contao 5 (Deutsch)`.
- Die Dokumentation liegt in `docs/en/` und `docs/de/` mit **denselben
  Dateinamen** (Skill `neo-doku`, `references/struktur.md`).

## README: kurz

| Abschnitt | Inhalt |
| --- | --- |
| Kurzbeschreibung | Was die Erweiterung tut, in drei Sätzen, ohne Herstellerbezug |
| Funktionen | Stichpunkte, höchstens acht; Stufen (kostenlos, mit Lizenz), falls es sie gibt |
| Voraussetzungen | Contao-, PHP-Fassung, PHP-Erweiterungen, fremde Dienste und Schlüssel |
| **Installation** | Contao Manager **und** Composer, Schritt für Schritt, danach Datenbank aktualisieren |
| **Dokumentation** | Link auf `docs/en/README.md` bzw. `docs/de/README.md`, dazu die wichtigsten Seiten (Einrichtung, Rechte, Bedienung, Fehlersuche) |
| Lizenz | eigene Lizenz (`LICENSE`) |

Einrichtung im Detail, Rechte, Bedienung, Anpassen, Datenschutz und
Fehlersuche stehen **nicht** im README, sondern in `docs/`. Zwei Stellen
für denselben Inhalt laufen auseinander.

```markdown
# <Name> for Contao 5

<What it does, three sentences.>

## Features
## Requirements
## Installation
### Contao Manager
### Composer
## Documentation
## License

# <Name> für Contao 5 (Deutsch)

## Funktionen
## Voraussetzungen
## Installation
### Contao Manager
### Composer
## Dokumentation
## Lizenz
```

## Dokumentation unter `docs/`

```
docs/
  README.md              Einstieg: Sprachen, Leitsprache, wo man anfängt
  en/
    README.md            Inhaltsverzeichnis, je Seite ein Satz
    installation.md
    setup.md
    permissions.md
    usage.md             oder usage/README.md mit Unterseiten
    customising.md       wenn die Erweiterung etwas im Frontend ausgibt
    privacy.md
    troubleshooting.md
    bilder/              Screenshots der englischen Oberfläche
  de/
    (dieselben Dateinamen)
    bilder/              Screenshots der deutschen Oberfläche
```

### Pflichtseiten

| Datei | Wer liest es | Inhalt |
| --- | --- | --- |
| `installation.md` | Agentur, Administrator | Voraussetzungen, Contao Manager, Composer, Datenbank aktualisieren, öffentliche Dateien, Aktualisieren auf eine neue Fassung, Entfernen |
| `setup.md` | Administrator | Einrichtung im Backend in der Reihenfolge, in der man sie braucht; je Schlüssel: woher man ihn bekommt, wo man ihn einträgt, wie man die Verbindung prüft |
| `permissions.md` | Administrator | Die Schalter der Erweiterung und **Contaos Rechte je Funktion** als Tabelle, mit Contaos Bezeichnungen (Backend-Module, Erlaubte Felder, Tabellenrechte …); fertige Beispielgruppen („Redaktion nur Texte", „Webdesign"); mehrere Websites in einer Installation |
| `usage.md` (oder `usage/`) | Redaktion | Die Bedienungsanleitung: je Ablauf Ziel, Voraussetzungen, nummerierte Schritte, Ergebnis, häufige Fehler; Bedienelemente wörtlich benannt; Screenshots mit Markierungen |
| `privacy.md` | Administrator, Datenschutzbeauftragte | Was gespeichert wird, wie lange, an welche Dienste es geht, was in die Datenschutzerklärung der Website gehört |
| `troubleshooting.md` | alle | Häufige Fehler als **Anzeichen → Ursache → Lösung**, vor allem fehlende Rechte; wo das Contao-Systemprotokoll den Grund nennt |

`customising.md` ist Pflicht, sobald die Erweiterung etwas im Frontend
ausgibt (CSS-Variablen, Template-Überschreibung, Texte im Backend).

### Regeln

- **Jede Funktion, die die Oberfläche anbietet, steht in der
  Bedienungsanleitung.** Eine neue Funktion ohne Doku ist nicht fertig.
- **Jedes Recht, das eine Funktion braucht, steht in `permissions.md`**,
  mit Contaos eigener Bezeichnung, so wie es in der Benutzergruppe steht.
  Wer die Gruppe nach der Tabelle einrichtet, dem funktioniert es.
- **Jeder Fehler, der in Tests oder bei Kunden aufgetreten ist, steht in
  `troubleshooting.md`**, im selben Schritt, in dem er behoben oder erklärt
  wird.
- Zielgruppen nach Skill `neo-doku`: In die Bedienungsanleitung gehören
  keine Endpunkte, Tabellen- oder Klassennamen. Die Rechte-Seite nennt
  Tabellennamen nur, wo Contao sie in der Benutzergruppe selbst zeigt
  (Erlaubte Felder, Tabellenrechte).
- Screenshots je Sprache in `bilder/`, aus der echten Erweiterung in der
  jeweiligen Oberflächensprache, mit Markierungen (Skill `neo-doku`,
  `references/screenshots.md`). Keine echten Namen oder Kundendaten im
  Bild.
- **Die Bilder entstehen mit einem Aufnahme-Skript im Repository**
  (`tools/docs-images/`, mit README: was die Testinstallation braucht, wie es
  aufgerufen wird). Der Ordner ist vom Paket ausgenommen (`.gitattributes`:
  `/tools export-ignore`). Passwörter kommen aus Umgebungsvariablen, nie aus
  der Datei. Nach einer Änderung an der Oberfläche werden die betroffenen
  Bilder damit neu aufgenommen, in jeder Sprache.
- Beispiele neutral (`neutralitaet.md`): `office@example.com`, `Max
  Mustermann`, `https://example.com`.
- Keine Zeile „Built by …" / „Entwickelt von …".
- `CHANGELOG.md` je Fassung, englisch, aus Sicht dessen, der
  aktualisiert: was neu ist, was er tun muss. Ändert eine Fassung die
  Bedienung oder die nötigen Rechte, ändert sie im selben Schritt die
  Doku.

## Abnahme

`bundle-check.py` prüft in der Gruppe `docs`: beide Sprachordner, die
Pflichtseiten, gleiche Dateinamen in beiden Sprachen, ein
Inhaltsverzeichnis je Ordner, das jede Seite verlinkt, und dass jeder
lokale Link und jedes Bild existiert. In der Gruppe `readme`: Installation
und der Link auf die Doku in beiden Teilen.

Ob die Doku **richtig** ist, prüft das Werkzeug nicht. Das belegt ein
Durchgang nach der Doku: eine leere Installation nach `installation.md`
und `setup.md` einrichten, eine Gruppe nach `permissions.md` anlegen und
mit diesem Benutzer jeden Ablauf aus `usage.md` durchspielen.
