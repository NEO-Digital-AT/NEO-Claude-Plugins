# Material Design 3 in Flutter

Lesekonvention siehe `SKILL.md`.

> **Vor dem Schreiben lesen:** <https://docs.flutter.dev/llms.txt> und
> <https://m3.material.io>. Geprüft 2026-08.

Material 3 wird **als System** übernommen — Farbrollen, Typografiestufen,
Formstufen, Zustandsdeckschichten — nicht als Sammlung einzelner Werte.
Gestaltet wird nichts selbst: **Variablen sind nur Farbe und Größe.**

## Was Flutter liefert und was nicht

Flutter setzt die **M3-Baseline** um, nicht die Expressive-Ausbaustufe.
Wer die Expressive-Größen braucht, setzt sie als `ButtonStyle` — aber
**ausschließlich mit den Original-Werten** der Referenzimplementierung
(Jetpack Compose Material3, generierte Tokens; offizielle API
`ButtonDefaults.textStyleFor` / `iconSizeFor` / `contentPaddingFor`), nie
mit selbst gewählten Zahlen.

Tasten sind dort **über die Höhe** parametrisiert:

| Klasse | Höhe | Beschriftung | Symbol | Randabstand | Form |
| --- | --- | --- | --- | --- | --- |
| M | 56 ≤ h < 96 | `titleMedium` | 24 | 24 | corner.large (16) |
| L | 96 ≤ h < 136 | `headlineSmall` | 32 | 48 | corner.extra-large (28) |

**Klasse L ist die EINE Abschluss-Taste je Bildschirm** — zwei davon
nebeneinander gibt es nicht.

## Skalen sind geschlossen

- **Symbolgrößen** nur 20 / 24 / 32 / 40.
- **Eckenradien** nur 0 / 4 / 8 / 12 / 16 / 28 / voll — die Baseline.
  Die erhöhten Stufen 20, 32 und 48 gehören zur Expressive-Ausbaustufe
  und gelten nur, wenn das Projekt sie ausdrücklich führt.
- **Höhenstufen** nur 0 / 1 / 3 / 6 / 8 / 12 dp. Die Stufe ist der
  Schatten: „sieht anders aus" ist fast immer die falsche Stufe, nicht
  die falsche Weichzeichnung.
- **Zustandsdeckschichten** nur 8 % (Überfahren), 10 % (Fokus), 10 %
  (Gedrückt), 16 % (Gezogen).
- **Textrollen** nur aus der Typoskala; eine eigene Größe gibt es nicht.
- **Karten, Textfelder, Dialoge**: die Flutter-Vorgaben SIND das
  Original — nicht überschreiben.

Eine Zahl außerhalb dieser Skalen ist ein Fehler, kein Feinschliff.

Die Zahlen stammen aus `androidx.compose.material3.tokens`
(`ShapeTokens.kt`, `ElevationTokens.kt`, `StateTokens.kt`,
<https://android.googlesource.com/platform/frameworks/support/>, geprüft
2026-08-29) — der von Google aus dem Tokensatz erzeugten
Referenzumsetzung. Ein Beispiel aus einer Anleitung ist keine Skala:
Googles eigene Compose-Anleitung zeigt ein Beispielschema mit 24 dp für
`extraLarge`, der Token ist 28 dp.

**Flutter führt diese Skalen nicht als Schnittstelle.** In der
Material-Bibliothek gibt es `Durations` und `Easing`, aber keine Formen-
und keine Höhenskala (api.flutter.dev, geprüft 2026-08-29); die Werte
stecken in den Vorgaben der einzelnen Widgets. **Was das Ziel nicht
führt, führt das Projekt** — als Tokendatei aus dem Erzeugungsschritt,
nie als Zahl im Widget. Geprüft wird sie maschinell:

```
python3 plugins/neo-design/scripts/md3-token-check.py lib/theme/ \
        --scale baseline
```

Null Befunde, sonst ist der Bau rot (Skill `neo-design`,
`references/entwurfsbruecke.md`, Abschnitt 2).

## Das Theme ist der einzige Ort

- **Kein `fontSize:`, keine Hex-Farbe, kein Radius im Bildschirmcode.**
  Farben kommen aus dem Farbschema, Größen aus dem Theme oder aus einem
  Baustein (Skill `neo-komponenten`).
- **Hell und dunkel an einer Stelle**, aus denselben Tokens erzeugt.
- Eine Design-Änderung passiert **an genau einer Stelle** — wenn dafür
  mehrere Dateien angefasst werden müssen, war der Aufbau falsch.
- **Maschinell durchsetzen**: ein Wächter-Test, der `fontSize:` und
  Hex-Farben in Bildschirmdateien verbietet, hält die Regel wach
  (Skill `neo-komponenten`, `references/waechter.md`).

## Bekannte Lücken des Rahmens

Manche Theme-Felder wirken nicht — Flutter ignoriert zum Beispiel
`DialogThemeData.actionsAlignment` und fällt hart auf rechtsbündig
zurück. **Solche Lücken werden EINMAL in einem eigenen Baustein
geschlossen**, nicht an jedem Aufrufort erneut. Der Baustein trägt den
Grund als Kommentar, damit niemand ihn später „aufräumt".

## Lesbarkeit ist eine Größenentscheidung

Die Typoskala bleibt Original — **welche Rolle** eine Fläche trägt, ist
die Variable. Für Geräte, die auf Abstand bedient werden (Kasse, Theke,
Werkstatt), gilt: Menü- und Listeneinträge sind Griffe, keine Fußnoten.
Wird eine Rolle angehoben, geschieht das zentral im Theme und wird durch
einen Test festgehalten, damit sie nicht stillschweigend zurückrutscht.

## Prüfen

- Bei **kleinster und größter Systemschrift**, hell und dunkel.
- Nach jeder Theme-Änderung: die Bildschirme, die die Rolle benutzen.
- Abweichungen vom Designsystem sind **Rückfragen**, keine
  Entscheidungen (Skill `neo-design`, `references/claude-design.md`).
