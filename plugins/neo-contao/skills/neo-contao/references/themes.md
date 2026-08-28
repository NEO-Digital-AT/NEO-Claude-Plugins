# Webdesign als Contao-Theme

Lesekonvention siehe `SKILL.md`. Gestaltungsregeln: Skill `neo-design`.
SCSS: `scss.md`.

> **Jedes Webdesign wird als Theme gebaut — exportierbar als `.cto` und
> anderswo installierbar, ohne dass jemand KI zu Hilfe nehmen muss.**

Ein Design, das nur in einer Installation existiert, ist einmal bezahlt
und einmal verwendet. Ein Theme ist ein Paket.

## Was in einer `.cto`-Datei steckt

Eine `.cto`-Datei ist ein ZIP-Archiv mit drei Teilen:

| Teil | Inhalt |
| --- | --- |
| `theme.xml` | Alle Datenbankdatensätze des Themes und seiner Bestandteile |
| `files/` | Die Dateien aus dem Upload-Verzeichnis, die beim Export zum Theme gehörten |
| `templates/` | Die eigenen Templates des Themes — nur vorhanden, wenn es welche gibt |

Daraus folgen drei Regeln, und alle drei werden regelmäßig übersehen:

### 1. Was das Theme braucht, muss vorher installiert sein

**Datensätze, die zu Tabellen oder Feldern einer nicht installierten
Erweiterung gehören, werden beim Import stillschweigend übergangen.**
Nicht abgebrochen, nicht gemeldet — übergangen. Das Theme importiert
scheinbar sauber und ist danach unvollständig.

Deshalb:

- **Das Theme führt eine Liste seiner Voraussetzungen**, mit
  Paketnamen und Versionsbereich, in `README.md` und in der
  Installationsanleitung — als Erstes, vor jedem anderen Schritt.
- **Je weniger Voraussetzungen, desto besser.** Ein Theme, das sechs
  Erweiterungen braucht, ist schwerer wiederzuverwenden als eines mit
  zwei.
- Wo möglich, wird eine Erweiterung ersetzt durch **Bordmittel**
  (`bordmittel.md`).
- **Nach dem Import wird geprüft**, ob alles da ist — nicht nur, ob der
  Import durchlief.

### 2. Templates in einen eigenen Unterordner

**Beim Import werden vorhandene Templates überschrieben.** Contao warnt,
aber die Warnung wird weggeklickt.

Deshalb liegen die Templates eines Themes in einem **eigenen
Unterordner** unter `templates/`, benannt nach dem Theme. Dann kann ein
Theme neben einem anderen bestehen, und ein Import zerstört keine fremde
Anpassung.

### 3. Ein Theme aus fremder Hand ist ein Sicherheitsthema

Ein Theme bringt Datensätze und Templates mit — beides kann Code
ausführen. **Nur aus vertrauenswürdiger Quelle importieren**, und vor dem
Import ansehen, was drin ist (Skill `neo-sicherheit`).

## Aufbau eines NEO-Themes

Ein Theme ist ein **eigenes Repository**, wie eine Erweiterung
(`erweiterungsbau.md`).

```
Contao-Theme-<Name>-by-NEO/
  theme/
    templates/neo_<name>/        eigene Templates, eigener Unterordner
    files/neo_<name>/            Bilder, Schriften, Symbole des Themes
    scss/                        Quellen, je Bereich und Bauteil eine Datei
    js/                          Quellen
  dist/
    neo_<name>.cto               Ausgabe des Exports, eingecheckt
  design/
    artboards/                   Entwurf aus Claude Design
    referenz/                    Referenzmessungen und -aufnahmen
  docs/
    en/                          Pflicht
    de/                          optional
  README.md
  CHANGELOG.md
```

- **Die Quellen liegen im Repository**, nicht nur in der Datenbank. SCSS,
  JavaScript, Templates, Bilder und der Entwurf sind versioniert.
- **Die `.cto` ist ein Erzeugnis, kein Original.** Sie wird aus der
  Installation exportiert und eingecheckt, damit jemand ohne Werkzeuge
  damit arbeiten kann. Nach jeder Designänderung wird sie neu erzeugt.
- **Layouts, Module und Bildgrößen bleiben in der Datenbank** — genau
  das nimmt der Export mit. Wer sie in eine Datei auslagert, gewinnt
  Versionierbarkeit und verliert die Exportierbarkeit. Das wäre eine
  Entscheidung des Projektinhabers, keine des Agenten.

## Vom Entwurf zum Theme

Die Gestaltung kommt fast immer aus **Claude Design**. Damit gilt der
gesamte Ablauf aus Skill `neo-design`, `references/claude-design.md` —
ohne Abstriche, weil es Contao ist:

1. **Inventar** aus dem Artboard, vor der ersten Zeile
   (`neo-design`, `references/claude-design.md`).
2. **Element für Element bauen**, nach jedem Element messen.
3. Gebaut wird in **Templates und SCSS**, nach den SCSS-Regeln
   (`scss.md`): je Bereich und Bauteil eine Datei, Verschachtelung,
   Schleifen, Berechnungen, Schichten.
4. **Jede Seitenvorlage** durchläuft die Messungen: Layout-, Stil- und
   Bildabgleich, dazu Überlauf und Textpassung auf acht Breiten
   (`/neo-design:neo-responsivpruefung`).
5. **Abweichungen sind Rückfragen**, nicht Entscheidungen des Agenten.

**Contao ist kein Grund für eine Abweichung.** Wo ein Contao-Element
nicht so aussieht wie im Entwurf, wird das Template angepasst — nicht der
Entwurf.

## Was ein Theme immer erfüllt

Zusätzlich zu allem, was für jede Seite gilt:

- **Alle Texte kommen aus der Datenbank**, kein fester Text im Template,
  Insert-Tags für Wiederkehrendes (`SKILL.md`).
- **Barrierefreiheit nach WCAG 2.2 AA**, geprüft und gerechnet — nicht
  vom Lighthouse-Wert abgeleitet (Skill `neo-design`,
  `references/barrierefreiheit.md`).
- **PageSpeed mobil je Seitenvorlage**: Best Practices und SEO 100,
  agentisches Browsen 3/3, Leistung und Barrierefreiheit mindestens 95
  (Skill `neo-design`, `references/messwerte.md`).
- **`llms.txt` und `llms-full.txt`** an der Domain-Wurzel — bei
  Webseiten Pflicht (`betrieb.md`).
- **Kein waagrechtes Scrollen, nichts ragt hinaus, keine Löcher, kein
  abgeschnittener Text** auf acht Breiten (Skill `neo-design`,
  `references/responsiv.md`, `references/textpassung.md`).
- **Impressum, Datenschutzerklärung, Barrierefreiheitserklärung** und
  ein Einwilligungsdialog, vor dem nichts von Dritten lädt (Skill
  `neo-recht`).
- **Schriften selbst ausgeliefert**, nicht von einem fremden Dienst.
- **Die Seite sieht nicht KI-gebaut aus** (Skill `neo-design`,
  `references/webseiten.md`).

## Dokumentation im Paket

Wie bei einer Erweiterung: **im Paket, nicht daneben.**

```
docs/en/
  README.md          Inhaltsverzeichnis
  installation.md    Voraussetzungen zuerst, dann Import, dann Prüfung
  requirements.md    Jede benötigte Erweiterung mit Paketname und Version
  structure.md       Layouts, Module, Bildgrößen, Templates — was wozu
  editing.md         Bedienung für die Redaktion, mit Screenshots
  customising.md     Welche SCSS-Variablen und Felder gedacht sind
  upgrading.md       Was sich je Fassung ändert
```

- Englisch ist Pflicht, Deutsch optional (Skill `neo-doku`).
- **Die Installationsanleitung ist so geschrieben, dass sie ohne KI
  funktioniert.** Wer sie liest, installiert das Theme — Schritt für
  Schritt, mit Screenshots, mit der Reihenfolge, in der es geht.
- Screenshots mit Markierungen, eingecheckt (Skill `neo-doku`,
  `references/screenshots.md`).

## Abnahme eines Themes

- [ ] `.cto` liegt in `dist/` und stammt vom aktuellen Stand.
- [ ] Der Export wurde **in einer frischen Installation importiert** und
      danach geprüft — nicht nur exportiert.
- [ ] Alle Voraussetzungen sind dokumentiert und waren vor dem Import
      installiert.
- [ ] Die Templates liegen in einem eigenen Unterordner.
- [ ] Kein fester Text im Template.
- [ ] Alle Messungen aus Skill `neo-design` bestanden, je Seitenvorlage.
- [ ] Rechtliche Pflichtseiten vorhanden (Skill `neo-recht`).
- [ ] Doku vollständig, englisch, im Paket.
- [ ] Jemand ohne KI konnte das Theme nach der Anleitung installieren —
      **nachgewiesen, nicht angenommen.**

## Belege

- Inhalt einer `.cto`-Datei (`theme.xml`, `files/`, `templates/`),
  Prüfungen beim Import, Übergehen von Datensätzen fehlender
  Erweiterungen, Überschreiben vorhandener Templates, Sicherheitshinweis:
  <https://docs.contao.org/5.x/manual/en/layout/theme-manager/manage-themes/>

Stand der Prüfung: 2026-08. **Vor dem Verlassen auf eine dieser Angaben
nachsehen** (Skill `neo-grundregeln`, Belegpflicht).
