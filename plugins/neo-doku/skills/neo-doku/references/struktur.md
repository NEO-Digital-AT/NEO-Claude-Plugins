# Doku-Struktur im Detail

## Die drei festen Ebenen

```
docs / [frontend|backend] / <sprache> / <logische Pfade> / <datei>.md
        ^ nur wenn beides   ^ immer      ^ projektabhängig
```

Entscheidung, ob die erste Ebene gebraucht wird:

| Das Repo enthält | Struktur |
| --- | --- |
| Oberfläche **und** API | `docs/frontend/de/…` und `docs/backend/de/…` |
| nur eine Oberfläche | `docs/de/…` |
| nur eine API oder Bibliothek | `docs/de/…` |
| mehrere Oberflächen (z. B. Verwaltung und öffentliche Seite) | `docs/frontend/de/verwaltung/…` und `docs/frontend/de/statusseite/…` — die Trennung passiert **unter** der Sprache, nicht darüber |

Der Sprachordner steht **immer** da, auch bei nur einer Sprache. Wer ihn
später einzieht, bricht jeden Link, jedes Lesezeichen und jeden Verweis
aus dem Code.

## Aufbau einer `README.md` als Inhaltsverzeichnis

Jeder Ordner hat eine. Sie ist kurz und besteht aus Links mit je einem
Satz — kein Fließtext, keine Wiederholung des Inhalts.

```markdown
---
titel: Monitore bedienen
zielgruppe: anwender
sprache: de
stand: 2026-08-26
---

# Monitore bedienen

Anlegen, Ändern und Pausieren von Monitoren in der Verwaltung.

## Inhalt

| Seite | Worum es geht |
| --- | --- |
| [Monitor anlegen](anlegen.md) | Einen neuen Monitor einrichten, vom Typ bis zum ersten Testlauf |
| [Regeln festlegen](regeln.md) | Wann ein Monitor als beeinträchtigt oder ausgefallen gilt |
| [Monitor pausieren](pausieren.md) | Prüfungen vorübergehend aussetzen, etwa bei Wartung |

## Untergeordnet

- [Benachrichtigungen](benachrichtigungen/README.md) — wer wann worüber informiert wird
```

Regeln dazu:

- Die Reihenfolge folgt dem **Arbeitsablauf**, nicht dem Alphabet.
- Jeder Eintrag hat einen Satz. Ein Verzeichnis aus nackten Dateinamen
  ist keines.
- Unterordner werden verlinkt, nicht ausgeklappt. Die Tiefe entsteht
  durch die Kette der Verzeichnisse.
- Eine neue Datei ohne Eintrag im Verzeichnis gilt als nicht angelegt.
  Das ist Teil derselben Änderung, nicht der nächsten.

## Sprachen

- **Leitsprache ist Deutsch**, sofern das Projekt nichts anderes
  festlegt. Sie ist der Stand, gegen den übersetzt wird.
- Die Ordnernamen sind die zweibuchstabigen Sprachkürzel (`de`, `en`,
  `fr`, `it`), bei Bedarf mit Region (`de-AT`, `pt-BR`).
- **Die Dateinamen sind in allen Sprachen gleich.** `anlegen.md` heißt
  auch im englischen Baum `anlegen.md`. Sonst lässt sich nicht
  maschinell feststellen, was fehlt, und Querverweise brechen beim
  Sprachwechsel.
- Fehlt eine Übersetzung, wird sie **nicht** durch eine leere oder
  maschinell erzeugte Datei ersetzt. Der Sprachordner listet im
  Verzeichnis, was noch nicht übersetzt ist, und verlinkt vorerst auf die
  Leitsprache.
- Ändert sich die Leitsprache, gelten die Übersetzungen als veraltet und
  werden im selben Arbeitsschritt oder als benannte offene Aufgabe
  nachgezogen. Eine falsche Übersetzung ist schlimmer als eine fehlende.
- Screenshots sind **Teil der Sprache**: zeigt ein Bild Oberflächentext,
  gibt es je Sprache ein eigenes. Sprachneutrale Diagramme liegen unter
  `docs/assets/` und werden von allen Sprachen verlinkt.

## Umzüge

Eine Datei zu verschieben ist eine Änderung mit Folgen. In einem Schritt:

1. Datei verschieben.
2. Alle Verweise darauf suchen und anpassen — in der Doku, im Code, in
   Regeldateien, in der Navigation des Doku-Systems.
3. Inhaltsverzeichnisse beider Ordner anpassen.
4. Dasselbe in jedem Sprachbaum.
5. Wo eine Adresse öffentlich war: Weiterleitung einrichten oder die
   Änderung im Änderungsprotokoll benennen.

## Was nicht unter `docs/` gehört

| Inhalt | Wohin |
| --- | --- |
| Geplantes, Entwürfe, offene Konzepte | `/plan` bzw. `/plans` |
| Entscheidungsakten (ADR) | `docs/adr/` — sprachneutral, sie sind Entwicklerinhalt und werden nicht übersetzt |
| Regeln für Agenten | `CLAUDE.md` / `AGENTS.md` im Wurzelverzeichnis |
| Sitzungsübergaben | eigener Ordner nach Projektfestlegung, nicht in der Anwenderdoku |
| Änderungsprotokoll | `CHANGELOG.md` im Wurzelverzeichnis |

## Einstieg für Werkzeuge und Agenten

Eine `docs/README.md` im Wurzelverzeichnis der Doku nennt: welche
Bereiche es gibt, welche Sprachen gepflegt werden, welche die Leitsprache
ist und wo die Bedienungsdoku beginnt. Sie ist der einzige Einstiegspunkt,
den jemand kennen muss.

Wo das Projekt eine maschinenlesbare Übersicht führt (`llms.txt`), wird
sie aus derselben Quelle gepflegt und bei jeder Strukturänderung
nachgezogen.
