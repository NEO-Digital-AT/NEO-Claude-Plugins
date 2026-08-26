# NEO-Claude-Plugins

Projektübergreifende Arbeitsregeln der NEO Digital als
Claude-Code-Plugin-Marketplace. Ziel: in jedem Projekt derselbe
Qualitätsstandard — unabhängig von Sprache und Technik.

## Inhalt

| Plugin | Zweck | Wirkung |
| --- | --- | --- |
| `neo-grundregeln` | Arbeitsprozess, Entscheidungshoheit, Belegpflicht, Selbstkontrolle, Tests, Git | Kernregeln laufen über einen SessionStart-Hook in JEDE Sitzung; Vollfassung als Skill; Befehl `/neo-grundregeln:neo-selbstkontrolle` |
| `neo-design` | Gestaltung und Bedienung: Entwurf vor Bau, Aufbau, Eingabeführung, Farbe und Layout, Zustände, Barrierefreiheit, 320 px bis 4K | Skill mit sechs Referenzdateien, Kontrastrechner, Befehl `/neo-design:neo-oberflaechenpruefung` |
| `neo-komponenten` | Komponenten-Grundsatz (Neo*, LeoFlex*), Benennung, Pflichtkatalog, Größenskala, Frameworktreue | Skill mit Katalog-Referenz, lädt bei Oberflächenarbeit |
| `neo-doku` | Doku-Struktur, Zielgruppen, Bedienungsdoku mit markierten Screenshots, Agentenlesbarkeit | Skill mit drei Referenzdateien und der Markierungsebene für Screenshots |
| `neo-deployment` | Zweigmodell dev/main, Schutzregeln, Pflichtprüfungen, Ausrollung | Skill mit GitHub-Einstellungen und Workflow-Gerüsten |
| `neo-contao` | Contao-Websites: alles in Contao verwaltbar, Bordmittel, Erweiterungen, Betrieb | Skill mit drei Referenzdateien, lädt bei Contao-Arbeit |
| `neo-sicherheit` | EU-CRA-orientierte Baseline, Secrets, Härtung, Paritätsbetrieb, Release-Evidenz | Skill, lädt bei Sicherheits-, API-, Release-Arbeit |

## Was wo geregelt ist

- **Bevor eine Oberfläche entsteht:** `neo-design` — mehrere Vorschläge,
  Skizze, Änderungsrunden, Freigabe. Erst dann bauen.
- **Beim Bauen der Oberfläche:** `neo-komponenten` — jede Ansicht ruft
  nur `Neo*`- bzw. `LeoFlex*`-Komponenten auf und kennt das
  Designframework nicht.
- **Bevor ein Feld ein Textfeld wird:** `neo-design`,
  `references/eingaben.md` — was nicht eingegeben werden kann, kann nicht
  falsch sein.
- **Bevor eine Farbe gesetzt wird:** Kontrast rechnen, nicht schätzen:

  ```
  python3 plugins/neo-design/scripts/kontrast.py "#5C5470" "#FFFFFF"
  python3 plugins/neo-design/scripts/kontrast.py --paare design/kontrastpaare.json
  ```

- **Beim Dokumentieren:** `neo-doku` — feste Struktur
  `docs/[frontend|backend]/<sprache>/…`, `README.md` als
  Inhaltsverzeichnis je Ordner, Screenshots mit Markierungen im
  Repository.
- **Beim Zweig- und Ausrollen:** `neo-deployment` — nie direkt auf `dev`
  oder `main`, `main` nimmt nur `dev`, nur Grünes wird ausgerollt.
- **Bei Contao:** `neo-contao` — die Seite muss wirken, als wäre sie rein
  in Contao entstanden.

## Installation

Lokal (CLI und VS-Code-Erweiterung), gilt für alle Projekte des Nutzers:

```
claude plugin marketplace add C:\Entwicklung\neo-digital-at\NEO-Claude-Plugins
```

Danach die Plugins aktivieren — entweder über `/plugin` oder in
`~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "neo-grundregeln@neo-claude-plugins": true,
    "neo-design@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
    "neo-doku@neo-claude-plugins": true,
    "neo-deployment@neo-claude-plugins": true,
    "neo-contao@neo-claude-plugins": true,
    "neo-sicherheit@neo-claude-plugins": true
  }
}
```

