# Eine Contao-Erweiterung bauen

Lesekonvention siehe `SKILL.md`. Auswahl fremder Erweiterungen und die
Frage, ob überhaupt eine eigene entsteht: `erweiterungen.md`.

> **Alles, was für Contao gebaut wird, ist eine eigene Erweiterung in
> einem eigenen Repository.** Kein Code im Projektordner, der auch
> anderswo gebraucht werden könnte.

Der Grund ist nicht Ordnungsliebe: eine Funktion, die im Projekt liegt,
ist beim nächsten Kunden weg. Eine Erweiterung ist beim nächsten Kunden
ein Composer-Eintrag.

## Die Rangfolge vor der ersten Zeile

**In dieser Reihenfolge, und jede Stufe wird belegt, bevor die nächste
kommt:**

1. **Gibt es eine Bordmittel-Lösung?** Contao kann mehr, als es auf den
   ersten Blick zeigt (`bordmittel.md`).
2. **Gibt es eine fremde Erweiterung?** <https://extensions.contao.org>,
   Packagist, die Repositories von terminal42, netzmacht, MetaModels.
   Gefunden heißt vorgelegt, nicht eingebaut (`erweiterungen.md`).
3. **Gibt es eine eigene NEO-Erweiterung, die das schon kann?** Dann
   **wird sie verwendet**, nicht eine zweite gebaut.
4. **Gibt es eine, der nur etwas fehlt?** Dann **wird sie erweitert** —
   siehe unten. Eine zweite Erweiterung für dieselbe Aufgabe ist ein
   Regelverstoß.
5. **Erst dann eine neue** — nach Freigabe.

**Eine neue Erweiterung ohne Beleg für die Stufen 1 bis 4 wird nicht
gebaut.** Der Beleg steht in der Entscheidungsakte (Skill `neo-doku`).

## Eine bestehende Erweiterung erweitern

Der Normalfall, und der mit der wichtigsten Regel:

> **Die Erweiterung wird so ergänzt, dass jede bestehende Installation
> sie aktualisieren kann, ohne dass sich für sie etwas ändert.**

- **Neue Felder sind optional** und haben einen Standardwert, der das
  bisherige Verhalten erhält.
- **Kein Feld wird umbenannt oder entfernt**, solange eine Installation
  es nutzen könnte. Was weg soll, wird zuerst als veraltet markiert und
  in einer späteren Hauptversion entfernt.
- **Kein Standardwert wird geändert**, ohne dass eine Migration den alten
  Wert für bestehende Datensätze festschreibt.
- **Keine Pflicht wird nachträglich eingeführt.** Ein Feld, das gestern
  leer sein durfte, darf es heute auch.
- **Kein Template wird umbenannt**, ohne dass das alte weiter funktioniert.
- **Semantische Versionierung**, und sie wird eingehalten: neue Funktion
  = Minor, Verhaltensänderung = Major, Behebung = Patch.
- **Änderungsprotokoll je Fassung**, aus Sicht dessen, der aktualisiert
  (Skill `neo-doku`, `references/vorlagen.md`).

**Wer eine Erweiterung erweitert, arbeitet für alle Installationen.** Das
ist der Zweck der Regel: Ein Kunde bezahlt die Ergänzung, alle anderen
bekommen sie beim nächsten Update — und keiner von ihnen merkt etwas
Negatives davon.

## Aufbau

Nach dem offiziellen Weg für Contao 5. Belege am Ende dieses Textes.

```
Contao-Beispiel-by-NEO/
  composer.json
  src/
    ContaoBeispielBundle.php          Bundle-Klasse
    ContaoManager/Plugin.php          Managed Edition
    Controller/ContentElement/        Inhaltselemente
    Controller/FrontendModule/        Frontend-Module
    EventListener/                    Hooks und Callbacks
    Migration/                        Datenbank-Migrationen
    Model/                            Models
  config/
    services.yaml                     Dienste, autowire + autoconfigure
    routes.yaml                       Routen, wo nötig
  contao/
    dca/tl_neo_beispiel.php           Datenstruktur und Backend-Maske
    languages/de/…                    Übersetzungen
    languages/en/…                    Übersetzungen
    templates/                        Templates der Erweiterung
    config/config.php                 nur, was Dienste-Tags nicht können
  public/                             ausgelieferte Assets
  tests/                              Unit- und Funktionstests
  docs/                               Dokumentation, siehe unten
  README.md
  CHANGELOG.md
  LICENSE
```

