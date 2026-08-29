# Die Brücke vom Entwurf in die Anwendung

Lesekonvention siehe `SKILL.md`.

> **Warum eine Webseite nach dem Entwurf aussieht und eine Anwendung
> nicht.**

Der Unterschied ist strukturell, nicht handwerklich, und er erklärt den
ganzen Frust:

| | Was passiert | Ergebnis |
| --- | --- | --- |
| **Webseite** | Die Ausgabe des Entwurfswerkzeugs **ist** das Ergebnis: HTML und CSS gehen unverändert hinüber | trifft |
| **Anwendung** | Jemand **übersetzt** HTML und CSS in Widgets, Views oder Composables | schweift ab |

Für diese Übersetzung gibt es keine mechanische Abbildung. Und **wo eine
Abbildung fehlt, wird erfunden** — nicht aus Nachlässigkeit, sondern weil
etwas eingesetzt werden muss und der Entwurf die Frage nicht beantwortet.

**Mehr Prompts beheben das nicht.** Hundert Prompts sind hundert
Erfindungen. Es hilft nur zweierlei:

1. **Ein Vertrag statt einer Beschreibung** — Tokens.
2. **Eine Messung statt eines Blicks** — ein roter Test.

## 1. Der Vertrag: was ein Token sein muss

**Was nicht als Token existiert, darf in der Oberfläche nicht
vorkommen.** Kein Zahlenwert in einer View, keine Farbe, kein Abstand.

| Was | Beispiel eines Tokens |
| --- | --- |
| Farbe je Rolle | Fläche, Vordergrund, Umriss, Zustand, Fehler |
| Abstandsskala | 4, 8, 12, 16, 24, 32, 48 |
| Radien | klein, mittel, groß |
| Schriftmaße mit Zeilenhöhe | je Textrolle, nie einzeln |
| **Bedienhöhen** | die Höhe, die ein Knopf tatsächlich hat |
| Höchstbreiten | Inhaltsbereich, Textspalte, Eingabefeld |
| Schatten und Erhebung | je Stufe |
| Bewegungsdauer und Kurve | je Art des Übergangs |

Die **Bedienhöhen sind der am häufigsten vergessene Teil** — und genau
der, an dem eine Oberfläche „irgendwie anders" aussieht, obwohl alle
Farben stimmen.

- **Eine Quelle.** Die Tokens entstehen im Entwurf, nicht im Code.
- **Ein Erzeugungsschritt** schreibt sie in die Zielsprache — als
  erzeugte Datei, mit einem Kopf, der sagt „nicht von Hand ändern".
- **Die erzeugte Datei ist eingecheckt**, und der Erzeugungsschritt läuft
  in der CI: **weicht das Ergebnis ab, ist der Bau rot.** Sonst driftet
  der Code vom Entwurf weg, und niemand merkt es.
- **Kein zweiter Ort.** Ein Wert, der im Entwurf und noch einmal im Code
  steht, steht bald verschieden da.

## 2. Die Messung: je Ziel ein Werkzeug

Ein Bildschirm gilt als umgesetzt, wenn die Messung grün ist — nicht,
wenn er richtig aussieht.

| Ziel | Womit gemessen wird |
| --- | --- |
| Browser | `layout-diff.js`, `style-audit.js`, `image-diff.py` (`designsystem-abgleich.md`) |
| Flutter | **Golden-Tests** (`matchesGoldenFile`) |
| Jetpack Compose | Screenshot-Tests (Compose Preview Screenshot Testing, Paparazzi, Roborazzi) |
| SwiftUI | Snapshot-Tests |

## 3. Die Aufnahme aus dem Entwurf ist das Soll

Der übliche Einsatz einer goldenen Aufnahme misst **Rückschritt**: Man
nimmt den zuletzt genehmigten Stand auf und merkt, wenn er sich ändert.
Das ist nützlich — beantwortet aber nicht die Frage, um die es hier geht.

**Umgedreht wird daraus die Brücke:**

> Die goldene Aufnahme ist der **Export aus dem Entwurf**, nicht der
> zuletzt gebaute Stand. Der Test ist rot, solange der Bildschirm dem
> Entwurf nicht entspricht — und wird grün, wenn er es tut.

