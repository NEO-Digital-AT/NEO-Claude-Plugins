# Der Oberflächendurchlauf

Lesekonvention siehe `SKILL.md`.

> **Jedes Bedienelement wird an jeder Stelle geprüft, an der es
> vorkommt.**

Das ist die Regel, um die es hier geht, und sie ist die einzige, die den
teuersten Fehlertyp verhindert.

## Die Wiederverwendungsfalle

Ein Muster wird gebaut, auf seiner Seite geprüft und für erledigt
erklärt. Danach wird es an einer zweiten Stelle eingesetzt — dieselbe
Tabelle, derselbe Knopf, dieselbe Zeilenaktion — und dort funktioniert es
nicht. Niemand merkt es, weil der Test auf der ersten Seite grün bleibt.

Die Ursachen sind immer dieselben, und keine davon liegt in der
Komponente:

| Ursache | Was passiert |
| --- | --- |
| Ein anderer Elternteil | Der Knopf liegt in einem Bereich, der Klicks abfängt, überlagert oder das Ereignis stoppt |
| Ein anderer Zustand | Die zweite Seite lädt die Rechte, die Auswahl oder die Kennung nicht, die die Aktion braucht |
| Eine andere Datenquelle | Dieselbe Tabelle mit einer anderen Abfrage; ein Feld fehlt, das die Aktion braucht |
| Eine andere Route | Nach der Aktion wird zurückgeleitet — und die zweite Seite hat kein Ziel |
| Ein anderer Behälter | Dialog statt Seite: der Fokus, das Ereignis oder der Ladezustand verhält sich anders |
| Eine lokale Variante | Jemand hat die Komponente an einer Stelle „nur kurz" nachgebaut (Skill `neo-komponenten`) |

**Deshalb reicht ein Test je Komponente nicht.** Geprüft wird die
**Kombination** aus Element und Ort. Eine Komponente an sieben Stellen
sind sieben Prüfungen, nicht eine.

## Das Inventar

Vor dem Durchlauf entsteht eine Liste. Sie wird nicht geschätzt, sondern
aus der Anwendung erhoben — aus dem Router, den Views und dem
Komponentenkatalog:

```markdown
| Seite | Element | Marke | Erwartete Wirkung |
|---|---|---|---|
| /uebersicht | Zeilenaktion Löschen | zeile-loeschen | Dialog, dann Zeile weg, Meldung |
| /auftraege | Zeilenaktion Löschen | zeile-loeschen | wie oben |
| /auftraege/:id | Knopf Speichern | speichern | speichert, Meldung, kein Neuladen |
| /auftraege/:id | Knopf Abbrechen | abbrechen | zurück, ungespeicherte Warnung |
| … | | | |
```

- **Jede Seite, jeder Dialog, jeder Reiter, jeder Zustand.** Ein
  Bedienelement, das nur im Fehlerzustand erscheint, steht auch drin.
- **Dieselbe Marke an mehreren Orten ist der Normalfall** — genau diese
  Zeilen sind die wertvollen.
- Jedes Element trägt eine stabile Marke (`data-test`), die sich nicht
  mit Beschriftung oder Sprache ändert.
- **Die Liste ist der Maßstab für Vollständigkeit.** Ein Element ohne
  Zeile gilt als ungeprüft, nicht als „nicht vorhanden".

Die Zeilen entstehen einmal und werden **mit jeder neuen Ansicht
fortgeschrieben**. Eine Ansicht ohne Zeilen im Inventar ist nicht fertig.

## Was je Zeile geprüft wird

Nicht „der Knopf ist da", sondern **die Wirkung**:

1. **Das Element ist sichtbar und bedienbar** — nicht verdeckt, nicht
   außerhalb, nicht hinter einem Überlagerungselement.
2. **Die Bedienung löst die Aktion aus** — Klick **und** Tastatur.
3. **Das beobachtbare Ergebnis tritt ein**: die Zeile ist weg, der Wert
   steht in der Liste, die Route hat gewechselt, der Aufruf ist erfolgt.
