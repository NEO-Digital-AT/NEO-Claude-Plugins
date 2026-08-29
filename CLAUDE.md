# NEO-Claude-Plugins

Betriebsart: Regelwerk (Claude-Code-Marktplatz), kein ausgeliefertes Produkt
Stack: Markdown, Python 3 (Standardbibliothek), reines Browser-JavaScript
Sprachen: Regeln deutsch, Werkzeuge englisch — siehe unten
Zweigmodell: main mit Arbeitszweig (kein `dev`, siehe unten)

## Zielgruppen und Sprachstufen

| Bereich | Wer liest es | Stufe |
| --- | --- | --- |
| Regeltexte (`SKILL.md`, `references/`, `kernregeln.md`) | Projektinhaber und Agenten | 2 — kundig |
| Werkzeuge und ihre Meldungen (`scripts/`) | wer sie in einer CI einsetzt | 3 — technisch |
| README | wer das Regelwerk einbindet | 2 — kundig |

Stufe 2 heißt hier: Fachbegriffe der Sache ja (Token, Merge, Pull
Request), Werkzeugtechnik nur, wo sie gebraucht wird, und dort erklärt.
Kein Absatz setzt voraus, dass jemand programmiert.

## Geltende Regeln

Die NEO-Kernregeln gelten immer (`plugins/neo-grundregeln/rules/kernregeln.md`,
über den SessionStart-Hook geladen). Zusätzlich sind für dieses Repository
**verbindlich**:

| Skill | Wofür in diesem Projekt |
| --- | --- |
| `neo-grundregeln` | Prozess, Freigaben, **Auftragsliste**, Belegpflicht, Selbstkontrolle |
| `neo-code` | Aufbau und Lesbarkeit der Werkzeuge, Sprache im System |
| `neo-doku` | Trockene Sprache, IST-Zustand, keine Marketingsprache, keine Emojis |

Nicht geltend, mit Grund: alle übrigen Skills. Dieses Repository baut
keine Oberfläche (`neo-design`, `neo-komponenten`), keine API (`neo-api`),
keine Contao-Seite (`neo-contao`), keine App (`neo-mobil`), keinen
Assistenten (`neo-assistent`) — es **beschreibt** deren Regeln. Wer hier
arbeitet, liest den betroffenen Skill trotzdem, bevor er dessen Regeln
ändert.

## Besonderheiten dieses Projekts

- **Die Regeln sind deutsch, die Werkzeuge sind englisch.** Jede Datei
  unter `plugins/*/scripts/` hat englische Kommentare, Bezeichner,
  Meldungen und Dateinamen; jede Regeldatei ist deutsch. Beides
  zurückzudrehen ist ein Befund (Skill `neo-code`,
  `references/sprache.md`).
- **Kein Werkzeug hat Abhängigkeiten.** Python nur Standardbibliothek,
  JavaScript nur Browser-API. Jedes muss in einer fremden CI ohne
  Installation laufen.
- **Ein Werkzeug gilt erst als fertig, wenn es gegen eine absichtlich
  kaputte und eine saubere Vorlage geprüft wurde** und beide das erwartete
  Ergebnis liefern. Behauptet, nicht gemessen, zählt nicht.
- **Zweigmodell: `main` mit Arbeitszweig** (Kernregel 20). Kein `dev` —
  dieses Repository rollt nichts aus. Gearbeitet wird auf
  `claude/neo-plugins-design-system-yjuojp`, von dort mit Fast-Forward
  nach `main`. Kein direkter Push auf `main`.
- **Die `.gitignore` deckt ab, was die Werkzeuge beim Prüfen erzeugen**
  (Kernregel 21). Wer ein Werkzeug hinzufügt, das schreibt, trägt im
  selben Schritt ein, was es schreibt.
- **Versionen:** Wer eine Regel ändert, hebt die Fassung des betroffenen
  Plugins in dessen `.claude-plugin/plugin.json`. Umbenannte Dateien oder
  geänderte Schalter sind eine Nebenversion, keine Fehlerkorrektur.
- **Querverweise auf Kernregel-Nummern** stehen in `README.md` und in
  `plugins/neo-sicherheit/skills/neo-sicherheit/SKILL.md`. Wer eine
  Kernregel einfügt oder entfernt, zieht sie nach.
