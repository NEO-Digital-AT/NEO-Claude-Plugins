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
Erfindungen. Es hilft nur viererlei:

1. **Ein Wertvertrag** — Tokens.
2. **Ein Systemvertrag** — wessen Wert gilt, wenn Entwurf und
   Designsystem auseinandergehen.
3. **Ein Bauteilvertrag** — der Entwurf benennt die Komponente.
4. **Eine Messung statt eines Blicks** — ein roter Test.

## 1. Der Wertvertrag: was ein Token sein muss

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

- **Eine Quelle.** Die Tokens entstehen im Entwurf, nicht im Code —
  **mit Ausnahme der Werte, die dem Designsystem gehören**
  (Abschnitt 2).
- **Ein Erzeugungsschritt** schreibt sie in die Zielsprache — als
  erzeugte Datei, mit einem Kopf, der sagt „nicht von Hand ändern".
- **Die erzeugte Datei ist eingecheckt**, und der Erzeugungsschritt läuft
  in der CI: **weicht das Ergebnis ab, ist der Bau rot.** Sonst driftet
  der Code vom Entwurf weg, und niemand merkt es.
- **Kein zweiter Ort.** Ein Wert, der im Entwurf und noch einmal im Code
  steht, steht bald verschieden da.

## 2. Der Systemvertrag: wessen Wert gilt

**Ein Entwurfswerkzeug zeichnet ein Designsystem nach. Es setzt es nicht
um.** Was aus Claude Design kommt, sieht aus wie Material 3 — es ist
nicht Material 3. Radien, Schatten, Deckschichten und Bewegung liegen
nahe an der Vorlage, aber nicht auf ihr.

Das ist kein Vorwurf an das Werkzeug. Es zeichnet HTML und CSS; niemand
hat ihm gesagt, dass diese Ecke 28 dp haben muss und nicht 24. Zum
Problem wird es erst durch Abschnitt 1: Wenn die Tokens aus dem Entwurf
kommen und der Entwurf danebenliegt, **baut die Anwendung die
Ungenauigkeit des Werkzeugs sauber nach** — und zwar dauerhaft, weil sie
jetzt in der einen Quelle steht.

Deshalb hat der Wertvertrag zwei Seiten mit verschiedenen Eigentümern:

| Wert | Wem er gehört |
| --- | --- |
| Markenfarben und ihre Rollen | dem **Entwurf** |
| Anordnung, Raster, Abstandsrhythmus je Bildschirm | dem **Entwurf** |
| Welche Komponente wo steht, Inhalt, Reihenfolge | dem **Entwurf** |
| Eckenradien | dem **System** |
| Höhenstufen und die Schatten dazu | dem **System** |
| Zustandsdeckschichten | dem **System** |
| Größenklassen der Komponenten | dem **System** |
| Bewegungsdauern und -kurven | dem **System** |
| Typoskala | dem **System** |

> **Der Entwurf bestimmt, welche Komponente wo steht und welche Farbe sie
> trägt. Das System bestimmt, wie sie aussieht.**

- **Systemwerte werden aus der Quelle des Systems übernommen**, nicht aus
  dem Export abgemessen. Eine abgemessene Ecke ist eine Behauptung, ein
  Token der Referenzumsetzung ist der Wert.
- **Der Erzeugungsschritt aus Abschnitt 1 hat damit zwei Eingänge:** die
  Werte des Entwurfs und die Werte des Systems. Nur so kann die
  Ungenauigkeit nicht durchrutschen. Hängt sie an der Aufmerksamkeit
  dessen, der gerade baut, rutscht sie irgendwann durch.
- **Ein Beispiel aus einer Anleitung ist keine Skala.** Googles eigene
  Compose-Anleitung zeigt ein Beispiel-Formenschema mit 24 dp für
  `extraLarge`; der Token des Systems ist 28 dp. Wer aus dem Beispiel
  abschreibt, hat eine plausible Zahl und die falsche.
