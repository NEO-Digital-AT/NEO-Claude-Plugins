# Lokale Daten auf dem Gerät

Lesekonvention siehe `SKILL.md`.

Eine mobile Anwendung ist **offline-fähig oder sie ist es nicht** — ein
Nachrüsten kostet mehr als der erste Aufbau. Was auf dem Gerät liegt,
gehört getrennt und wird versioniert.

## Drei Ablagen, drei Zwecke

| Ablage | Inhalt | Beispiel |
| --- | --- | --- |
| Gerätestellungen | was NUR dieses Gerät betrifft | Erscheinungsbild, Sprache, zuletzt benutzte Kennung |
| Bewegungsdaten | was der Betrieb erzeugt | Vorgänge, Journale, Warteschlangen |
| Stammdaten | was von außen kommt | Artikel, Benutzer, Konfiguration |

- **Nicht vermischen.** Stammdaten aus der Cloud dürfen Bewegungsdaten
  nie überschreiben; ein abgeschlossener Vorgang trägt **Kopien** der
  Werte, nicht Verweise (sonst ändert eine Preispflege die Vergangenheit).
- **Geheimnisse gehören nicht hierher** (Skill `neo-sicherheit`):
  Schlüssel in den Schlüsselbund des Systems, nicht in die Einstellungen.

## Schema und Migration

- **Jede Schemaänderung erhöht die Version um eins** und trägt ihren
  Migrationsschritt ein. Keine Änderung ohne Schritt.
- **Der Migrationsschritt bekommt einen Test**: eine Datenbank in der
  ALTEN Fassung roh anlegen, öffnen, prüfen, dass die Altdaten
  unversehrt sind und die neue Spalte benutzbar ist.
- **Neustart-Simulation** als Test: zweite Instanz auf derselben Datei —
  laufende Nummern laufen fort, nichts wird wiederverwendet.
- **Vorwärts, ohne Datenverlust.** Eine Spalte wird ergänzt, nicht
  ersetzt; eine Umbenennung ist eine Migration mit Umkopieren.

## Aufzeichnungen sind unveränderlich

Wo das Gesetz oder die Fachlichkeit eine lückenlose Aufzeichnung
verlangt (Journale, Kassenbücher, Protokolle):

- **Nur anhängen.** Kein `UPDATE`, kein `DELETE` — der Datenzugriff
  bietet solche Wege gar nicht erst an; dass es sie nicht gibt, IST die
  Garantie.
- **Fortlaufende Nummer** je Aufzeichnung, lückenlos, nie wiederverwendet.
- **Korrektur ist eine Gegenbuchung**, kein Überschreiben.
- Änderbare Nebendaten (etwa ein Druckvermerk) werden **benannt und
  begründet** — alles andere bleibt fest.

## Schreiben vor Aufräumen

**Erst dauerhaft, dann sichtbar.** Der Warenkorb wird geleert, nachdem
der Vorgang in der Datenbank liegt — nie davor. Schlägt das Schreiben
fehl, bleibt der Zustand stehen und der Fehler steigt auf; der Benutzer
darf nie mit leerem Bildschirm und verlorenem Vorgang dastehen.

Wer eine Ablage ändert, **frischt die Leser auf**. Ein Anhängen ohne
Auffrischen zeigt alte Listen an — der häufigste stille Fehler dieser
Schicht.

## Plattformweiche

Datenbanken über Fremdcode (SQLite, FFI) laufen nicht überall. Die
Weiche gehört **in den Start der Anwendung** (bedingter Import), nie in
einen Bildschirm oder einen Provider: die Oberfläche darf nicht wissen,
auf welcher Plattform sie läuft. Ein Test hält fest, dass der
web-sichere Teil web-sicher bleibt.

## Prüfen

- Migrationstest je Schemaversion, Neustart-Simulation, Test gegen die
  Unveränderlichkeit der Aufzeichnungen.
- Ein Durchlauf **ohne Netz**: was gehen soll, geht; was nicht geht,
  sagt es (Skill `neo-grundregeln`, `references/tests.md`).
