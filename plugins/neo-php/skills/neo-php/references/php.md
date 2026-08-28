# PHP: Sprache und Werkzeuge

Lesekonvention siehe `SKILL.md`.

## Was in jeder Datei steht

```php
<?php

declare(strict_types=1);

namespace App\Auftrag;
```

**Ohne `strict_types` rechnet PHP still um.** `"5 Äpfel"` wird zu `5`,
ein `null` zu `0`, und der Fehler taucht drei Schichten später auf.

## Typen

- **Jeder Parameter, jeder Rückgabewert, jede Eigenschaft typisiert.**
- `mixed` ist eine Entscheidung mit Begründung, kein Standardfall.
- **Union- und Schnittstellentypen** nutzen, statt zu prüfen und zu raten.
- `never` für Methoden, die nie zurückkehren; `void` für die, die nichts
  liefern — nicht `null` zurückgeben.
- **Generics über die Anmerkung** der statischen Analyse, wo die Sprache
  sie nicht kennt: eine Liste ist `array<int, Auftrag>`, nicht `array`.

## Enums statt Zeichenketten

```php
enum Auftragsstatus: string
{
    case Offen = 'offen';
    case Erledigt = 'erledigt';
    case Storniert = 'storniert';

    public function istAbgeschlossen(): bool
    {
        return $this !== self::Offen;
    }
}
```

- **Ein Status ist nie eine Zeichenkette.** Ein Tippfehler in `'ofen'`
  fällt erst im Betrieb auf; ein Tippfehler im Enum fällt beim Übersetzen
  auf.
- Verhalten, das zum Wert gehört, steht **im Enum**, nicht in einer
  `match`-Kette an fünf Stellen.
- In Eloquent über `$casts`, in der Datenbank als Wert des Enums.

## Unveränderlich, wo möglich

```php
final readonly class Zeitraum
{
    public function __construct(
        public DateTimeImmutable $von,
        public DateTimeImmutable $bis,
    ) {
        if ($bis < $von) {
            throw new InvalidArgumentException('Ende liegt vor dem Beginn.');
        }
    }
}
```

- **Konstruktor-Eigenschaftsförderung** statt Zuweisungsblock.
- **`readonly`**, wo sich nichts ändern soll — das ist der Normalfall für
  Wertobjekte.
- **`final`**, solange keine Vererbung geplant ist. Wer erben will,
  begründet es.
- **Die Prüfung steht im Konstruktor.** Ein Objekt, das existiert, ist
  gültig.
- `DateTimeImmutable`, nie `DateTime`. Ein veränderliches Datum, das
  durch drei Methoden gereicht wird, ist eine Fehlersuche für später.

## Arrays sind keine Datenstrukturen

Ein assoziatives Array mit festen Schlüsseln ist eine Klasse, die noch
niemand geschrieben hat.

| Statt | Besser |
| --- | --- |
| `['name' => …, 'email' => …]` als Rückgabewert | ein Wertobjekt oder ein `readonly` DTO |
| `array` als Parametertyp | eine typisierte Liste, mit Anmerkung |
| Konfiguration als verschachteltes Array durchgereicht | ein Objekt mit benannten Eigenschaften |

Arrays bleiben richtig für: Listen gleichartiger Dinge, Daten auf dem Weg
nach draußen (JSON), Konfiguration in der Konfigurationsdatei.

## Ausnahmen

- **Ausnahmen für Ausnahmen**, nicht für erwartbare Fachfälle. „Kunde
  nicht gefunden" ist ein Ergebnis, kein Absturz (Skill `neo-code`).
- **Eigene Ausnahmeklassen** je Fachbereich, nicht `Exception` überall.
- **Die Meldung sagt, was zu tun ist**, und enthält keine Geheimnisse.
- **Nie `catch (\Throwable) {}`.** Ein verschlucktes Problem kommt später
  teurer wieder.

## Codestil und statische Analyse

| Was | Werkzeug | Regel |
| --- | --- | --- |
| Codestil | Laravel Pint oder PHP-CS-Fixer | maschinell, in der CI, nie in der Durchsicht besprochen |
| Statische Analyse | PHPStan oder Psalm | **hohe Stufe**, in der CI, als **Blocker** |
| Abhängigkeiten | Composer Audit | in der CI, bekannte Lücken brechen den Bau |

- **Die Stufe wird nicht gesenkt, um grün zu werden.** Das ist derselbe
  Regelverstoß wie eine abgeschwächte Testzusicherung.
- **Jede Unterdrückung trägt eine Begründung** in derselben Zeile. Eine
  Baseline-Datei ist eine Schuld mit Fälligkeitsdatum, keine Lösung.
- Der Stand wird berichtet: Stufe, Fehlerzahl, Zahl der Unterdrückungen.

## Composer

- **Versionsbereiche mit `^`**, kein festgenagelter Punkt in einer
  Bibliothek; in einer Anwendung entscheidet die Sperrdatei.
- **Die Sperrdatei ist eingecheckt.**
- **Kein `dev-master` in Produktion.**
- Jede neue Abhängigkeit wird **vorgelegt** — mit Zweck, Alternative,
  Pflegezustand und Lizenz (Skill `neo-grundregeln`).
- `require-dev` bleibt `require-dev`; in Produktion wird ohne installiert.

## PHP-Fassung

- **Die aktuelle unterstützte Fassung**, nicht die, die auf dem Server
  zufällig läuft. Der unterstützte Zeitraum wird nachgeschlagen, nicht
  erinnert.
- Die geforderte Fassung steht in `composer.json` und wird in der CI
  gegen genau diese geprüft.
- Ein Sprung auf eine neue Hauptfassung ist eine Änderung mit Auswirkung:
  vorlegen, testen, freigeben (Skill `neo-grundregeln`).