- **„Material 3" ist eine Fassung, kein Zustand.** Die Skalen wachsen:
  Zu den Radien der Baseline sind mit der Expressive-Ausbaustufe 20, 32
  und 48 dp dazugekommen. Welche Fassung gilt, steht in der Regeldatei
  des Projekts, mit Fundstelle und Datum.

### Die Werte, gegen die geprüft wird

Quelle: `androidx.compose.material3.tokens` — die von Google aus dem
Tokensatz **erzeugte** Referenzumsetzung, abgerufen am 2026-08-29 von
<https://android.googlesource.com/platform/frameworks/support/>
(`ShapeTokens.kt` VERSION 14_1_0, `ElevationTokens.kt` VERSION v0_210,
`StateTokens.kt` VERSION v0_103). Nicht aus `m3.material.io`
abgeschrieben: die Seite wird im Browser zusammengesetzt und ist damit
keine zitierfähige Fundstelle.

| Eckenradius | dp | | Höhenstufe | dp | | Deckschicht | Deckung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | 0 | | Stufe 0 | 0 | | Überfahren | 8 % |
| extra-small | 4 | | Stufe 1 | 1 | | Fokus | 10 % |
| small | 8 | | Stufe 2 | 3 | | Gedrückt | 10 % |
| medium | 12 | | Stufe 3 | 6 | | Gezogen | 16 % |
| large | 16 | | Stufe 4 | 8 | | | |
| large-increased | 20 | | Stufe 5 | 12 | | | |
| extra-large | 28 | | | | | | |
| extra-large-increased | 32 | | | | | | |
| extra-extra-large | 48 | | | | | | |
| full | Kreis | | | | | | |

**Die Höhenstufe ist der Schatten.** „Schatten sieht anders aus" ist fast
nie eine Frage von Weichzeichnung und Deckkraft, sondern der falschen
Stufe: Eine Karte auf Stufe 1 und eine Karte auf Stufe 3 unterscheiden
sich um den Faktor drei. Die Stufe kommt aus der Komponente, nicht aus
dem Auge.

**Nicht jedes Ziel führt die Skalen als Schnittstelle.** Jetpack Compose
hat sie als `Shapes` und `ElevationTokens`; Flutter hat sie nicht — in
der Material-Bibliothek gibt es `Durations` und `Easing`, aber keine
Formen- und keine Höhenskala (api.flutter.dev, geprüft 2026-08-29). Die
Werte stecken dort in den Vorgaben der einzelnen Widgets. **Wo das Ziel
die Skala nicht führt, führt sie das Projekt** — als Tokendatei, aus dem
Erzeugungsschritt, nicht als Zahl im Widget.

### Wenn Entwurf und System auseinandergehen

**Das ist eine Rückfrage, keine Reparatur.** Der Agent zieht weder den
Entwurf still auf das System noch das System still auf den Entwurf.
Vorgelegt wird beides mit Zahlen: welcher Wert im Entwurf steht, welcher
im System, und wie viel das ausmacht.

Entschieden wird vom Projektinhaber, einmal für das Projekt und im
Zweifel je Fall:

| Entscheidung | Was daraus folgt |
| --- | --- |
| **Das System gewinnt** | Der Entwurf wird auf die Systemwerte gezogen, **bevor** er zur goldenen Aufnahme wird |
| **Der Entwurf gewinnt** | Der abweichende Wert wird als bewusste Abweichung geführt, mit Grund, und der Systemabgleich nimmt ihn ausdrücklich aus |

Das Erste ist der Regelfall, wenn das Ergebnis „original Material 3"
sein soll. Das Zweite ist zulässig, aber nie stillschweigend: Eine
Abweichung ohne Vermerk sieht in einem Jahr wie ein Fehler aus, und
niemand traut sich, sie zu ändern.

**Reihenfolge, sonst misst man gegen ein falsches Lineal:** erst den
Entwurf auf das System ziehen, dann die goldene Aufnahme legen
(Abschnitt 5). Wer die Aufnahme aus einem Entwurf legt, dessen Radien um
vier Punkte danebenliegen, hat die Abweichung zum Soll erklärt.

### Gemessen wird das auch

