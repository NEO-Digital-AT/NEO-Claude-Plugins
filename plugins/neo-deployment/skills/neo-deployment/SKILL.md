---
name: neo-deployment
description: >
  NEO-Zweigmodell und Auslieferungsregeln. Diesen Skill laden bei jeder
  Arbeit an Zweigen, Pull Requests, Merges, Schutzregeln, GitHub-Rulesets,
  CODEOWNERS, GitHub Actions, Umgebungen, Freigaben und Ausrollung — sowie
  beim Anlegen eines neuen Repositories, beim Einrichten von dev und main,
  bei der Frage, von wo ein Zweig abzweigt, wohin gemergt werden darf, wer
  mergen darf und warum ein Deployment blockiert ist. Ebenso bei Hotfixes
  und beim Zurückrollen eines Releases.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# NEO-Zweigmodell und Auslieferung

## Die zwei geschützten Zweige

| Zweig | Bedeutung | Wird ausgerollt nach | Nimmt entgegen |
| --- | --- | --- | --- |
| `main` | Live. Was hier liegt, läuft beim Kunden. | Produktion | **ausschließlich** Merges aus `dev` |
| `dev` | Integrationsstand. | Entwicklungsumgebung | Merges aus Arbeitszweigen |

Arbeitszweige gehen **immer von `dev`** aus, nie von `main` und nie
voneinander.

```
   Arbeitszweig ─┐
   Arbeitszweig ─┼──► dev ──► main ──► Produktion
   Arbeitszweig ─┘      │
                        └──► Entwicklungsumgebung
```

## Die harten Regeln

1. **Nie direkt auf `dev` oder `main` pushen.** Beide Zweige nehmen
   Änderungen ausschließlich über einen Pull Request entgegen. Kein
   `git push origin dev`, kein Force-Push, kein Löschen.
2. **Jeder neue Zweig zweigt von `dev` ab** und ist vor dem Merge auf
   den aktuellen Stand von `dev` gebracht.
3. **`main` nimmt nur `dev`.** Ein Pull Request nach `main`, dessen
   Quelle nicht `dev` ist, wird maschinell abgewiesen — GitHub kennt
   dafür keine eigene Einstellung, deshalb erledigt das eine
   Pflichtprüfung (siehe `references/github-einstellungen.md`).
4. **`dev` nach `main` immer als Merge-Commit.** Nie Squash, nie Rebase:
   beides erzeugt neue Commits, `dev` und `main` laufen auseinander, und
   jeder folgende Release-Merge meldet Konflikte, die es nicht gibt.
5. **Auf beiden Zweigen laufen Tests, und nur Grünes wird ausgerollt.**
   Der Auslieferungsschritt hängt am Testschritt (`needs`), nicht daneben.
   Ein rotes Ergebnis blockiert die Ausrollung, es wird nicht übergangen.
6. **Wer wohin mergen darf, steht in den Repository-Einstellungen**, nicht
   in der Absprache. Ohne Ruleset ist die Regel eine Bitte.

## Geltung

dev und main sind die **Vorgabe für jedes neue Repository** der NEO
Digital. Wer ohne `dev` auskommen will — ein reines Regel-, Doku- oder
Bibliotheks-Repo ohne eigene Ausrollung —, begründet das und holt die
Freigabe des Projektinhabers. Bestehende Repositories werden bei der
nächsten Gelegenheit nachgezogen, nicht im Vorbeigehen umgestellt: die
Umstellung ist eine eigene, angekündigte Änderung.

## Ablauf einer Änderung

1. `dev` holen, davon abzweigen. Zweigname nach dem Muster des Projekts.
2. Arbeiten, committen (Skill `neo-grundregeln`, Abschnitt 7).
3. Vor dem Pull Request `dev` in den Arbeitszweig mergen und lokal
   validieren: Abhängigkeiten → Lint/Analyse → Tests → Build.
4. Pull Request **nach `dev`**. Beschreibung nennt Umfang, Auswirkungen
   und Belege. Prüfungen müssen grün sein, Kommentare aufgelöst.
5. Merge nach `dev` — durch den, der es darf. Die Entwicklungsumgebung
   wird ausgerollt und dort geprüft.
6. Für ein Release: Pull Request **`dev` → `main`**, als Merge-Commit.
   Nach dem Merge rollt die Produktion aus.
7. Version und Änderungsprotokoll gehören zum Release, nicht danach.

## Hotfix

Ein Fehler in der Produktion wird ebenfalls über `dev` behoben: Zweig von
`dev`, Pull Request nach `dev`, dann `dev` → `main`. Regel 3 gilt ohne
Ausnahme.

**Folge, die vor dem ersten Hotfix zu klären ist:** liegt in `dev`
unfertige Arbeit, geht sie beim Hotfix mit nach `main`. Damit dieser Weg
trägt, muss `dev` **jederzeit ausrollfähig** sein — unfertige Arbeit
bleibt im Arbeitszweig oder hinter einem Schalter. Wo das im Einzelfall
nicht gilt, entscheidet der Projektinhaber ausdrücklich über den
Ausnahmeweg; der Agent entscheidet das nie selbst.

## Zurückrollen

Ein fehlerhaftes Release wird zurückgerollt, indem der Merge-Commit auf
`main` rückgängig gemacht wird (`git revert -m 1`) — nie durch
Force-Push und nie durch Zurücksetzen des Zweigs. Der Rückbau wird
anschließend nach `dev` zurückgeführt, sonst holt der nächste
Release-Merge den Fehler wieder.

## Was der Agent nie tut

- Auf `dev` oder `main` pushen, auch nicht „nur diese eine Zeile".
- Einen Pull Request selbst mergen, ohne dass der Projektinhaber es
  verlangt hat.
- Eine Prüfung abschalten, überspringen, als „nicht erforderlich"
  markieren oder einen Ausnahmeeintrag setzen, damit ein Merge durchgeht.
- Einen roten Test als Flakiness abtun, ohne es zu belegen.
- Schutzregeln oder Rulesets ändern. Das ist eine Entscheidung des
  Projektinhabers.
- Einen leeren Commit oder ein Schließen-und-Öffnen verwenden, um eine
  Prüfung erneut anzustoßen.

## Einrichtung

Konkrete Einstellungen — Rulesets für `dev` und `main`, Pflichtprüfungen,
Umgebungen mit Zweigrichtlinie, erlaubte Merge-Verfahren, CODEOWNERS:
`references/github-einstellungen.md`.

Workflow-Gerüste für Tests auf beiden Zweigen, die Herkunftsprüfung des
Release-Pull-Requests und die Ausrollung mit Testtor:
`references/workflows.md`.

Zugehörige Skills: `neo-grundregeln` (Commit-Hygiene, Tests),
`neo-sicherheit` (Release-Evidenz, Secrets in Workflows, Lieferkette).
