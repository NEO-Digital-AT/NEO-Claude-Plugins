---
name: neo-contao
description: >
  NEO-Regeln für Contao. Diesen Skill laden bei jeder Arbeit an einer
  Contao-Website oder -Erweiterung: Seitenstruktur, Layouts, Themes,
  Artikel, Inhaltselemente, Module, Templates, Twig, DCA, Insert-Tags,
  Imagesets und Bildkompression, MetaModels oder Contao Catalog,
  Backend-Rechte, Composer-Bundles, Migrationen und Seed, Deployment,
  Minifizierung von CSS und JavaScript, llms.txt. Ebenso bei der Frage,
  ob eine fremde Erweiterung eingesetzt oder eine eigene gebaut wird.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, belegt an NEO-Digital-AT/website (docs/STANDARD-PROMPT-CONTAO.md, composer.json, bundles/), Stand 2026-08
---

# NEO-Regeln für Contao

NEO Digital baut Websites fast ausschließlich mit **Contao CMS**.

## Der Maßstab: die Seite ist eine Contao-Seite

Am Ende muss die Website aussehen und sich verhalten, **als wäre sie rein
in Contao entstanden**. Nichts daneben, nichts vorbei.

- Layouts, Themes, Seitentypen, Artikel, Inhaltselemente, Module,
  Formulargenerator, Imagesets, Mehrsprachigkeit, Suche, Sitemap: alles
  kommt aus Contao und wird im Backend gepflegt.
- **Eine Person ohne IT-Kenntnisse muss jeden Inhalt pflegen können** —
  ohne Datei anzufassen, ohne Entwickler.
- **Keine festen Texte in Templates.** Jeder sichtbare Text, jede Adresse,
  jedes Bild, jede Zahl kommt aus einem Feld in der Datenbank. Ein
  Template, das einen Satz enthält, ist ein Fehler, kein Zwischenstand.
- **Insert-Tags verwenden**, wo Contao sie vorsieht — Links, Bilder,
  Seiteneigenschaften, Umgebungswerte. Nie Pfade oder Adressen im
  Template zusammensetzen.
- Was in Contao nicht sichtbar ist, existiert für die Redaktion nicht.

Prüffrage vor jeder Fertigmeldung: **Kann der Kunde diesen Inhalt selbst
ändern, ohne uns anzurufen?** Nein heißt: noch nicht fertig.

## Contao zuerst — Bordmittel vor Eigenbau

Vor jeder Zeile Code die Frage: **Wie löst Contao das nativ?**

- Bilder und Galerien haben eigene Inhaltselemente. Tabellen, Listen,
  Akkordeons, Downloads, Formulare ebenfalls. Nichts davon wird
  nachgebaut.
- Bildgrößen, Zuschnitt und Ausgabeformat kommen **ausschließlich aus den
  Imagesets** von Contao, gepflegt im Backend. Keine eigene
  Bildverarbeitung, keine im Build erzeugten Varianten neben Contao.
- Datumsformate, Sprachen, Weiterleitungen, Zugriffsschutz,
  Suchmaschinen-Einstellungen: Contao-Einstellungen, keine Eigenlösung.
- Im Zweifel die offizielle Dokumentation abrufen, nicht raten:
  <https://docs.contao.org/5.x/manual/de/>

Welche Bordmittel es gibt, welcher Feldtyp wofür, und die Fallen bei
DCA und Rechten: `references/bordmittel.md`.

## Feldtypen richtig verwenden

Wenn doch eigener Code entsteht, gilt dieselbe Regel wie in jeder
NEO-Oberfläche: **was nicht eingegeben werden kann, kann nicht falsch
sein** (Skill `neo-design`).

- Eine Aufzählung ist **kein** Textfeld mit Kommas, sondern ein
  Listenelement oder eine Kind-Tabelle.
- Eine Tabelle ist eine Kind-Tabelle, kein Blob.
- Eine Auswahl ist ein Select mit echten Optionen, keine freie Eingabe.
- Eine Datei ist ein Datei-Picker, kein Pfad als Text.
- Eine Seite ist ein Seiten-Picker, kein von Hand getipptes Insert-Tag.

## Kern und Erweiterungen sind tabu

**Der Contao-Kern und fremde Erweiterungen werden niemals bearbeitet.**
Kein Patch, kein Hack, keine Änderung in `vendor/`.

Lässt sich eine Erweiterung nicht installieren, ist sie für die
eingesetzte Contao-Version nicht freigegeben. Dann: eine andere
Erweiterung suchen oder eine Eigenentwicklung vorschlagen — nie den Kern
oder die Erweiterung zurechtbiegen.

## Erweiterungen: fremd vor eigen

- **Fremde Erweiterungen sind ausdrücklich erwünscht.** Zuerst die
  Extension-Liste durchsehen: <https://extensions.contao.org/>
- **Möglichst keine kostenpflichtigen.** Wo nur eine kostenpflichtige
  passt: nachfragen, nicht entscheiden.
