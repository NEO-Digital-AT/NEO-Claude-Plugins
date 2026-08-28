# Sprache im Code und im System

Lesekonvention siehe `SKILL.md`.

> **Alles, was zum System gehört, ist englisch. Deutsch ist nur, was ein
> deutschsprachiger Mensch liest.**

Der Grund ist nicht Mode. Er ist praktisch: Ein System, das intern
deutsch spricht, lässt sich nicht mehrsprachig machen, ohne dass jemand
Bezeichner umbenennt — und es lässt sich von einem Entwickler, der kein
Deutsch spricht, nicht warten.

## Die Trennlinie

| Englisch — ausnahmslos | Deutsch — wo das Publikum deutsch ist |
| --- | --- |
| Bezeichner: Klassen, Methoden, Variablen, Felder, Tabellen, Spalten | Oberflächentexte eines deutschsprachigen Produkts |
| Kommentare im Code | Dokumentation eines Kundenprojekts (Skill `neo-doku`) |
| Protokolleinträge und Protokollmeldungen | Bedienungsanleitungen für die Redaktion |
| **Technische Fehlermeldungen**, Ausnahmetexte, Fehlercodes | Rechtstexte, Kundenkorrespondenz |
| Schnittstellen: Endpunktnamen, Felder, Aufzählungswerte | Commit-Nachrichten und Pull-Request-Texte |
| Konfigurationsschlüssel, Umgebungsvariablen, Merkmalsschalter | — |
| Übersetzungsschlüssel (`order.created`, nicht `auftrag.angelegt`) | — |
| Backend-Oberflächen, Verwaltungsansichten, Werkzeuge | — |
| Doku einer Erweiterung oder Bibliothek (Skill `neo-contao`) | — |

**Commit-Nachrichten bleiben deutsch** — sie richten sich an das eigene
Team. Wo Deutsch geschrieben wird, gilt weiterhin: **echte Umlaute**,
nie `ue`, `ae`, `oe`, `ss` (Kernregel).

## Fehlermeldungen: lieber englisch als gar nicht

Der Fall, um den es wirklich geht.

> **Eine englische Fehlermeldung ist besser als eine deutsche, die es nur
> auf Deutsch gibt.**

In einem mehrsprachigen Produkt — Anwendung, Portal, Kassensystem —
lautet die Reihenfolge:

1. **Die Meldung existiert in der Sprache des Nutzers.** Das ist das Ziel.
2. **Sonst auf Englisch.** Englisch ist die Rückfallsprache, immer.
3. **Nie ein Schlüssel, nie ein leerer Text, nie eine Ausnahme, weil eine
   Übersetzung fehlt.**

Daraus folgt für den Bau:

- **Die Leitsprache eines Produkts ist Englisch.** Neue Texte entstehen
  englisch; die Übersetzung folgt.
- **Der Rückfall ist Englisch**, konfiguriert und geprüft — nicht die
  Sprache des Entwicklers.
- **Technische Fehler bleiben englisch**, auch in einem deutschen
  Produkt: Stapelspuren, Ausnahmetexte, Protokolle, Fehlercodes. Sie
  richten sich an Entwickler und Betrieb.
- **Fachliche Fehler werden übersetzt**, weil sie der Anwender liest —
  „Der Auftrag wurde bereits storniert", nicht `409 Conflict`
  (Skill `neo-api`).

Die Grenze verläuft am Publikum, nicht am Schweregrad.

## Das Regelwerk selbst

Dieses Regelwerk ist der Beleg für die Trennlinie, nicht die Ausnahme
davon:

- **Die Regeln sind deutsch.** Sie sind Text für Menschen, die deutsch
  lesen — dieselbe Kategorie wie eine Bedienungsanleitung.
- **Die Werkzeuge sind englisch.** Jedes Skript in `plugins/*/scripts/`
  hat englische Kommentare, englische Bezeichner, englische Meldungen
  und einen englischen Dateinamen. Ein Werkzeug ist Code, kein Text.
- **Deutsch bleibt, wo es gesucht wird.** Ein Prüfmuster, das nach
  deutschem Wortlaut sucht, enthält deutschen Wortlaut — das ist
  gesuchter Text, keine Programmiersprache, und wird im Kopf des Skripts
  vermerkt.

Wer ein Skript hier ergänzt, schreibt englisch. Wer eine Regel ergänzt,
schreibt deutsch. Beides zurückzudrehen ist ein Befund.

## Bezeichner

- **Englisch, durchgängig, ohne Mischung.** `OrderService`, nicht
  `AuftragService`; `created_at`, nicht `erstellt_am`.
- **Keine deutschen Fachwörter mit englischer Grammatik.** Ein
  `getAuftraege()` ist beides falsch.
- **Ein Begriff je Sache**, im ganzen System — auch über Schichten
  hinweg: Wenn die Tabelle `orders` heißt, heißt die Klasse `Order` und
  das API-Feld `order`.
- **Fachbegriffe, die es nur auf Deutsch gibt** — steuerliche,
  rechtliche, branchenspezifische —, bleiben deutsch und werden **einmal
  erklärt**: `Vorsteuer`, nicht `preTax`. Ein erfundenes englisches Wort
  für einen deutschen Rechtsbegriff ist schlimmer als das deutsche.
- Ausnahmen dieser Art werden im Glossar des Projekts festgehalten
  (Skill `neo-doku`).

## Kommentare

- **Englisch**, auch in einem Projekt, in dem nur Deutschsprachige
  arbeiten. Ein Kommentar überlebt das Team.
- **Kommentare erklären das Warum**, nicht das Was — das steht im Code
  (Skill `neo-code`).
- Codedokumentation, die in eine API-Referenz einfließt, ist englisch.

## Datenbank

- **Tabellen und Spalten englisch**, in der Schreibweise des Stacks.
- **Aufzählungswerte englisch** und kanonisch: `cancelled`, nicht
  `storniert`. Was der Anwender sieht, ist die Beschriftung dazu — aus
  der Sprachdatei, nicht aus der Spalte (Skill `neo-assistent`,
  `references/sprachen.md`).
- Ein Wert, der übersetzt in der Datenbank steht, lässt sich nicht mehr
  suchen, nicht mehr filtern und nicht mehr auswerten.

## Prüfen

- **Ein Bezeichner in deutscher Sprache ist ein Befund**, kein Stilfehler.
  Wo die statische Analyse eine Namensregel kennt, wird sie gesetzt.
- **Neue deutsche Bezeichner fallen in der Durchsicht auf** und werden
  nicht durchgewinkt.
- Der Rückfall auf Englisch wird **geprüft**, nicht angenommen: eine
  fehlende Übersetzung führt zum englischen Text, nicht zum Schlüssel
  (Skill `neo-design`, `references/uebersetzungen.md`).

## Was das nicht heißt

- **Kein Zwang zu englischen Oberflächen.** Ein deutschsprachiges Produkt
  spricht mit seinen Anwendern deutsch — über die Sprachdatei.
- **Keine englischen Commit-Nachrichten**, keine englische Projektdoku
  für einen deutschen Kunden.
- **Keine erfundenen Übersetzungen** für deutsche Rechtsbegriffe.
