# Lesbarkeit: sauber heißt nicht abstrakt

Lesekonvention siehe `SKILL.md`. Schichten und Benennung: `SKILL.md`.
Sprache im Code: `sprache.md`.

> **„Das hast du mit der KI geschrieben, gell — das kann keiner mehr
> lesen."**

Das ist der Satz, den dieser Text verhindert. Er wird nicht gesagt, weil
der Code schlampig ist. Er wird gesagt, weil er **überbaut** ist: drei
Dateien für eine Aufgabe, ein Interface je Klasse, eine Funktion für
jedes `if`, eine Fabrik für die eine Umsetzung, die es gibt.

**Der häufigste Fehler in maschinell geschriebenem Code ist nicht
Schlamperei, sondern Überbau.**

## Der Maßstab: wer den Code lesen können muss

Nicht der Architekt. **Ein Entwickler, der programmieren kann und von
objektorientierter Programmierung nur die Grundlagen hat.** Jemand, der
noch nie mit diesem Rahmenwerk gearbeitet hat.

Der Test ist nicht abstrakt, sondern ein Ablauf:

1. Er bekommt eine **Fehlermeldung**.
2. Er findet die **Datei**, die sie ausgelöst hat.
3. Von dort findet er die **Stelle, an der die Ursache liegt** — ohne die
   Konventionen des Rahmenwerks auswendig zu kennen.

**Wie viele Dateien muss er dafür öffnen?** Diese Zahl wird genannt, wenn
ein Ablauf gebaut wurde. Mehr als drei ist ein Hinweis, mehr als fünf ist
ein Befund.

## Wann eine eigene Funktion entsteht

Eine eigene Funktion entsteht, wenn **mindestens eines** zutrifft:

- Sie wird **mehr als zweimal** gebraucht.
- Ihr Name **ersetzt einen Kommentar**: `istAbgelaufen()` sagt mehr als
  vier Zeilen Datumsvergleich.
- Sie muss **eigenständig testbar** sein.
- Sie trennt zwei **Abstraktionsebenen** in einer Methode, die sonst
  Fachlogik und Technik mischt.

Sie entsteht **nicht**, weil:

- „man das so macht",
- eine Methode dadurch drei Zeilen kürzer wird,
- ein Werkzeug eine Kennzahl meldet,
- jemand sie später vielleicht wiederverwenden könnte.

> **Nicht für jede Kleinigkeit eine Funktion.** Ein `if` mit zwei Zeilen
> bleibt ein `if`. Wer es auslagert, zwingt jeden Leser zu einem Sprung,
> der nichts erklärt.

**Die Regel der Wiederholung: beim dritten Mal.** Zwei ähnliche Stellen
sind noch kein Muster — sie sind zwei Stellen. Drei sind ein Muster und
werden zusammengelegt. Wer beim zweiten Mal abstrahiert, abstrahiert
meistens das Falsche, weil er die dritte Form noch nicht kennt.

## Wann etwas zusammengelegt wird — und wann nicht

**Zwei Funktionen, die dasselbe tun, sind eine zu viel.** Wenn Modul A
und Modul B jeweils eine eigene Funktion haben, die dieselbe Aufgabe
erfüllt, gibt es künftig **eine**, die beide verwenden.

Sonst gilt: ein Fehler ist zwanzigmal zu beheben, und beim ersten Mal
sucht jemand erst, wo überall.

**Wohin sie kommt:**

- In eine **gemeinsame Schicht**, die beide Module verwenden dürfen —
  nicht in Modul A, das Modul B dann importiert. Sonst hängt B an A, und
  A lässt sich nicht mehr entfernen.
- Mit einem Namen, der die **Sache** benennt, nicht das erste Modul, in
  dem sie stand.

**Wenn die beiden Fassungen sich unterscheiden:** Das ist der Normalfall,
und die Antwort ist **nicht**, beide zu behalten.

1. **Herausfinden, warum sie sich unterscheiden.** Meist hat eine einen
   Fehler, den die andere nicht hat — oder eine kennt einen Grenzfall,
   den die andere nie gesehen hat.
2. **Die gemeinsame Fassung bedient beide Fälle korrekt.** Der Grenzfall
   wird übernommen, der Fehler nicht.
3. **Ein Test je Fall**, aus beiden Modulen, bevor zusammengelegt wird.
4. Beide Module rufen danach dieselbe Stelle.

**Die Gegenregel, genauso wichtig:**

> **Was gleich aussieht, ist nicht immer dasselbe.** Zwei Funktionen, die
> heute denselben Code haben, sich aber aus **verschiedenen Gründen**
> ändern werden, bleiben getrennt.

Woran man das erkennt: Ändert sich die eine, weil das Steuerrecht sich
ändert, und die andere, weil ein Lieferant sein Format ändert? Dann sind
es zwei. Legt man sie zusammen, entsteht eine Sammelklasse mit fünf
Schaltern — und die ist schlimmer als die Kopie.

Im Zweifel: **erst trennen lassen, beim dritten Mal zusammenlegen.**

## Vom Fehler zur Ursache

Der wichtigste Abschnitt, weil er entscheidet, wie teuer ein Fehler wird.

- **Jede Fehlermeldung nennt was, wo und womit.** „Fehler beim Speichern"
  ist keine Meldung. „Order A-4711 could not be saved: customer 88 not
  found" ist eine.
