# Ladezeit und Stabilität: der Referenzaufbau

**Vorgabe Erich Nigg, 20.10.2026:** Der Aufbau von
`ergotherapie-schumann.at` ist die Referenz für jede NEO-Website. Jede
neue Seite übernimmt alle Bausteine dieser Datei. Bei einer bestehenden
Seite werden sie beim nächsten Auftrag an der Seite nachgezogen.

Ergebnis dort, PageSpeed Insights mobil (Moto G Power, langsames 4G),
20.10.2026:

| Leistung | Barrierefreiheit | Best Practices | SEO | Agentisches Browsen |
| --- | --- | --- | --- | --- |
| 98 | 100 | 100 | 100 | 3/3 |

| First Contentful Paint | Largest Contentful Paint | Total Blocking Time | Cumulative Layout Shift | Speed Index |
| --- | --- | --- | --- | --- |
| 0,9 s | 2,4 s | 0 ms | 0,017 | 1,7 s |

Quellen: Website `NEO-Digital-AT/Customer_ergotherapie-schumann.at_Contao_2026-10-19`,
Theme `NEO-Digital-AT/Customer_ergotherapie-schumann.at_Contao_2026-10-19_Theme`.
Übernommen wird der Aufbau, nicht die Gestaltung.

## Die Bausteine

| Nr. | Baustein | Kurzregel |
| --- | --- | --- |
| 1 | Skripte | Genau eine Skriptdatei je Seite, mit `defer` |
| 2 | Stylesheets | Kleine Bündel ins HTML einbetten; Spätes erst nach dem Laden |
| 3 | Schriften | Selbst ausgeliefert, beschnitten, nur der erste Bildschirm vorgeladen |
| 4 | Bühnenbild | Vorgeladen mit `fetchpriority="high"`, Größen aus Contao |
| 5 | Abschnitte unterhalb | `content-visibility: auto` mit gemessener Schätzhöhe |
| 6 | SVG | Ohne Metadaten, gerundet, ohne Kurvennäherung |
| 7 | Neuladen | Die Scrollposition bleibt auf den Pixel gleich |
| 8 | Webserver | Komprimiert, Stempel in der Adresse, lange Haltbarkeit |

## 1. Skripte: eine Datei je Seite, mit `defer`

**Jede Seite lädt genau eine Skriptdatei** (Vorgabe Erich Nigg). Was
jede Seite braucht (Kopfzeile, Menü, Barrierefreiheits-Werkzeug,
Einwilligung), liegt in einem Grundmodul; jede Seitengattung hat eine
eigene Einstiegsdatei, die das Grundmodul **importiert**:

```
theme/js/modules/base.js   Grundmodul: initBase(), onReady()
theme/js/site.js           Inhaltsseiten: nur das Grundmodul
theme/js/home.js           Startseite: Grundmodul + Zeitleiste, FAQ, Formular …
```

Der Bündler (esbuild) macht aus jeder Einstiegsdatei genau eine Datei.
Im Contao-Layout steht genau **eine** davon.

- **Der Fehler, der vorkam:** Das Startseiten-Layout wählte `site.js` und
  `home.js`. Beide waren gebündelt, die Seite stellte trotzdem zwei
  Anfragen. Gebündelt heißt: eine Datei auf der Seite, nicht eine Datei
  je Quelle.
- Eine bestehende Datenbank wird per Migration umgestellt, und nur, wenn
  das Layout noch exakt die alte Kombination trägt
  (`LayoutScriptMigration` im Referenzprojekt).

**`defer` setzt das Seiten-Template.** Contao schreibt die im Layout
gewählten Skripte als `<script src="…">` ohne `defer` ans Seitenende
(`PageRegular`, `Template::generateScriptTag()`). Chrome lädt ein solches
Skript mit erhöhter Priorität vor Bühnenbild und Schriften, und
Lighthouse führt es im „Netzwerkabhängigkeitsbaum" als kritische
Anfrage. Der Kern bleibt unverändert; das Theme-Template ergänzt
`defer`, **außerhalb jedes Blocks**:

```twig
{% extends '@Contao/fe_page.html.twig' %}

{% set mootools = mootools|replace({'<script src="': '<script defer src="'}) %}
```

Ein `set` außerhalb der Blöcke eines erbenden Twig-Templates gilt im
Kontext der Elternvorlage, die `{{ mootools|… }}` ausgibt. Jedes
Seiten-Template des Themes trägt diese Zeile. Das Skript läuft mit
`defer` zum selben Zeitpunkt wie vorher (nach dem Einlesen, vor
`DOMContentLoaded`); es muss trotzdem DOM-bereit-sicher geschrieben sein
(`onReady()` prüft `document.readyState`).

## 2. Stylesheets

**Kleine Bündel werden ins HTML eingebettet.** Ein Antwort-Listener
(`InlineStylesheetListener`, `kernel.response`, Priorität −490, vor dem
HTML-Minifizierer bei −500 und dem Mail-Schutz bei −512) ersetzt jeden
`<link rel="stylesheet">` auf eine Datei des Theme-Ordners durch
`<style>`. Relative Adressen im CSS werden absolut; der HTTP-Cache von
Contao speichert das Ergebnis. Im Referenzprojekt sind es zwei Bündel
mit je 8–9 KB komprimiert; die Zusatzbytes je Seite kosten weniger als
die Rundreise, auf die ein Telefon sonst vor dem ersten Bild wartet.

Bei großen Bündeln wird nur der erste Bildschirm eingebettet und der
Rest nachgeladen: Verfahren `CriticalCssListener` in
`NEO-Digital-AT/website`.

**Was der erste Bildschirm nicht braucht, kommt nach dem Laden.** Im Kopf
des Seiten-Templates:

```twig
<noscript data-late-styles><link rel="stylesheet" href="{{ italic }}"></noscript>
```

Ein Modul (`late-styles.js`) fügt den Inhalt nach `load` im Leerlauf ein
(`requestIdleCallback`, sonst 200 ms); ohne JavaScript greift das
`<noscript>`. Im Referenzprojekt betrifft das die kursive Literata
(67 KB), die erst weiter unten vorkommt.

## 3. Schriften

- **Selbst ausgeliefert**, WOFF2 (Skill `neo-recht`).
- **Beschnitten** mit fontTools (`tools/subset-fonts.py` im Theme): je
  Schnitt eine Datei mit den Zeichen deutscher Texte und eine
  Ergänzungsdatei mit dem Rest, verbunden über `unicode-range`. Der
  Browser lädt die Ergänzung nur, wenn ein Text ein solches Zeichen
  enthält. Behalten werden die OpenType-Merkmale, die Browser von selbst
  anwenden, plus die tatsächlich genutzten (`tnum`). Variable Achsen
  werden auf den genutzten Bereich begrenzt, Glyph für Glyph gegen das
  Original geprüft.
- **Vorgeladen werden nur die Schnitte des ersten Bildschirms**, je
  Seitengattung als Liste im Seiten-Template, mit `crossorigin` und mit
  exakt der Adresse aus dem Stylesheet (einschließlich `?v=…`). Eine
  Vorladung, die die Seite nicht nutzt, erzeugt eine Konsolenwarnung und
  kostet Best Practices.

## 4. Bühnenbild

- Größen und Formate (AVIF, WebP) aus den Contao-Bildgrößen, nie aus dem
  Build.
- Das Inhaltselement der Bühne lädt das Bild vor:

```twig
{% set lcp = image.image.sources|first %}
{% add 'hero_preload' to head %}
    <link rel="preload" as="image" imagesrcset="{{ lcp.srcset }}" imagesizes="{{ lcp.sizes }}" type="{{ lcp.type }}" fetchpriority="high">
{% endadd %}
```

