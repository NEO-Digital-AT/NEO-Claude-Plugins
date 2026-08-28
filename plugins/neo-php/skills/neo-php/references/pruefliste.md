# Abnahmeliste PHP und Laravel

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Quelle

- [ ] Die verwendete API wurde **nachgeschlagen**, nicht erinnert — über
      Laravel Boost oder die offizielle Doku **der eingesetzten Fassung**.
- [ ] Keine Signatur aus dem Gedächtnis, keine aus einer anderen Fassung.

## Sprache

- [ ] `declare(strict_types=1)` in **jeder** Datei.
- [ ] Parameter, Rückgabewerte und Eigenschaften vollständig typisiert;
      jedes `mixed` ist begründet.
- [ ] Statuswerte sind **Enums**, keine Zeichenketten.
- [ ] Wertobjekte sind `readonly` und prüfen im Konstruktor.
- [ ] `DateTimeImmutable`, nie `DateTime`.
- [ ] Kein assoziatives Array mit festen Schlüsseln als Datenstruktur.
- [ ] Ausnahmen nur für Ausnahmen; kein leeres `catch`.

## Laravel

- [ ] Validierung in Formularanfragen, Rechte in Policies, Ausgabe in
      Ressourcen — nichts davon im Controller.
- [ ] Controller sind dünn; Fachlogik in Diensten und Modellen.
- [ ] Keine Fassaden im Fachcode; eingespritzt statt statisch gerufen.
- [ ] Lange Arbeit in der Warteschlange, Wiederkehrendes im Scheduler.
- [ ] `env()` nur in Konfigurationsdateien, sonst `config()`.
- [ ] `.env` nicht eingecheckt, `.env.example` aktuell.
- [ ] Debug und Fehleranzeige in Produktion aus.

## Datenbank

- [ ] **Kein N+1** — die Abfragezahl je Ansicht ist **gemessen** und
      berichtet, nicht geschätzt.
- [ ] `$fillable` gesetzt; kein `$guarded = []`.
- [ ] `$casts` für Enums, Datum, Wahrheitswerte, JSON.
- [ ] Keine Abfrage in Blade.
- [ ] Migrationen vorwärtsgerichtet, ohne Datenverlust, kein Neuaufbau.
- [ ] Neue Spalten nullbar oder mit Standardwert; Indizes gleich mit.
- [ ] Gegen eine **Kopie eines echten Bestands** geprüft.
- [ ] Transaktionen um alles, was zusammengehört.

## Warteschlangen

- [ ] Jobs sind **idempotent** und wurden zweimal hintereinander geprüft.
- [ ] Versuche, Zeitgrenze und ein Weg für den endgültigen Fehlschlag
      sind gesetzt; gescheiterte Aufgaben werden gesehen.
- [ ] Scheduler mit Überlappungsschutz, auf genau einem Server.

## Sicherheit

- [ ] Massenzuweisung, Autorisierung und Mandantentrennung je Route
      geprüft (Skill `neo-sicherheit`).
- [ ] Kein Benutzertext in Abfrage, Pfad oder Shell-Aufruf.
- [ ] Blade-Escaping an; jedes `{!! !!}` begründet.
- [ ] Uploads serverseitig geprüft, außerhalb des Web-Wurzelverzeichnisses.
- [ ] Keine Secrets im Repository; Composer Audit grün.

## Tests

- [ ] Feature-Test je Route mit den sechs Pflichtfällen (Skill `neo-api`,
      `references/tests.md`).
- [ ] Datenbank-Tests gegen **denselben Treiber** wie in Produktion.
- [ ] Fabriken statt handgeschriebener Datensätze.
- [ ] HTTP, Mail, Warteschlange und Ablage in Tests gefälscht.
- [ ] Oberflächendurchlauf für Blade- und Livewire-Ansichten (Skill
      `neo-grundregeln`, `references/durchlauf.md`).

## Werkzeuge

- [ ] Codestil maschinell, in der CI.
- [ ] Statische Analyse auf **hoher Stufe**, als Blocker, Stufe nicht
      gesenkt; jede Unterdrückung begründet.
- [ ] Stufe, Fehlerzahl und Zahl der Unterdrückungen **berichtet**.
- [ ] Sperrdatei eingecheckt, kein `dev-master` in Produktion.
- [ ] Jede neue Abhängigkeit wurde vorgelegt, mit Zweck und Lizenz.
