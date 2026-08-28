---
name: neo-contao
description: >
  NEO-Regeln für Contao. Diesen Skill laden bei jeder Arbeit an einer
  Contao-Website oder -Erweiterung: Seitenstruktur, Layouts, Themes,
  Artikel, Inhaltselemente, Module, Templates, Twig, DCA, Insert-Tags,
  Imagesets und Bildkompression, SCSS und dessen Einbindung im Layout,
  MetaModels oder Contao Catalog,
  Backend-Rechte, Composer-Bundles, Migrationen und Seed, Deployment,
  Minifizierung von CSS und JavaScript, llms.txt. Ebenso beim Bau einer
  eigenen Contao-Erweiterung (Bundle, Plugin): composer.json,
  Manager-Plugin, Dienste-Tags, DCA, Migrationen, Aktualisierung ohne
  Schaden für bestehende Installationen. Ebenso bei Themes: Aufbau,
  Export als .cto, Import anderswo, Voraussetzungen. Ebenso bei der Frage,
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
- Im Zweifel die offizielle Dokumentation abrufen, nicht raten. Zwei
  Quellen, zwei Sichten:
  - **Handbuch** (Redaktion, Backend, Bordmittel):
    <https://docs.contao.org/5.x/manual/de/>
  - **Entwicklerhandbuch** (DCA, Widgets, Insert-Tags, Bundles, Hooks,
    Migrationen): <https://docs.contao.org/5.x/dev/>

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

## Styles: ausnahmslos SCSS

- Styles werden **nur** in SCSS geschrieben, mit Verschachtelung,
  Variablen, Mixins, Funktionen, Schleifen und Berechnungen — kein
  handgeschriebenes CSS, keine Stile im Template.
- **Jeder Bereich und jede Komponente hat ihre eigene Datei.** Gebaut
  wird in Ebenen: Tokens, Grundlage, Komponenten, Bereiche, Seiten.
- **Achtung bei der Syntax:** Contaos eigener Renderer versteht nur die
  alte Form — `@import`, globale `$variablen`, `@mixin` und `@include`.
  Kein `@use`, kein `@forward`, keine Modulnamensräume. Wird dagegen im
  Build mit Dart Sass übersetzt, ist die moderne Form erlaubt. **Vor der
  ersten Zeile feststellen, welcher Renderer läuft**, und einen
  Kompiliertest fahren.
- **Stylesheets werden im Contao-Layout gewählt, genau wie JavaScript.**
- **Jede Seite liefert nur, was sie braucht.** Kein großes Gesamt-CSS,
  sondern ein Einstiegsbündel je Seitengattung.

Ebenen, Auslagerung, Namensfallen und die Regeln im Einzelnen:
`references/scss.md`.

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
  Leerzeichen. Composer-Paket `neo/<name>-bundle`, Namensraum
  `Neo\Contao<Name>Bundle`, Tabellen `tl_neo_*`, Templates mit
  eigenem Präfix.
- Keine Projekt-Spezifika im Bundle: alles, was ein anderes Projekt
  anders braucht, ist ein Einstellungsfeld — Routen statt fester
  Adressen, Auswahl statt eingebauter Firmenregel.

**Die Rangfolge vor der ersten Zeile Code, jede Stufe belegt:**

1. Bordmittel? → 2. fremde Erweiterung? → 3. **bestehende NEO-Erweiterung,
die das schon kann?** → 4. **eine, der nur etwas fehlt?** → 5. erst dann
eine neue, nach Freigabe.

> **Zwei Erweiterungen für dieselbe Aufgabe sind ein Regelverstoß.**
> Fehlt einer bestehenden etwas, wird **sie** ergänzt — dann haben alle
> Installationen etwas davon.

**Und zwar so, dass jede bestehende Installation aktualisieren kann, ohne
dass sich für sie etwas ändert.** Neue Felder sind optional mit
Standardwert; kein Feld wird umbenannt oder entfernt, solange es jemand
nutzen könnte; keine Pflicht wird nachträglich eingeführt; kein
Standardwert ändert sich ohne Migration. Semantische Versionierung und
ein Änderungsprotokoll je Fassung.

Aufbau eines Bundles, `composer.json`, Registrierung über Dienste-Tags,
Migrationen, Tests und die Doku im Paket: `references/erweiterungsbau.md`.

In `NEO-Digital-AT/website` liegen bereits Bundles, die noch **nicht** in
eigenen Repositories stehen und weiterverwendet werden dürfen:
`neo/super-agent-bundle` (KI-Chat), `neo/brevo-newsletter-bundle`,
`neo/llms-bundle`. Beim Herauslösen gilt die Namensregel oben.

## Webdesign ist ein Theme

**Jedes Webdesign wird als Theme gebaut**, exportierbar als `.cto` und
anderswo installierbar, **ohne dass jemand KI zu Hilfe nehmen muss**.

- Die Quellen — Templates, SCSS, Bilder, der Entwurf — liegen im
  Repository. Die `.cto` ist ein eingechecktes Erzeugnis, kein Original.
- **Templates in einem eigenen Unterordner.** Ein Import überschreibt
  vorhandene Templates.
