# Die Auftragsliste

Lesekonvention siehe `SKILL.md`.

> **Eine neue Nachricht ist ein zusätzlicher Auftrag, nie ein Ersatz für
> den laufenden.**

Der Projektinhaber arbeitet so: Er sieht etwas, er schreibt es sofort —
auch mitten in einer laufenden Aufgabe, auch fünfmal hintereinander, auch
mit Screenshots dazu. Das ist die Arbeitsweise, nicht ein Fehler darin.
Der Agent hat sich darauf einzustellen, nicht umgekehrt.

Der Schaden, wenn er es nicht tut, ist groß und unsichtbar: Ein Tag voller
Anweisungen, und am Abend ist die Hälfte davon nie umgesetzt worden — weil
jede neue Nachricht die vorige verdrängt hat. Niemand merkt es sofort. Es
fällt Wochen später auf.

## Die Regel

**Eine eingehende Nachricht bricht nichts ab.** Sie wird an das Ende der
Auftragsliste gehängt. Die laufende Arbeit wird zuerst zu Ende gebracht.

```
Offen
  2  Knopf „Speichern" fehlt auf der Detailseite     in Arbeit
  3  Screenshot: Abstand über der Karte zu groß      offen
  4  Auf dev mergen                                  wartet auf deine Freigabe
```

Geführt wird die Liste **vollständig**, mitgeschrieben und nicht im
Kopf — was nicht auf ihr steht, gilt als vergessen. **Am Ende jeder
Antwort steht nur, was offen ist und was vom Projektinhaber gebraucht
wird**, in kurzen Sätzen. Erledigtes verschwindet aus der Antwort; es
steht in Commit, Pull Request oder Worklog.

## Was erlaubt ist, während etwas läuft

**Eine Zeile Bestätigung**, mehr nicht:

> Aufgenommen als Punkt 4. Ich bin noch bei Punkt 2.

Nicht erlaubt, solange ein Punkt läuft:

- eine Rückfrage zum neuen Punkt, die den laufenden anhält,
- ein Themenwechsel („interessant, dann schauen wir uns doch gleich…"),
- das Vorziehen des neuen Punkts, ohne zu fragen,
- das stillschweigende Fallenlassen des laufenden Punkts.

**Ausnahme, und nur diese:** Die neue Nachricht macht den laufenden Punkt
gegenstandslos oder falsch („stopp, nicht die Tabelle, die Liste"). Dann
wird der laufende Punkt angehalten — und das wird gesagt, mit dem Stand,
in dem er liegen bleibt.

## Punkte bilden

- **Eine Nachricht ist ein Punkt.** Enthält sie mehrere Aufträge, wird
  jeder ein eigener Punkt mit eigener Nummer.
- **Zwei Nachrichten hintereinander sind oft eine.** Ein Nachtrag, ein
  Screenshot zur vorigen Zeile, eine Korrektur eines Tippfehlers
  („mergen, nicht merken") gehören zum vorigen Punkt.
- **Ein Screenshot ohne Text ist ein Punkt** und keine Verzierung: Er
  zeigt etwas, das nicht stimmt. Was genau, wird gefragt — aber erst,
  wenn der Punkt an der Reihe ist.
- **Nummern werden nicht neu vergeben.** Punkt 3 bleibt Punkt 3, auch
  wenn 1 und 2 erledigt sind. So lässt sich darüber reden.

## Punkte abarbeiten

**Punkt für Punkt, in der Reihenfolge des Eingangs.** Jeder Punkt bekommt,
was er braucht: Analyse, Rückfrage, Freigabe, Umsetzung, Prüfung. Ein
Punkt, der auf eine Antwort wartet, blockiert die Liste nicht — er wird
als **wartend** markiert, und der nächste beginnt.

```
  3  Abstand über der Karte      wartend (Rückfrage: 16 px oder 24 px?)
  4  Auf dev mergen              in Arbeit
```

**Kein Punkt verfällt.** Nicht durch eine neue Nachricht, nicht durch
einen Kontextwechsel, nicht dadurch, dass ein anderer Punkt freigegeben
wird. Ein Punkt verschwindet nur, wenn er **erledigt** ist oder der
Projektinhaber ihn **streicht**.

## Anweisungen werden ausgeführt

„Auf `dev` mergen", „auf `main` durchstellen", „committen", „pushen",
„Pull Request aufmachen" sind Punkte der Liste wie jeder andere.

**Sie gelten erst als erledigt, wenn es geschehen ist** — nicht, wenn es
bestätigt wurde. Der Beleg gehört in die Antwort: der Commit-Hash, die
Ausgabe des Push, die Nummer des Pull Requests.

> Falsch: „Ich merge das dann auf dev."
> Richtig: „Auf `dev` gemerged, `a1b2c3d`, gepusht."

Geht es nicht — rote Tests, Konflikt, fehlende Rechte —, ist das **eine
Meldung mit Grund**, kein stilles Auslassen. Der Punkt bleibt offen und
bekommt den Grund dazu.

## Vor der Fertigmeldung

**Fertig ist die Arbeit erst, wenn die Liste leer ist**, nicht wenn der
zuletzt genannte Punkt erledigt ist. Vor jeder Fertigmeldung:

- [ ] Jeder Punkt der Liste ist erledigt oder gestrichen.
- [ ] Kein Punkt steht auf **wartend**, ohne dass die Rückfrage offen
      sichtbar gestellt wurde.
- [ ] Jede Anweisung zu Git ist **ausgeführt und belegt**, nicht angekündigt.
- [ ] Die Antwort nennt nur, was offen ist und was gebraucht wird; ist
      nichts offen, sagt sie das in einem Satz.

## Wenn der Kontext knapp wird

Wird die Sitzung lang und der Kontext zusammengefasst, ist die
Auftragsliste **das Erste**, was in die Zusammenfassung gehört — vor
jedem technischen Detail. Ein Punkt, der bei einer Zusammenfassung
verlorengeht, ist genau der Fall, den diese Regel verhindern soll.

Bei mehr als zehn offenen Punkten wird die Liste zusätzlich in
`/plan/auftragsliste.md` geschrieben und dort geführt. Dann überlebt sie
auch einen Sitzungsabbruch.
