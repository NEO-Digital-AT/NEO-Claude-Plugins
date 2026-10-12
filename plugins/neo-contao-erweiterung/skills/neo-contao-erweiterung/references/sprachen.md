# Sprachen

## Die elf Sprachen

| Code | Sprache |
| --- | --- |
| en | Englisch (Bezugssprache) |
| de | Deutsch |
| fr | Französisch |
| nl | Niederländisch |
| it | Italienisch |
| pl | Polnisch |
| cs | Tschechisch |
| hu | Ungarisch |
| sl | Slowenisch |
| hr | Kroatisch |
| es | Spanisch |

Jede Erweiterung liefert **alle elf** — Backend und alle Standardtexte.
Eine Sprache, die fehlt, macht die Erweiterung unfertig.

## Wo die Texte liegen

| Was | Ort | Format |
| --- | --- | --- |
| Backend: Feldnamen, Hilfen, Legenden, Knöpfe, Meldungen | `contao/languages/<code>/*.php` | Contao-Sprachdatei |
| Texte für Besucher, PDF, E-Mail, Fehlermeldungen im Frontend | `translations/<domain>.<code>.yaml` | Symfony-Übersetzung |

- Die **Dateien und Schlüssel jeder Sprache sind dieselben** wie im
  Englischen. Englisch ist die Bezugssprache für die Prüfung.
- Ein neuer Schlüssel entsteht in **allen elf Dateien im selben Commit**.
- Texte, die der Kunde ändern darf (Betreff, Knopftext, Rechtshinweis),
  sind zusätzlich als Feld im Backend überschreibbar; die Übersetzung ist
  der Standardwert.

## Wortwahl

- Für Menschen ohne IT-Vorwissen schreiben, in jeder Sprache.
- Anrede in der höflichen Form der jeweiligen Sprache (Sie, vous, Lei …).
- Typografie der Sprache: deutsche Anführungszeichen „…", französische
  « … », Leerzeichen vor Doppelpunkt im Französischen.
- Beispielwerte übersetzen und neutral halten (`neutralitaet.md`).

## Prüfen

`bundle-check.py` vergleicht jede Sprache mit Englisch — fehlende Ordner,
Dateien und Schlüssel, für Backend und Frontend. Ergebnis null Befunde.
