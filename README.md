# NEO-Claude-Plugins

Projektübergreifende Arbeitsregeln der NEO Digital als
Claude-Code-Plugin-Marketplace. Ziel: in jedem Projekt derselbe
Qualitätsstandard — unabhängig von Sprache und Technik.

## Inhalt

| Plugin | Zweck | Wirkung |
| --- | --- | --- |
| `neo-grundregeln` | Arbeitsprozess, Entscheidungshoheit, Belegpflicht, Selbstkontrolle, Debugging, Tests, Oberflächendurchlauf, Git, Projektstart | Kernregeln laufen über einen SessionStart-Hook in JEDE Sitzung; Skill mit acht Referenzdateien; Befehle `/neo-grundregeln:neo-selbstkontrolle` und `/neo-grundregeln:neo-projektstart` |
| `neo-code` | Codeaufbau nach den Vorgaben von .NET 10, Vue 3 und Flutter; Schichten, Benennung, Werkzeuge, Querschnitt, **Lesbarkeit vor Abstraktion**, **Sprache im System: englisch** | Skill mit sechs Referenzdateien, lädt beim Anlegen von Dateien, Klassen, Modulen |
| `neo-php` | PHP und Laravel: API nachschlagen statt erinnern (Laravel Boost), strict_types und volle Typisierung, Enums, Laravel wie gemeint verwendet, kein N+1, Migrationen ohne Datenverlust, statische Analyse als Blocker | Skill mit drei Referenzdateien, lädt bei PHP-Arbeit |
| `neo-vue` | Vue 3, Nuxt, Nuxt UI, Vuetify, Pinia: llms.txt vor dem Schreiben lesen, script setup mit TypeScript, Reaktivität ohne Überraschung, Server-Browser-Grenze in Nuxt, genau eine UI-Bibliothek hinter den Wrappern | Skill mit drei Referenzdateien, lädt bei Vue- und Nuxt-Arbeit |
| `neo-angular` | Angular, Angular Material, Material Design 3: standalone und inject(), Signals gegen RxJS, OnPush, typisierte reaktive Formulare, Theme aus Tokens statt `::ng-deep`, MD3 als System | Skill mit zwei Referenzdateien, lädt bei Angular-Arbeit |
| `neo-mobil` | Flutter und Material 3: kleine Widgets, Ressourcen freigeben, eine Zustandsverwaltung, Größen auf Telefon und Tablet bei jeder Systemschrift, keine Geheimnisse im Paket, Flutter oder nativ als Entscheidung des Inhabers | Skill mit einer Referenzdatei, lädt bei App-Arbeit |
| `neo-design` | Gestaltung und Bedienung in zwei Betriebsarten (Anwendung/Portal, Webseite): Entwurf vor Bau, Bauen nach Claude Design, Abgleich mit dem Designsystem, Eingabeführung, Farbe und Layout, Zustände, Barrierefreiheit, responsive Anwendungen von 320 px bis 4K, Text im Layout, Übersetzungen, Messwerte | Skill mit zwölf Referenzdateien, acht Werkzeugen, Befehle `/neo-design:neo-designumsetzung`, `/neo-design:neo-designabgleich`, `/neo-design:neo-responsivpruefung` und `/neo-design:neo-oberflaechenpruefung` |
| `neo-komponenten` | Komponenten-Grundsatz (Neo*, LeoFlex*), Benennung, Pflichtkatalog, Komponentenvertrag, Größenskala, Wächter-Test, Bestandsbibliotheken | Skill mit fünf Referenzdateien, lädt bei Oberflächenarbeit |
| `neo-api` | Swagger und OpenAPI als Pflicht, Dokumentschnitt, Versionierung, Fehlerhülle, Autorisierung, Betrieb, sechs Pflichttestfälle je Endpunkt | Skill mit drei Referenzdateien, lädt bei Endpoint-, Vertrags- und Betriebsarbeit |
| `neo-doku` | Doku-Struktur, Zielgruppen, Bedienungsdoku mit markierten Screenshots, Entscheidungsakten, Sprache, Vorlagen, Agentenlesbarkeit | Skill mit sieben Referenzdateien und der Markierungsebene für Screenshots |
| `neo-recht` | Impressum, Datenschutz, Barrierefreiheitserklärung, Consent, CRA-Dokumentenpaket | Skill mit vier Referenzdateien, lädt bei Pflichtseiten- und Consent-Arbeit |
| `neo-ki` | KI im Produkt: EU-KI-Verordnung, Offenlegung, Kennzeichnung, Datenweitergabe, Prüfung der Ausgaben | Skill mit zwei Referenzdateien, lädt bei jeder KI-Funktion |
| `neo-assistent` | Bau von KI-Assistenten mit Werkzeugzugriff: Schichten statt großem Prompt, Absichten statt Schlüsselwörter, Schema statt Prosa, Mehrsprachigkeit, Goldfälle und Härtefälle, Modellzugang über Requesty, Modellwahl, Umbau eines gewachsenen Assistenten | Skill mit neun Referenzdateien, drei Werkzeugen, Befehle `/neo-assistent:neo-assistentpruefung`, `/neo-assistent:neo-goldlauf` und `/neo-assistent:neo-haertefaelle` |
| `neo-deployment` | Zweigmodell dev/main, Schutzregeln, Pflichtprüfungen, Ausrollung | Skill mit GitHub-Einstellungen und Workflow-Gerüsten |
| `neo-betrieb` | Sicherung und Wiederherstellung, Notfall, E-Mail-Zustellbarkeit, Umzug und Weiterleitungen | Skill mit vier Referenzdateien, lädt bei Betriebs- und Umzugsarbeit |
| `neo-contao` | Contao-Websites: alles in Contao verwaltbar, Bordmittel, Erweiterungsbau als eigenes Bundle, Themes mit `.cto`-Export, Migrationen ohne Schaden, Betrieb | Skill mit sieben Referenzdateien, lädt bei Contao-Arbeit |
| `neo-sicherheit` | Zehn harte Verbote, Autorisierung und Mandantentrennung, Secrets und Protokolle, hochsensible Daten, Härtung, Lieferkette, Release-Evidenz, Paritätsbetrieb | Skill mit sechs Referenzdateien, lädt bei Sicherheits-, API-, Release-Arbeit |

