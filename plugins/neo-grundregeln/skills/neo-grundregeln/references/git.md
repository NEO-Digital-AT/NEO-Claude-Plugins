# Git, Commits, Zweige

Lesekonvention siehe `SKILL.md`.

## Vor jedem Commit

Sieben Prüfungen, jede ein Blocker:

- [ ] **Tests laufen** — und sind grün. Zahlen genannt.
- [ ] **Deutsche Texte mit echten Umlauten**, kein ue/ae/oe/ss.
- [ ] **Keine Secrets** — im Diff, nicht nur in den neuen Dateien.
- [ ] **Keine TODOs, keine FIXMEs.**
- [ ] **Keine temporären Dateien**, keine Debug-Ausgaben, kein
      auskommentierter Code.
- [ ] **Keine leeren Ordner** nach einem Refactoring.
- [ ] **Der Diff entspricht dem freigegebenen Umfang** — Datei für
      Datei durchgesehen.

## Die Commit-Nachricht

**Die Commit-Nachricht ist ein deutscher Text.** Sie trägt echte
Umlaute, keine Ersatzschreibung — ebenso Titel und Text eines Pull
Requests. Ein Dateiname oder ein Slug in der Nachricht bleibt ASCII
(`references/loeschkonzept.md`), der Fließtext daneben nicht.

Aufbau:

```
Kurzfassung in einer Zeile, was sich ändert

Warum es sich ändert. Was vorher galt und warum das nicht reichte.
Nicht, was der Diff ohnehin zeigt.

- Der eine wichtige Punkt
- Der zweite, wenn es einen gibt
- Was dabei bewusst NICHT gemacht wurde
```

| Regel | Folge bei Verstoß |
| --- | --- |
| Erste Zeile sagt, was sich ändert, nicht was getan wurde | Muss |
| Erste Zeile ohne Punkt am Ende, unter etwa 70 Zeichen | Sollte |
| Der Rumpf erklärt das **Warum** | Muss |
| Keine Emojis | Blocker |
| Echte Umlaute | Blocker |
| Keine Kennung eines KI-Modells in Nachricht, Titel oder Rumpf | Blocker |

**Was nicht in eine Commit-Nachricht gehört:** eine Aufzählung der
geänderten Dateien (das zeigt der Diff), Entschuldigungen, Vermutungen
ohne Kennzeichnung, ein Verweis auf ein Gespräch, das niemand mehr
findet.

## Ein Commit-Paket

**Ein abgeschlossener, freigegebener Schritt = ein sauberes
Commit-Paket.** Nicht ein Tag Arbeit, nicht eine Datei.

- Der Commit ist für sich lauffähig: Tests grün, Build durch.
- **Querschnitts-Refactorings nie auf einem unfertigen Feature-Zweig** —
  sie kommen von einem stabilen, getesteten Stand aus, als eigener
  Schritt.
- **Formatierung wird nie in einem Fachcommit vermischt.** Eine
  Formatierungsänderung ist ein eigener Commit, sonst ist der Diff
  unprüfbar.
- Eine Migration und der Code, der sie braucht, gehören in denselben
  Commit.
- Doku und Code gehören in denselben Commit (Skill `neo-doku`).

## Committen und pushen

**Committen und pushen nur, wenn der Projektinhaber es verlangt oder
das Projekt es so festlegt.** Ein Commit ohne diese Grundlage ist ein
Regelverstoß, auch wenn die Arbeit fertig ist.

## Zweige

- **Nie direkt auf `dev` oder `main` pushen.** Beide nehmen Änderungen
  ausschließlich über einen Pull Request entgegen.
- Arbeitszweige gehen von `dev` aus. `main` nimmt ausschließlich Merges
  aus `dev`.
- **Nie Historie umschreiben auf einem Zweig, an dem jemand anderes
  arbeitet** — kein Rebase, kein Amend, kein Force-Push. Auf einem
  eigenen Zweig nur mit `--force-with-lease` und nur, wenn der
  Projektinhaber es weiß.
- Zweigmodell, Schutzregeln, Pflichtprüfungen und Ausrollung:
  Skill `neo-deployment`.

## Was nie ins Repository gehört

| Nie | Wohin stattdessen |
| --- | --- |
| Secrets, Tokens, Schlüssel, Zertifikate mit privatem Teil | Umgebungskonfiguration, Tresor |
| Echte Kundendaten, echte Abzüge der Datenbank | Anonymisiert, freigegeben, dokumentiert |
| Erzeugnisse: `node_modules`, `vendor`, Build-Ausgaben, Zwischenspeicher | `.gitignore` |
| Große Binärdateien ohne Zweck | Erzeugen statt einchecken |
| Persönliche Editor-Einstellungen | Lokal, nicht im Repo |
| Ein Screenshot mit personenbezogenen Daten | Maskiert aufnehmen (Skill `neo-doku`) |

Ein Secret, das einmal im Verlauf steht, gilt als kompromittiert und
wird gewechselt — es reicht nicht, den Commit zu entfernen
(Skill `neo-sicherheit`).

## Pull Requests

- Titel und Text nach denselben Regeln wie eine Commit-Nachricht.
- Der Text nennt: Umfang, Auswirkungen, Belege (Testzahlen), was
  bewusst offen blieb.
- **Ein roter Lauf wird nicht durch einen leeren Commit erneut
  angestoßen.** Ursache suchen, beheben, pushen.
- Der Agent **merged nicht selbst**, solange der Projektinhaber es nicht
  verlangt hat.
