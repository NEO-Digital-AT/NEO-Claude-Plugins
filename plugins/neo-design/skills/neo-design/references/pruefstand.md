# Der Prüfstand

Lesekonvention siehe `SKILL.md`. **Was** gemessen wird, steht in
`designsystem-abgleich.md` (Layout, Stil, Bild) sowie in `responsiv.md`
und `textpassung.md` (Breiten und Text). Dieser Text behandelt das,
**worin** gemessen wird.

> **Der Prüfstand ist selbst ein Bauwerk. Was er falsch macht, sieht aus
> wie ein Mangel der geprüften Anwendung.**

Ein Prüfstand — die Browserumgebung, das Aufnahmeskript, die Bühne, auf
der eine Ansicht für die Messung steht — friert Bedingungen ein, damit
zwei Läufe vergleichbar sind. Genau dieses Einfrieren erzeugt die Fallen
in diesem Text. Keine davon ist projektspezifisch: sie kosten jeden
Anwender dieselbe Zeit.

**Die Wirkungsrichtung ist bei allen dieselbe, und darum sind sie
teuer:** Der Fehler sitzt im Prüfstand, das Ergebnis zeigt auf die
Anwendung.

| Falle | Was die Messung sagt | Wonach es aussieht |
| --- | --- | --- |
| Die Uhr steht | Tastatur, Listen und Menüs reagieren nicht | Bedienung kaputt, WCAG 2.1.1 |
| Der Vorschauserver läuft als Kindprozess | nichts — das Skript endet nicht | ein hängender Lauf, den niemand deutet |
| Die Bühne hat eine feste Breite | Elemente überlappen auf schmalen Breiten | schwerer Layoutmangel bei 320 und 768 px |

> **Bevor ein Befund gemeldet wird, wird der Prüfstand ausgeschlossen.**
> Ein Befund, der nur im Prüfstand auftritt, ist ein Befund über den
> Prüfstand.

**Die vierte Falle liegt daneben und hat einen eigenen Skill:** Ein
leeres Bild, eine stumm zurückgefallene Schrift, ein schwarzer
Aufnahmeausschnitt oder ein `SecurityError` am Canvas ist zuerst eine
Herkunftsgrenze und erst danach ein Mangel der Anwendung — besonders in
einem Prüfstand, der über `file://` lädt und damit die Herkunft `null`
hat. Skill `neo-cors`.

## 1. Die eingefrorene Uhr

**Der Anlass ist richtig.** Ein Prüfstand nagelt `Date.now()` auf einen
festen Zeitpunkt fest, damit Aufnahmen vergleichbar bleiben:
Datumsangaben stehen still, „heute" und „gestern" gruppieren in jedem
Lauf gleich, relative Zeiten ändern sich nicht. Ohne das schlägt jeder
Bildabgleich an einer Uhrzeit an.

**Die Nebenwirkung, die kaum jemand vermutet.** Der DOM-Teil von Vue
verwirft einen Ereigniszuhörer (Listener), wenn
`e._vts <= invoker.attached` gilt — `@vue/runtime-dom` 3.5.x, im Umfeld
von `createInvoker`. Beide Werte stammen aus `Date.now()`. Steht die Uhr,
sind sie gleich, die Bedingung trifft zu, und **jeder Zuhörer, den ein
Ereignis nur über das Hochblubbern (Bubbling) erreicht, wird
übersprungen**. Der Mechanismus existiert, damit ein Ereignis keinen
Zuhörer auslöst, der erst durch dieses Ereignis angehängt wurde; mit
stehender Uhr trifft er alle.

**Die Wirkungsrichtung — daran erkennt man es.** Direkte Zuhörer am
Element selbst arbeiten weiter. Deshalb sind Klicktests auf Knöpfen
unauffällig, während **Tastaturbedienung, Listen- und Menünavigation als
tot gemessen werden, obwohl sie funktionieren**.

Der Fall, an dem es aufgefallen ist: Eine Ordner- und eine
Nachrichtenliste wirkten im Prüfstand mit den Pfeiltasten unbedienbar.
Das Tastenereignis erreichte den Listenrumpf nachweislich, aber
`defaultPrevented` blieb `false`. Mit wieder laufender Uhr arbeitete die
Listennavigation des Rahmenwerks einwandfrei. Der Befund
„Tastaturbedienung kaputt, WCAG 2.1.1" war frei erfunden — von der
Messung, nicht von der Anwendung.

**Die Lösung: fester Startpunkt, laufende Uhr.** Nicht ein fester Wert,
sondern der feste Wert **plus die verstrichenen Millisekunden** seit dem
Start. Die Zeitangaben auf dem Bild bleiben stabil, weil sich der
Startpunkt nicht ändert; Ereignisse verhalten sich wieder wie in der
Anwendung.