**composer.json — die vier Pflichtangaben:**

```json
{
  "name": "neo/beispiel-bundle",
  "type": "contao-bundle",
  "require": { "php": "^8.2", "contao/core-bundle": "^5.3" },
  "autoload": { "psr-4": { "Neo\\ContaoBeispielBundle\\": "src/" } },
  "extra": {
    "contao-manager-plugin": "Neo\\ContaoBeispielBundle\\ContaoManager\\Plugin"
  }
}
```

- **`type` ist `contao-bundle`.** Ohne diesen Typ findet der Contao
  Manager die Erweiterung nicht.
- **Der Manager-Plugin-Eintrag ist Pflicht** für die Managed Edition;
  die Klasse setzt die Ladereihenfolge nach dem Core-Bundle.
- **Versionsbereiche mit `^`**, nie ein festgenagelter Punkt: eine
  Erweiterung, die genau eine Contao-Fassung erlaubt, blockiert jedes
  Update ihrer Installationen.
- Fremde Abhängigkeiten sparsam. Jede ist eine, die der Kunde
  mitaktualisieren muss.

**Namen, verbindlich:**

| Was | Regel | Beispiel |
| --- | --- | --- |
| Repository | `Contao-<Name>-by-NEO` | `Contao-Terminplaner-by-NEO` |
| Composer-Paket | `neo/<name>-bundle`, Kleinbuchstaben | `neo/terminplaner-bundle` |
| Namensraum | `Neo\Contao<Name>Bundle` | `Neo\ContaoTerminplanerBundle` |
| Tabellen | `tl_neo_<name>` | `tl_neo_termin` |
| Templates | eigener Präfix | `ce_neo_termin`, `mod_neo_termin` |
| Dienste | Namensraum, kein Alias-Wildwuchs | — |

## Registrieren über Dienste-Tags, nicht über config.php

Contao 5 registriert Inhaltselemente, Frontend-Module, Hooks, Callbacks
und Cronjobs über **Dienste-Tags bzw. Attribute**. `config.php` bleibt
für das, was anders nicht geht.

- `autowire: true`, `autoconfigure: true` in `config/services.yaml`.
- Ein Inhaltselement ist eine Controller-Klasse mit Attribut, kein
  Eintrag in einem Array.
- **Kein Zugriff auf `$GLOBALS`, wo es einen Dienst gibt.**

## Datenbank: Änderungen ohne Schaden

Die Struktur steht in der DCA (`'sql' => …`); der Abgleich erzeugt daraus
die Tabellen. **Alles, was der Abgleich nicht kann, ist eine Migration.**

Eine Migration ist ein Dienst mit dem Tag `contao.migration`, der
`MigrationInterface` erfüllt — meist über `AbstractMigration`:

| Methode | Aufgabe |
| --- | --- |
| `getName()` | Ein Satz, den ein Mensch im Install-Tool liest |
| `shouldRun()` | Läuft diese Migration noch? |
| `run()` | Führt sie aus, gibt ein `MigrationResult` zurück |

**Regeln, die daraus folgen:**

- **`shouldRun()` wird defensiv geschrieben.** Die Anwendung kann in
  jedem Zustand sein: Tabelle fehlt, Spalte fehlt schon, Migration lief
  bereits, halb gelaufen. Jeder dieser Fälle wird geprüft, bevor
  irgendetwas angefasst wird.
- **Eine Migration ist wiederholbar**, ohne Schaden anzurichten. Sie
  läuft im Zweifel zweimal.
- **Kein Datenverlust.** Eine Spalte wird gefüllt, nicht ersetzt; ein
  Feld wird ergänzt, nicht umgewidmet. Wo etwas wirklich weg muss, geht
  eine Fassung mit Warnung voraus.
- **Eine Ausnahme in `run()` bricht den ganzen Vorgang ab.** Also: prüfen
  statt hoffen, und einen sprechenden Fehler werfen.