- **Voraussetzungen zuerst installieren.** Datensätze zu Feldern einer
  fehlenden Erweiterung werden beim Import **stillschweigend
  übergangen** — das Theme sieht importiert aus und ist unvollständig.
  Deshalb führt jedes Theme eine Liste seiner Voraussetzungen.
- Die Installationsanleitung ist so geschrieben, dass sie **ohne KI**
  funktioniert — und das wird nachgewiesen, nicht angenommen.

Aufbau, Ablauf vom Entwurf zum Theme und die Abnahme:
`references/themes.md`.

## Die Gestaltung kommt aus Claude Design

Fast jede NEO-Seite wird in Claude Design entworfen. Dann gilt **Skill
`neo-design`, `references/claude-design.md` ohne Abstriche**: Inventar vor
der ersten Zeile, Element für Element bauen, nach jedem Element messen,
jede Abweichung ist eine Rückfragen — auch hier.

**Contao ist kein Grund für eine Abweichung.** Wo ein Contao-Element
nicht so aussieht wie im Entwurf, wird das Template angepasst, nicht der
Entwurf. Ebenso gelten ohne Abzug: Barrierefreiheit nach WCAG 2.2 AA
(gerechnet, nicht vom Lighthouse-Wert abgeleitet), die PageSpeed-Zielwerte
mobil je Seitenvorlage, und die Größenprüfung auf acht Breiten
einschließlich Textpassung.

## Auslieferung

- **Immer die aktuellste LTS-Fassung** von Contao (Managed Edition). Die
  gültige LTS-Nummer wird nachgeschlagen, nicht aus dem Gedächtnis
  gesetzt.
- **Alles minifiziert und komprimiert ausliefern**: HTML, CSS,
  JavaScript. Contao kann JavaScript nur zusammenfassen, nicht
  minifizieren — dafür kommt eine Erweiterung dazu, keine Handarbeit.
- **`llms.txt` und `llms-full.txt` sind bei einer Webseite Pflicht**, an
  der Domain-Wurzel. Bei Web-Anwendungen und APIs sind sie es nicht —
  dort ist OpenAPI der Vertrag (Skill `neo-api`).
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

Die Struktur steht in der DCA, alles Weitere ist eine **Migration**
(`contao.migration`, `MigrationInterface`). Dabei gilt: `shouldRun()`
wird **defensiv** geschrieben — die Anwendung kann in jedem Zustand sein
—, die Migration ist **wiederholbar**, und sie **verliert keine Daten**.
Getestet wird gegen eine Kopie eines echten Bestands; eine leere
Datenbank besteht jede Migration.

Migrationen, idempotenter Seed, Übertragung von `files/` und Assets:
`references/betrieb.md`. Migrationen im eigenen Bundle:
`references/erweiterungsbau.md`.

## Dokumentation

Jede Änderung an Contao — Konfiguration, Erweiterung, Eigenentwicklung —
wird dokumentiert, **einschließlich Bedienungsanleitung** für die
Redaktion.

- Eigenentwicklungen brauchen eine vollständige Doku über mehrere Seiten.
  **Englisch ist Pflicht und Leitsprache** (`docs/en/`), Deutsch ist
  optional (`docs/de/`). Eine Erweiterung ohne englische Doku gilt als
  unfertig — sie richtet sich an das Contao-Ökosystem, nicht an einen
  einzelnen Kunden.
- **Diese Sprachregel gilt nur für die Doku von Erweiterungen.** Die
  Dokumentation einer Kundenwebsite bleibt deutsch, nach der Leitsprache
  aus dem Skill `neo-doku`. Zwei verschiedene Publika, zwei verschiedene
  Sprachen — im selben Repo möglich, wenn Erweiterung und Projekt darin
  liegen.
- Struktur, Inhaltsverzeichnisse, Screenshots mit Markierungen und
  Agentenlesbarkeit: Skill `neo-doku`.
- Bedienung heißt Bedienung im Backend: welches Modul, welches Feld,
  welche Wirkung — mit Screenshots aus dem Contao-Backend.

## Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.

## Projektstart

Für ein neues Kundenprojekt gilt zusätzlich der Standardprompt
`docs/STANDARD-PROMPT-CONTAO.md` aus `NEO-Digital-AT/website`: Docker-
Aufbau, getrennter Admin-Port, Grundkonfiguration als idempotenter
Befehl, Rechtemodell für Redakteure, Pflicht-Bausteine jeder Seite
(Mail-Schutz, Consent, SEO, Barrierefreiheit) und die Abnahmekriterien.

Zugehörige Skills: `neo-design` (Gestaltung nach Claude Design,
Eingabeführung, Barrierefreiheit, Größen, Messwerte), `neo-doku`
(Dokumentation, Screenshots), `neo-deployment` (Zweige und Ausrollung),
`neo-recht` (Pflichtseiten, Consent), `neo-sicherheit` (Secrets, Härtung,
Lieferkette), `neo-code` (PHP- und Symfony-Konventionen),
`neo-grundregeln` (Prozess, Freigabe, Tests).