## Was wo geregelt ist

- **Bevor eine Oberfläche entsteht:** `neo-design` — mehrere Vorschläge,
  Skizze, Änderungsrunden, Freigabe. Erst dann bauen.
- **Beim Bauen der Oberfläche:** `neo-komponenten` — jede Ansicht ruft
  nur `Neo*`- bzw. `LeoFlex*`-Komponenten auf und kennt das
  Designframework nicht.
- **Bevor ein Feld ein Textfeld wird:** `neo-design`,
  `references/eingaben.md` — was nicht eingegeben werden kann, kann nicht
  falsch sein.
- **Wenn ein Entwurf aus Claude Design vorliegt:**
  `/neo-design:neo-designumsetzung` — der Entwurf gibt vor, der Agent
  setzt um und gestaltet nicht. Keine eigene Gestaltungsentscheidung,
  jede Abweichung ist eine Rückfrage mit zwei Bildern nebeneinander.
  Gebaut wird nach Inventar, Element für Element, nach jedem Element
  gemessen. Welche Felder ein Formular hat und welche Werte in einer
  Auswahl stehen, bestimmt dagegen die Fachlichkeit.
- **Wenn eine bestehende Ansicht zu prüfen ist:**
  `/neo-design:neo-designabgleich` — fertig heißt gemessen, nicht
  behauptet. Verglichen wird das Aussehen und das Verhalten, nicht der
  Inhalt: null Abweichungen im Layoutabgleich, null erfundene Werte im
  Stilabgleich.
