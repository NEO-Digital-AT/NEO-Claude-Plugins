# GitHub einrichten — dev und main

Die Regeln des Zweigmodells sind nur so verbindlich wie die
Einstellungen, die sie erzwingen. Ohne Ruleset ist „nie direkt pushen"
eine Bitte.

Alles hier wird **vom Projektinhaber** eingerichtet oder ausdrücklich
freigegeben. Der Agent schlägt vor und prüft, er ändert keine
Schutzregeln.

## Repository-Grundeinstellungen

| Einstellung | Wert | Warum |
| --- | --- | --- |
| Standardzweig | `dev` | Wer klont, zweigt automatisch von `dev` ab, und ein neuer Pull Request zeigt von selbst nach `dev`. Das macht Regel 2 zum Normalfall statt zur Disziplinfrage. Zu bedenken: der Standardzweig ist auch der, den die Repo-Startseite zeigt und auf den sich Dependabot und Code-Scanning voreinstellen. |
| Merge commits erlauben | ja | `dev` → `main` **muss** ein Merge-Commit sein. |
| Squash merging erlauben | ja | Für Arbeitszweig → `dev` sinnvoll: ein Commit je fertiger Änderung. |
| Rebase merging erlauben | nein | Erzeugt neue Commits und lässt `dev` und `main` auseinanderlaufen. |
| Head-Zweig nach Merge löschen | ja | Hält die Zweigliste lesbar. |

## Ruleset für `dev`

Einstellungen → Rules → Rulesets → New branch ruleset. Ziel: `dev`.
Erzwingungsstatus **Active**. Umgehungsliste (Bypass) leer lassen; jeder
Eintrag dort ist ein Loch in der Regel.

| Regel | Einstellung |
| --- | --- |
| Restrict deletions | an |
| Block force pushes | an |
| Require a pull request before merging | an |
| — Required approvals | mindestens 1 (bei Alleinarbeit 0, dann tragen die Prüfungen allein) |
| — Dismiss stale approvals on new commits | an |
| — Require review from Code Owners | an, sobald eine `CODEOWNERS` existiert |
| — Require conversation resolution | an |
| — Allowed merge methods | Squash und Merge |
| Require status checks to pass | an |
| — Require branches to be up to date before merging | an — das erzwingt, dass der Arbeitszweig den aktuellen Stand von `dev` enthält |
| — Pflichtprüfungen | die Testjobs aus `references/workflows.md` |
| Require linear history | aus — es sollen Merge-Commits möglich bleiben |

## Ruleset für `main`

Ziel: `main`. Wie `dev`, mit diesen Abweichungen:

| Regel | Einstellung |
| --- | --- |
| — Allowed merge methods | **nur Merge**. Squash und Rebase abschalten, sonst laufen `dev` und `main` auseinander. |
| — Pflichtprüfungen | zusätzlich die Prüfung `zweigherkunft` |
| Require deployments to succeed | an, wenn die Entwicklungsumgebung vor dem Release erfolgreich bespielt sein soll |

### „Nur aus dev" ist keine GitHub-Einstellung

GitHub kann nicht ausdrücken, dass ein Zweig nur aus einem bestimmten
anderen Zweig gemergt werden darf. Rulesets regeln **wer** pushen und
mergen darf, nicht **woher**.

Durchgesetzt wird es deshalb durch eine Pflichtprüfung: ein Workflow
läuft bei jedem Pull Request nach `main` und schlägt fehl, wenn der
Quellzweig nicht `dev` ist (`zweigherkunft` in
`references/workflows.md`). Als Pflichtprüfung eingetragen, blockiert er
den Merge-Knopf.

## Umgebungen

Einstellungen → Environments. Die Zweigrichtlinie ist der Punkt, der
verhindert, dass ein Arbeitszweig versehentlich die Produktion bespielt.

| Umgebung | Deployment branches | Required reviewers | Secrets |
| --- | --- | --- | --- |
| `entwicklung` | Selected branches → nur `dev` | keine | Zugangsdaten der Entwicklungsumgebung |
| `produktion` | Selected branches → nur `main` | Projektinhaber | Zugangsdaten der Produktion |

Produktions-Secrets liegen ausschließlich an der Umgebung `produktion`,
nie als Repository-Secret — sonst erreicht sie jeder Workflow von jedem
Zweig aus (Skill `neo-sicherheit`).

## Pflichtprüfungen — die drei üblichen Fallen

1. **Der Name muss stimmen.** Eingetragen wird der Name des **Jobs**, wie
   er in der Prüfliste des Pull Requests erscheint — nicht der Name der
   Workflow-Datei. Bei einer Matrix erscheint je Kombination ein eigener
   Eintrag.
2. **Eine Prüfung, die nie läuft, blockiert für immer.** Wird ein
   Workflow über `paths` gefiltert und ist zugleich Pflicht, bleibt der
   Pull Request hängen, sobald der Filter nicht greift. Entweder ohne
   Pfadfilter laufen lassen, oder einen Job ergänzen, der bei
   ausgelassenem Filter erfolgreich meldet.
3. **Erst nach dem ersten Lauf auswählbar.** Eine Prüfung erscheint in
   der Auswahlliste erst, nachdem sie einmal gelaufen ist. Also zuerst
   den Workflow mergen, dann als Pflicht eintragen.

## CODEOWNERS

`.github/CODEOWNERS` regelt, wer welchen Bereich freigeben muss. In
Verbindung mit „Require review from Code Owners" ist das die Antwort auf
„wer darf wohin mergen".

```
*                       @NEO-Digital-AT/entwicklung
/.github/               @erichnigg
/docs/                  @NEO-Digital-AT/entwicklung
```

## Nachprüfen

Die Einrichtung gilt erst als erledigt, wenn sie belegt ist:

- Ein Push auf `dev` wird abgewiesen.
- Ein Pull Request von einem Arbeitszweig nach `main` wird von
  `zweigherkunft` abgewiesen.
- Ein Pull Request mit rotem Test lässt sich nicht mergen.
- Der Merge-Knopf bei `dev` → `main` bietet nur „Create a merge commit".
- Ein Workflow von einem Arbeitszweig kommt nicht an die
  Produktions-Secrets.

Diese fünf Punkte in der Repository-Doku festhalten, mit Datum.
