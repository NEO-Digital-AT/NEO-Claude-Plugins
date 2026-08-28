---
name: neo-php
description: >
  NEO-Regeln für PHP und Laravel. Diesen Skill laden, sobald PHP-Code
  entsteht oder geändert wird: Laravel-Anwendung, Artisan-Befehl,
  Eloquent-Modell, Migration, Queue-Job, Event, Middleware, Blade oder
  Livewire, Formularanfrage, Policy, Ressource, Dienst, Repository.
  Ebenso bei Symfony-Anteilen — etwa in einem Contao-Bundle —, bei
  Composer, PSR-Standards, statischer Analyse, Pest oder PHPUnit, bei
  Fragen zu Typen, strict_types, Enums und readonly, zu Eloquent gegen
  Query Builder, N+1, Transaktionen, Warteschlangen, geplanten Aufgaben,
  Caching, Dateiablage und Mail. Ebenso bei der Frage, wie Laravel
  aktuell etwas macht — dann wird nachgeschlagen, nicht erinnert.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# PHP und Laravel

Lesekonvention siehe `README.md` des Regel-Repositorys.

**PHP ist bei NEO gesetzt, Laravel der Regelfall.** Symfony kommt dort
vor, wo Contao es mitbringt (Skill `neo-contao`). Schichten, Benennung
und Querschnittsthemen stehen im Skill `neo-code` und gelten zusätzlich.

## Der Satz vorweg

> **Die API wird nachgeschlagen, nicht erinnert.**

Laravel ändert sich schneller, als ein Modell trainiert wird. Eine
erinnerte Signatur ist eine Vermutung mit gutem Ruf.

**Für Laravel gibt es keine `llms.txt` — der Hersteller liefert
stattdessen Laravel Boost**: einen MCP-Server mit Werkzeugen für die
eigene Anwendung, mitgelieferten KI-Richtlinien und einer
Dokumentations-Schnittstelle. **Wo Boost verfügbar ist, ist es die
Quelle.** Wo nicht, die offizielle Dokumentation der eingesetzten Fassung
— nicht die einer anderen (Skill `neo-grundregeln`, Belegpflicht).

## 1. Die Sprache wird ausgereizt

PHP kann seit Jahren mehr, als in den meisten Projekten benutzt wird.
Was möglich ist, wird verwendet:

- **`declare(strict_types=1)` in jeder Datei.** Ohne Ausnahme.
- **Alles typisiert**: Parameter, Rückgabewerte, Eigenschaften,
  Konstanten. `mixed` ist eine Entscheidung, die begründet wird.
- **Enums statt Zeichenkettenkonstanten.** Ein Status ist ein Enum, kein
  `'offen'`.
- **`readonly` für alles, was sich nicht ändern soll**, und
  Konstruktor-Eigenschaftsförderung statt Zuweisungsschleifen.
- **Keine Arrays als Datenstruktur, wo ein Objekt gemeint ist.** Ein
  assoziatives Array mit festen Schlüsseln ist eine Klasse, die noch
  niemand geschrieben hat.
- **Nullsicherheit statt `isset`-Ketten**, Null-Coalescing,
  `never` für Abbrüche.

Werkzeuge und Grenzwerte: `references/php.md`.

## 2. Laravel so verwenden, wie Laravel gemeint ist

**Framework vor Eigenbau** (Skill `neo-grundregeln`, Frameworktreue). Wer
in Laravel etwas selbst baut, das es gibt, hat zweimal verloren: beim
Bauen und beim nächsten Update.

- **Validierung in Formularanfragen**, nicht im Controller.
- **Autorisierung in Policies und Gates**, nicht in `if`-Zweigen.
- **Ausgabeform in API-Ressourcen**, nicht als handgebautes Array.
- **Lange Arbeit in Warteschlangen**, nicht in der Anfrage.
- **Wiederkehrendes im Scheduler**, nicht im System-Cron.
- **Container und Dienste** statt Fassaden im Fachcode; Fassaden sind
  Bequemlichkeit an der Kante, kein Baustein.
