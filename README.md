# NEO-Claude-Plugins

Projektübergreifende Arbeitsregeln der NEO Digital als
Claude-Code-Plugin-Marketplace. Ziel: in jedem Projekt derselbe
Qualitätsstandard — unabhängig von Sprache und Technik.

## Inhalt

| Plugin | Zweck | Wirkung |
| --- | --- | --- |
| `neo-grundregeln` | Arbeitsprozess, Entscheidungshoheit, Belegpflicht, Selbstkontrolle, Tests, Git | Kernregeln laufen über einen SessionStart-Hook in JEDE Sitzung; Vollfassung als Skill; Befehl `/neo-grundregeln:neo-selbstkontrolle` |
| `neo-doku` | Dokumentationsregeln (trocken, IST-Zustand, Zielgruppen, /plan, Umlaute) | Skill, lädt bei Doku-Arbeit |
| `neo-komponenten` | Komponenten-Grundsatz (Neo*, LeoFlex*), Frameworktreue, Design-Tokens | Skill, lädt bei Oberflächenarbeit |
| `neo-sicherheit` | EU-CRA-orientierte Baseline, Secrets, Härtung, Paritätsbetrieb, Release-Evidenz | Skill, lädt bei Sicherheits-, API-, Release-Arbeit |

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
    "neo-doku@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
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
      "source": { "source": "github", "repo": "<owner>/NEO-Claude-Plugins" }
    }
  },
  "enabledPlugins": {
    "neo-grundregeln@neo-claude-plugins": true,
    "neo-doku@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
    "neo-sicherheit@neo-claude-plugins": true
  }
}
```

## Wie die Regeln wirken

- Der SessionStart-Hook lädt die Kernregeln
  (`plugins/neo-grundregeln/rules/kernregeln.md`) beim Sitzungsstart in
  den Kontext — sie gelten immer. Der Hook nutzt `cat` mit dem
  Platzhalter `${CLAUDE_PLUGIN_ROOT}`; Claude Code ersetzt den
  Platzhalter vor der Ausführung und führt Hooks unter Windows über Git
  Bash aus (ohne Git Bash über PowerShell, wo `cat` als Alias für
  Get-Content vorhanden ist).
- Die Skills laden ihre Vollfassung, wenn die Aufgabe passt (Doku-Arbeit,
  Oberflächenarbeit, Sicherheitsarbeit). Projekt-Regeldateien (CLAUDE.md)
  können zusätzlich auf die Skills verweisen.
- Projektspezifische Regelwerke (z. B. NEOcash CLAUDE.md, LeoFlex
  AGENTS.md) bleiben führend, wo sie konkreter sind. Diese Plugins
  liefern den gemeinsamen Unterbau.

## Herkunft

Destilliert aus den Vorgaben von Erich Nigg sowie den Regelwerken der
NEOcash- und LeoFlex-Repos (CLAUDE.md, AGENTS.md, Security-/CRA-Doku,
UI- und Design-System-Regeln). Struktur nach dem Muster der
ITEAS-Claude-Plugins. Ergänzend empfohlen: das ITEAS-Plugin
`ste-writing` (deutscher Schreibstil nach ASD-STE100-Prinzipien samt
Linter) — dieses Repo kopiert es bewusst nicht, sondern setzt auf die
parallele Installation des ITEAS-Marketplace.

## Pflege

- Regeländerung = Textänderung hier + Versionssprung im betroffenen
  `plugin.json` + Commit. Die Regeln dieses Repos gelten auch für dieses
  Repo selbst (echte Umlaute, IST-Zustand, keine Marketingsprache).
- Neue Plugins in `.claude-plugin/marketplace.json` registrieren.