4. **Die Rückmeldung erscheint** und benennt, was passiert ist.
5. **Vor dem Destruktiven kommt der Dialog** — und **Abbrechen im Dialog
   ändert nachweislich nichts**.
6. **Der deaktivierte Zustand löst nichts aus.**
7. **Der Fehlerfall wird angezeigt**, nicht verschluckt: der Aufruf wird
   auf Fehler gestellt, die Meldung muss erscheinen.
8. **Nach der Aktion ist die Ansicht wieder bedienbar** — kein
   hängender Ladezustand, kein toter Dialog.

Punkt 3 ist der, der die Wiederverwendungsfalle fängt. „Der Klick wurde
registriert" genügt nicht — geprüft wird, dass **die Wirkung eingetreten
ist**, auf dieser Seite.

## Der Durchlauf

Ein Ende-zu-Ende-Lauf, der die Anwendung tatsächlich bedient:

1. Anmelden mit einer Rolle aus der Testliste.
2. **Jede Seite des Inventars aufrufen.** Beim Aufruf: keine Fehler in
   der Konsole, keine fehlgeschlagenen Netzaufrufe, kein leerer
   Hauptbereich.
3. **Jede Zeile des Inventars bedienen** und die acht Punkte prüfen.
4. Dabei **jede Prüfbreite** mitnehmen, mindestens schmal und breit
   (Skill `neo-design`, `references/responsiv.md`).
5. Am Ende: welche Zeilen gelaufen sind, welche grün, welche nicht.

**Der Durchlauf ersetzt keine Komponententests.** Er beantwortet eine
andere Frage: nicht „tut die Komponente, was sie soll", sondern **„tut
sie es auch hier"**.

## Rauchtest je Seite

Der kleine Bruder des Durchlaufs, und er läuft bei **jedem** Commit —
kein Bedienen, nur Aufrufen:

- Jede Route lädt und rendert ihren Hauptbereich.
- **Keine Fehlermeldung in der Konsole**, auch keine Warnung über
  fehlende Schlüssel oder fehlgeschlagene Auflösungen.
- Kein Netzaufruf mit 4xx oder 5xx, der nicht ausdrücklich erwartet ist.
- Die Überschrift der Seite steht da, der Ladezustand ist beendet.
- Kein leerer Zustand, wo Daten vorhanden sind — und ein sauberer leerer
  Zustand, wo keine da sind.

Ein Rauchtest ist billig und fängt die halbe Klasse der Fehler, die sonst
erst der Kunde meldet: eine Route, die nach einer Umbenennung ins Leere
zeigt; eine Komponente, die nur mit einer bestimmten Datenlage rendert.

## Wenn ein Element an einer Stelle bricht

1. **Zuerst den Regressionstest**, der genau diese Kombination aus
   Element und Ort zeigt — vor dem Beheben (`tests.md`).
2. **Dann prüfen, wo dasselbe Element sonst noch vorkommt.** Ein Fehler,
   der an einer Stelle auftritt, ist an den anderen wahrscheinlich auch
   da, nur unbemerkt.
3. Behoben wird in der **Komponente**, nicht an der Fundstelle. Eine
   Behebung nur an der einen Seite ist die Ursache des nächsten
   Vorfalls.
4. Das Inventar wird ergänzt, wenn die Kombination darin gefehlt hat.

## Was der Agent nie tut

- Ein Element als geprüft melden, weil dieselbe Komponente **anderswo**
  einen Test hat.
- Nur prüfen, dass ein Ereignis ausgelöst wurde, statt dass die Wirkung
  eingetreten ist.
- Den Durchlauf auf die „wichtigen" Seiten beschränken. Der Fehler sitzt
  auf der unwichtigen.
- Eine Zeile aus dem Inventar streichen, weil sie schwer zu prüfen ist.
  Was schwer zu prüfen ist, ist meist auch schwer zu bedienen.
- Testzahlen schätzen. Sie werden genannt: wie viele Zeilen im Inventar,
  wie viele gelaufen, wie viele grün.
