---
name: neo-dotnet
description: >
  NEO-Regeln für Serveranwendungen mit .NET und ASP.NET Core. Diesen
  Skill laden, sobald ein Backend entsteht oder geändert wird: Endpunkt,
  Controller, Minimal API, Dienst, Middleware, Filter, Hintergrunddienst,
  Hosting und Start. Ebenso bei Konfiguration und Geheimnissen, bei
  Datenzugriff mit Entity Framework Core einschließlich Migrationen und
  Mandantentrennung, bei Authentifizierung und Autorisierung, bei
  Protokollen, Health-Endpunkten und Beobachtbarkeit sowie bei
  Integrationstests gegen eine echte Datenbank. Ebenso beim Aufsetzen des
  Baus (Analyse als Blocker, zentrale Paketverwaltung, Sperrdatei,
  Architekturtests), bei Leistungsfragen mit Zeitbudget und Lasttest und
  bei der Härtung der Anwendung.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# .NET und ASP.NET Core

Lesekonvention siehe `README.md` des Regel-Repositorys.

Sprache, Projektschnitt und Stil stehen im Skill `neo-code`,
`references/dotnet.md` — hier geht es um die **Serveranwendung**:
Endpunkte, Konfiguration, Datenzugriff, Betrieb. Verträge, Fehlerhülle
und Autorisierungsregeln der Schnittstelle regelt der Skill `neo-api`;
was dort steht, gilt hier ohne Abzug.

## Der Satz vorweg

> **Die API wird nachgeschlagen, nicht erinnert.**

Offizielle Doku der **eingesetzten** Fassung, nicht die Erinnerung an
eine frühere. Die Fassung ist eine **LTS-Entscheidung des
Projektinhabers** und steht als Entscheidungsakte fest (Skill
`neo-doku`); ein Sprung auf eine neue Hauptfassung ist eine Änderung mit
Auswirkung, kein Nebenbei.

## 1. Der Bau ist streng

Einzelheiten: `references/bau.md`.

- **Die Strenge steht in `Directory.Build.props`**, einmal für die ganze
  Mappe: `Nullable`, `TreatWarningsAsErrors`, hohe Analysestufe,
  `EnforceCodeStyleInBuild`. In einer einzelnen Projektdatei wird sie
  beim nächsten neuen Projekt vergessen.
- **Zentrale Paketverwaltung und eingecheckte Sperrdatei**, in der CI
  wiederhergestellt mit `--locked-mode`. Zwei Fassungen desselben Pakets
  in zwei Projekten sind sonst der Normalfall.
- **Die Schichtgrenze wird gemessen, nicht behauptet**: ein
  Architekturtest, sobald es mehr als ein Projekt gibt. `Domain` verweist
  auf nichts — und ein Test beweist es.
- **Der Bau ist reproduzierbar.** Feste SDK-Fassung, frischer Container.

## 2. Endpunkte bleiben dünn

- **Annehmen, prüfen, an einen Dienst geben, antworten.** Mehr steht in
  keinem Endpunkt — weder in einem Controller noch in einer Minimal API.
- **Minimal API oder Controller ist eine Projektentscheidung**, einmal
  getroffen und durchgehalten; beides nebeneinander ist keine Wahl,
  sondern ein Versäumnis.
- **Keine Fachlogik, kein Datenzugriff, keine Abfrage im Endpunkt.**
- **Eingaben werden am Rand geprüft** und als eigener Typ
  weitergereicht, nicht als loses Wörterbuch.

## 3. Konfiguration und Geheimnisse

- **Options-Muster** statt Zugriff auf die Konfiguration im Fachcode;
  die Optionen werden **beim Start geprüft** — eine Anwendung mit
  fehlender Pflichteinstellung startet nicht, statt später zu scheitern.
- **Keine Geheimnisse in `appsettings`** und nicht im Repository:
  Entwicklung über User Secrets, Betrieb über Umgebung oder Tresor
  (Skill `neo-sicherheit`).
- **Verbindungszeichenfolgen sind Geheimnisse**, auch die zur
  Testdatenbank.

## 4. Datenzugriff

Einzelheiten und Fallstricke: `references/efcore.md`.

- **Kein N+1**, und die Abfragezahl wird **gemessen**, nicht geschätzt.
- **Lesepfade ohne Verfolgung** (`AsNoTracking`), Schreibpfade in einer
  Arbeitseinheit.
- **Mandantentrennung liegt im Datenzugriff**, nicht in der Sorgfalt des
  Aufrufers: Wer sie vergessen kann, wird sie vergessen (Skill
  `neo-sicherheit`).
- **Migrationen vorwärtsgerichtet, ohne Datenverlust**, neue Spalten
  nullbar oder mit Vorgabewert, geprüft gegen eine **Kopie eines echten
  Bestands**.

## 5. Asynchron durchgehend

- **`async` vom Endpunkt bis zur Datenbank**, ohne Bruch.
- **`CancellationToken` wird durchgereicht** — bricht der Aufrufer ab,
  bricht die Arbeit ab.
