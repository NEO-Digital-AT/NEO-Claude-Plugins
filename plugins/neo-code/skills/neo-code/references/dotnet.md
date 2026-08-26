# .NET und C#

Maßgeblich sind die **C#-Codierungskonventionen** und die **Framework
Design Guidelines** von Microsoft. Was dort steht, gilt; hier steht nur,
was NEO zusätzlich festlegt oder wo erfahrungsgemäß gestritten wird.

## Projektschnitt

```
src/
  <Produkt>.Domain           Fachlichkeit, Entitäten, Regeln, Verträge
  <Produkt>.Infrastructure   EF Core, fremde APIs, Dateien, Mail
  <Produkt>.Api              Endpoints, Middleware, Konfiguration
  <Produkt>.Tests            Unit- und Integrationstests
```

Belegt an `NEO-Digital-AT/uptime`. Weitere Projekte (Worker, Shared)
kommen dazu, wo sie gebraucht werden — nie ein Projekt „für später".

**Die Verweisrichtung ist eine Einbahnstraße.** `Domain` verweist auf
nichts. Ein Verweis in die falsche Richtung ist kein Stilfehler, sondern
ein Architekturbruch.

## Sprache und Stil

- **Nullable Reference Types aktiv**, projektweit. Ein `!` braucht einen
  Kommentar, der sagt, warum es sicher ist.
- **Dateibezogene Namensräume** (`namespace X;`), ein Typ je Datei,
  Dateiname gleich Typname.
- `PascalCase` für Typen, Methoden, Eigenschaften, Konstanten;
  `camelCase` für Parameter und lokale Variablen; `_camelCase` für
  private Felder; `I`-Präfix nur für Schnittstellen.
- `var` dort, wo der Typ rechts steht; sonst der Typ.
- Ausdruckskörper für Einzeiler, sonst Block.
- Keine Regionen. Wer sie braucht, hat eine zu große Datei.
- `sealed` als Voreinstellung für Klassen, die nicht zur Vererbung
  gedacht sind.

## Asynchronität

- **`async` durchgängig.** Kein `.Result`, kein `.Wait()`, kein
  `.GetAwaiter().GetResult()` — das ist der klassische Weg in einen
  Deadlock.
- Methodennamen enden auf `Async`.
- `CancellationToken` wird durchgereicht, bis er dort ankommt, wo
  tatsächlich gewartet wird.
- `ConfigureAwait(false)` in Bibliotheken; in der Anwendung nicht nötig.
- Kein `async void` außer in Ereignisbehandlern.

## Abhängigkeitsinjektion

- Konstruktorinjektion. Kein Service Locator, kein statischer Zugriff auf
  den Container.
- Lebensdauern bewusst wählen. Ein `DbContext` ist niemals `Singleton`;
  ein `Singleton`, der einen `Scoped`-Dienst hält, ist ein Fehler, der
  erst unter Last auffällt.
- Schnittstellen dort, wo es eine zweite Umsetzung gibt oder ein Test sie
  braucht — nicht für jede Klasse aus Prinzip.

## Datenzugriff

- **EF Core, nur Migrationen** (Skill `neo-api`, `references/betrieb.md`).
- Abfragen liefern das, was gebraucht wird, nicht die ganze Entität mit
  allen Beziehungen. `AsNoTracking()` für Lesepfade.
- Kein N+1: Beziehungen werden bewusst geladen.
- **Anlegen über das `DbSet`, nicht über eine Navigation**, wenn der
  Schlüssel schon feststeht. Eine nur über die Navigation gefundene Zeile
  hält EF für bestehend, schickt ein UPDATE hinaus, trifft null Zeilen
  und reißt die Anfrage mit einem Nebenläufigkeitsfehler ab. Dieser
  Fehler ist in NEO Uptime dreimal aufgetreten — jedes Mal erst im
  Laufzeitlauf, nie im Test.
- Rohes SQL nur parametrisiert und nur mit Begründung.

## Fehler und Ergebnisse

- Ausnahmen für **Ausnahmen**, nicht für erwartbare Fachfälle. „Kunde
  nicht gefunden" ist ein Ergebnis, kein Wurf.
- Nie leer fangen. Wer fängt, behandelt oder wirft weiter — mit Kontext,
  ohne den Stapel zu verlieren (`throw;`, nicht `throw ex;`).
- Nach außen gilt die einheitliche Fehlerhülle (Skill `neo-api`), nie ein
  Stacktrace.

## Analyse

- `TreatWarningsAsErrors` an, `EnableNETAnalyzers` an, `AnalysisLevel`
  aktuell.
- `.editorconfig` im Repo, für alle verbindlich.
- `dotnet format --verify-no-changes` in der CI.
- Eine Unterdrückung trägt eine Begründung und steht in der
  Projektkonfiguration, nicht verstreut im Code.

## Tests

- Benennung `Methode_Bedingung_Erwartung`.
- Ein Verhalten je Test, aussagekräftige Zusicherungen — kein Test, der
  nur prüft, dass nichts geworfen wurde.
- Integrationstests gegen eine echte Datenbank in einem Container, nicht
  gegen einen In-Memory-Ersatz, der andere Semantik hat.
- Fremde Anbieter gefälscht (Skill `neo-api`).
