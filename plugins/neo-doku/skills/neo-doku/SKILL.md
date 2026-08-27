---
name: neo-doku
description: >
  NEO-Dokumentationsregeln. Diesen Skill laden bei jeder Doku-Arbeit:
  Entwicklerdokumentation, Anwender- und Bedienungsdokumentation
  (Handbuch), API-Beschreibung, README, Inhaltsverzeichnis,
  Entscheidungsakten (ADR), Änderungsprotokoll, Übergaben,
  Planungsdokumente unter /plan bzw. /plans, VitePress-Seiten, Release
  Notes, Übersetzung von Doku. Ebenso beim Anlegen oder Umbauen der
  Ordnerstruktur unter docs, beim Erzeugen und Markieren von Screenshots
  für die Doku und wenn Dokumentation auch für generative Agenten lesbar
  sein soll.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, destilliert aus NEOcash- und LeoFlex-Regelwerken, Stand 2026-08
---

# NEO-Dokumentationsregeln

## Wie diese Regeln zu lesen sind

| Wort | Bedeutung |
| --- | --- |
| **Nie**, **immer**, **muss** | Verbindlich. Ein Verstoß ist ein **Blocker**: die Änderung gilt als nicht fertig. |
| **Ausnahme** | Nur mit ausdrücklicher Freigabe des Projektinhabers, festgehalten mit Grund und Datum. **Ohne Vermerk gibt es keine Ausnahme.** |
| **Sollte** | Begründet abweichbar, die Abweichung wird gemeldet. |

## Der Grundsatz: Doku ist Teil der Änderung

- Die Dokumentation beschreibt **immer den aktuellen IST-Zustand**. Sie
  behauptet nie etwas, das nicht mehr vorhanden ist, noch nicht umgesetzt
  wurde oder falsch ist.
- **Doku wird im selben Schritt nachgezogen** — idealerweise im selben
  Commit. Nicht im nächsten, nicht morgen. Eine Änderung ohne
  nachgezogene Doku ist **nicht fertig**.
- Jede Verhaltens-, Architektur-, Kommando- oder Routenänderung prüft die
  ganze Kette: Entwicklerdoku, Anwenderdoku, Inhaltsverzeichnisse,
  Screenshots, Änderungsprotokoll, Regeldateien für Agenten
  (CLAUDE.md/AGENTS.md).
- **Verhalten, das künftige Agenten-Entscheidungen prägt, gehört in die
  Regeldatei**, nicht nur in die README.
