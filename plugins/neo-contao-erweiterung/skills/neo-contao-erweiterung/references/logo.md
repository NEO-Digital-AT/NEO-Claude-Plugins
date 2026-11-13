# Logo im Contao Manager

Jede Erweiterung der Familie hat dasselbe Logo, nur das Icon wechselt
(Vorgabe des Inhabers vom 13.11.2026, Variante B). So erkennt man die
Erweiterungen im Contao Manager als Familie und unterscheidet sie trotzdem.

## Aufbau

- **Quadratisch (1:1)**, Kachel mit abgerundeten Ecken im Markenviolett
  `#2a025f`.
- **Das Icon** in Neongrün `#a8f20d`, groß, mit dünner Linie, leicht
  schräg gestellt. Es ragt links über die Kachel hinaus und ist am Rand des
  Logos abgeschnitten, nie außerhalb sichtbar.
- **Das NEO-Wort** (N, E und O aus der Marke) klein rechts unten, mit einem
  schmalen Rand in Kachelfarbe: Linien des Icons enden davor, statt durch
  die Buchstaben zu laufen.
- Kein weiterer Text im Logo. Den Namen zeigt der Contao Manager daneben.

Lage, Winkel, Größe, Strichstärke und Farben legt das Werkzeug fest; sie
werden pro Erweiterung nicht verändert.

## Name: englisch

Der Titel des Logos und der Eintrag im Contao Manager tragen den
**englischen Namen** der Erweiterung mit „NEO“ davor: „NEO Cookie
Consent“, „NEO Accessibility“, „NEO Website Check“, nicht „Cookie-Hinweis“
oder „Barrierefreiheit“. Das Werkzeug bekommt den Namen ohne „NEO“ und
lehnt Umlaute ab.

## Das Icon zeichnen

Eine SVG-Datei auf dem Raster 64 × 64 (`viewBox="0 0 64 64"`), mit Linien
gezeichnet, im Stil der vorhandenen Icons:

- Formen ohne Füllung: `path`, `rect`, `circle`, `ellipse`, `line`,
  `polyline`, `polygon`, gruppiert mit `g`. Das Werkzeug zieht sie in
  Neongrün mit derselben Strichstärke nach.
- Ein gefülltes Detail (Punkt, Stern): `fill="currentColor"`, es bekommt
  keinen Umriss.
- Eine Form, die Linien dahinter verdeckt (der Stift über dem Fenster):
  `fill="#2a025f"`, sie behält ihren Umriss.
- Keine eigenen Farben, Striche, Texte, Bilder, Stile oder Skripte. Das
  Werkzeug lehnt sie mit dem Grund ab und schreibt dann nichts.
- Das Motiv füllt das Raster etwa von 8 bis 56; wichtige Teile nicht an den
  linken Rand legen, dort wird abgeschnitten.

Die Quelle liegt in der Erweiterung unter `tools/contao-manager/icon.svg`,
das erzeugte Logo daneben als `logo.svg`. `tools/` gehört nicht zum Paket.

## Erzeugen

```
python3 plugins/neo-contao-erweiterung/scripts/module-logo.py \
  tools/contao-manager/icon.svg --name "Cookie Consent" \
  --out tools/contao-manager/logo.svg --preview /tmp/vorschau.html
```

Die Vorschau zeigt das Logo in der Listengröße des Contao Managers (48 px),
kleiner (32 px) und groß, auf hellem und dunklem Grund. Vor dem Einreichen
ansehen: Ist das Motiv in 32 px noch erkennbar? Läuft keine Linie durch das
NEO-Wort?

## Basic bekommt kein Logo

Basic ist ein Unterbau, im Contao Manager mit `dependency: true` aus der
Suche genommen. Es braucht kein Logo.

## Einreichen

Das Logo kommt mit `de.yml` und `en.yml` als `logo.svg` in den Pull
Request an `contao/package-metadata`
(`meta/neo-digital/<paket>/logo.svg`, siehe `veroeffentlichen.md`).
