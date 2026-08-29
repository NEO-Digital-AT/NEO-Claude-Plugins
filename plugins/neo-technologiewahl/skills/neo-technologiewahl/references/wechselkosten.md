# Wechselkosten

Lesekonvention siehe `SKILL.md`.

> **Ein Wechsel wirkt teurer, als er ist — und wird billiger gerechnet,
> als er ist.**

Teurer, weil man die Zeilen sieht. Billiger, weil man vergisst, dass
alles noch einmal gelernt, getestet und in Betrieb gebracht werden muss.
Beides löst man nur mit Zahlen auf.

## Was wohin wandert

| Schicht | Beim Wechsel | Aufwand |
| --- | --- | --- |
| **Fachlogik** (Regeln, Berechnung, Fiskalisierung) | wird **portiert**, mit ihren Tests | begrenzt und planbar |
| **Datenzugriff** | wird portiert, an das neue Werkzeug angepasst | mittel |
| **Oberfläche** | entsteht **neu** | wäre ohnehin neu entstanden |
| **Übersetzungen, Testdaten, Aufnahmen** | sind **Daten**, wandern mit | gering |
| **Pläne, Datenmodell, Schnittstellenentwurf** | **bleiben** | keiner |
| **Fachwissen** (Recht, Branche, Abläufe) | **bleibt** | keiner |

**Der letzte Punkt ist der größte und der unsichtbarste.** Zu wissen, wie
eine Fiskalisierung funktioniert, welche Felder ein Beleg braucht und
welcher Ablauf am Tresen trägt, ist die eigentliche Arbeit. Die steckt in
Plänen und Akten, nicht in der Sprache.

## Zählen statt schätzen

Vor jeder Aussage über Wechselkosten:

```
Zeilen je Schicht, je Paket
Anteil Oberfläche gegen Anteil Logik
Anteil Übersetzungen und erzeugte Dateien
Zahl der Plattformkanäle und fremden Pakete
```

- **Erzeugte Dateien zählen nicht als Aufwand** — sie werden neu erzeugt.
- **Übersetzungen zählen nicht als Aufwand** — sie sind Daten.
- **Eine Oberfläche, die ohnehin neu gebaut wird**, ist kein
  Wechselkosten-Posten, sondern ein Posten, der so oder so anfällt. Wer
  sie dem Wechsel zurechnet, rechnet den Wechsel künstlich teuer.

## Der Zeitpunkt entscheidet mehr als der Umfang

> **Der günstigste Schnitt liegt vor der teuersten Strecke.**

Bei jedem Projekt gibt es eine Strecke, die den Großteil des Aufwands
trägt — und die man beim Wechsel zweimal zahlt, wenn sie schon gebaut
ist:

| Art des Projekts | Die teuerste Strecke |
| --- | --- |
| Kassensystem, Geräteanwendung | Peripherie und Betriebssystemnähe |
| Fachanwendung | Fachlogik und Berichte |
| Portal, Webseite | Inhaltspflege und Redaktionsanbindung |
| Schnittstelle | Verträge, Fassungen, angebundene Verbraucher |

**Deshalb wird ausdrücklich beantwortet:** Ist die teuerste Strecke schon
gebaut? Steht sie noch bevor? Ein Wechsel davor kostet einen Bruchteil
eines Wechsels danach — und diese Frage wird zu selten gestellt, weil sie
unangenehm ist, wenn die Antwort „danach" lautet.

## Was ein Wechsel zusätzlich kostet

Ehrlich benannt, sonst wird er schöngerechnet:

- **Lernkurve**, auch mit einem Agenten: Die Regeln des neuen Systems
  müssen ins Regelwerk, sonst entsteht dort dieselbe Beliebigkeit wie
  vorher.
- **Werkzeugkette**: Bau, Tests, Ausrollung, Signatur, Geräteverteilung —
  alles noch einmal.
- **Doppelbetrieb**, wenn das Alte noch läuft, während das Neue entsteht.
- **Der zweite Durchlauf durch alle Abnahmen.**
- **Die Zeit, bis das Neue so verlässlich ist wie das Alte.** Das Alte
  hat Fehler, die man kennt; das Neue hat Fehler, die man noch nicht
  kennt.

## Was ein Bleiben kostet

Die andere Seite, genauso ehrlich:

- **Jede fehlende Komponente wird wiederholt nachgebaut** — nicht einmal.
- **Jede Lücke des Rahmenwerks wird bei jeder Fassung nachgezogen.**
- **Eine Abweichung zwischen Entwurf und Umsetzung wächst**, wenn sie
  nicht gemessen wird — und jede Sitzung kostet Prompts, die niemand
  zählt.
- **Ein Rahmenwerk, dessen Anbieter die Richtung verlassen hat**, wird
  teurer, je länger man wartet.

## Die Entscheidungsregel

Ein Wechsel lohnt, wenn **alle drei** zutreffen:

1. **Die Ursache liegt wirklich im Rahmenwerk** — belegt, nicht vermutet.
   Häufiger liegt sie im fehlenden Vertrag zwischen Entwurf und Umsetzung
   (Skill `neo-design`, `references/entwurfsbruecke.md`).
2. **Die teuerste Strecke steht noch bevor** — oder der Schaden des
   Bleibens übersteigt sie.
3. **Ein Nachbau hat es gezeigt**, nicht ein Argument (`SKILL.md`,
   Abschnitt 5).

Trifft eines davon nicht zu, wird nicht gewechselt — sondern die
tatsächliche Ursache behoben.

## Abnahme

- [ ] Zeilen je Schicht **gezählt**, nicht geschätzt, und berichtet.
- [ ] Getrennt ausgewiesen: portiert, neu, bleibt, wandert mit.
- [ ] Die teuerste Strecke benannt und beantwortet, ob sie gebaut ist.
- [ ] Kosten des Wechsels **und** Kosten des Bleibens beide benannt.
- [ ] Die Ursache belegt, nicht vermutet.
- [ ] Ein Nachbau liegt vor, mit vorher festgelegtem Maßstab.