- **Die Korrelationskennung steht in der Meldung und im Protokoll.** Ohne
  sie beginnt jede Fehlersuche mit dem Sammeln von Bruchstücken (Skill
  `neo-code`, `references/querschnitt.md`).
- **Die Ursache wird nie verschluckt.** Wer eine Ausnahme fängt und eine
  neue wirft, hängt die alte an. Ein leeres `catch` ist ein Regelverstoß.
- **Der Name sagt, wo man sucht.** Wer `OrderService` liest, sucht in
  `OrderService`. Eine Datei, die etwas anderes tut, als ihr Name sagt,
  kostet mehr als jede fehlende Abstraktion.
- **Ein Einstieg je Ablauf.** Von der Route zur Fachlogik in höchstens
  drei Sprüngen. Wer vier braucht, hat eine Schicht zu viel.
- **Keine Auflösung, die man nicht suchen kann.** Ein Aufruf, dessen Ziel
  nur über Namenskonvention, Reflexion oder einen Ereignisbus gefunden
  wird, ist für den Leser eine Sackgasse. Wo der Rahmen das tut, steht es
  in der Dokumentation des Ablaufs — mit dem Ziel.
- **Kein Fehler wird stillschweigend behandelt.** Ein Rückfall auf einen
  Standardwert, den niemand sieht, ist der Fehler von morgen.

## Richtwerte

Hinweise, keine Verbote — aber jeder Überschritt wird **begründet**, nicht
übersehen:

| Was | Richtwert | Was darüber bedeutet |
| --- | --- | --- |
| Funktion oder Methode | 30 Zeilen | Sie tut wahrscheinlich zwei Dinge |
| Verschachtelungstiefe | 3 | Frühe Rückgabe statt tiefer Bäume |
| Parameter | 4 | Ein Objekt wartet darauf, geschrieben zu werden |
| Klasse | 300 Zeilen | Zwei Verantwortungen in einer Datei |
| Datei | 400 Zeilen | Ein Modul, das sich teilen will |
| Dateien je Ablauf | 3 | Eine Schicht ohne Aufgabe |

**Und die Gegenrichtung, weil sie öfter verletzt wird:** eine Datei mit
zwölf Zeilen, die nur eine andere aufruft, ist auch ein Befund.

## Was Enterprise nicht heißt

Enterprise heißt: **es hält, es ist auffindbar, es ist änderbar.** Nicht:
es hat viele Dateien.

| Kein Muster ohne Anlass | Warum |
| --- | --- |
| Interface für **eine** Umsetzung | Eine Abstraktion ohne zweite Umsetzung erklärt nichts und versteckt eine |
| Fabrik für **einen** Typ | Ein `new` mit Umweg |
| Repository um **eine** Abfrage | Eine Schicht, die nur weiterreicht |
| DTO, Mapper und Assembler für drei Felder | Drei Dateien für eine Zuweisung |
| Ereignis, das genau **einen** Zuhörer hat | Ein Aufruf, den man nicht mehr finden kann |
| Konfigurationsschalter „für später" | Ein Zweig, den niemand testet |
| Generisches `T` für einen Fall | Lesbarkeit gegen nichts eingetauscht |

**Ein Muster wird eingeführt, wenn das Problem da ist** — nicht, wenn es
denkbar ist. Und wenn es eingeführt wird, wird es begründet (Skill
`neo-doku`, Entscheidungsakte).

## Was Lesbarkeit nicht bedeutet

Damit die Regel nicht in die andere Richtung kippt:

- **Keine Ausrede für fehlende Fehlerbehandlung.** Fehler werden
  abgefangen, benannt und behandelt — das macht Code nicht unlesbar,
  sondern vollständig.
- **Keine Ausrede für fehlende Typen.** Typen sind gelesene Dokumentation
  (`php.md`, `dotnet.md`).
- **Keine Ausrede für lange Methoden.** Kurz und flach ist beides zu
  haben.
- **Keine Ausrede für Kopien.** Die Regel der Wiederholung erlaubt zwei
  Stellen, nicht zwanzig.
- **Keine Ausrede für fehlende Schichtgrenzen.** Die Importrichtung
  bleibt eine Einbahnstraße (`SKILL.md`).

## Selbstprüfung vor der Fertigmeldung

Der Lesetest, und er wird wirklich gemacht:

1. **Eine Datei, die gerade entstanden ist, lesen, als hätte man sie nie
   gesehen.** Ist in 60 Sekunden klar, was sie tut?
2. **Einen Ablauf von außen nachverfolgen** — von der Route bis zur
   Datenbank. **Wie viele Dateien?** Die Zahl nennen.
3. **Jede neue Abstraktion begründen** — in einem Satz. Wer keinen Satz
   findet, nimmt sie heraus.
4. **Jede neue Funktion zählen:** Wie oft wird sie aufgerufen? Einmal ist
   ein Hinweis.
5. **Nach Zwillingen suchen:** Gibt es die Funktion schon, unter einem
   anderen Namen? Vor dem Schreiben suchen, nicht danach.

Berichtet wird mit Zahlen: „Ablauf über 3 Dateien, längste Methode 24
Zeilen, 1 neue Abstraktion (Grund: …), keine Zwillinge gefunden."
