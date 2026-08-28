# Übersetzungen: vollständig, oder es ist nicht fertig

Lesekonvention siehe `SKILL.md`. Wortlaut und Formulierung:
`oberflaechentexte.md`. Sprache im Code und in technischen Meldungen:
Skill `neo-code`, `references/sprache.md`.

> **In einem mehrsprachigen Produkt hat jeder sichtbare Text in jeder
> ausgelieferten Sprache eine Übersetzung. Das wird gemessen, nicht
> angenommen.**

Eine fehlende Übersetzung fällt niemandem auf, der die Leitsprache
spricht. Sie fällt dem Kunden auf, in der Sprache, die er nicht versteht
— oder als Schlüssel mitten im Satz.

## Die Rückfallkette

1. **Die Sprache des Nutzers.** Das Ziel.
2. **Englisch.** Die Rückfallsprache, immer — konfiguriert und geprüft,
   nicht die Sprache des Entwicklers.
3. **Nie ein Schlüssel, nie ein leerer Text, nie ein Absturz.**

Ein `order.created` mitten in einer Oberfläche ist der sichtbarste
Qualitätsmangel, den ein Produkt haben kann. **Er wird verhindert, nicht
entdeckt.**

## Was geprüft wird

`scripts/uebersetzungen.py` liest die Sprachdateien und vergleicht sie
gegen die Leitsprache. Sieben Befundarten, in der Reihenfolge ihrer
Schwere:

| Art | Bedeutung | Schwere |
| --- | --- | --- |
| **Schlüssel fehlt** | In der Leitsprache vorhanden, hier nicht | Blocker |
| **Platzhalter weicht ab** | `{name}` fehlt oder ist zu viel | **Blocker, der schlimmste** |
| **Wert ist leer** | Schlüssel da, Text leer — wirkt wie ein Fehler | Blocker |
| **Pluralform fehlt** | Leitsprache hat eine, diese Sprache nicht | Blocker |
| **Unübersetzt geblieben** | Wortgleich mit der Leitsprache | Befund |
| **Verwaister Schlüssel** | Nur hier, nicht in der Leitsprache | Befund |
| **Ohne Fundstelle** | Im Quelltext nicht gefunden | Verdacht |

**Der abweichende Platzhalter ist der gefährlichste**, weil er nicht wie
ein Übersetzungsfehler aussieht: Je nach Rahmenwerk bricht der Aufruf zur
Laufzeit oder es steht eine Lücke im Satz — „Auftrag wurde angelegt"
statt „Auftrag 4711 für Frau Huber wurde angelegt".

## Messen

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/uebersetzungen.py lang/ --leitsprache en
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/uebersetzungen.py app/locales \
  --leitsprache en --sprachen de,fr,it --quellen app/,resources/ \
  --bericht uebersetzungen.json
```

Gelesen werden **JSON und ARB**, **PHP-Rückgabe-Arrays** (Laravel,
Contao) und **flaches YAML**. Was der Leser nicht sicher lesen kann,
**meldet er** — er rät nicht.

Der Bericht nennt je Sprache die **Abdeckung in Prozent** und die Zahl
der Befunde:

```
  OK    fr         7 Schlüssel   Abdeckung 100.0 %   0 Befunde
  FEHL  de         8 Schlüssel   Abdeckung  85.7 %   6 Befunde
