# Auslieferung, Datenbank, Deployment

## Contao-Version

- Verwendet wird **immer die aktuellste LTS-Fassung** (Managed Edition).
- Die gültige LTS-Nummer wird bei Contao nachgeschlagen, nicht aus dem
  Gedächtnis gesetzt: <https://contao.org/> und
  <https://docs.contao.org/>.
- Ein Versionssprung ist eine eigene, angekündigte Änderung mit
  Freigabe — nie nebenbei beim Einbau einer Erweiterung.
- Beobachteter Stand: `NEO-Digital-AT/website` läuft auf Contao 5.7
  Managed Edition (`composer.json`). Das ist der IST-Zustand jenes
  Projekts, keine Vorgabe für neue.

## Minifizierung und Kompression

Jede Seite wird **minifiziert und komprimiert** ausgeliefert.

| Was | Wie |
| --- | --- |
| HTML | Minifizierung in der Antwort |
| CSS | im Build minifiziert oder über eine Erweiterung |
| JavaScript | über eine Erweiterung minifiziert — **Contao fasst nur zusammen, es minifiziert nicht** |
| Übertragung | gzip bzw. brotli am Webserver |
| Statische Dateien | lange Haltbarkeitsangaben mit Stempel in der Adresse |

Die Erweiterung für die Minifizierung wird nach dem Auswahlweg in
`references/erweiterungen.md` gesucht, geprüft und **vorgeschlagen** —
nicht gesetzt. Keine Handarbeit an ausgelieferten Dateien, keine
minifizierten Dateien im Repository neben den Quellen.

**Prüfung nach dem Ausrollen:** die ausgelieferte Antwort ansehen —
Inhaltskodierung, Größe vor und nach der Kompression, ob die
JavaScript-Dateien tatsächlich minifiziert ankommen. Eine Behauptung
ohne diesen Beleg zählt nicht.

## Bilder

Bildkompression, Größen, Zuschnitt und Ausgabeformat kommen
**ausschließlich aus den Imagesets** von Contao, gepflegt im Backend.
Kein zweiter Wandler, keine von Hand erzeugten Varianten, keine
Bildverarbeitung im Build neben Contao.

Was sich ändern soll, ändert sich im Imageset — dann rechnet Contao neu.

## llms.txt

**Jede Seite hat `llms.txt`**, dazu die vollständige **`llms-full.txt`**.

- Erzeugt aus der Datenbank, nicht von Hand gepflegt. In
  `NEO-Digital-AT/website` erledigt das `neo/llms-bundle`.
- Inhalt und Seitenbestand müssen zusammenpassen: eine neue Seite ohne
  Eintrag ist ein Fehler wie ein fehlender Sitemap-Eintrag.
- Nach jeder Strukturänderung prüfen, ob beide Dateien den aktuellen
  Stand zeigen.

## Datenbank

- **Migrierfähig.** Jede Schemaänderung ist eine Migration im Code, kein
  Handgriff im Backend und kein Abgleich von Hand.
- **Nie neu aufbauen.** Kein Löschen des Schemas, kein Leeren von
  Tabellen, kein Einspielen eines Abzugs über den Bestand. Es ändert sich
  nur, was sich ändern muss — die Inhalte des Kunden überleben jedes
  Deployment.
- **Migrationen prüfen den tatsächlichen Zustand.** Contao führt eine
  Migration aus, wenn sie sich dafür zuständig erklärt. Diese Prüfung
  fragt den Ist-Zustand ab („gibt es die Spalte schon?", „steht der Wert
  schon so?") — nicht einen Zähler und kein Datum. Nur so ist ein
  zweiter Lauf harmlos.
- Migrationen sind **vorwärts und rückwärts** durchdacht: was passiert
  bei einem Rückbau, was passiert mit bereits erfassten Daten.
- Vor einer Migration auf einem Bestandssystem: Sicherung, und die
  Migration einmal gegen eine Kopie laufen lassen.

## Seed

- Der Seed **läuft automatisch** beim Ausrollen.
- Er **wiederholt sich nicht**. Ein zweiter Push darf nichts erneut
  anlegen und nichts überschreiben, was die Redaktion seither geändert
  hat.
- Erkannt wird das an einem **stabilen Merkmal im Bestand** (ein
  Schlüssel, ein Alias, ein Kennzeichen an der Zeile), nicht an einer
  Datei im Container und nicht an einem Zeitstempel — Container sind
  flüchtig.
- Der Seed ist ein **idempotenter Befehl**. Der NEO-Standardprompt nennt
  ihn `app:sync-base`: Grundkonfiguration, Benutzergruppen, Medienordner,
  Seitengerüst — beliebig oft ausführbar, ohne etwas neu zu setzen.
- Was der Seed anlegt, gehört danach der Redaktion. Er stellt es her,
  wenn es fehlt; er stellt es nicht wieder her, wenn es geändert wurde.

## Deployment ohne Handgriff

Nach dem Ausrollen ist die Seite vollständig, ohne dass jemand etwas
nachträgt.

| Teil | Regel |
| --- | --- |
| Code und Abhängigkeiten | aus dem Repository, Installation im Ablauf |
| Datenbank | Migrationen laufen automatisch, danach der Seed |
| Build-Erzeugnisse (CSS, JS, Assets) | werden mit übertragen oder im Ablauf erzeugt — nie von Hand hochgeladen |
| Build-verwaltete Dateiordner (z. B. `files/theme`) | werden ersetzt |
| Redaktionelle Dateiordner (z. B. `files/media`) | werden **nie** gelöscht oder überschrieben; Uploads des Kunden sind Daten, kein Build-Ergebnis |
| Zwischenspeicher | wird nach dem Ausrollen geleert bzw. neu aufgebaut |
| Dateirechte | nach dem Ausrollen gesetzt, damit das Backend schreiben kann |

Ein Deployment, das eine Anleitung mit manuellen Schritten braucht, ist
nicht fertig. Das gilt auch für den ersten Aufbau: was einmal von Hand
gemacht wird, fehlt beim nächsten Mal.

Zweigmodell, Schutzregeln und das Tor „nur Grünes wird ausgerollt":
Skill `neo-deployment`.

## Abnahme

- [ ] Alle Seiten antworten mit 200.
- [ ] HTML, CSS und JavaScript kommen minifiziert und komprimiert an —
      belegt an der Antwort, nicht behauptet.
- [ ] Bilder kommen aus den Imagesets, in den vorgesehenen Formaten.
- [ ] `llms.txt` und `llms-full.txt` bilden den aktuellen Seitenbestand
      ab.
- [ ] Ein zweiter Durchlauf des Deployments ändert nichts an den Inhalten.
- [ ] Migrationen laufen auf einer Kopie des Bestands fehlerfrei durch.
- [ ] Ein Testredakteur kann alle Inhalte pflegen und kommt nicht an
      Layouts, Module und Einstellungen.
- [ ] Kein fester Text in einem Template.
- [ ] Kern und fremde Erweiterungen sind unverändert.