- Gefundene Erweiterungen werden **analysiert und vorgeschlagen**, nicht
  stillschweigend eingebaut: was sie kann, ob sie für die Contao-Version
  freigegeben ist, wie gepflegt sie ist, welche Lizenz, welche Risiken.
  Die Entscheidung fällt der Projektinhaber.
- Für Datenstrukturen sind **MetaModels** und **Contao Catalog** oft die
  richtige Antwort, bevor ein eigenes Bundle entsteht.
- **Eine eigene Erweiterung nur, wenn es keine marktreife gibt** — und
  auch dann erst nach Freigabe.

Auswahlkriterien, MetaModels gegen Catalog gegen Eigenbau, Aufbau eines
eigenen Bundles und die vorhandenen NEO-Bundles:
`references/erweiterungen.md`.

## Eigene Erweiterungen: eigenes Repository

- Alles, was für Contao gebaut wird, ist eine **eigene Extension in einem
  eigenen Repository**.
- Repository-Name: **`Contao-<NameDerErweiterung>-by-NEO`**, ohne
  Leerzeichen.
- Composer-Paket `neo/<name>-bundle`, Tabellen `tl_neo_*`.
- Keine Projekt-Spezifika im Bundle: alles, was ein anderes Projekt
  anders braucht, ist ein Einstellungsfeld — Routen statt fester
  Adressen, Auswahl statt eingebauter Firmenregel.

In `NEO-Digital-AT/website` liegen bereits Bundles, die noch **nicht** in
eigenen Repositories stehen und weiterverwendet werden dürfen:
`neo/super-agent-bundle` (KI-Chat), `neo/brevo-newsletter-bundle`,
`neo/llms-bundle`. Beim Herauslösen gilt die Namensregel oben.

## Auslieferung

- **Immer die aktuellste LTS-Fassung** von Contao (Managed Edition). Die
  gültige LTS-Nummer wird nachgeschlagen, nicht aus dem Gedächtnis
  gesetzt.
- **Alles minifiziert und komprimiert ausliefern**: HTML, CSS,
  JavaScript. Contao kann JavaScript nur zusammenfassen, nicht
  minifizieren — dafür kommt eine Erweiterung dazu, keine Handarbeit.
- **Jede Seite hat `llms.txt`**, dazu die vollständige `llms-full.txt`.
- Bildkompression und Formate ausschließlich über die Imagesets.

Konkrete Einstellungen, Erweiterungen für die Minifizierung und die
Prüfung der Auslieferung: `references/betrieb.md`.

## Datenbank und Deployment

- **Migrierfähig.** Änderungen laufen als Migration, nicht als
  Handgriff im Backend und nicht als Neuaufbau.
- **Die Datenbank wird nie komplett neu aufgebaut.** Es ändert sich nur,
  was sich ändern muss. Bestehende Inhalte des Kunden überleben jedes
  Deployment.
- **Der Seed läuft automatisch und genau einmal.** Ein zweiter Push darf
  ihn nicht wiederholen und nichts überschreiben, was die Redaktion
  seither geändert hat.
- **Deployment ohne Handgriff.** Dateien und Assets werden mit
  übertragen; nach dem Ausrollen ist die Seite vollständig, ohne dass
  jemand etwas nachträgt.

Migrationen, idempotenter Seed, Übertragung von `files/` und Assets:
`references/betrieb.md`.

## Dokumentation

Jede Änderung an Contao — Konfiguration, Erweiterung, Eigenentwicklung —
wird dokumentiert, **einschließlich Bedienungsanleitung** für die
Redaktion.

- Eigenentwicklungen brauchen eine vollständige Doku über mehrere Seiten,
  **zweisprachig Englisch und Deutsch**, wobei **Englisch die
  Hauptsprache** ist. Das weicht bewusst von der sonstigen NEO-Leitsprache
  ab, weil eine Contao-Erweiterung ein internationales Publikum hat.
- Struktur, Inhaltsverzeichnisse, Screenshots mit Markierungen und
  Agentenlesbarkeit: Skill `neo-doku`.
- Bedienung heißt Bedienung im Backend: welches Modul, welches Feld,
  welche Wirkung — mit Screenshots aus dem Contao-Backend.

## Projektstart

Für ein neues Kundenprojekt gilt zusätzlich der Standardprompt
`docs/STANDARD-PROMPT-CONTAO.md` aus `NEO-Digital-AT/website`: Docker-
Aufbau, getrennter Admin-Port, Grundkonfiguration als idempotenter
Befehl, Rechtemodell für Redakteure, Pflicht-Bausteine jeder Seite
(Mail-Schutz, Consent, SEO, Barrierefreiheit) und die Abnahmekriterien.

Zugehörige Skills: `neo-design` (Gestaltung, Eingabeführung,
Barrierefreiheit), `neo-doku` (Dokumentation), `neo-deployment` (Zweige
und Ausrollung), `neo-sicherheit` (Secrets, Härtung, Lieferkette),
`neo-grundregeln` (Prozess und Freigabe).
