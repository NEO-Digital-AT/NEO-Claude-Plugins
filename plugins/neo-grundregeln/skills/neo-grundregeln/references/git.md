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

## Einheitlicher Stil: Zweige, Commits, Releases

Projektinhaber 15.11.2026: Die Liste der Commits auf GitHub ist sauber,
jeder Commit sagt klar, was sich geändert hat, immer im selben Stil —
kein „Commit-Friedhof“, keine Fantasie- oder Zufallswörter.

**Zweignamen:** `<typ>/<kurzbeschreibung>` — englisch, klein, Wörter
mit Bindestrich, ohne Leerzeichen, ohne Zufallskennung. Beispiele:
`fix/post-head-buttons`, `feat/sidebar-over-the-page`,
`docs/contao-manager-metadata`.

**Commit-Betreff nach Conventional Commits 1.0** (der übliche Standard;
GitHub, Release-Werkzeuge und Changelog-Generatoren lesen ihn):

```
<typ>(<bereich>): <Kurzbeschreibung>
```

| Typ | Wofür |
| --- | --- |
| `feat` | neue Funktion |
| `fix` | Fehlerkorrektur |
| `docs` | nur Doku, README, Metadaten |
| `refactor` | Umbau ohne geändertes Verhalten |
| `perf` | schneller, sparsamer |
| `test` | nur Tests |
| `style` | nur Formatierung |
| `build` / `ci` | Abhängigkeiten, Build, Prüf-Workflows |
| `chore` | Pflege ohne Wirkung auf das Produkt |
| `revert` | nimmt einen Commit zurück |

`<bereich>` ist optional (z. B. `feat(sidebar): …`); Kurzbeschreibung
englisch, klein begonnen, ohne Punkt am Ende. Eine
brechende Änderung trägt `!` nach dem Typ (`feat!: …`) und im Rumpf eine
Zeile `BREAKING CHANGE: …`. Keine Nummern im Betreff: Commits sind über
ihren Hash eindeutig, gezählt werden Releases (SemVer) und Pull Requests.

**Logisch zusammenfassen, bevor gemergt wird.** Auf dem eigenen
Arbeitszweig werden Zwischenstände, Korrekturen („Tests angepasst“,
„Tippfehler“) und doppelte Commits zu logischen Commits zusammengelegt
(je Änderung einer, z. B. ein `feat` mit seinen Tests und seiner Doku,
ein `fix`), erst dann wird gemergt. Viele Commits je Release sind in
Ordnung, solange jeder eine abgeschlossene Änderung ist. Historie
anderer Zweige wird nie umgeschrieben.

**Weg eines Commits:** Arbeitszweig → `dev` (Testseite) → `main`. Ein
Merge nach `main` ist immer ein Release: Version nach SemVer
(`MAJOR.MINOR.PATCH`), Tag `v<Version>`, Titel `<Version>`, Text = der
Abschnitt der Version im CHANGELOG (Keep a Changelog: `Added`,
`Changed`, `Fixed`, `Removed`, `Security`, in dieser Reihenfolge, je
Punkt ein englischer Satz). Jede Fassung, jedes
Projekt, auch LeoFlex, im selben Aufbau.

**Versionsnummer `MAJOR.MINOR.PATCH` (Semantic Versioning 2.0):** Die
Fassung hebt genau eine Stelle, nach der größten Änderung seit dem
letzten Release; die Stellen rechts davon fallen auf 0 (1.4.2 → 2.0.0,
1.4.2 → 1.5.0, 1.4.2 → 1.4.3).

| Stelle | Wann | Beispiele |
| --- | --- | --- |
| **MAJOR** (1.x.x → 2.0.0) | Wer aktualisiert, muss selbst etwas tun, oder etwas Bestehendes funktioniert nicht mehr wie vorher | öffentliche Methode, Schnittstelle, Template-Variable, Einstellung oder Feld entfernt oder umbenannt; Contao- oder PHP-Fassung fällt weg; Daten werden so umgebaut, dass es kein Zurück gibt; LeoFlex: Relaunch, geänderte API für Kunden |
| **MINOR** (1.4.x → 1.5.0) | Neues kommt dazu, alles Bestehende läuft unverändert weiter | neue Funktion, neue Einstellung, neue Sprache, neues Modul, neue Contao- oder PHP-Fassung unterstützt; etwas wird als veraltet markiert, aber noch nicht entfernt |
| **PATCH** (1.4.2 → 1.4.3) | Nur Korrekturen, kein neues Verhalten | Fehler behoben, Sicherheitslücke geschlossen, Text, Übersetzung oder Doku korrigiert, Darstellung repariert |