- Am `<img>` selbst `fetchpriority="high"`, kein `loading="lazy"`,
  `width`/`height` gesetzt.
- **„Bildübermittlung verbessern" ist hier kein Fehler.** Lighthouse
  vergleicht die geladene Datei mit der angezeigten Größe **ohne die
  Pixeldichte** des Testgeräts (1,75×): 500 px Datei für 277 px Anzeige
  sind richtig, nötig sind 485 px. Eine kleinere Datei wird am Telefon
  unscharf. Nicht „beheben"; im Bericht so benennen.

## 5. Abschnitte unterhalb des ersten Bildschirms

```scss
main > section:not(:first-child),
.ds-footer {
  content-visibility: auto;
  contain-intrinsic-size: auto 2600px;   // höchster Abschnitt am Telefon
}
```

- **Die Schätzhöhe ist mindestens so hoch wie der höchste Abschnitt am
  Telefon — gemessen, nicht geschätzt.** Im Referenzprojekt stand sie auf
  1500 px, der Kontaktbereich ist am Telefon rund 2300 px hoch. Lighthouse
  mobil meldete daraufhin zu wenig Kontrast (Barrierefreiheit 97): In der
  Schätzung ragte ein Knopf in den nächsten Abschnitt. Kein echter
  Farbfehler, aber ein echter Punktverlust.
- `auto` merkt sich die echte Höhe, sobald ein Abschnitt einmal angezeigt
  war.
- Skripte lesen beim Laden keine Größen (`getBoundingClientRect`,
  `offsetHeight`, `scrollY`); sie nutzen `IntersectionObserver` oder
  warten den ersten Bildaufbau ab. Jeder Lesezugriff erzwingt das Layout
  der übersprungenen Abschnitte.

## 6. SVG-Grafiken

Grafikprogramme schreiben Herkunftsdaten (C2PA-Manifest) und Koordinaten
mit sieben Nachkommastellen in die Datei. Gemessen, übertragen mit gzip:

| Datei | vorher | nachher |
| --- | --- | --- |
| Logo im Kopf | 25,3 KB | 13,5 KB |
| Bildmarke (Maske im Fuß) | 16,4 KB | 6,6 KB |
| Fremdlogo (Auszeichnung) | 7,3 KB | 4,7 KB |

- Optimiert mit SVGO und der Konfiguration `tools/svgo.config.mjs` des
  Referenz-Themes: Metadaten und Editor-Daten entfernt, vier
  Nachkommastellen, Pfaddaten nur verlustfrei gekürzt.
- **Nicht das SVGO-Standardpaket verwenden.** Es nähert Kurven an
  (`convertToQ`, `makeArcs`, `straightCurves`) und entfernt kurze
  Segmente; das verschob Kanten bis zu einem Pixel. Abgeschaltet:
  `convertToQ`, `makeArcs`, `straightCurves`, `curveSmoothShorthands`,
  `removeUseless`, `convertToZ`, `collapseRepeated`.
- **Belegt wird mit einem Pixelvergleich:** alt und neu bei 120, 289, 600
  und 1200 px Breite auf hellem und dunklem Grund rendern. Zulässig sind
  Abweichungen der Kantenglättung an einzelnen Pixeln.
- Liegt die Datei im Redaktionsordner (`files/media`), tauscht eine
  Migration sie aus — nur solange ihr SHA-1 dem der alten Seed-Datei
  entspricht. Name und UUID bleiben, danach `DbafsManager::sync()`
  (`MediaLogosMigration` im Referenzprojekt). Eine von der Redaktion
  ersetzte Datei bleibt unangetastet.

## 7. Neuladen: die Scrollposition bleibt

Chrome stellt die Position nach dem Neuladen über ein **Bezugselement**
wieder her (Scroll Anchoring). Wählt es dafür ein bewegtes Element — eine
treibende Hintergrundform — oder die Hauptüberschrift der Bühne, steht
die Seite danach daneben. Gemessen im Referenzprojekt ab 1024 px Breite: 9 bis
35 px tiefer, **auch ganz oben** (0 → 19 px).

