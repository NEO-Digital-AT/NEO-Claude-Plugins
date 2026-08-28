# Laravel

Lesekonvention siehe `SKILL.md`.

> **Die API wird nachgeschlagen, nicht erinnert.** Wo **Laravel Boost**
> verfügbar ist, ist es die Quelle: MCP-Werkzeuge für die eigene
> Anwendung, mitgelieferte KI-Richtlinien, Dokumentations-Schnittstelle.
> Sonst die offizielle Dokumentation **der eingesetzten Fassung**.

Dieser Text sagt nicht, wie Laravel funktioniert. Er sagt, **wie NEO es
verwendet** — und was nicht gemacht wird.

## Wo was hingehört

| Aufgabe | Ort | Nicht |
| --- | --- | --- |
| Eingaben prüfen | Formularanfrage | im Controller |
| Rechte prüfen | Policy, Gate | `if`-Zweige in der Methode |
| Ausgabe formen | API-Ressource | handgebautes Array |
| Fachlogik | Dienst, Aktion, Modellmethode | Controller |
| Lange Arbeit | Warteschlangen-Job | in der Anfrage |
| Wiederkehrendes | Scheduler | System-Cron |
| Abfragen bündeln | Query Scope, Repository | derselbe `where`-Block an acht Stellen |

**Ein Controller ist dünn**: entgegennehmen, delegieren, antworten. Mehr
als 20 Zeilen in einer Controller-Methode sind ein Hinweis.

**Fassaden sind Bequemlichkeit an der Kante.** Im Fachcode wird
eingespritzt, damit die Klasse ohne Framework testbar bleibt (Skill
`neo-code`).

## Eloquent

- **Beziehungen bewusst laden.** `with()` an der Stelle, an der die
  Abfrage entsteht — nicht Lazy Loading in einer Schleife im Template.
- **N+1 wird gemessen**, nicht vermutet: Abfragezähler im Test, strenges
  Lazy Loading in der Entwicklung abgeschaltet lassen.
- **`$fillable`, nicht `$guarded = []`.** Eine offene Massenzuweisung ist
  eine Rechteerweiterung, die auf ihren Tag wartet.
- **`$casts` für alles**, was kein reiner Text ist: Enums, Datumsangaben,
  Wahrheitswerte, JSON, verschlüsselte Felder.
- **Keine Abfragen in Blade.** Was die Ansicht braucht, kommt fertig an.
- **`select()` statt `*`** bei breiten Tabellen und Listen.
- Modelle bleiben **schlank**: Beziehungen, Casts, Scopes, kleine
  Fachmethoden. Ein Modell mit 600 Zeilen ist ein Dienst im Versteck.

## Migrationen

- **Vorwärtsgerichtet und ohne Datenverlust.** Kein `migrate:fresh`
  außerhalb der Entwicklung, kein Neuaufbau, keine Handgriffe in der
  Datenbank.
- **Eine Migration je Änderung**, benannt nach dem, was sie tut.
- **Erst hinzufügen, dann befüllen, dann umstellen, später entfernen** —
  in getrennten Fassungen, damit die alte Anwendung weiterläuft, während
  die neue ausgerollt wird.
- **Neue Spalten sind nullbar oder haben einen Standardwert.** Eine
  `NOT NULL`-Spalte ohne Standardwert bricht jede laufende Instanz.
- **Indizes gehören zur Migration**, nicht in eine spätere Runde: jeder
  Fremdschlüssel, jede Spalte in einem `where` einer Listenabfrage.
- **Gegen eine Kopie eines echten Bestands geprüft**, nicht gegen eine
  leere Datenbank (Skill `neo-grundregeln`).

## Warteschlangen und geplante Aufgaben

- **Jobs sind idempotent.** Sie laufen zweimal, weil ein Arbeiter
  neustartet.
- **Versuche und Zeitgrenze gesetzt**, dazu ein Weg für den endgültigen
  Fehlschlag — eine gescheiterte Aufgabe, die niemand sieht, ist ein
  stiller Datenverlust.
- **Kein Modell im Job serialisiert festhalten**, wo eine Kennung reicht.
- **Der Scheduler läuft mit Überlappungsschutz** und auf **einem**
  Server, wenn es mehrere gibt.
- Was länger dauert als eine Anfrage darf, gehört in die Warteschlange —
  Mail, PDF, Bildverarbeitung, fremde Schnittstellen.

## Zwischenspeicher, Ablage, Mail

- **Zwischenspeicher mit Schlüsselschema und Verfallszeit**, nie
  unbegrenzt. Ein Eintrag ohne Verfall ist ein Fehler, der irgendwann
  ausgeliefert wird.
- **Ungültig machen, wo geschrieben wird** — nicht hoffen, dass der
  Verfall es richtet.
- **Dateien über die Ablage-Abstraktion**, nie mit `file_put_contents` in
  einen Pfad. Der Treiber wechselt, der Code nicht.
- **Uploads**: Typ und Größe serverseitig geprüft, außerhalb des
  Web-Wurzelverzeichnisses, Zugriff über eine Route mit Rechteprüfung.
- **Mail über die Warteschlange**, mit einem eigenen Absender je Zweck,
  und im Test gefälscht (Skill `neo-betrieb` für Zustellbarkeit).

## Ereignisse

- **Ein Ereignis meldet, was geschehen ist** — Vergangenheitsform, keine
  Anweisung.
- **Nichts, was für die Antwort gebraucht wird**, hängt an einem
  Zuhörer.
- Zuhörer, die dauern, sind **in die Warteschlange gestellt**.
- Kein Ereignisgewitter: wenn drei Zuhörer immer zusammen laufen, ist es
  ein Dienst.

## Konfiguration und Umgebung

- **`env()` nur in Konfigurationsdateien**, sonst `config()`. Nach dem
  Zwischenspeichern der Konfiguration liefert `env()` im Code `null` —
  und das fällt erst in Produktion auf.
- **`.env` nie eingecheckt**, `.env.example` immer aktuell.
- **Debug aus, Fehleranzeige aus** in Produktion; die Prüfung steht in der
  Abnahmeliste (Skill `neo-sicherheit`).
- Konfiguration, Routen, Ansichten und Ereignisse werden beim Ausrollen
  zwischengespeichert — und der Zwischenspeicher wird dabei geleert.

## Blade

- **Escaping bleibt an.** `{!! !!}` ist eine Entscheidung mit Begründung.
- **Keine Fachlogik im Template**, keine Abfrage, keine Berechnung, die
  woanders hingehört.
- **Komponenten statt Wiederholung**, und die Komponenten folgen dem
  Komponenten-Grundsatz (Skill `neo-komponenten`).
- Texte kommen aus den Sprachdateien, nicht aus dem Template (Skill
  `neo-design`, `references/oberflaechentexte.md`).