- Tag `v<Version>` (`v1.5.0`), Release-Titel `<Version>` (`1.5.0`).
- **Ein veröffentlichter Tag wird nie verschoben oder neu vergeben.**
  Ein Fehler darin wird mit der nächsten PATCH-Fassung behoben.
  Ausnahme nur vor der ersten Veröffentlichung (Packagist, Store).
- Testfassungen auf `dev` tragen einen Zusatz: `1.5.0-beta.1`,
  `1.5.0-rc.1`; ohne Zusatz nur, was nach `main` geht.
- Jedes Paket hat seine eigene Nummer. Abhängigkeiten verlangen die
  kleinste nötige Fassung mit `^` (`^1.2`), damit MINOR und PATCH ohne
  Änderung ankommen.
- Im Zweifel die höhere Stelle: lieber MINOR als PATCH, wenn sich
  Verhalten ändert.

**Öffentliche Repositories zeigen nur `main`** mit seinen
Release-Commits; Arbeits- und `dev`-Zweige liegen nur im privaten
Repository. Gemergte Arbeitszweige werden gelöscht.

## Die Commit-Nachricht

**Auf GitHub ist Englisch die Hauptsprache** (Projektinhaber
15.11.2026), in jedem Repository, auch in privaten wie LeoFlex:
Commit-Nachrichten, Titel und Text von Pull Requests, Release-Texte und
CHANGELOG sind englisch, damit auch Entwickler ohne Deutsch mitarbeiten
können. Deutsch bleiben nur Inhalte, die für deutschsprachige Leser
geschrieben sind (deutsche Doku, deutsche Oberflächentexte) — dort mit
echten Umlauten.

Aufbau (Betreff im Stil oben):

```
feat(sidebar): one-line summary of what changes

Why it changes. What applied before and why that was not enough.
Not what the diff shows anyway.

- The one important point
- The second, if there is one
- What was deliberately NOT done
```

| Regel | Folge bei Verstoß |
| --- | --- |
| Erste Zeile sagt, was sich ändert, nicht was getan wurde | Muss |
| Erste Zeile ohne Punkt am Ende, unter etwa 70 Zeichen | Sollte |
| Der Rumpf erklärt das **Warum** | Muss |
| Keine Emojis | Blocker |
| Englisch (Betreff, Rumpf, Pull Request, Release-Text) | Muss |
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

## Zweige: drei Modelle, das Projekt sagt welches

> **Das Zweigmodell des letzten Projekts gilt hier nicht.** Es steht in
> der `CLAUDE.md`; fehlt der Eintrag, gilt das strengste Modell und es
> wird nachgefragt.

### Ein Auftrag, ein Zweig — und erst mergen, dann der nächste

> **Kein zweiter Zweig, solange der erste offen ist.**

```
öffnen  →  fertigstellen  →  mergen  →  Zweig weg  →  nächster Zweig
```

- **Ein Zweig ohne Merge ist eine unfertige Aufgabe**, kein Zwischenstand
  zum Liegenlassen. Er gehört auf die Auftragsliste (Kernregel 3), bis er
  durch ist.
- **Neue Arbeit zweigt nie von einem offenen Zweig ab.** Wer das tut,
  hängt zwei unfertige Dinge aneinander; geht das erste nicht durch, ist
  das zweite mit blockiert.
- **Ein gemergter Zweig wird gelöscht.** Fehlt das Recht dazu, wird er
  trotzdem nicht weiterverwendet und in der Fertigmeldung als erledigt
  genannt.
- **Vor jeder Fertigmeldung werden die offenen Zweige berichtet** — Zahl
  und Namen:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/branch-check.py --into dev
```

**Warum das so hart ist:** Fünfzehn offene Zweige, auf denen teilweise
schon dieselben Dateien geändert wurden, lassen sich nicht mehr
zusammenführen — sie lassen sich nur noch einzeln herauspicken
(`cherry-pick`). Danach weiß niemand mehr sicher, was im Baum steht, und
jede Prüfung fängt von vorne an. Der Aufwand dafür ist ein Vielfaches
dessen, was das rechtzeitige Mergen gekostet hätte.

### Modell `dev` — der Regelfall bei NEO und LeoFlex

```
main    ←── nur von dev
 ↑
dev     ←── nur von Arbeitszweigen
 ↑