Für Claude Code im Web (claude.ai/code) und für Team-Nutzung muss das
Repo auf GitHub liegen (privat reicht). Dann je Projekt in
`.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "neo-claude-plugins": {
      "source": { "source": "github", "repo": "NEO-Digital-AT/NEO-Claude-Plugins" }
    }
  },
  "enabledPlugins": {
    "neo-grundregeln@neo-claude-plugins": true,
    "neo-design@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
    "neo-doku@neo-claude-plugins": true,
    "neo-deployment@neo-claude-plugins": true,
    "neo-contao@neo-claude-plugins": true,
    "neo-sicherheit@neo-claude-plugins": true
  }
}
```

`neo-contao` und `neo-deployment` dürfen in Projekten weggelassen werden,
die weder Contao einsetzen noch ein Zweigmodell mit `dev` und `main`
führen.

## Werkzeuge in den Plugins

| Werkzeug | Wo | Wofür |
| --- | --- | --- |
| `kontrast.py` | `plugins/neo-design/scripts/` | Kontrastverhältnis nach WCAG 2.2 rechnen und prüfen, einzeln oder als Paardatei in der CI. Kennt durchsichtige Farben und rechnet sie über ihren Grund zusammen. Ohne Abhängigkeiten. |
| `markierung.js` | `plugins/neo-doku/scripts/` | Markierungsebene für Doku-Screenshots: Rahmen, Pfeile, Nummern, Infokästen, Textmarker, Scheinwerfer. Wird vor der Aufnahme in die Seite eingeblendet und mitfotografiert. |

## Wie die Regeln wirken

- Der SessionStart-Hook lädt die Kernregeln
  (`plugins/neo-grundregeln/rules/kernregeln.md`) beim Sitzungsstart in
  den Kontext — sie gelten immer. Der Hook nutzt `cat` mit dem
  Platzhalter `${CLAUDE_PLUGIN_ROOT}`; Claude Code ersetzt den
  Platzhalter vor der Ausführung und führt Hooks unter Windows über Git
  Bash aus (ohne Git Bash über PowerShell, wo `cat` als Alias für
  Get-Content vorhanden ist).
- Die Skills laden ihre Vollfassung, wenn die Aufgabe passt
  (Oberflächenarbeit, Doku-Arbeit, Zweigarbeit, Contao-Arbeit,
  Sicherheitsarbeit). Die Referenzdateien unter `references/` liest der
  Agent erst, wenn er sie braucht — so bleibt die Kernfassung kurz.
- Projekt-Regeldateien (CLAUDE.md) können zusätzlich auf die Skills
  verweisen.
- Projektspezifische Regelwerke (z. B. NEOcash CLAUDE.md, LeoFlex
  AGENTS.md, NEO Uptime CLAUDE.md) bleiben führend, wo sie konkreter
  sind. Diese Plugins liefern den gemeinsamen Unterbau.

## Herkunft

Destilliert aus den Vorgaben von Erich Nigg sowie den Regelwerken der
NEOcash-, LeoFlex-, NEO-Uptime- und Website-Repos (CLAUDE.md, AGENTS.md,
Security-/CRA-Doku, UI- und Design-System-Regeln, ADRs, Wächter-Tests,
Standardprompt Contao). Aufbau nach dem Standardmuster für
Claude-Code-Marketplaces: ein Repo, ein Marketplace-Manifest, je Plugin
ein eigener Ordner.

## Pflege

- Regeländerung = Textänderung hier + Versionssprung im betroffenen
  `plugin.json` + Commit. Die Regeln dieses Repos gelten auch für dieses
  Repo selbst (echte Umlaute, IST-Zustand, keine Marketingsprache).
- Neue Plugins in `.claude-plugin/marketplace.json` registrieren.
- Eine Regel gehört in genau ein Plugin. Wo zwei Plugins dieselbe Sache
  berühren, verweist das eine auf das andere, statt sie zu wiederholen.
