# Dokumentation einer Erweiterung

## Reihenfolge der Sprachen

**Erst Englisch, dann Deutsch.** Das README enthält beide Teile
vollständig, der englische steht oben. Der deutsche Teil beginnt mit
einer Überschrift erster Ebene, die „(Deutsch)" trägt, z. B.
`# Website-Check für Contao 5 (Deutsch)`.

Ausführliche Doku über mehrere Seiten liegt in `docs/en/` und `docs/de/`
mit denselben Dateinamen (Skill `neo-doku`). Das README verweist darauf.

## Was das README enthält — in beiden Sprachen

| Abschnitt | Inhalt |
| --- | --- |
| Kurzbeschreibung | Was die Erweiterung tut, in drei Sätzen, ohne Herstellerbezug |
| Funktionen | Was der Besucher sieht, was die Redaktion kann |
| Voraussetzungen | Contao-, PHP-Fassung, PHP-Erweiterungen, fremde Dienste und Schlüssel |
| **Installation** | Contao Manager **und** Composer, Schritt für Schritt, danach Datenbank aktualisieren |
| Einrichtung | Welches Backend-Modul, welche Felder, in welcher Reihenfolge; woher man einen Schlüssel bekommt |
| Bedienung | Wie die Redaktion das Element/Modul einsetzt; Verweis auf `docs/` mit Screenshots |
| Anpassen | CSS-Variablen, Template-Überschreibung, Texte im Backend |
| Rechte | Welche Module und Tabellen eine Redakteursgruppe braucht |
| Datenschutz | Was gespeichert wird, wie lange, an welche Dienste es geht |
| Fehlersuche | Häufige Fehler, „Verbindung prüfen" |
| Sprachen | Die elf Sprachen, wie man eine weitere ergänzt |
| Lizenz | MIT |

## Gerüst

```markdown
# <Name> for Contao 5

<What it does, three sentences.>

## Features
## Requirements
## Installation
### Contao Manager
### Composer
## Setup
## Usage
## Customising
## Back-end permissions
## Privacy
## Troubleshooting
## Languages
## License

# <Name> für Contao 5 (Deutsch)

## Funktionen
## Voraussetzungen
## Installation
## Einrichtung
## Bedienung
## Anpassen
## Backend-Rechte
## Datenschutz
## Fehlersuche
## Sprachen
## Lizenz
```

## Regeln

- Beispiele in Doku und Konfigurationsausschnitten sind neutral
  (`neutralitaet.md`): `office@example.com`, `Max Mustermann`,
  `https://example.com`.
- Keine Zeile „Built by …" / „Entwickelt von …".
- `CHANGELOG.md` je Fassung, englisch, aus Sicht dessen, der
  aktualisiert: was neu ist, was er tun muss.
- Screenshots aus dem Backend mit Markierungen, ohne echte Namen oder
  Kundendaten im Bild (Skill `neo-doku`, `references/screenshots.md`).