Der Systemvertrag ist prüfbar, also wird er geprüft und nicht
eingehalten:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/md3-token-check.py tokens/tokens.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/md3-token-check.py lib/theme/ --scale baseline
```

Das Werkzeug liest die Tokendatei des Projekts — JSON, CSS, Dart, Kotlin,
SCSS — und vergleicht jeden Radius, jede Höhenstufe und jede
Zustandsdeckschicht mit dem Original. Es meldet die Abweichung als Zahl
und ist bei einem Fund rot. Bewusste Abweichungen stehen in einer
Ausnahmedatei, mit Grund; was dort nicht steht, ist ein Befund.

## 3. Der Bauteilvertrag: der Entwurf benennt die Komponente

**Ein Entwurfswerkzeug zeichnet, wie etwas aussieht. Es sagt nicht, was
es ist.**

Im Entwurf ist ein Knopf ein Kasten mit Polster, Radius und Beschriftung.
In Material 3 ist er ein **gefüllter Knopf der Größe L**. Beides sieht
gleich aus — aber nur das zweite ist eine Komponente mit Zuständen,
Deckschichten, Bewegung und Barrierefreiheit.

Wer nur das Bild bekommt, muss die Komponente **erraten**. Und er rät
falsch, denn dieselbe Optik lässt sich mit mehreren Komponenten
erzeugen: ein gefüllter Knopf, ein Kasten mit Farbe, eine Kachel, ein
Listeneintrag mit Hintergrund. Alle vier sehen im Standbild gleich aus
und verhalten sich verschieden.

**Deshalb trägt jedes Element im Entwurf seine Komponente als Marke:**

```html
<div data-komponente="FilledButton"
     data-variante="filled"
     data-groesse="L"
     data-zustand="enabled">Abschließen</div>