- **Ein Controller ist dünn.** Er nimmt entgegen, delegiert, antwortet.
  Fachlogik liegt in Diensten und Modellen (Skill `neo-code`).

Eloquent, Migrationen, Warteschlangen, Ereignisse, Zwischenspeicher und
Dateiablage: `references/laravel.md`.

## 3. Die Datenbank ist kein Nebenschauplatz

- **Kein N+1.** Beziehungen werden bewusst geladen; die Abfragezahl wird
  gemessen, nicht geschätzt.
- **Migrationen sind vorwärtsgerichtet und ohne Datenverlust.** Kein
  Neuaufbau, kein `fresh` außerhalb der Entwicklung.
- **Massenzuweisung ist eingeschränkt**, und zwar mit `$fillable`, nicht
  mit `$guarded = []`.
- **Transaktionen um alles, was zusammengehört.** Ein halb gespeicherter
  Vorgang ist schlimmer als ein abgebrochener.
- **Kein rohes SQL ohne Parameter und ohne Begründung.**
- Weiches gegen hartes Löschen, Historie und Aufbewahrung nach Skill
  `neo-code`, `references/datenmodell.md`.

## 4. Sicherheit ist nicht optional

- **Massenzuweisung, Autorisierung und Mandantentrennung** werden je
  Endpunkt geprüft (Skill `neo-sicherheit`).
- **Keine Secrets im Repository**, `.env` nie eingecheckt, Konfiguration
  über `config()` statt `env()` außerhalb der Konfigurationsdateien.
- **Kein Benutzertext in einer Abfrage, einem Dateipfad, einem
  Shell-Aufruf.**
- **Blade escaped standardmäßig** — `{!! !!}` ist eine Entscheidung mit
  Begründung, keine Bequemlichkeit.
- Datei-Uploads: Typ und Größe serverseitig geprüft, außerhalb des
  Web-Wurzelverzeichnisses abgelegt.

## 5. Tests

Es gilt Skill `neo-grundregeln`, `references/tests.md`. Zusätzlich:

- **Pest oder PHPUnit**, eine Wahl je Projekt, nicht beides.
- **Feature-Tests für jede Route**, mit den sechs Pflichtfällen aus Skill
  `neo-api`, `references/tests.md`.
- **Datenbank-Tests gegen eine echte Datenbank**, nicht gegen SQLite im
  Arbeitsspeicher, wenn produktiv etwas anderes läuft. Ein Unterschied im
  Treiber ist ein Unterschied im Verhalten.
- **Fabriken für Testdaten**, keine handgeschriebenen Datensätze.
- **Fremde Dienste gefälscht**: HTTP, Mail, Warteschlange, Ablage.

## 6. Statische Analyse ist ein Tor, kein Hinweis

- **Statische Analyse auf hoher Stufe**, in der CI, als Blocker.
- **Codestil maschinell**, nicht in der Durchsicht besprochen.
- **Die Stufe wird nicht gesenkt, um grün zu werden**, und eine
  Unterdrückung trägt eine Begründung in derselben Zeile.
- Der Stand wird berichtet: Stufe, Fehlerzahl, Unterdrückungen.

## 7. Symfony in Contao

Ein Contao-Bundle ist Symfony: Dienste mit Autowiring, Tags statt
Registrierungsarrays, Konfiguration in `services.yaml`. Es gelten die
Regeln aus Skill `neo-contao`, `references/erweiterungsbau.md` — dieser
Skill liefert die Sprachebene darunter.

## 8. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.

Zugehörige Skills: `neo-code` (Schichten, Benennung, Querschnitt),
`neo-api` (Endpunkte, OpenAPI, Endpunkttests), `neo-sicherheit`
(Autorisierung, Secrets, Mandanten), `neo-contao` (Bundles),
`neo-grundregeln` (Prozess, Belegpflicht, Tests), `neo-doku`.