- Offene Punkte ehrlich benennen („derzeit nicht umgesetzt") statt
  Zielzustände als Gegenwart zu beschreiben.

## Struktur — verbindlich

```
docs / [frontend|backend] / <sprache> / <logische Pfade> / <datei>.md
        ^ nur wenn beides    ^ immer     ^ projektabhängig
```

- **`docs/` ist der Ort.** Geplantes gehört nach `/plan` bzw. `/plans`.
- **`frontend/` und `backend/`** trennen Oberflächen- und
  API-Dokumentation. Hält ein Repo nur eines von beiden, entfällt diese
  Ebene.
- **Der Sprachordner steht immer da** (`de`, `en`, `fr`, `it`, …), auch
  bei nur einer Sprache. Wer ihn später einzieht, bricht jeden Link.
- **Jeder Ordner hat eine `README.md`** als Inhaltsverzeichnis: je
  Eintrag Link und ein Satz.
- **Bilder liegen in `bilder/` neben ihrer Doku.** Sprachneutrale
  Grafiken unter `docs/assets/`.
- Dateinamen sind Slugs: klein, mit Bindestrich, ohne Umlaute.

Aufbau der Verzeichnisse, Sprachen, Umzüge, was **nicht** unter `docs/`
gehört: `references/struktur.md`.

## Zielgruppen strikt trennen

| Dokument | Publikum | Inhalt |
| --- | --- | --- |
| Entwickler- und Systemdoku | Entwickler, Agenten | Architektur, Datenhaltung, das WARUM von Entscheidungen, Eigenheiten fremder APIs, Teststrategie |
| Anwenderdoku (Handbuch, Bedienungsanleitung) | Endanwender | Schritt-für-Schritt-Abläufe, Bedeutung von Einstellungen, Fehlerfälle aus Nutzersicht |

**In die Anwenderdoku gehören NIE:** Implementierungsdetails,
Komponenten- oder Store-Namen, Endpoints, Code, Architektur,
Datenbanktabellen, Konfigurationsschlüssel.

**Doku erklärt das WARUM**, nicht das Was, das der Code ohnehin zeigt.
Das gilt auch für Code-Kommentare.

## Bedienung wird dokumentiert

Jede Oberfläche bekommt eine Bedienungsdoku. Sie ist fertig, wenn jemand
die Aufgabe damit **ohne Rückfrage** erledigt.

- Je Ablauf: Ziel, Voraussetzungen, nummerierte Schritte, Ergebnis,
  häufige Fehler und was dann zu tun ist.
- **Bedienelemente werden wörtlich benannt**, wie sie in der Oberfläche
  stehen: die Schaltfläche „Auftrag anlegen", nicht „der Anlegen-Knopf".
- **Screenshots gehören dazu**, einschließlich Detailausschnitten, im
  Repository eingecheckt.
- Wichtige Stellen werden markiert: roter Rahmen, roter Pfeil,
  Nummernmarken, Markerfläche, Infokasten.
- **Ein Screenshot ergänzt den Text, er ersetzt ihn nie.** Was nur im
  Bild steht, ist für Vorlesegeräte, für die Suche und für Agenten nicht
  vorhanden.

Erzeugung, Markierung, Benennung, Pflege: `references/screenshots.md`.

## Entscheidungen werden festgehalten

**Jede tragende Entscheidung bekommt eine Entscheidungsakte (ADR) — vor
der Umsetzung.** Sie beantwortet, warum es so und nicht anders gebaut
wurde, und was verworfen wurde.

Format, Nummerierung, Pflichtabschnitte und der Abschnitt „Was dabei
schiefging": `references/entscheidungsakten.md`.

## Auch für Agenten lesbar

Jede Doku wird so gebaut, dass ein generatives Modell sie **ohne den Rest
des Repositories** versteht: eindeutiger Titel, ein Thema je Datei,
stabile Überschriften, ausgeschriebene Namen statt „siehe oben",
Tabellen für Parameter, jede Aussage im Text und nicht nur im Bild.
Regeln und Vorlage: `references/agentenlesbarkeit.md`.

## Geplantes: /plan bzw. /plans

- **Alles, was geplant, aber nicht fertig ist, liegt unter /plan** — nie
  in /docs. Dort liegen auch die Oberflächen-Entwürfe (Skill
  `neo-design`).
- Jede geplante Funktion dort genau beschreiben: Zweck, Aufbau,
  betroffene Bausteine, offene Fragen, Abhängigkeiten.
- Nach der Umsetzung wandert der Inhalt in die Dokumentation (IST); der
  Plan wird als umgesetzt markiert oder entfernt.
- **/docs und /plan dürfen sich nie widersprechen.**

## Die Bereiche

| Bereich | Referenz |
| --- | --- |
| Ordnerstruktur, Sprachen, Inhaltsverzeichnisse, Umzüge | `references/struktur.md` |
| Screenshots erzeugen, markieren, ablegen, pflegen | `references/screenshots.md` |
| Doku, die auch ein Agent versteht | `references/agentenlesbarkeit.md` |
| Entscheidungsakten (ADR) | `references/entscheidungsakten.md` |
| Sprache: Verbotslisten, Muster, Beispiele vorher/nachher | `references/sprache.md` |
| Vorlagen: Bedienung, Entwicklerseite, Änderungsprotokoll, Übergabe | `references/vorlagen.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

## Werkzeug

`scripts/markierung.js` blendet Rahmen, Pfeile, Nummern, Infokästen,
Textmarker und Scheinwerfer **vor** der Aufnahme in die Seite ein und
wird mitfotografiert — vektorscharf, an den Elementen ausgerichtet.