```

Benannt wird:

| Was | Beispiel |
| --- | --- |
| **Komponente** | `FilledButton`, `NavigationRail`, `ListItem`, `Card` |
| **Variante** | `filled`, `outlined`, `tonal`, `elevated`, `text` |
| **Größe** | die Größenklasse des Systems, nicht eine Pixelzahl |
| **Zustand** | `enabled`, `hover`, `focus`, `pressed`, `disabled`, `error` |

Damit wird aus **Übersetzen** ein **Nachschlagen** — und genau dort
verschwindet die Erfindung.

- **Die Marke steht im Entwurf**, nicht erst im Prompt. Ein Prompt, der
  die Komponente nennt, hilft einmal; eine Marke hilft immer.
- **Der gebaute Bildschirm nennt dieselbe Komponente.** Die Views rufen
  ohnehin nur die Wrapper der Produktfamilie auf (Skill
  `neo-komponenten`) — geprüft wird zusätzlich, dass es der **richtige**
  Wrapper ist.
- **Gibt es für das Gezeichnete keine Komponente des Systems, ist das
  eine Rückfrage**, kein Nachbau. Entweder das System kann es und die
  Komponente heißt anders, oder es kann es nicht — dann entscheidet der
  Projektinhaber, ob der Entwurf sich ändert oder ob eine eigene
  Komponente entsteht, mit Begründung und Entscheidungsakte.
- **Eine eigene Komponente ist eine Ausnahme mit Vermerk**, nicht die
  Voreinstellung. Jede eigene Komponente ist Code, den niemand pflegt
  außer NEO.

**Der häufigste Fall in der Praxis:** Das Entwurfswerkzeug gibt keine
Komponenten des Zielsystems aus — es gibt HTML und CSS. Dann ist die
Marke der **einzige** Ort, an dem die Absicht steht. Ohne sie ist jede
Umsetzung eine Interpretation, und jede Interpretation ist beim nächsten
Bildschirm eine andere.

## 4. Die Messung: je Ziel ein Werkzeug

Ein Bildschirm gilt als umgesetzt, wenn die Messung grün ist — nicht,
wenn er richtig aussieht.

| Ziel | Womit gemessen wird |
| --- | --- |
| Browser | `layout-diff.js`, `style-audit.js`, `image-diff.py` (`designsystem-abgleich.md`) |
| Flutter | **Golden-Tests** (`matchesGoldenFile`) |
| Jetpack Compose | Screenshot-Tests (Compose Preview Screenshot Testing, Paparazzi, Roborazzi) |
| SwiftUI | Snapshot-Tests |

## 5. Die Aufnahme aus dem Entwurf ist das Soll

Der übliche Einsatz einer goldenen Aufnahme misst **Rückschritt**: Man
nimmt den zuletzt genehmigten Stand auf und merkt, wenn er sich ändert.
Das ist nützlich — beantwortet aber nicht die Frage, um die es hier geht.

**Umgedreht wird daraus die Brücke:**

> Die goldene Aufnahme ist der **Export aus dem Entwurf**, nicht der
> zuletzt gebaute Stand. Der Test ist rot, solange der Bildschirm dem
> Entwurf nicht entspricht — und wird grün, wenn er es tut.

Damit ist „sieht aus wie im Entwurf" kein Streitpunkt mehr, sondern ein
Testergebnis. Genau das verlangt Kernregel 11: **Fertig heißt gemessen.**

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

## 6. Der Ablauf je Bildschirm

```
1  Entwurf freigegeben            (entwurfsverfahren.md)
2  Systemwerte abgeglichen        Radien, Höhenstufen, Deckschichten
3  Bauteile benannt               je Element Komponente, Variante, Größe
4  Tokens erzeugt                 eine Quelle, erzeugte Datei eingecheckt
5  Bildschirm gebaut              nur aus Tokens, nur benannte Bauteile
6  Goldene Aufnahme gelegt        aus dem berichtigten Entwurf
7  Test läuft, bis grün           Abweichung als Zahl, nicht als Gefühl
8  Fertigmeldung                  mit der Zahl, nicht mit „passt"
```

**Schritt 2 vor Schritt 6, und Schritt 6 vor Schritt 7.** Wer die goldene
Aufnahme aus dem eigenen Bau erzeugt, hat sich selbst bestätigt und
nichts gemessen. Wer sie aus einem Entwurf legt, der die Systemwerte
verfehlt, hat die Abweichung zum Soll erklärt.

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
| Ein Element verhält sich anders als erwartet, sieht aber richtig aus | Falsche Komponente gewählt — der Entwurf hat sie nicht benannt |
| Ecken und Schatten wirken knapp daneben, sonst stimmt alles | Systemwerte aus dem Entwurf abgemessen statt aus dem System übernommen (Abschnitt 2) |

**Ein Prompt, der eine Abweichung beschreibt, ist der teuerste Weg.** Ein
Test, der sie misst, ist der billigste.

## Abnahme

- [ ] Es gibt **eine** Tokenquelle; die erzeugte Datei ist eingecheckt.
- [ ] **Radien, Höhenstufen und Deckschichten stammen aus dem System**,
      nicht aus dem Entwurf abgemessen; `md3-token-check.py` meldet null
      Befunde, die geprüfte Fassung ist benannt.
- [ ] Abweichungen zwischen Entwurf und System wurden **vorgelegt** und
      entschieden; bewusste Abweichungen stehen mit Grund in der
      Ausnahmedatei.
- [ ] Der Erzeugungsschritt läuft in der CI und ist bei Abweichung rot.
- [ ] Kein Zahlenwert, keine Farbe in einer View — alles aus Tokens.
- [ ] **Jedes Element im Entwurf nennt seine Komponente**, Variante,
      Größe und Zustand; der gebaute Bildschirm benutzt dieselbe.
- [ ] Eigene Komponenten gezählt und je Stück begründet.
- [ ] **Bedienhöhen sind Tokens**, nicht Einzelwerte.
- [ ] Je Bildschirm eine goldene Aufnahme, **aus dem Entwurf** gelegt.
- [ ] Aufnahmebedingungen festgehalten und in Entwurf und Test gleich.
- [ ] Toleranz benannt; ausgenommene Bereiche benannt und begründet.
- [ ] Die Abweichung wird als **Zahl** berichtet, nicht als „passt".