- **Nie ein Neuaufbau der Datenbank.** Es ändert sich, was sich ändern
  muss — Kundeninhalte überleben jedes Update (`betrieb.md`).
- **Getestet gegen eine Kopie eines echten Bestands**, nicht gegen eine
  leere Datenbank. Eine leere Datenbank besteht jede Migration.

## Mehrsprachig und mandantenfähig von Anfang an

- **Kein fester Text im Code oder im Template.** Alles über die
  Sprachdateien; im Frontend über Felder und Insert-Tags (`SKILL.md`).
- **Deutsch und Englisch** liegen bei, weitere Sprachen sind vorgesehen.
- Die Doku der Erweiterung ist **englisch** (Pflicht), deutsch optional
  (Skill `neo-doku`, `references/sprache.md`).
- Keine Projekt-Spezifika: was ein anderes Projekt anders braucht, ist
  ein **Einstellungsfeld** — Route statt fester Adresse, Auswahl statt
  eingebauter Firmenregel, Imageset statt fester Maße.

## Tests

- **Unit-Tests** für die Fachlogik, mit `contao/test-case`.
- **Funktionale Tests** für Inhaltselemente und Module: gerendert und
  auf das Ergebnis geprüft, nicht auf den Aufruf.
- **Migrationstests**: `shouldRun()` in jedem Zustand, `run()` zweimal
  hintereinander.
- Die allgemeinen Testregeln gelten (Skill `neo-grundregeln`,
  `references/tests.md`), einschließlich Oberflächendurchlauf für alles
  mit Backend-Maske (`references/durchlauf.md`).

## Was im Paket mitgeliefert wird

**Eine Erweiterung ohne Dokumentation ist nicht fertig.** Sie liegt im
Paket, nicht in einem Wiki, das der nächste nicht findet.

```
docs/
  en/
    README.md          Inhaltsverzeichnis
    installation.md    Voraussetzungen, Installation, Konfiguration
    usage.md           Bedienung im Backend, mit Screenshots
    fields.md          Jedes Feld: Bedeutung, Wertebereich, Wirkung
    upgrading.md       Was sich je Fassung ändert, was zu tun ist
    troubleshooting.md Häufige Fehler und was dann zu tun ist
  de/                  optional, gleiche Dateinamen
```

- Aufbau, Kopfdaten und Agentenlesbarkeit nach Skill `neo-doku`.
- **Screenshots der Backend-Maske** mit Markierungen, eingecheckt
  (`references/screenshots.md`).
- `README.md` im Wurzelverzeichnis: was die Erweiterung tut, welche
  Contao- und PHP-Fassungen, wie installiert, Verweis auf `docs/`.
- `CHANGELOG.md` je Fassung, aus Sicht dessen, der aktualisiert.

## Veröffentlichen

- Eigenes Repository, Zweigmodell nach Skill `neo-deployment`.
- Tests, Lint und Codestil laufen in der CI, bevor eine Fassung
  entsteht.
- Fassungen werden **getaggt**; ein Tag ohne grüne CI entsteht nicht.
- Ob die Erweiterung öffentlich auf Packagist geht, entscheidet der
  Projektinhaber — nicht der Agent.

## Belege

- Erweiterung anlegen, `type: contao-bundle`, PSR-4, Manager-Plugin:
  <https://docs.contao.org/5.x/dev/getting-started/extension/>
- Migrationen, `MigrationInterface`, `shouldRun()` defensiv,
  `AbstractMigration`, Tag `contao.migration`:
  <https://docs.contao.org/5.x/dev/framework/migrations/>
- Dienste-Tags für Hooks, Inhaltselemente, Module, Cronjobs und
  DCA-Callbacks:
  <https://docs.contao.org/5.x/dev/getting-started/starting-development/>
- Manager-Plugin:
  <https://docs.contao.org/5.x/dev/framework/manager-plugin/>
- Aufbau in der Praxis: die Bundles von terminal42, netzmacht und
  MetaModels auf GitHub.

Stand der Prüfung: 2026-08. **Vor dem Verlassen auf eine dieser Angaben
nachsehen** (Skill `neo-grundregeln`, Belegpflicht).
