# Flutter und Dart

Maßgeblich sind **Effective Dart** (Style, Documentation, Usage, Design)
und der Regelsatz `flutter_lints`, eingebunden über
`analysis_options.yaml`.

## Benennung und Dateien

- `lowercase_with_underscores` für Dateien, Ordner und Pakete.
- `UpperCamelCase` für Typen, `lowerCamelCase` für alles andere.
- Ein Widget je Datei, Dateiname passend zum Widget.
- Keine Sammelimporte über `part`/`part of` außer für erzeugten Code.

## Widgets

- **Zusammensetzen statt vererben.** Ein eigenes Widget entsteht durch
  Komposition, nicht durch Ableiten von einem fremden Widget.
- **`const` überall, wo es geht.** Ein `const`-Konstruktor spart einen
  Neuaufbau und ist der billigste Leistungsgewinn im ganzen Baum.
- **Kleine Widgets statt großer `build`-Methoden.** Eine `build`-Methode,
  die man scrollen muss, wird geteilt — in eigene Widget-Klassen, nicht
  in Methoden, die Widgets zurückgeben: nur eigene Klassen lassen sich
  einzeln neu aufbauen.
- `Key` setzen, wo Elemente ihre Position in einer Liste tauschen können.
- Kein Layoutwert aus der Luft: Größen, Abstände und Farben kommen aus
  Theme und Tokens (Skill `neo-komponenten`).
- Bei NEO ruft ein Screen nur Komponenten der Produktfamilie auf, nie
  Material-Widgets direkt.

## Zustand

- Der Zustand liegt so tief wie möglich und so hoch wie nötig.
- `setState` für lokalen Zustand eines Widgets. Für alles, was mehrere
  Bildschirme sehen, die im Projekt festgelegte Zustandslösung — eine,
  nicht drei.
- Keine Geschäftslogik in `build`. `build` kann jederzeit und mehrfach
  laufen.
- Controller, Abonnements und Zeitgeber werden in `dispose` freigegeben.
  Ein vergessener Controller ist ein Speicherleck, das erst nach
  Stunden auffällt.

## Asynchronität

- `async`/`await`, keine verschachtelten `then`-Ketten.
- **Nach einem `await` nie ungeprüft `context` verwenden** — das Widget
  kann inzwischen weg sein (`if (!mounted) return;`).
- Fehler werden behandelt, nicht verschluckt; ein `Future` ohne
  Fehlerpfad ist unfertig.

## Struktur

```
lib/
  main.dart
  app/            Einstieg, Routen, Theme
  features/<name>/
    data/         Quellen, Modelle, Repositories
    domain/       Fachlichkeit
    presentation/ Screens und Widgets
  shared/
    widgets/      Komponenten der Produktfamilie
    utils/
```

Der Schnitt nach Funktionsbereich schlägt den Schnitt nach Technik: alles
zu einem Thema liegt beieinander.

## Werkzeuge

- `analysis_options.yaml` mit `flutter_lints`, Warnungen als Fehler, wo
  möglich.
- `dart format` maschinell, in der CI geprüft.
- `flutter analyze` als CI-Blocker.
- Tests: Widget- und Integrationstests für **jedes** Bedienelement
  (Skill `neo-grundregeln`, Abschnitt Tests). Ein Knopf ohne Test gilt
  als ungetestet, auch wenn die Logik dahinter getestet ist.
