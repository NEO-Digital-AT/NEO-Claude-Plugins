# Sprache in der Dokumentation

Lesekonvention siehe `SKILL.md`. Die Regeln hier gelten für jede
NEO-Dokumentation, jede Regeldatei, jede Commit-Nachricht und jeden
Code-Kommentar.

## Trocken und zäh

**Keine Marketingsprache.** Diese Adjektive sind verboten, ersatzlos:

> nahtlos · leistungsstark · robust · hochmodern · zukunftssicher ·
> ganzheitlich · innovativ · revolutionär · mühelos · elegant ·
> intuitiv (als Behauptung) · leistungsfähig · modernst · state of the art

**Keine Meta-Sätze über den Text selbst.** Direkt mit dem Inhalt
beginnen:

| Verboten | Stattdessen |
| --- | --- |
| „Dieses Dokument beschreibt …" | Der Inhalt selbst |
| „Zusammenfassend lässt sich sagen …" | Die Aussage |
| „Im Folgenden wird erläutert …" | Die Erläuterung |
| „Es ist wichtig zu beachten, dass …" | Die Sache, die wichtig ist |
| „Wie bereits erwähnt …" | Die Sache noch einmal, ausgeschrieben |

**Keine Füllwörter.** Streichen, nicht ersetzen:

> grundsätzlich · eigentlich · im Wesentlichen · letztendlich ·
> in der Regel · quasi · sozusagen · durchaus · natürlich · selbstredend ·
> bekanntlich · gewissermaßen

## Satzbau

| Regel | Beispiel |
| --- | --- |
| **Kurze Sätze.** Ein Gedanke je Satz | — |
| **Aktiv statt Passiv** | „Der Dienst prüft die Signatur" statt „Die Signatur wird geprüft" |
| **Ein Verb je Handlung** | „prüfen" statt „die Durchführung der Prüfung vornehmen" |
| **Kein „erfolgt" als Ersatzverb** | „Die Anmeldung läuft über …" statt „Die Anmeldung erfolgt über …" |
| **Anweisungen im Infinitiv-Imperativ** | „Den Dienst starten" statt „Starten Sie den Dienst" |
| **Keine Du-Anrede in der Doku** | — |
| Kundenseitige deutsche Texte in der **Sie-Form** | Oberfläche, Mails, Rechtstexte |

## Vorher und nachher

| Vorher | Nachher |
| --- | --- |
| „Das System bietet eine leistungsstarke und intuitive Möglichkeit zur Verwaltung von Aufträgen." | „Aufträge werden unter Überblick → Aufträge verwaltet." |
| „Es ist grundsätzlich möglich, dass die Prüfung fehlschlägt." | „Die Prüfung schlägt fehl, wenn das Ziel nicht innerhalb von 10 Sekunden antwortet." |
| „Die Konfiguration erfolgt über die Datei." | „Die Datei `app.yaml` konfiguriert den Dienst." |
| „Nach erfolgter Durchführung der Migration …" | „Nach der Migration …" |
| „Der Wert sollte idealerweise nicht zu hoch gewählt werden." | „Höchstens 300 Sekunden. Darüber weist die Anwendung den Wert zurück." |
| „Dieses Kapitel beschreibt die Einrichtung." | „Einrichtung" (als Überschrift) |

Das Muster: **Zahlen statt Adjektive, Namen statt Umschreibungen,
Bedingungen statt Andeutungen.**

## Fachwörter

- **Beim ersten Auftreten erklären.** Die Doku richtet sich nicht nur an
  Programmierer.
- **Ein Begriff je Sache**, im ganzen Projekt. Nicht „Lauf", „Job"
  und „Auftrag" für dasselbe.
- Wo Synonyme im Umlauf sind, werden sie einmal in einer Begriffsliste
  zugeordnet und dann nicht mehr verwendet.
- Englische Fachwörter nur, wo es kein etabliertes deutsches gibt.
  „Commit" bleibt Commit, „Deployment" heißt Ausrollung.

## Schriftzeichen

| Regel | Folge bei Verstoß |
| --- | --- |
| **Echte Umlaute** (ä ö ü ß) in **jedem** deutschen Text | **Blocker** |
| ASCII-Ersatz (ue/ae/oe/ss) | Verboten. Ausnahme nur: Slugs, URLs, Dateinamen, Code, englische Bezeichner |
| **Keine Emojis** in Doku, Commits und Oberflächen | Blocker |
| Gedankenstrich als Halbgeviert (–) oder Geviert (—), je Dokument einheitlich | Muss. **Nie** als Doppel-Bindestrich |
| Deutsche Anführung: „ … " | Sollte |
| Auslassung als einzelnes Zeichen (…), nicht drei Punkte | Sollte |
| Keine Versalienschreibung ganzer Wörter zur Betonung | Muss |

**Die Commit-Nachricht ist ein deutscher Text** und fällt unter dieselbe
Regel (Skill `neo-grundregeln`, `references/git.md`).

## Auszeichnung

- **Fett** für das eine Wort, auf das es ankommt — nicht für ganze
  Absätze. Wer alles hervorhebt, hebt nichts hervor.
- *Kursiv* sparsam, für Begriffe, die gerade eingeführt werden.
- `Code-Auszeichnung` für alles, was wörtlich so eingegeben oder
  gefunden wird: Pfade, Befehle, Feldnamen, Werte, Klassennamen.
- Tabellen für alles, was sich zählen oder vergleichen lässt. Ein Absatz
  mit fünf Kommas ist eine Tabelle, die noch nicht gesetzt wurde.
- Aufzählungen für Gleichrangiges, Nummerierung nur, wo die Reihenfolge
  zählt.

## Belege

**Jede Behauptung mit Fundstelle** (Skill `neo-grundregeln`,
`references/belegpflicht.md`). Eine Fundstelle ist eine Datei mit
Position oder eine Adresse mit Abschnitt — „steht in der Doku" ist
keine.

## Was der Agent nie tut

- Ein verbotenes Adjektiv verwenden, auch nicht in einer Kurzfassung.
- Einen Zielzustand als Gegenwart beschreiben.
- Eine Zahl durch „schnell", „groß" oder „viel" ersetzen.
- Einen Text schreiben, der beschreibt, dass er etwas beschreibt.
- ASCII-Ersatzschreibungen verwenden, auch nicht „nur schnell".