```

**Erlaubt sind null Blocker.** Für „unübersetzt geblieben" und
„verwaist" entscheidet der Projektinhaber, ob sie behoben oder begründet
werden — sie sind Befunde, keine Formfehler.

## In der CI

- **Bei jeder Änderung** an einer Sprachdatei oder an der Oberfläche.
- **Als Tor**: Rückgabewert 1 bricht den Bau. Eine fehlende Übersetzung
  darf nicht in die Auslieferung.
- **Vor jeder Freigabe**, mit dem Bericht im Pull Request.
- Eine **neue Sprache** wird erst ausgeliefert, wenn sie bei 100 %
  Abdeckung steht — nicht „schon mal freischalten und nachziehen".

## Was das Werkzeug nicht sieht

Ehrlich benannt, damit niemand sich darauf verlässt:

- **Harte Zeichenketten im Quelltext.** Ein Text, der nie zu einem
  Schlüssel wurde, taucht in keiner Sprachdatei auf und fehlt deshalb
  auch nicht. Er wird in der **Durchsicht** gefunden — und im
  Oberflächendurchlauf, wenn die Anwendung in einer anderen Sprache
  bedient wird (Skill `neo-grundregeln`, `references/durchlauf.md`).
- **Falsche Übersetzungen.** Ein Text kann vollständig, gut formatiert
  und inhaltlich falsch sein. Das beurteilt ein Mensch.
- **Zusammengesetzte Sätze.** Wer einen Satz aus drei Schlüsseln baut,
  bekommt in einer anderen Sprache eine falsche Wortstellung — und das
  Werkzeug meldet drei vollständige Schlüssel.
- **Texte aus der Datenbank.** Inhalte, die die Redaktion pflegt, sind
  nicht Sache der Sprachdatei (Skill `neo-contao`).

## Regeln, die das Werkzeug voraussetzt

- **Ein Schlüssel je Text**, nie ein Satz aus Teilen zusammengesetzt.
  „Es wurden" + `n` + „Aufträge gefunden" ergibt in jeder zweiten Sprache
  Unsinn. Stattdessen ein Schlüssel mit Platzhalter und Pluralform.
- **Schlüssel sind englisch und beschreiben die Stelle**, nicht den Text:
  `order.list.empty`, nicht `keine_auftraege_vorhanden`. Ein Schlüssel,
  der den deutschen Text abbildet, ist falsch, sobald der Text sich
  ändert (Skill `neo-code`, `references/sprache.md`).
- **Keine Zeichenkette in der Oberfläche**, die nicht aus der Sprachdatei
  kommt — auch nicht „nur kurz", auch nicht in einem Fehlerfall, auch
  nicht in einem Platzhaltertext.
- **Zahlen, Datum, Zeit und Währung** über die Formatierung der Sprache,
  nie zusammengesetzt.
- **Platzhalter tragen sprechende Namen**: `{count}`, nicht `{0}`. Ein
  Übersetzer, der `{0}` sieht, weiß nicht, was er verschiebt.
- **Kontext für den Übersetzer**, wo der Schlüssel ihn nicht hergibt: ein
  Kommentar oder ein Beschreibungsfeld. „Save" ist ein Knopf oder ein
  Substantiv — das entscheidet die Übersetzung.

## Rechts nach links und lange Sprachen

- **Deutsche Beschriftungen sind rund 30 % länger als englische**,
  französische ähnlich. Gemessen wird in der **längsten** ausgelieferten
  Sprache, nicht in der kürzesten (`textpassung.md`).
- Wo eine Sprache von rechts nach links läuft, ist das eine Entscheidung
  mit Auswirkung auf das ganze Layout — sie wird vorgelegt, nicht
  nebenbei eingebaut.

## Abnahme

- [ ] `uebersetzungen.py` läuft in der CI und bricht bei Befunden.
- [ ] **Null Blocker** je Sprache: nichts fehlt, nichts ist leer, keine
      Platzhalter- und keine Pluralabweichung.
- [ ] **Abdeckung je Sprache berichtet**, als Zahl.
- [ ] Der Rückfall auf Englisch ist konfiguriert und **geprüft** — eine
      fehlende Übersetzung ergibt englischen Text, nie einen Schlüssel.
- [ ] Kein Satz aus Teilschlüsseln zusammengesetzt.
- [ ] Schlüssel englisch und nach der Stelle benannt.
- [ ] Keine harte Zeichenkette in der Oberfläche — in der Durchsicht
      geprüft, weil das Werkzeug sie nicht sieht.
- [ ] Die Oberfläche wurde **in jeder Sprache bedient**, nicht nur in der
      Leitsprache (Skill `neo-grundregeln`, `references/durchlauf.md`).
- [ ] Größen und Textpassung in der **längsten** Sprache gemessen.