fix/…, feature/…   ←── von dev abgezweigt
```

- **Kein direkter Push auf `dev`.** Auch keine „winzige Korrektur".
- **Kein Arbeitszweig direkt nach `main`.** `main` nimmt nur `dev`.
- **Kein Merge nach `main` aus irgendetwas anderem als `dev`** — kein
  Hotfix-Zweig, keine Ausnahme für Eiliges. Ein Fehler in der Produktion
  geht denselben Weg: Zweig von `dev`, nach `dev`, dann `dev` → `main`.
- Beide Zweige sind geschützt, beide nehmen nur Pull Requests.

### Modell `main` mit Arbeitszweig — Projekte ohne `dev`

```
main    ←── nur von Arbeitszweigen
 ↑
claude/…, fix/…    ←── von main abgezweigt
```

- **Kein direkter Push auf `main`**, auch hier nicht.
- Der Arbeitszweig wird nach `main` zusammengeführt, sonst nichts.

### Modell `main` direkt

- **Nur, wo der Projektinhaber es ausdrücklich festgelegt hat**, und nur
  für dieses Projekt. Es ist keine Bequemlichkeitsstufe, die man wählt,
  wenn es schnell gehen soll.

### Für alle Modelle

- **Nie Historie umschreiben auf einem Zweig, an dem jemand anderes
  arbeitet** — kein Rebase, kein Amend, kein Force-Push. Auf einem
  eigenen Zweig nur mit `--force-with-lease` und nur, wenn der
  Projektinhaber es weiß.
- **Ein Zweig hat eine Aufgabe.** Zwei Themen in einem Zweig ergeben
  einen Pull Request, den niemand prüfen kann.
- Schutzregeln, Pflichtprüfungen und Ausrollung: Skill `neo-deployment`.

## Die .gitignore

> **Sie gehört zum ersten Commit, nicht zum Aufräumen** (Kernregel 21).

Was einmal eingecheckt ist, bleibt im Verlauf. Ein nachträglicher Eintrag
in der `.gitignore` entfernt nichts — er verhindert nur die nächste
Datei. Deshalb entsteht sie **vor** der ersten Datei, die nicht
hineingehört.

**Vier Gruppen, in jedem Projekt:**

| Gruppe | Beispiele |
| --- | --- |
| Abhängigkeiten | `node_modules/`, `vendor/`, `.venv/`, `Pods/` |
| Bau und Zwischenspeicher | `dist/`, `build/`, `bin/`, `obj/`, `__pycache__/`, `*.pyc`, `.gradle/`, `.dart_tool/` |
| Erzeugnisse der Werkzeuge | Aufnahmen, Unterschiedsbilder, Prüfberichte, Protokolle, Abdeckungsberichte |
| Lokales | `.env*` (außer `.env.example`), `.idea/`, `.vscode/`, `.DS_Store`, `Thumbs.db` |

**Die dritte Gruppe wird am häufigsten vergessen** — und sie ist die, die
tausend Dateien auf einmal erzeugt. Jedes Werkzeug, das schreibt, wird im
selben Schritt eingetragen, in dem es eingeführt wird: der Bildabgleich
schreibt Unterschiedsbilder, der Testlauf schreibt Berichte, der
Übersetzer schreibt Zwischenstände.

- **Erzeugte Dateien, die eingecheckt gehören, sind die Ausnahme** und
  tragen einen Kopf „nicht von Hand ändern" — etwa eine Tokendatei aus
  dem Erzeugungsschritt (Skill `neo-design`).
- **Kein `*` mit Ausnahmenliste.** Eine `.gitignore`, die alles sperrt
  und einzeln wieder freigibt, versteht nach drei Monaten niemand.
- **Vor jedem Commit die Liste der Dateien ansehen**, nicht nur die
  Nachricht schreiben:

```
git status --short
git diff --cached --stat
```

  Fällt dabei etwas auf, das nicht hineingehört: Muster eintragen,
  `git rm --cached` für das bereits Aufgenommene, dann committen.
- **`git add -f` nur mit Grund und Vermerk.**
- Ein Geheimnis, das einmal im Verlauf steht, gilt als kompromittiert und
  wird gewechselt (Kernregel 19, Skill `neo-sicherheit`).

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
- **Nach `dev` merged der Agent selbst**, sobald Tests und CI grün und
  die Review-Befunde erledigt sind — ohne Rückfrage (Kernregel 20). Nach
  `main` merged er nur, wenn der Projektinhaber es verlangt hat.
- **Nach dem Merge wird der Zweig gelöscht**, im selben Arbeitsgang.
