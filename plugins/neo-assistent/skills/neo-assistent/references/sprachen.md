# Mehrsprachige Assistenten

Lesekonvention siehe `SKILL.md`.

## Die Prüffrage

> **Eine neue Sprache dazuschalten darf keine einzige Zeile des
> Systemprompts, keine Absicht und kein Werkzeugschema ändern.**

Was sich ändert: die Oberflächentexte und die Goldfälle in der neuen
Sprache. Sonst nichts.

Muss doch etwas am Prompt geändert werden, hängt der Ablauf an Wörtern.
Das ist ein Befund, kein Aufwand — und er wächst mit jeder weiteren
Sprache.

## Zwei Sprachen, nicht eine

| | Was | Beispiel |
| --- | --- | --- |
| **Arbeitssprache** | fest, kanonisch, sichtbar für niemanden | Absichtsnamen, Werkzeugnamen, Aufzählungswerte, Feldnamen, Protokolle, Fehlercodes |
| **Antwortsprache** | die des Benutzers, je Gespräch bestimmt | alles, was er liest |

Die Arbeitssprache wird **einmal** festgelegt und nie übersetzt. Der
Systemprompt kann in ihr geschrieben sein oder in der Hauptsprache des
Hauses — er darf nur keine Sprachlogik enthalten.

**Was nie übersetzt wird:**

- Absichtsnamen und Werkzeugnamen.
- Aufzählungswerte in Argumenten. `grund: "kundenwunsch"` bleibt
  `kundenwunsch`, auch wenn der Benutzer Italienisch spricht. Was der
  Benutzer sieht, ist die Beschriftung dazu — aus der Sprachdatei, nicht
  aus dem Modell.
- Kennungen, Codes, Statuswerte.
- Datums-, Zahlen- und Währungsformate im Argument. Kanonisch hin,
  lokalisiert zurück.

Die Trennung erzwingt das Schema, nicht der Prompt: ein `enum` mit
kanonischen Werten kann nicht übersetzt gefüllt werden.

## Die Antwortsprache

- **Einmal bestimmt, nicht je Satz geraten.** Die Einordnung liefert das
  Feld `sprache` (`absichten.md`); es gilt für das Gespräch, bis der
  Benutzer erkennbar wechselt.
- **Nur aus den ausgelieferten Sprachen.** Erkennt die Einordnung eine
  Sprache, für die es keine Oberflächentexte gibt, gilt die Vorgabesprache
  — mit einem Satz dazu, nicht stillschweigend.
- **Die Sprache der Anwendung geht vor**, wo sie bekannt ist. Wer die
  Oberfläche auf Italienisch bedient, bekommt italienische Antworten,
  auch wenn er eine englische Kennung eintippt.
- Zahlen, Datum und Währung werden in der **Antwortsprache** formatiert,
  über die Formatierung der Sprache, nie vom Modell zusammengesetzt
  (Skill `neo-design`).

## Beispiele im Prompt

**Beispieldialoge in nur einer Sprache verzerren alle anderen.** Das
Modell übernimmt Satzbau, Länge und Höflichkeitsform des Beispiels auch
dort, wo sie nicht passen.

- Am besten: **keine** Beispieldialoge. Was ein Beispiel erklären soll,
  gehört meist in eine Werkzeugbeschreibung oder ein Schema.
- Wenn Beispiele nötig sind: **je Sprache eigene**, gleich lang und
  gleich aufgebaut — oder gar keine.
- Was ein Beispiel niemals ersetzen darf: eine Aufzählung im Schema.

## Neue Sprache dazuschalten

1. **Oberflächentexte übersetzen** — Begrüßung, Rückfragen,
   Fehlermeldungen, Beschriftungen der Aufzählungswerte. Sprachdatei,
   nicht Prompt.
2. **Goldfälle übersetzen** — jeden Fall, mit derselben Kennung und
   Sprachsuffix (`suchen-klar.it`). Übersetzt wird der **Benutzertext**;
   die Erwartung — Werkzeug und Argumente — bleibt **identisch**. Genau
   darin liegt der Beweis.
3. **Messen** — `goldlauf.py --sprache it`. Die neue Sprache muss
   dieselben Schwellen erreichen wie die bestehenden.
4. **Vergleichen** — sinkt die Trefferquote nur in der neuen Sprache,
   liegt es fast immer an einem der drei Punkte oben: ein Wort im Prompt,
   ein Beispiel in einer Sprache, ein übersetzter Aufzählungswert.

**Kein Prompt-Eingriff in Schritt 1 bis 3.** Wird einer nötig, ist er der
eigentliche Befund und wird vorgelegt, nicht nebenbei gemacht.

## Typische Fehler und woran man sie erkennt

| Was passiert | Ursache | Woran erkennbar |
| --- | --- | --- |
| Sprache A gut, Sprache B schlecht | Schlüsselwort-Routing | Trefferquote fällt nur in einer Sprache |
| Antwort mischt Sprachen | Antwortsprache je Satz neu bestimmt | Kanonische Werte tauchen im Antworttext auf |
| Argumente kommen übersetzt | Aufzählung ohne `enum` | Schemafehler bei genau einer Sprache |
| Falsches Datum bei einer Sprache | Datumsformat aus dem Text geraten | `heute` fehlt im Zustand (`architektur.md`) |
| Höflichkeitsform falsch | Beispieldialog in einer Sprache | Antworten ähneln dem Beispiel auffällig |
| Umlaute oder Akzente verschluckt | Kodierung im Adapter oder im Protokoll | Goldfall mit Umlaut im Namen schlägt fehl |

Für jede Zeile dieser Tabelle gehört mindestens ein Goldfall in die
Sammlung — sonst fällt der Fehler erst dem Kunden auf.

## Der Assistent gibt sich zu erkennen — in jeder Sprache

Der Hinweis, dass hier eine Maschine antwortet, ist in **jeder**
ausgelieferten Sprache vorhanden, sichtbar und vollständig. Eine Sprache
ohne Hinweis ist kein Schönheitsfehler, sondern ein Verstoß gegen
Artikel 50 der KI-Verordnung (Skill `neo-ki`).