- **Bevor eine Abstraktion entsteht:** `neo-code`,
  `references/lesbarkeit.md` — der häufigste Fehler in maschinell
  geschriebenem Code ist Überbau. Eine Funktion ab der dritten
  Wiederholung, kein Interface für eine Umsetzung, und von der
  Fehlermeldung in drei Sprüngen zur Ursache.
- **Sobald etwas benannt wird:** `neo-code`, `references/sprache.md` —
  das System spricht englisch, der Mensch deutsch. Eine englische
  Fehlermeldung ist besser als eine deutsche, die es nur auf Deutsch gibt.
- **Sobald es mehr als eine Sprache gibt:** `neo-design`,
  `references/uebersetzungen.md` — jeder Text in jeder Sprache, gemessen
  mit `uebersetzungen.py`. Ein Schlüssel mitten in der Oberfläche ist der
  sichtbarste Mangel, den ein Produkt haben kann.
- **Bevor Code gegen eine Bibliothek entsteht:** ihre `llms.txt` lesen,
  nicht die Signatur erinnern — Nuxt, Nuxt UI, Vue, Vuetify, Angular und
  Flutter liefern eine; Laravel liefert stattdessen Laravel Boost. Die
  Liste mit Prüfdatum steht in `neo-grundregeln`,
  `references/belegpflicht.md`.
- **Bevor für Contao etwas gebaut wird:** `neo-contao` — die Rangfolge
  Bordmittel → fremde Erweiterung → bestehende NEO-Erweiterung →
  bestehende ergänzen → neu, jede Stufe belegt. Zwei Erweiterungen für
  dieselbe Aufgabe sind ein Regelverstoß.
- **Bevor eine Oberfläche als fertig gilt:**
  `/neo-design:neo-responsivpruefung` — acht Breiten, null Befunde. Kein
  waagrechtes Scrollen, nichts ragt hinaus, Tabellen füllen, keine Löcher
  beim Umbrechen, Bedienziele groß genug. Gilt für Anwendungen wie für
  Webseiten.
- **Und weil der Überlauf nur die Hälfte ist:** derselbe Befehl misst mit
  `text-fit.js`, was **innen** nicht passt — abgeschnittener Text,
  Spalten mit zwei Zeichen je Zeile, Umbrüche mitten im Wort. Nichts
  davon erzeugt einen Scrollbalken; alles davon sieht falsch aus.
- **Wenn ein Knopf an zwei Stellen vorkommt:** `neo-grundregeln`,
  `references/durchlauf.md` — er wird an **beiden** geprüft. Ein Element,
  das auf Seite A getestet ist und auf Seite B nicht, bricht auf Seite B.
- **Bevor ein KI-Assistent entsteht oder wächst:** `neo-assistent` —
  ein Assistent ist eine Architektur, kein Prompt. Absichten statt
  Schlüsselwörter, Schema statt Prosa, und keine Änderung an Prompt,
  Werkzeug oder Modell ohne Goldfall-Lauf davor und danach.
- **Bevor ein Assistent abgenommen wird:** `/neo-assistent:neo-haertefaelle`
  — der klare Fall beweist, dass er funktioniert, der Härtefall, dass er
  nicht schadet. Elf Pflichtklassen, je Sprache, schreibende Werkzeuge
  und Einmalgeheimnisse bei 100 Prozent.
- **Bevor eine Farbe gesetzt wird:** Kontrast rechnen, nicht schätzen:

  ```
  python3 plugins/neo-design/scripts/contrast.py "#5A6273" "#FFFFFF"
  python3 plugins/neo-design/scripts/contrast.py --pairs design/contrast-pairs.json
  ```

- **Beim Dokumentieren:** `neo-doku` — feste Struktur
  `docs/[frontend|backend]/<sprache>/…`, `README.md` als
  Inhaltsverzeichnis je Ordner, Screenshots mit Markierungen im
  Repository.
- **Beim Zweig- und Ausrollen:** `neo-deployment` — nie direkt auf `dev`
  oder `main`, `main` nimmt nur `dev`, nur Grünes wird ausgerollt.