Damit ist „sieht aus wie im Entwurf" kein Streitpunkt mehr, sondern ein
Testergebnis. Genau das verlangt Kernregel 10: **Fertig heißt gemessen.**

Damit die Messung etwas aussagt, werden die Bedingungen festgehalten und
sind in Entwurf und Test **dieselben**:

- Gerätegröße und Bildmaßstab
- Farbschema (hell/dunkel) und Sprache
- Schriften geladen, **vor** der Aufnahme
- Bewegung abgeschaltet
- **Feste Testdaten** — dieselben Namen, dieselben Beträge, dasselbe
  Datum
- Eine benannte **Toleranz**, nicht null: Kantenglättung unterscheidet
  sich zwischen Rechnern

## 4. Der Ablauf je Bildschirm

```
1  Entwurf freigegeben            (entwurfsverfahren.md)
2  Tokens erzeugt                 eine Quelle, erzeugte Datei eingecheckt
3  Bildschirm gebaut              ausschließlich aus Tokens
4  Goldene Aufnahme gelegt        aus dem Entwurf, nicht aus dem Bau
5  Test läuft, bis grün           Abweichung als Zahl, nicht als Gefühl
6  Fertigmeldung                  mit der Zahl, nicht mit „passt"
```

**Schritt 4 vor Schritt 5, und beide vor der Fertigmeldung.** Wer die
goldene Aufnahme aus dem eigenen Bau erzeugt, hat sich selbst bestätigt
und nichts gemessen.

## Was das nicht ist

- **Keine Pixeljagd auf dynamischen Inhalten.** Gemessen wird der Rahmen
  — Anordnung, Maße, Farben, Typografie —, nicht ein Betrag, der aus der
  Datenbank kommt. Bereiche mit veränderlichem Inhalt werden ausgenommen
  und die Ausnahme wird benannt.
- **Kein Ersatz für den Entwurf.** Ein Test kann nur prüfen, was
  entworfen wurde. Fehlt ein Zustand im Entwurf — Fehler, leer, ladend —,
  fehlt er auch im Test (`entwurfsverfahren.md`).
- **Kein Ersatz für den Durchgang.** Ein Bildschirm kann pixelgenau
  stimmen und trotzdem unbedienbar sein (`responsiv.md`,
  `barrierefreiheit.md`).

## Wenn es trotzdem nicht passt

Bevor der nächste Prompt geschrieben wird, wird die Ursache benannt:

| Beobachtung | Ursache, fast immer |
| --- | --- |
| Farben stimmen, alles wirkt „zu luftig" oder „zu eng" | Abstände und Bedienhöhen sind keine Tokens |
| Einzelne Bildschirme stimmen, das Ganze wirkt uneinheitlich | Zweiter Ort für Werte, Erzeugungsschritt läuft nicht in der CI |
| Der Bildschirm sieht anders aus als der Entwurf, niemand weiß wo | Keine Messung — es wird verglichen, was man gerade ansieht |
| Nach jeder Änderung verschiebt sich etwas anderes | Werte in den Views statt in der Komponente (Skill `neo-komponenten`) |

**Ein Prompt, der eine Abweichung beschreibt, ist der teuerste Weg.** Ein
Test, der sie misst, ist der billigste.

## Abnahme

- [ ] Es gibt **eine** Tokenquelle; die erzeugte Datei ist eingecheckt.
- [ ] Der Erzeugungsschritt läuft in der CI und ist bei Abweichung rot.
- [ ] Kein Zahlenwert, keine Farbe in einer View — alles aus Tokens.
- [ ] **Bedienhöhen sind Tokens**, nicht Einzelwerte.
- [ ] Je Bildschirm eine goldene Aufnahme, **aus dem Entwurf** gelegt.
- [ ] Aufnahmebedingungen festgehalten und in Entwurf und Test gleich.
- [ ] Toleranz benannt; ausgenommene Bereiche benannt und begründet.
- [ ] Die Abweichung wird als **Zahl** berichtet, nicht als „passt".