```js
const FEST = Date.parse('2026-09-16T09:00:00+02:00')

// Falsch: die Uhr steht — Ereignisse mit gleichem Zeitstempel fallen aus
Date.now = () => FEST

// Richtig: der Startpunkt ist fest, die Uhr läuft
const echt = Date.now
const start = echt()
Date.now = () => FEST + (echt() - start)
```

> **Ein Prüfstand mit eingefrorener Uhr darf niemals zur Beurteilung von
> Barrierefreiheit oder Tastaturbedienung herangezogen werden**, solange
> das nicht behoben ist. Ein Befund über die Tastaturbedienung aus einem
> solchen Prüfstand ist keiner (`barrierefreiheit.md`).

## 2. Der Vorschauserver als Kindprozess

**Die Ursache.** Ein Aufnahmeskript startet den Vorschauserver als
Kindprozess — `npx vite preview` oder ein vergleichbarer Aufruf — und
schickt am Ende `SIGTERM`. Das trifft nur den `npx`-Wrapper. Der
eigentliche Server überlebt, und das Handle des Kindprozesses hält die
Ereignisschleife von Node offen.

**Die Wirkungsrichtung.** Alle Bilder sind bereits geschrieben, das
Skript scheint fertig — und beendet sich nicht. Eine Kette
`shoot && compare` läuft deshalb **nie in den Vergleich**. Wer die
Ursache nicht kennt, beendet den Prozess von Hand und startet den
Vergleich getrennt — und sieht sie nie.

**Die Lösung ist Frameworktreue** (Kernregel 8): die
Programmierschnittstelle des Werkzeugs benutzen, statt einen Prozess zu
starten. Bei Vite ist das `preview` aus `vite` — Server im selben
Prozess, `await server.close()` im `finally`. Kein Kindprozess, kein
Signal, nichts zu töten.

```js
import { preview } from 'vite'

const server = await preview()
try {
  await aufnehmen(server.resolvedUrls.local[0])
} finally {
  await server.close()
}
```

Damit ist der Prüfstand zugleich das bessere Beispiel für die Grundregel
des Skills: **Was das Rahmenwerk bereitstellt, wird benutzt.** Im
Prüfstand gelten keine schlechteren Regeln als im Produkt.

## 3. Die Bühne mit fester Breite

**Die Ursache.** Eine Prüfstands-Bühne, die auf einer Breite festgenagelt
ist — etwa 1440 px, damit Aufnahmen vergleichbar bleiben —, nimmt den
Umbruchpunkt der Anwendung nicht mit. Bei 320 oder 768 px bleibt ein
dreispaltiges Raster dreispaltig und ist dann breiter als der Schirm.

**Die Wirkungsrichtung.** `overflow.js` und `text-fit.js` melden dort
Überlappungen zwischen Elementen, die im Produkt gar nicht
nebeneinanderstehen — die Spalten liegen physisch übereinander. Die
Zahlen sehen nach einem schweren Mangel bei schmalen Breiten aus und
sind ein Artefakt der Bühne.

**Das Erkennungsmerkmal:** Die gemeldeten Paare koppeln **ausnahmslos**
ein Element der einen Spalte mit einem der anderen; **innerhalb** einer
Spalte überlappt nichts.

Daraus folgt dreierlei:

- Zahlen einer festen Bühne unterhalb ihres Umbruchpunkts sind **nur
  untereinander** vergleichbar. Als Aussage über die Anwendung taugen sie
  nicht.
- **Vor der Meldung wird jeder Befund daraufhin geprüft, ob er
  spaltenübergreifend ist.** Ist er es ausnahmslos, ist er kein Befund,
  sondern die Bühne.
- Für schmale Breiten wird eine **mitwachsende Bühne** gebaut: Sie
  übernimmt die Prüfbreite, statt sie zu überschreiben. Erst dann sagen
  die Zahlen etwas über die Anwendung.

## Abnahme

- [ ] Die Uhr des Prüfstands läuft; fest ist nur ihr Startpunkt.
- [ ] **Kein Urteil über Tastaturbedienung oder Barrierefreiheit aus
      einem Prüfstand mit stehender Uhr.**
- [ ] Das Aufnahmeskript beendet sich von selbst; die Kette aus Aufnahme
      und Vergleich läuft ohne Handgriff durch.
- [ ] Der Vorschauserver läuft über die Programmierschnittstelle im
      selben Prozess, nicht als Kindprozess.
- [ ] Die Bühne übernimmt die Prüfbreite. Tut sie es nicht, ist benannt,
      dass die Zahlen unterhalb des Umbruchpunkts nur untereinander
      vergleichbar sind.
- [ ] Jeder Befund auf schmaler Breite wurde daraufhin geprüft, ob er
      ausnahmslos spaltenübergreifend ist.
