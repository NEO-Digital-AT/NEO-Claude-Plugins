# Veröffentlichen

Eine Erweiterung lebt in zwei Repositories (Vorgabe des Inhabers vom
12.11.2026):

| Repository | Zweck | Inhalt |
| --- | --- | --- |
| `NEO-Contao-<Name>` (privat) | Entwicklung | alles, was beim Bauen gebraucht wird: `CLAUDE.md`, Entwürfe (`plan/`), Prüfstand (`dev/`), Werkzeuge (`tools/`) |
| `contao-<name>-bundle` (öffentlich) | Auslieferung, Quelle für Packagist | nur das Paket, je Fassung ein Commit `Release <Fassung>` mit Tag `v<Fassung>` |

Gearbeitet wird nur im Entwicklungs-Repository. Das öffentliche wird nie von
Hand geändert, sondern nur mit `release-bundle.py` befüllt.

## Was ins Paket gehört

Was nicht ausgeliefert wird, steht in der `.gitattributes` des
Entwicklungs-Repositorys mit `export-ignore`, zum Beispiel:

```
/CLAUDE.md export-ignore
/.claude export-ignore
/dev export-ignore
/plan export-ignore
/tools export-ignore
/.gitattributes export-ignore
```

`docs/` bleibt: Die Dokumentation gehört zum Paket.

Im öffentlichen Repository steht nichts, das auf das Werkzeug zeigt, mit dem
gebaut wurde: keine Notizen für Agenten, keine Sitzungslinks, keine
Mitautor-Zeilen, keine Entwicklungsgeschichte. Die Release-Commits tragen den
Hersteller als Autor (`NEO Digital <noreply@neo-digital.at>`), keinen
Personennamen und keinen Vermerk eines Werkzeugs.

## `composer.json`

- `name` wie in `aufbau.md` (`neo-digital/contao-<name>-bundle`). Den Namen
  legt `composer.json` fest, nicht das Konto bei Packagist. Den vorderen Teil
  (`neo-digital`) bekommt das Konto, das als Erstes ein Paket damit einreicht.
- **Keine `version`.** Packagist liest die Fassung aus dem Tag. Die ZIP für
  den Contao Manager bekommt sie vom Werkzeug.
- `contao/manager-plugin` unter `require-dev` (`^2.0`), dazu `"conflict":
  {"contao/manager-plugin": "<2.0 || >=3.0"}` (Contao-Doku, Manager Plugin).
- `homepage`, `support.source` und `support.issues` zeigen auf das
  öffentliche Repository.
- Zugesagt wird nur, was getestet ist: keine Contao-Hauptfassung im
  `require`, die es noch nicht gibt.

## `CHANGELOG.md`

Je Fassung ein Abschnitt `## [1.0.0] - JJJJ-MM-TT`. Vor dem Veröffentlichen
ist der Abschnitt „Unreleased“ leer oder fehlt. Die erste öffentliche Fassung
fasst zusammen, was die Erweiterung kann; die Zwischenstände der Entwicklung
gehören nicht hinein.

## Fassungen

Semantische Versionierung: `1.0.0` ist die erste öffentliche Fassung.
Fehlerkorrektur hebt die letzte Stelle, neue Funktionen ohne Bruch die
mittlere, ein Bruch (umbenannte Schalter, entfernte Felder) die erste.

## Ablauf

1. Im Entwicklungs-Repository: Abnahme nach `pruefliste.md`, `CHANGELOG.md`
   mit Datum, Merge nach `main`.
2. Öffentliches Repository lokal klonen, dann:

   ```
   python3 plugins/neo-contao-erweiterung/scripts/release-bundle.py \
     ../NEO-Contao-<Name> --version 1.0.0 --ref origin/main \
     --repo-url https://github.com/<organisation>/contao-<name>-bundle \
     --out ../dist --target ../contao-<name>-bundle \
     --author "NEO Digital <noreply@neo-digital.at>" \
     --forbid "<Vorname>" --forbid "<Nachname>" …
   ```

   Das Werkzeug exportiert den Stand (`git archive`, also ohne nicht
   eingecheckte Änderungen und ohne `export-ignore`), prüft Hinweise,
   `composer.json`, `CHANGELOG.md` und `bundle-check.py`, schreibt die ZIP
   und legt im öffentlichen Klon Commit und Tag an. Es lädt nichts hoch.
   Bei einem Befund entsteht nichts.
3. Hochladen erst nach Freigabe des Inhabers: `git push origin HEAD` und
   `git push origin v<Fassung>` im öffentlichen Klon.
4. Packagist: Der Inhaber reicht das öffentliche Repository einmal ein
   (packagist.org, „Submit“). Ist sein Konto mit GitHub verbunden, kommt
   jede neue Fassung mit ihrem Tag von selbst.

## ZIP für den Contao Manager

Die ZIP enthält nur das Paket, mit `composer.json` im obersten Ordner und
der Fassung darin. Abhängigkeiten, auch Basic, lädt der Contao Manager bei
der Installation von Packagist nach. Darum wird Basic zuerst veröffentlicht.
Vorschläge (`suggest`) wie ein Sprachwechsler kommen nie in die ZIP.

## Im Contao Manager sichtbar

Der Contao Manager findet ein Paket von selbst, sobald es auf Packagist mit
einem Tag liegt, vom Typ `contao-bundle` ist und ein Manager-Plugin nennt.
Titel, Beschreibung je Sprache, Logo und das Ausblenden aus der Suche kommen
über einen Pull Request an `contao/package-metadata`
(`meta/neo-digital/<paket>/<sprache>.yml`, `logo.svg`). Basic bekommt dort
`dependency: true`: Es ist ein Unterbau und soll in der Suche nicht als
eigene Erweiterung erscheinen, und kein Logo.

Die Einträge liegen in der Erweiterung unter `tools/contao-manager/`
(`de.yml`, `en.yml`, `icon.svg`, `logo.svg`), also nicht im Paket. Titel
englisch mit „NEO“ davor. Das Logo erzeugt `module-logo.py` aus dem Icon,
für alle Erweiterungen gleich aufgebaut: `logo.md`.

Der Pull Request an `contao/package-metadata` kommt erst, wenn das Paket
auf Packagist liegt. Dessen Prüfung liest die Texte mit `aspell`; Namen
(NEO, Produktnamen) und richtige deutsche Zusammensetzungen, die das
Wörterbuch nicht kennt, kommen im selben Pull Request in
`linter/allowlists/default.txt` bzw. `linter/allowlists/de.txt`.

## Tests im öffentlichen Repository, nicht beim Kunden

PHPUnit und die Tests braucht nur die Entwicklung. Das öffentliche Repository behält
`tests/`, `phpunit.xml.dist` und `.github/` (dort läuft die CI). `release-bundle.py` trägt
dafür `export-ignore` in die `.gitattributes` des Pakets ein: Das Archiv, das Composer beim
Kunden aus dem öffentlichen Repository lädt, enthält sie nicht, die ZIP für den Contao
Manager auch nicht. PHPUnit steht in `require-dev` und wird beim Kunden nie installiert.
Im Entwicklungs-Repository stehen die Tests deshalb nicht auf `export-ignore`.