- **Bevor eine Datei, Klasse oder Komponente entsteht:** `neo-code` —
  es gilt, was der Stack offiziell vorgibt, damit ein fremder Entwickler
  sich sofort zurechtfindet.
- **Bevor ein Endpoint entsteht:** `neo-api` — OpenAPI ist Pflicht, eine
  Fehlerhülle für alles, Autorisierung deny-by-default.
- **Bei Contao:** `neo-contao` — die Seite muss wirken, als wäre sie rein
  in Contao entstanden; Styles ausnahmslos SCSS, im Layout gewählt.
- **Vor jeder Fertigmeldung einer Webseite:** `neo-recht` — Impressum,
  Datenschutz, Barrierefreiheitserklärung, und im Netzwerkmitschnitt
  kein fremder Host vor der Einwilligung.
- **Bevor ein Repo entsteht:** `/neo-grundregeln:neo-projektstart` — was
  am ersten Tag fehlt, fehlt in zwei Jahren immer noch.
- **Bei jeder KI-Funktion:** `neo-ki` — der Assistent gibt sich zu
  erkennen, seit 02.08.2026 verbindlich.
- **Vor dem Livegang:** `neo-betrieb` — eine Sicherung gilt erst, wenn
  eine Wiederherstellung protokolliert ist.
- **Vor jeder Neuauflage einer Website:** `neo-betrieb`,
  `references/relaunch.md` — alte Adressen erheben, bevor umgebaut wird.
