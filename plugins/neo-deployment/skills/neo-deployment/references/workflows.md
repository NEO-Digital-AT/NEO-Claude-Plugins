# Workflow-Gerüste

Zwei Dateien reichen: eine, die prüft und ausrollt, und eine, die die
Herkunft eines Release-Pull-Requests kontrolliert. Die Projektbefehle
(Zeilen mit `# Projektbefehl`) werden durch die tatsächlichen Befehle
des Repositories ersetzt — nicht erfunden, sondern aus dessen Regeldatei
übernommen.

**Der Kern beider Gerüste:** Das Ausrollen hängt am Prüfen (`needs`).
Damit ist „nur Grünes wird ausgerollt" keine Absprache, sondern die
Struktur des Laufs.

## `.github/workflows/ci.yml`

```yaml
name: Prüfen und ausrollen

on:
  pull_request:
  push:
    branches: [dev, main]

# Ein neuer Push auf denselben Zweig bricht den vorigen Lauf ab.
# Bei push auf dev/main NICHT abbrechen — ein halber Rollout ist schlimmer
# als ein doppelter Lauf.
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

permissions:
  contents: read

jobs:
  pruefung:
    name: pruefung
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Reihenfolge nach neo-grundregeln §4:
      # Abhängigkeiten → Lint/Analyse → Tests → Build.
      - name: Abhängigkeiten
        run: echo "# Projektbefehl einsetzen"

      - name: Lint und Analyse
        run: echo "# Projektbefehl einsetzen"

      - name: Tests
        run: echo "# Projektbefehl einsetzen"

      - name: Build
        run: echo "# Projektbefehl einsetzen"

      # Oberflächen-Prüfungen aus dem Skill neo-design gehören hierher:
      # Wächter-Test, Kontrastpaare, kein horizontales Scrollen.
      # contrast.py wird aus dem Plugin neo-design ins Projekt übernommen
      # (tools/contrast.py) — die CI erreicht das Plugin nicht.
      - name: Kontrastpaare
        if: hashFiles('design/contrast-pairs.json') != ''
        run: python3 tools/contrast.py --pairs design/contrast-pairs.json

  ausrollen-entwicklung:
    name: ausrollen-entwicklung
    needs: pruefung
    if: github.event_name == 'push' && github.ref == 'refs/heads/dev'
    runs-on: ubuntu-latest
    environment: entwicklung
    steps:
      - uses: actions/checkout@v4
      - name: Ausrollen
        run: echo "# Projektbefehl einsetzen"

  ausrollen-produktion:
    name: ausrollen-produktion
    needs: pruefung
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: produktion
    steps:
      - uses: actions/checkout@v4
      - name: Ausrollen
        run: echo "# Projektbefehl einsetzen"
```

Als Pflichtprüfung wird `pruefung` eingetragen — der Jobname, nicht der
Dateiname.

## `.github/workflows/zweigherkunft.yml`

Setzt Regel 3 durch: `main` nimmt nur `dev`. GitHub kann das nicht selbst,
deshalb diese Prüfung.

```yaml
name: Zweigherkunft

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  zweigherkunft:
    name: zweigherkunft
    runs-on: ubuntu-latest
    steps:
      - name: Quellzweig prüfen
        env:
          QUELLE: ${{ github.event.pull_request.head.ref }}
          QUELL_REPO: ${{ github.event.pull_request.head.repo.full_name }}
          ZIEL_REPO: ${{ github.repository }}
        run: |
          if [ "$QUELL_REPO" != "$ZIEL_REPO" ]; then
            echo "::error::main nimmt keine Pull Requests aus einer Abspaltung ($QUELL_REPO)."
            exit 1
          fi
          if [ "$QUELLE" != "dev" ]; then
            echo "::error::main nimmt ausschliesslich Merges aus dev. Dieser Pull Request kommt aus '$QUELLE'."
            echo "::error::Der Weg ist: $QUELLE -> dev, danach dev -> main."
            exit 1
          fi
          echo "Quellzweig ist dev."
```

Als Pflichtprüfung für `main` eintragen: `zweigherkunft`.

## Hinweise

- **`pull_request` statt `pull_request_target`.** `pull_request_target`
  läuft mit den Rechten des Ziel-Repositories und hat Zugriff auf
  Secrets — bei fremdem Code ist das eine Übernahme. Nur mit
  ausdrücklicher Freigabe und ohne Auschecken des fremden Standes
  (Skill `neo-sicherheit`).
- **`permissions` immer angeben**, so eng wie möglich. Der Standard eines
  Repositories kann schreibend sein.
- **Aktionen auf eine Version festnageln.** `@v4` ist die Untergrenze;
  wo die Lieferkette streng geprüft wird, auf den Commit-Hash festlegen.
- **Secrets nur an der Umgebung**, nie als Repository-Secret, sonst
  erreicht sie jeder Zweig.
- **Keine Prüfung überspringen, um ein Deployment zu erzwingen.**
  `continue-on-error` an einem Testschritt hebt das Tor auf und ist
  ohne Freigabe verboten.
- **Ein roter Lauf wird nicht durch einen leeren Commit erneut
  angestoßen.** Ursache suchen, beheben, pushen.
