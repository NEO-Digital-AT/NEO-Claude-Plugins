---
name: neo-doku
description: >
  NEO-Dokumentationsregeln. Diesen Skill laden bei jeder Doku-Arbeit:
  Entwicklerdokumentation, Anwender- und Bedienungsdokumentation
  (Handbuch), API-Beschreibung, README, Inhaltsverzeichnis,
  Änderungsprotokoll, Planungsdokumente unter /plan bzw. /plans,
  VitePress-Seiten, Release Notes, Übersetzung von Doku. Ebenso beim
  Anlegen oder Umbauen der Ordnerstruktur unter docs, beim Erzeugen und
  Markieren von Screenshots für die Doku und wenn Dokumentation auch für
  generative Agenten lesbar sein soll.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, destilliert aus NEOcash- und LeoFlex-Regelwerken, Stand 2026-08
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
  ganze Kette: Entwicklerdoku, Anwenderdoku, Inhaltsverzeichnisse,
  Screenshots, Änderungsprotokoll, Regeldateien für Agenten
  (CLAUDE.md/AGENTS.md). Verhalten, das künftige Agenten-Entscheidungen
  prägt, gehört in die Regeldatei, nicht nur in die README.
- Offene Punkte ehrlich benennen („derzeit nicht umgesetzt") statt
  Zielzustände als Gegenwart zu beschreiben.

## Struktur und Ablage — verbindlich

```
docs/
  frontend/            nur wenn das Repo beides hält
    de/                je Sprache ein Ordner: de, en, fr, it, …
      README.md        Inhaltsverzeichnis dieses Ordners
      bedienung/
        README.md
        monitore/
          README.md
          anlegen.md
          bilder/
            monitor-anlegen.png
      entwicklung/
        README.md
        ...
    en/
      README.md
      ...
  backend/
    de/
      README.md
      ...
  assets/              sprachneutrale Bilder (Diagramme, Marken)
```

- **`docs/` ist der Ort.** Alles Dokumentierte liegt dort. Geplantes
  gehört nach `/plan` bzw. `/plans`.
- **`frontend/` und `backend/`** trennen Oberflächen- und
  API-Dokumentation. **Hält ein Repo nur eines von beiden, entfällt
  diese Ebene** — dann folgen die Sprachordner direkt unter `docs/`.
- **Danach immer der Sprachordner** (`de`, `en`, `fr`, `it`, …), auch
  wenn es zunächst nur eine Sprache gibt. Nachträglich eingezogen wird
  er nie ohne Bruch aller Links.
- **Darunter logisch nach Thema gegliederte Pfade**, jede Doku als
  `.md`-Datei. Die Gliederung ist projektabhängig, die drei Ebenen
  darüber sind es nicht.
- **Jeder Ordner hat eine `README.md`** als Inhaltsverzeichnis: je
  Eintrag Link und ein Satz, worum es geht. GitHub zeigt sie beim Öffnen
  des Ordners von selbst an.
- **Bilder liegen bei ihrer Doku**, in einem `bilder/`-Ordner neben der
  Datei, die sie verwendet. Sprachneutrale Grafiken unter `docs/assets/`.
- Dateinamen sind Slugs: klein, mit Bindestrich, ohne Umlaute
  (`monitor-anlegen.md`). Der Titel im Dokument trägt die Umlaute.
- Nutzt das Projekt ein Doku-System (VitePress o. ä.), gelten dessen
  Konventionen zusätzlich: Navigation und Sidebar mitpflegen, interne
  Linkform verwenden, der Build muss durchlaufen.

Aufbau der Inhaltsverzeichnisse, Übersetzungspflege, Umzüge und
Beispiele: `references/struktur.md`.

## Zielgruppen strikt trennen

| Dokument | Publikum | Inhalt |
| --- | --- | --- |
| Entwickler-/Systemdoku | Entwickler, Agenten | Architektur, Datenhaltung, das WARUM von Entscheidungen, Eigenheiten fremder APIs, Teststrategie |
| Anwenderdoku (Handbuch, Bedienungsanleitung) | Endanwender | Schritt-für-Schritt-Abläufe, Bedeutung von Einstellungen, Fehlerfälle aus Nutzersicht |

In die Anwenderdoku gehören NIE: Implementierungsdetails, Komponenten-
oder Store-Namen, Endpoints, Code, Architektur.

Doku erklärt das WARUM (Entscheidungen, Einschränkungen, Regeln), nicht
das Was, das der Code ohnehin zeigt. Das gilt auch für Code-Kommentare.

## Bedienung wird dokumentiert

Jede Oberfläche bekommt eine Bedienungsdoku. Sie ist fertig, wenn jemand
die Aufgabe damit ohne Rückfrage erledigt.

- Je Ablauf: Ziel, Voraussetzungen, nummerierte Schritte, Ergebnis,
  häufige Fehler und was dann zu tun ist.
- Bedienelemente werden **wörtlich** benannt, wie sie in der Oberfläche
  stehen: die Schaltfläche „Monitor anlegen", nicht „der Anlegen-Knopf".
- **Screenshots gehören dazu**, einschließlich Detailausschnitten. Sie
  werden erzeugt, markiert und ins Repo eingecheckt, damit sie von dort
  angezeigt werden.
- Wichtige Stellen im Bild werden markiert: roter Rahmen, roter Pfeil,
  Nummernmarken, Markerfläche, Infokasten mit Text.
- Ein Screenshot **ergänzt** den Text, er ersetzt ihn nie. Was nur im
  Bild steht, ist für Vorlesegeräte und für Agenten nicht vorhanden.

Erzeugung, Markierung, Benennung, Auflösung und Pflege der Bilder:
`references/screenshots.md`.

## Auch für Agenten lesbar

Jede Doku wird so gebaut, dass ein generatives Modell sie ohne den Rest
des Repositories versteht: eindeutiger Titel, ein Thema je Datei,
stabile Überschriften, ausgeschriebene Namen statt Verweise wie „siehe
oben", Tabellen für Parameter, jede Aussage im Text und nicht nur im
Bild. Regeln und Vorlage: `references/agentenlesbarkeit.md`.

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

## Geplantes: /plan bzw. /plans

- Alles, was geplant, aber nicht fertig ist, liegt unter /plan bzw.
  /plans — nie in /docs. Jede geplante Funktion dort genau beschreiben:
  Zweck, Aufbau, betroffene Bausteine, offene Fragen, Abhängigkeiten.
  Dort liegen auch die Oberflächen-Entwürfe (Skill `neo-design`).
- Nach der Umsetzung wandert der Inhalt in die Dokumentation (IST);
  den Plan als umgesetzt markieren oder entfernen. /docs und /plan
  dürfen sich nie widersprechen.

## Übergaben

Sitzungs- oder Aufgabenübergaben als Datei im Repo festhalten: Stand und
Branch, was erledigt und verifiziert ist, Belege (Testzahlen, Logs),
nächster Schritt, offene Entscheidungen.
