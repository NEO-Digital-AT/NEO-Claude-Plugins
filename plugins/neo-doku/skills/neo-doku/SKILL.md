---
name: neo-doku
description: >
  NEO-Dokumentationsregeln. Diesen Skill laden bei jeder Doku-Arbeit:
  Entwicklerdokumentation, Anwenderdokumentation (Handbuch,
  Bedienungsanleitung), README, Änderungsprotokoll, Planungsdokumente
  unter /plan bzw. /plans, VitePress-Seiten, Release Notes. Regelt
  Sprache, Struktur, Zielgruppen-Trennung und die Pflicht, Doku im selben
  Schritt wie den Code zu ändern.
metadata:
  herkunft: NEO Digital — destilliert aus NEOcash- und LeoFlex-Regelwerken, Stand 2026-08
---

# NEO-Dokumentationsregeln

## Grundsatz: Doku ist Teil der Änderung

- Die Dokumentation beschreibt immer den aktuellen IST-Zustand. Sie
  behauptet nie etwas, das nicht mehr vorhanden ist, noch nicht umgesetzt
  wurde oder falsch ist.
- Mit jeder Änderung einer Funktion oder des Frontend-Designs die
  betroffene Dokumentation im selben Schritt (idealerweise im selben
  Commit) nachziehen. Die Doku ist nie „hinterher".
- Jede Verhaltens-, Architektur-, Kommando- oder Routenänderung prüft die
  ganze Kette: Entwicklerdoku, Anwenderdoku, Änderungsprotokoll,
  Regeldateien für Agenten (CLAUDE.md/AGENTS.md). Verhalten, das künftige
  Agenten-Entscheidungen prägt, gehört in die Regeldatei, nicht nur in
  die README.
- Offene Punkte ehrlich benennen („derzeit nicht umgesetzt") statt
  Zielzustände als Gegenwart zu beschreiben.

## Sprache: trocken und zäh

- Keine Marketingsprache. Verbotene Adjektive: nahtlos, leistungsstark,
  robust, hochmodern, zukunftssicher, ganzheitlich, innovativ,
  revolutionär, mühelos, elegant.
- Keine Meta-Sätze über den Text selbst („Dieses Dokument beschreibt …",
  „Zusammenfassend lässt sich sagen …"). Direkt mit dem Inhalt beginnen.
- Keine Füllwörter: grundsätzlich, eigentlich, im Wesentlichen,
  letztendlich, in der Regel, quasi, sozusagen. Streichen, nicht ersetzen.
- Kurze Sätze, Aktiv statt Passiv, ein Verb pro Handlung (keine
  „Durchführung der Prüfung", sondern „prüfen"). Kein „erfolgt" als
  Ersatzverb. Anweisungen im Infinitiv-Imperativ („Den Dienst starten"),
  keine Du-Anrede in der Doku.
- Fachwort beim ersten Auftreten erklären — die Doku richtet sich nicht
  nur an Programmierer. Jede Behauptung mit Fundstelle.
- **Echte Umlaute** (ä ö ü ß) in jedem deutschen Text; ASCII-Ersatz
  (ue/ae/oe/ss) ist verboten. Ausnahmen: Slugs, URLs, Code,
  englischsprachige Bezeichner. Keine Emojis. Kundenseitige deutsche
  Texte in der Sie-Form.
- Gedankenstrich als Halbgeviertstrich (–) oder Geviertstrich (—), je
  Dokument einheitlich — nie als Doppel-Bindestrich.

## Zielgruppen strikt trennen

| Dokument | Publikum | Inhalt |
| --- | --- | --- |
| Entwickler-/Systemdoku | Entwickler, Agenten | Architektur, Datenhaltung, das WARUM von Entscheidungen, Eigenheiten fremder APIs, Teststrategie |
| Anwenderdoku (Handbuch, Bedienungsanleitung) | Endanwender | Schritt-für-Schritt-Abläufe, Bedeutung von Einstellungen, Fehlerfälle aus Nutzersicht |

In die Anwenderdoku gehören NIE: Implementierungsdetails, Komponenten-
oder Store-Namen, Endpoints, Code, Architektur.

Doku erklärt das WARUM (Entscheidungen, Einschränkungen, Regeln), nicht
das Was, das der Code ohnehin zeigt. Das gilt auch für Code-Kommentare.

## Struktur und Ablage

- Saubere Hierarchien: getrennt nach Sprache (de, en, …) und nach
  logischer Gruppierung. Die konkrete Aufteilung ist projektabhängig —
  sie VOR dem Anlegen einer neuen Doku-Struktur beim Projektinhaber
  erfragen, nie eigenmächtig festlegen.
- Nutzt das Projekt ein Doku-System (z. B. VitePress), gelten dessen
  Konventionen: Navigation und Sidebar mitpflegen, interne Linkform des
  Systems verwenden, Build der Doku muss durchlaufen.
- Existiert eine Doku-Vorlage im Projekt (z. B. docs/VORLAGE.md), gilt
  sie wortwörtlich.
- Ein Änderungsprotokoll (was/wann/warum je Änderung) pflegen, wo das
  Projekt eines vorsieht.

## Geplantes: /plan bzw. /plans

- Alles, was geplant, aber nicht fertig ist, liegt unter /plan bzw.
  /plans — nie in /docs. Jede geplante Funktion dort genau beschreiben:
  Zweck, Aufbau, betroffene Bausteine, offene Fragen, Abhängigkeiten.
- Nach der Umsetzung wandert der Inhalt in die Dokumentation (IST);
  den Plan als umgesetzt markieren oder entfernen. /docs und /plan
  dürfen sich nie widersprechen.

## Übergaben

Sitzungs- oder Aufgabenübergaben als Datei im Repo festhalten: Stand und
Branch, was erledigt und verifiziert ist, Belege (Testzahlen, Logs),
nächster Schritt, offene Entscheidungen.