```scss
.ds-organic { overflow-anchor: none; }   // bewegte Dekoration
.site-hero  { overflow-anchor: none; }   // Bühne des ersten Bildschirms
```

Das Verankern bleibt für alle übrigen Abschnitte an — das braucht
`content-visibility` (Baustein 5), damit beim Hochscrollen nichts
springt.

**Weiches Scrollen erst nach dem Laden.** `scroll-behavior: smooth` am
`html` gilt auch für die Wiederherstellung: Der Browser fuhr die alte
Stelle sichtbar von oben an.

```scss
html[data-smooth-scroll] { scroll-behavior: smooth; }

@media (prefers-reduced-motion: reduce) {
  html, html[data-smooth-scroll] { scroll-behavior: auto; }
}
```

```js
// modules/smooth-scroll.js, im Grundmodul aufgerufen
export function initSmoothScroll() {
  const enable = () => requestAnimationFrame(() => setTimeout(() => {
    document.documentElement.setAttribute('data-smooth-scroll', '');
  }));
  if (document.readyState === 'complete') enable();
  else window.addEventListener('load', enable, { once: true });
}
```

Sprünge über Links innerhalb der Seite scrollen danach weiter weich. Ein
Modus „Animationen stoppen" im Barrierefreiheits-Werkzeug setzt
`scroll-behavior: auto` auch am `html` selbst, nicht nur an dessen
Nachfahren.

**Neues bewegtes Element im ersten Bildschirm → `overflow-anchor: none`.**

## 8. Webserver

- gzip (Stufe 6) für HTML, CSS, JavaScript, JSON, JSON-LD und
  **`image/svg+xml`**.
- Dateien mit Stempel in der Adresse (`?v=<Inhaltsprüfsumme>`):
  `max-age=31536000, immutable`; ohne Stempel 30 Tage. Contaos
  Bildvarianten unter `assets/images/`: ein Jahr.
- HTML minifiziert (Antwort-Listener), HTTP-Cache von Contao aktiv; nach
  dem Ausrollen wird er geleert.

## Prüfung nach jedem Ausrollen

| Prüfung | Soll |
| --- | --- |
| PageSpeed Insights mobil, je Seitenvorlage | Werte nach Skill `neo-design`, `references/messwerte.md` |
| Skriptdateien des Themes je Seite | genau 1, mit `defer` |
| Konsole beim Laden und bei der Bedienung (Einwilligung, Menü, Formular) | leer |
| Neuladen bei 0, 120, 300, 700, 1500, 3000 px, Breiten 390 bis 1920 | sichtbarer Inhalt verschiebt sich um 0 px |
| Positionen während der Wiederherstellung | 1 (keine Fahrt) |
| Sprung über einen Link innerhalb der Seite | weich |
| Übertragene Größen (`curl -H 'Accept-Encoding: gzip' -w '%{size_download}'`) | wie im Build erwartet, komprimiert |

**Der Neuladetest** (Playwright): Position anfahren, Lage aller
Überschriften, Absätze und Bilder im Fenster merken, neu laden, erneut
messen, Differenz bilden. `window.scrollY` allein reicht nicht — die
Seite kann nach dem Laden anders hoch sein, entscheidend ist, ob der
**sichtbare Inhalt** an derselben Stelle steht.

**Lighthouse aus einer Sandbox ist kein Leistungsbeleg.** Läuft der
Browser über einen Proxy mit HTTP/1.1 und auf langsamer CPU, meldet
Lighthouse fehlendes HTTP/2 und hohe Blockierzeiten, die die Seite nicht
hat. Leistungswerte kommen aus PageSpeed Insights; lokal werden die
Ursachen untersucht, nicht die Zahl berichtet.