- **Vor der Abnahme:** mobil messen. Best Practices und SEO 100,
  agentisches Browsen 3/3, Leistung und Barrierefreiheit mindestens 95.

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
    "neo-code@neo-claude-plugins": true,
    "neo-php@neo-claude-plugins": true,
    "neo-vue@neo-claude-plugins": true,
    "neo-angular@neo-claude-plugins": true,
    "neo-mobil@neo-claude-plugins": true,
    "neo-design@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
    "neo-api@neo-claude-plugins": true,
    "neo-doku@neo-claude-plugins": true,
    "neo-recht@neo-claude-plugins": true,
    "neo-ki@neo-claude-plugins": true,
    "neo-assistent@neo-claude-plugins": true,
    "neo-deployment@neo-claude-plugins": true,
    "neo-betrieb@neo-claude-plugins": true,
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
    "neo-code@neo-claude-plugins": true,
    "neo-php@neo-claude-plugins": true,
    "neo-vue@neo-claude-plugins": true,
    "neo-angular@neo-claude-plugins": true,
    "neo-mobil@neo-claude-plugins": true,
    "neo-design@neo-claude-plugins": true,
    "neo-komponenten@neo-claude-plugins": true,
    "neo-api@neo-claude-plugins": true,
    "neo-doku@neo-claude-plugins": true,
    "neo-recht@neo-claude-plugins": true,
    "neo-ki@neo-claude-plugins": true,
    "neo-assistent@neo-claude-plugins": true,
    "neo-deployment@neo-claude-plugins": true,
    "neo-betrieb@neo-claude-plugins": true,
    "neo-contao@neo-claude-plugins": true,
    "neo-sicherheit@neo-claude-plugins": true
  }
}
```

`neo-contao`, `neo-deployment` und `neo-ki` dürfen in Projekten
weggelassen werden, die weder Contao einsetzen noch ein Zweigmodell mit
`dev` und `main` führen noch KI verwenden. `neo-recht` und `neo-betrieb`
bleiben aktiv, sobald etwas veröffentlicht oder betrieben wird.

## Werkzeuge in den Plugins

| Werkzeug | Wo | Wofür |
| --- | --- | --- |
| `contrast.py` | `plugins/neo-design/scripts/` | Kontrastverhältnis nach WCAG 2.2 rechnen und prüfen, einzeln oder als Paardatei in der CI. Kennt durchsichtige Farben und rechnet sie über ihren Grund zusammen. Ohne Abhängigkeiten. |
| `layoutabgleich.js` | `plugins/neo-design/scripts/` | Misst Geometrie und Aussehen jedes markierten Elements — Breite, Höhe, Position, Polster, Randstärken, Lücken, Radien, Schriftmaße — und vergleicht Entwurf gegen gebaute Ansicht. **Liest den Inhalt der Felder nicht**, ist also blind für dynamische Werte. Statische Texte auf Ansage zuschaltbar. |
| `overflow.js` | `plugins/neo-design/scripts/` | Misst je Prüfbreite, was nicht in den Bildschirm passt: waagrechtes Scrollen, Elemente über dem Rand, Inhalt breiter als sein Platz, Tabellen unter der Inhaltsbreite, zu kleine Bedienziele und **Löcher in umgebrochenen Reihen** — drei Kacheln, die auf zwei Spalten umbrechen und eine halbe Reihe frei lassen. Framework-unabhängig am fertigen DOM. |
| `uebersetzungen.py` | `plugins/neo-design/scripts/` | Vergleicht die Sprachdateien gegen die Leitsprache und meldet fehlende Schlüssel, leere Werte, **abweichende Platzhalter** (der gefährlichste Fall: die Meldung bricht oder lässt eine Lücke im Satz), fehlende Pluralformen, unübersetzt Gebliebenes, verwaiste und tote Schlüssel. Liest JSON, ARB, PHP-Rückgabe-Arrays und flaches YAML; was es nicht sicher lesen kann, meldet es. Ohne Abhängigkeiten. |
| `text-fit.js` | `plugins/neo-design/scripts/` | Prüft, ob der Text in seinen Bereich passt — der Gegenspieler zum Überlauf, denn nichts davon erzeugt einen Scrollbalken: waagrecht und senkrecht abgeschnittener Text, Kürzung ohne erreichbaren Volltext, überlappende Texte, Bereiche unter acht Zeichen je Zeile, Umbruch mitten im Wort, `hyphens: auto` ohne `lang` und zu kleine Schrift. |
| `bildabgleich.py` | `plugins/neo-design/scripts/` | Vergleicht zwei PNG-Aufnahmen — Entwurf gegen gebaute Oberfläche — nennt die Abweichung in Prozent und schreibt ein Unterschiedsbild, das jede abweichende Stelle magenta markiert. Bereiche mit veränderlichem Inhalt lassen sich ausnehmen. Ohne Abhängigkeiten. |
| `style-audit.js` | `plugins/neo-design/scripts/` | Liest die berechneten Stile der laufenden Oberfläche und meldet jede Farbe, jeden Radius, jede Schriftgröße und jeden Schatten, der nicht aus den Tokens stammt. Arbeitet am fertigen DOM und damit unabhängig vom Framework. |
| `comparison.js` | `plugins/neo-design/scripts/` | Stellt für eine Rückfrage zwei Aufnahmen nebeneinander — links die Vorgabe aus dem Designsystem, rechts der Vorschlag — mit Titeln, Maßen und Hinweisfeld. Meldet ein nicht geladenes Bild sichtbar, statt eine leere Gegenüberstellung auszuliefern. |
| `goldlauf.py` | `plugins/neo-assistent/scripts/` | Führt Goldfälle gegen einen laufenden KI-Assistenten aus und prüft, ob er die richtigen Werkzeuge mit den richtigen Argumenten aufruft. Läuft jeden Fall mehrfach, weil ein Modell nicht deterministisch antwortet, und wertet nach Sprache und Absicht aus. Kennt keinen Anbieter — er ruft einen Adapter des Projekts. Ohne Abhängigkeiten. |
| `requesty_adapter.py` | `plugins/neo-assistent/scripts/` | Verbindet den Goldfall-Prüfer mit dem Requesty-EU-Router. Fährt einen Fall gegen das echte Modell, zeichnet jeden Werkzeugaufruf auf, **ohne ihn auszuführen**, und prüft die Argumente gegen das Schema. Schlüssel nur aus `REQUESTY_API_KEY`; warnt, wenn Router oder Modellkennung die Verarbeitung aus der EU führen. Ohne Abhängigkeiten. |
| `promptinventar.py` | `plugins/neo-assistent/scripts/` | Vermisst einen gewachsenen Systemprompt und meldet Schlüsselwort-Verzweigung, Schemata in der Prosa, wortgleiche Wiederholungen und zu große Abschnitte, jeweils mit Zeilennummer. Zählt und findet Muster; es urteilt nicht. Ohne Abhängigkeiten. |
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
  AGENTS.md) bleiben führend, wo sie konkreter
  sind. Diese Plugins liefern den gemeinsamen Unterbau.

## Herkunft

Destilliert aus den Vorgaben von Erich Nigg sowie den Regelwerken der
NEOcash-, LeoFlex-, Website- und weiterer Anwendungs-Repos (CLAUDE.md, AGENTS.md,
Security-/CRA-Doku, UI- und Design-System-Regeln, ADRs, Wächter-Tests,
Standardprompt Contao). Aufbau nach dem Standardmuster für
Claude-Code-Marketplaces: ein Repo, ein Marketplace-Manifest, je Plugin
ein eigener Ordner.

## Ausnahmen für dieses Repo

Die Regeln dieses Repos gelten auch für dieses Repo — mit einer
festgehaltenen Ausnahme:

- **Kein `dev`-Zweig** (Kernregel 16, Skill `neo-deployment`). Dieses
  Repo rollt nichts aus und hält nur Regeltexte; ein Integrationszweig
  ohne Ausrollung brächte einen Schritt ohne Nutzen. Entschieden vom
  Projektinhaber am 26.08.2026. Arbeit läuft weiterhin über Zweige und
  Pull Requests gegen `main`.

## Aufbau der Plugins

Alle siebzehn folgen demselben Muster:

- **`SKILL.md`** — Wegweiser: die Lesekonvention, die harten Regeln, eine
  Tabelle der Bereiche. 100 bis 180 Zeilen, damit sie ganz gelesen wird.
- **`references/*.md`** — die Tiefe, erst bei Bedarf gelesen. Je Plugin
  zwei bis neun Dateien.
- **`references/pruefliste.md`** — die Abnahmeliste, wo es eine gibt.
  Abhakbar, mit dem Satz „Nicht Geprüftes gilt als nicht erfüllt".
- **`scripts/`** — Werkzeuge, wo eine Regel messbar ist.
- **`commands/`** — Befehle, wo eine Prüfung wiederkehrt.

**Die Beispiele sind projektneutral.** Wo ein Beispiel einen fachlichen
Gegenstand braucht, steht ein Platzhalter — `Auftrag`, `Account`,
`Invoice`, dazu ein Platzhaltersatz Farben. Kein Beispiel beschreibt ein
bestimmtes NEO-Projekt, und keines ist als Vorgabe für ein Datenmodell,
eine Farbe oder eine Fachlichkeit zu lesen. Übernommen wird die **Form**,
nicht der Inhalt.

Die Lesekonvention ist in allen Skills dieselbe:

| Wort | Bedeutung |
| --- | --- |
| **Nie**, **immer**, **muss** | Verbindlich. Ein Verstoß ist ein Blocker. |
| **Ausnahme** | Nur mit dokumentierter Freigabe, mit Grund und Datum. Ohne Vermerk gibt es keine. |
| **Sollte** | Begründet abweichbar, die Abweichung wird gemeldet. |

## Pflege

- Regeländerung = Textänderung hier + Versionssprung im betroffenen
  `plugin.json` + Commit. Die Regeln dieses Repos gelten auch für dieses
  Repo selbst (echte Umlaute, IST-Zustand, keine Marketingsprache).
- Neue Plugins in `.claude-plugin/marketplace.json` registrieren.
- Eine Regel gehört in genau ein Plugin. Wo zwei Plugins dieselbe Sache
  berühren, verweist das eine auf das andere, statt sie zu wiederholen.