- **Kein sync-over-async** (`.Result`, `.Wait()`): das ist die häufigste
  Ursache für einen blockierten Server unter Last.
- **Lange Arbeit gehört nicht in eine Anfrage**, sondern in einen
  Hintergrunddienst oder eine Warteschlange — **idempotent**, weil sie
  wiederholt wird.
- **Die Zeit kommt aus `TimeProvider`**, nicht aus `DateTime.Now`: im
  Container stimmt die Zeitzone sonst nicht, und kein Test kann die Uhr
  stellen. Gespeichert wird UTC.

## 6. Fehler und Antworten

- **Eine Fehlerhülle für alle Fehlerantworten** (`ProblemDetails`),
  gestaltet nach Skill `neo-api`.
- **Ausnahmen sind kein Steuerfluss.** Erwartbare Fälle sind Ergebnisse,
  keine Ausnahmen (Skill `neo-code`, `references/dotnet.md`).
- **Keine internen Einzelheiten nach außen**: kein Stapelabzug, kein
  SQL, kein Dateipfad in einer Antwort — im Protokoll steht das Ganze,
  in der Antwort eine Kennung.

## 7. Beobachtbarkeit

- **Strukturierte Protokolle** mit Feldern statt zusammengesetzter
  Sätze; **keine Geheimnisse, keine Personendaten** im Protokoll (Skill
  `neo-sicherheit`, `references/secrets-und-logging.md`).
- **Jede Anfrage trägt eine Korrelationskennung** durch alle Schichten.
- **Health-Endpunkte** trennen „lebt" von „bereit"; der ausführliche
  Zustand ist **abgesichert**, nicht öffentlich.

## 8. Leistung und Härtung

**Leistung ohne Zahl ist eine Meinung** — `references/leistung.md`:

- **Jeder Endpunkt hat ein Zeitbudget**, vor dem Bau festgelegt, gegen
  einen realistischen Bestand gemessen, mit Zahl berichtet.
- **Keine Abfrage ohne Obergrenze**, die Abfragezahl je Endpunkt wird
  gemessen und im Test festgehalten.
- **Ausgehende Aufrufe über `IHttpClientFactory`**, jeder mit
  Zeitgrenze; ein fremder Dienst darf ausfallen, ohne die eigene
  Anwendung mitzunehmen.
- **Zuerst die Abfrage reparieren, dann zwischenspeichern.**

**Deny-by-default ist eine Zeile im Start**, nicht ein Vorsatz —
`references/haertung.md`:

- **Globale Rückfallregel** verlangt auf jedem Endpunkt einen
  authentifizierten Aufrufer; was öffentlich ist, wird einzeln
  freigegeben und **gezählt**.
- **Ratenbegrenzung nach dem authentifizierten Aufrufer**, engere Grenze
  für Anmeldung und kostenauslösende Endpunkte.
- **Grenzen für Rumpf, Uploads und Deserialisierung** sind gesetzt.
- **Eigene Ein- und Ausgabetypen je Endpunkt** — keine Entität am Rand,
  sonst setzt eine Anfrage ein Feld, das niemand gemeint hat.

## 9. Tests

Es gilt Skill `neo-grundregeln`, `references/tests.md`. Zusätzlich:

- **Integrationstests gegen die echte Datenbank** (Container), nicht
  gegen eine Attrappe: Migrationen, Fremdschlüssel und Rechte fallen nur
  dort auf.
- **Die Anwendung wird im Test gehostet** (`WebApplicationFactory`), mit
  denselben Diensten wie im Betrieb; ausgetauscht wird nur, was außen
  liegt (Zahlungsanbieter, Postversand).
- **Sechs Pflichttestfälle je Endpunkt** nach Skill `neo-api`.
- **Ein Migrationslauf gegen eine Bestandskopie** gehört zur Abnahme.

## 10. Ausrollung

Zweigmodell, Schutzregeln und Pflichtprüfungen: Skill `neo-deployment`.
Eine Anwendung, die sich nicht **reproduzierbar** bauen und ausrollen
lässt, gilt als nicht fertig.

## 11. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.
Die Abschnitte zu Bau, Leistung und Härtung tragen jeweils eine eigene
Abnahmeliste am Ende ihrer Referenzdatei.

| Bereich | Referenz |
| --- | --- |
| Bau, Analyse, Pakete, Architekturtests | `references/bau.md` |
| Zeitbudget, Abfragezahl, ausgehende Aufrufe, Lasttest | `references/leistung.md` |
| Rückfallregel, Ratenbegrenzung, Grenzen, Zeit | `references/haertung.md` |
| EF Core, Migrationen, Mandantentrennung | `references/efcore.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

Zugehörige Skills: `neo-code` (Sprache, Schichten), `neo-api`
(Verträge, Fehlerhülle, Autorisierung), `neo-sicherheit` (Geheimnisse,
Mandantentrennung, Härtung), `neo-deployment` (Zweige, Ausrollung),
`neo-doku` (Entscheidungsakten), `neo-grundregeln` (Belegpflicht, Tests).
