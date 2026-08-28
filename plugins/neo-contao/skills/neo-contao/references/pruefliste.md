# Abnahmeliste Contao

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.
Was bewusst nicht erfüllt ist, wird benannt, mit Grund.

## Verwaltbarkeit

- [ ] **Kein fester Text in einem Template.** Jeder sichtbare Text kommt
      aus einem Feld; Wiederkehrendes über Insert-Tags.
- [ ] Jede Seite, jedes Element und jedes Bild ist im Backend änderbar,
      ohne dass jemand Code anfasst.
- [ ] **Feldtypen passen zur Sache**: Listenelement statt
      kommagetrenntem Textfeld, Auswahl statt Freitext, Datumsfeld statt
      Zeichenkette.
- [ ] Bilder und Galerien über die Contao-Elemente, nicht selbst gebaut.
- [ ] Bildkompression und Formate **ausschließlich** über Imagesets.

## Bordmittel und Erweiterungen

- [ ] Vor jeder Eigenentwicklung wurde die Rangfolge belegt: Bordmittel →
      fremde Erweiterung → bestehende NEO-Erweiterung → bestehende
      erweitern → neu.
- [ ] Der Beleg liegt als Entscheidungsakte vor (Skill `neo-doku`).
- [ ] **Keine zweite Erweiterung für dieselbe Aufgabe.**
- [ ] Fremde Erweiterungen wurden analysiert und **vorgelegt**, nicht
      still eingebaut; die Entscheidung traf der Projektinhaber.
- [ ] Kostenpflichtige Erweiterungen nur nach Freigabe.
- [ ] **Kern und fremde Erweiterungen sind unverändert.** Keine
      Anpassung im Vendor-Verzeichnis.

## Eigene Erweiterung

- [ ] Eigenes Repository `Contao-<Name>-by-NEO`, Paket `neo/<name>-bundle`,
      Namensraum `Neo\Contao<Name>Bundle`, Tabellen `tl_neo_*`, Templates
      mit eigenem Präfix.
- [ ] `composer.json`: `type: contao-bundle`, PSR-4 auf `src/`,
      `extra.contao-manager-plugin` gesetzt, Versionsbereiche mit `^`.
- [ ] Registrierung über **Dienste-Tags und Attribute**; `config.php` nur
      für das, was anders nicht geht.
- [ ] **Keine Projekt-Spezifika**: was ein anderes Projekt anders
      braucht, ist ein Einstellungsfeld.
- [ ] Deutsch und Englisch in den Sprachdateien, weitere Sprachen
      vorgesehen.
- [ ] Unit-, Funktions- und Migrationstests laufen grün; Backend-Masken
      sind im Oberflächendurchlauf enthalten (Skill `neo-grundregeln`).

## Aktualisierbarkeit bestehender Installationen

- [ ] **Neue Felder sind optional** und haben einen Standardwert, der das
      bisherige Verhalten erhält.
- [ ] Kein Feld umbenannt oder entfernt, das eine Installation nutzen
      könnte; Veraltetes ist markiert, nicht gelöscht.
- [ ] Keine nachträglich eingeführte Pflicht, kein still geänderter
      Standardwert.
- [ ] Kein umbenanntes Template ohne funktionierendes altes.
- [ ] **Semantische Versionierung** eingehalten, Änderungsprotokoll je
      Fassung aus Sicht dessen, der aktualisiert.

## Datenbank

- [ ] Struktur in der DCA, alles Weitere als **Migration**
      (`contao.migration`).
- [ ] `shouldRun()` **defensiv**: fehlende Tabelle, fehlende Spalte,
      bereits gelaufen, halb gelaufen — jeder Zustand geprüft.
- [ ] Migration **zweimal hintereinander** gelaufen, ohne Schaden.
- [ ] **Kein Datenverlust**, kein Neuaufbau der Datenbank.
- [ ] Gegen eine **Kopie eines echten Bestands** getestet, nicht gegen
      eine leere Datenbank.
- [ ] Der Seed läuft automatisch und **genau einmal**; ein zweiter Push
      überschreibt nichts, was die Redaktion geändert hat.

## Theme

- [ ] Das Webdesign ist ein **Theme** mit eigenem Repository.
- [ ] Quellen im Repository, `.cto` in `dist/` und aus dem aktuellen
      Stand erzeugt.
- [ ] Der Export wurde **in einer frischen Installation importiert** und
      danach geprüft — nicht nur exportiert.
- [ ] Templates in einem **eigenen Unterordner**.
- [ ] Alle Voraussetzungen dokumentiert und vor dem Import installiert;
      nach dem Import geprüft, dass nichts stillschweigend fehlt.
- [ ] Jemand **ohne KI** konnte das Theme nach der Anleitung
      installieren — nachgewiesen.

## Gestaltung

- [ ] Der Entwurf aus Claude Design wurde nach `neo-design`,
      `references/claude-design.md` umgesetzt: Inventar, Element für
      Element, nach jedem Element gemessen.
- [ ] **Eigene Gestaltungsentscheidungen: 0.**
- [ ] Layout-, Stil- und Bildabgleich bestanden, je Seitenvorlage.
- [ ] Kein waagrechtes Scrollen, nichts ragt hinaus, Tabellen füllen,
      keine Löcher, Bedienziele groß genug, kein Text abgeschnitten —
      auf acht Breiten (`/neo-design:neo-responsivpruefung`).
- [ ] SCSS nach `scss.md`: je Bereich und Bauteil eine Datei,
      Verschachtelung, Schleifen, Berechnungen, Schichten; je Seite nur
      das, was sie braucht.

## Auslieferung und Messwerte

- [ ] Aktuellste LTS-Fassung von Contao (nachgeschlagen, nicht geraten).
- [ ] HTML, CSS und JavaScript minifiziert und komprimiert; die
      Minifizierung über eine Erweiterung, nicht von Hand.
- [ ] **`llms.txt` und `llms-full.txt`** an der Domain-Wurzel, aus dem
      Bestand erzeugt — bei einer Webseite Pflicht.
- [ ] PageSpeed **mobil je Seitenvorlage**: Best Practices 100, SEO 100,
      agentisches Browsen 3/3, Leistung und Barrierefreiheit mindestens
      95 (Skill `neo-design`).
- [ ] Barrierefreiheit nach WCAG 2.2 AA **gerechnet und berichtet**, nicht
      vom Lighthouse-Wert abgeleitet.
- [ ] Deployment ohne Handgriff, einschließlich `files/` und Assets.

## Recht

- [ ] Impressum, Datenschutzerklärung und Barrierefreiheitserklärung
      vorhanden und inhaltlich vollständig (Skill `neo-recht`).
- [ ] Vor der Einwilligung lädt nichts von Dritten — auch kein
      eingebettetes Video.
- [ ] Schriften selbst ausgeliefert, nicht von einem fremden Dienst.

## Dokumentation

- [ ] Doku **im Paket**, nicht daneben: `docs/en/` Pflicht, `docs/de/`
      optional.
- [ ] Bedienungsanleitung für die Redaktion, mit Screenshots aus dem
      Backend und Markierungen (Skill `neo-doku`).
- [ ] `README.md` und `CHANGELOG.md` im Wurzelverzeichnis.
- [ ] Bei einer Erweiterung zusätzlich: Installation, Felder, Upgrade,
      Fehlerbehebung.
