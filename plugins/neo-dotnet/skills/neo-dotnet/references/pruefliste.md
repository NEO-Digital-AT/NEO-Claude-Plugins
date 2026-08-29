# Abnahmeliste Serveranwendung (.NET)

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Quelle

- [ ] APIs aus der offiziellen Doku der **eingesetzten** Fassung
      nachgeschlagen, nicht erinnert.
- [ ] Die Fassung ist als Entscheidungsakte festgehalten.

## Bau

Einzelheiten: `bau.md`.

- [ ] `Directory.Build.props` mit `Nullable`, `TreatWarningsAsErrors`,
      hoher Analysestufe und `EnforceCodeStyleInBuild`.
- [ ] Unterdrückungen gezählt, jede mit Begründung.
- [ ] Zentrale Paketverwaltung; `packages.lock.json` eingecheckt, CI mit
      `--locked-mode`.
- [ ] Quellenzuordnung gesetzt, `NuGetAudit` an, **null** offene
      Schwachstellen.
- [ ] Architekturtest vorhanden und grün, geprüfte Regeln benannt.

## Aufbau

- [ ] Endpunkte dünn: annehmen, prüfen, an einen Dienst geben, antworten.
- [ ] Minimal API **oder** Controller — eine Bauart im Projekt.
- [ ] Keine Fachlogik und kein Datenzugriff im Endpunkt.
- [ ] Eingaben am Rand geprüft, als eigener Typ weitergereicht.

## Konfiguration

- [ ] Options-Muster, beim Start geprüft; fehlende Pflichteinstellung
      verhindert den Start.
- [ ] **Keine Geheimnisse** in `appsettings` oder im Repository —
      Verbindungszeichenfolgen eingeschlossen.

## Daten

- [ ] Abfragezahl **gemessen** und als Erwartung im Test festgehalten;
      kein N+1.
- [ ] Lesepfade ohne Verfolgung, Projektion statt ganzer Entität.
- [ ] Paginierung überall, wo die Menge wachsen kann.
- [ ] Migration vorwärtsgerichtet, ohne Datenverlust, gegen eine
      **Bestandskopie** geprüft; Rückweg beschrieben.
- [ ] Mandantentrennung im Datenzugriff **und** durch einen Test belegt.

## Laufzeit

- [ ] `async` durchgehend, `CancellationToken` durchgereicht.
- [ ] Kein `.Result`, kein `.Wait()`.
- [ ] Lange Arbeit im Hintergrunddienst oder in der Warteschlange,
      **idempotent**.

## Leistung

Einzelheiten: `leistung.md`.

- [ ] Je Endpunkt ein **Zeitbudget** benannt und gemessen, mit Zahl
      berichtet.
- [ ] Keine Abfrage ohne Obergrenze.
- [ ] Ausgehende Aufrufe über `IHttpClientFactory`, jeder mit Zeitgrenze;
      Verhalten beim endgültigen Fehlschlag benannt.
- [ ] Zwischenspeicher mit Schlüsselschema und Verfallszeit.
- [ ] Lasttest gegen einen realistischen Bestand: p50, p95, Fehlerquote,
      Abfragezahl berichtet.

## Härtung

Einzelheiten: `haertung.md`.

- [ ] Globale Rückfallregel setzt Authentifizierung durch; öffentliche
      Endpunkte einzeln benannt und **gezählt**.
- [ ] Test belegt: unangemeldeter Aufruf → 401.
- [ ] Ratenbegrenzung nach dem authentifizierten Aufrufer; 429 mit
      `Retry-After` in der Fehlerhülle.
- [ ] Grenzen für Rumpf, Uploads und Deserialisierung gesetzt.
- [ ] Eigene Ein- und Ausgabetypen je Endpunkt; keine Entität am Rand.
- [ ] CORS mit benannten Ursprüngen.
- [ ] Kein `DateTime.Now` im Fachcode; Zeit über `TimeProvider`, UTC
      gespeichert.

## Antworten

- [ ] Eine Fehlerhülle für alle Fehlerantworten.
- [ ] Keine internen Einzelheiten in der Antwort; Kennung statt
      Stapelabzug.
- [ ] Sechs Pflichttestfälle je Endpunkt erfüllt (Skill `neo-api`).

## Betrieb

- [ ] Strukturierte Protokolle, **ohne** Geheimnisse und Personendaten.
- [ ] Korrelationskennung durch alle Schichten.
- [ ] Health-Endpunkte getrennt (lebt/bereit), ausführlicher Zustand
      abgesichert.
- [ ] Bau und Ausrollung reproduzierbar.

## Tests

- [ ] Integrationstests gegen eine **echte** Datenbank im Container.
- [ ] Anwendung im Test gehostet, außen liegende Dienste ausgetauscht.
- [ ] Migrationslauf gegen eine Bestandskopie gelaufen.
