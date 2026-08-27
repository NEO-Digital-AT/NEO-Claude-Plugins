# Modellwahl und Modellwechsel

Lesekonvention siehe `SKILL.md`.

## Der Satz vorweg

> **Ein Modellwechsel ist keine Reparatur.** Er ist eine Änderung mit
> Auswirkung — und wie jede wird er gemessen, nicht geglaubt.

Wenn ein Assistent mit einem stärkeren Modell „endlich läuft", ist die
Struktur zu schwach und das Modell trägt sie gerade noch. Der nächste
Anbau bringt sie zurück, dann ohne Ausweg nach oben.

**Erst Struktur, dann messen, dann Modelle vergleichen.** In dieser
Reihenfolge, nie in einer anderen.

## Ein Modell je Stufe

| Stufe | Aufgabe | Was zählt |
| --- | --- | --- |
| **Einordnung** | Anfrage einer Absicht zuordnen, Sprache erkennen | schnell, billig, verlässlich in einer geschlossenen Auswahl |
| **Bearbeitung** | Werkzeug wählen, Argumente bilden, antworten | Werkzeugtreue, Argumentgenauigkeit, mehrsprachig |
| **Nachbereitung** (optional) | Ergebnis formulieren, zusammenfassen | Sprache und Ton, kein Werkzeugzugriff |

Für die Einordnung ist das stärkste Modell selten das richtige: die
Aufgabe ist klein, die Auswahl geschlossen, und sie läuft bei **jeder**
Anfrage. Ein kleines Modell mit strukturierter Ausgabe ist hier meist
genauer, weil die Aufgabe schmal ist — und um ein Vielfaches billiger.

Für die Bearbeitung zählt nur eines: die gemessene Trefferquote der
Werkzeugwahl und der Argumente (`goldfaelle.md`). Alles andere ist
Werbematerial.

## Feste Fassung

- **Nie „latest", nie ein gleitender Alias.** Ein Anbieter, der die
  Fassung hinter dem Alias austauscht, ändert das Verhalten des
  Assistenten ohne eine einzige Codeänderung. Das ist der Fehler, der am
  schwersten zu finden ist, weil niemand etwas getan hat.
- **Die Fassung steht in der Konfiguration**, versioniert, nicht im Code
  (Skill `neo-ki`).
- **Die Fassung steht im Goldfall-Bericht.** Ein Bericht ohne
  Modellfassung ist nicht vergleichbar.
- **Ein wöchentlicher Goldlauf ohne Änderung** deckt eine stille
  Verschiebung auf, bevor der Kunde sie meldet.

## Ein Modell vergleichen

Ein Vergleich ist nur dann einer, wenn **alles außer dem Modell gleich
bleibt**: derselbe Prompt, derselbe Katalog, dieselben Werkzeuge,
dieselben Goldfälle, dieselbe Zahl Läufe.

1. **Ausgangsmessung** mit dem heutigen Modell, **zehn Läufe**, Bericht
   als Datei aufbewahren.
2. **Nur das Modell tauschen.** Keine Prompt-Anpassung „passend zum neuen
   Modell" — sonst vergleicht man zwei Dinge.
3. **Dieselbe Messung**, zehn Läufe, zweiter Bericht.
4. **Gegenüberstellen**, je Absicht und je Sprache. Ein Mittelwert allein
   verdeckt genau den Einbruch, der wehtut.
5. **Kosten und Antwortzeit** danebenlegen — je Anfrage, hochgerechnet
   auf einen Tag im Betrieb.
6. **Vorlegen und entscheiden lassen.** Die Entscheidung liegt beim
   Projektinhaber (Skill `neo-grundregeln`), das Ergebnis wird als
   Entscheidungsakte festgehalten (Skill `neo-doku`).

**Ein Modellwechsel wird nie nebenbei mit einer anderen Änderung
ausgeliefert.** Ein Commit, eine Änderung, ein Messergebnis.

## Wenn das neue Modell schlechter ist

Das kommt vor, und es ist kein Rückschritt des Modells, sondern ein
Hinweis auf den eigenen Aufbau:

- **Prompt auf ein Modell hin optimiert** — Formulierungen, die für die
  alte Fassung nötig waren, stören die neue. Zu erkennen daran, dass
  Abschnitte mit Sonderbehandlung betroffen sind.
- **Beispieldialoge** — je stärker das Modell, desto genauer folgt es
  ihnen, auch dort, wo sie nicht passen (`sprachen.md`).
- **Formulierungen statt Schema** — ein Modell, das Prosa anders
  gewichtet, macht sichtbar, was nie erzwungen war (`werkzeuge.md`).

Die Antwort ist in allen drei Fällen dieselbe: **das Erzwungene stärken,
nicht den Prompt nachjustieren.**

## Nachrüsten statt hochrüsten

Bevor ein stärkeres Modell gewählt wird, sind diese Schritte billiger und
wirken zuverlässiger:

1. **Weniger Werkzeuge je Anfrage** — nur die der eingeordneten Absicht.
2. **Abgrenzung in den Werkzeugbeschreibungen** — die wirksamste einzelne
   Zeile.
3. **Aufzählungen statt Freitext** in den Argumenten.
4. **Zustand statt Erraten** — `heute`, Mandant, Auswahl mitgeben.
5. **Fachwissen aus dem Prompt** in ein Nachschlagewerkzeug.
6. **Zweite Stufe** einziehen.

Erst wenn diese sechs gemessen ausgereizt sind, ist die Modellfrage eine
Frage. Meistens ist sie es dann nicht mehr.

## Der Anbieter

- **Hinter der eigenen Abstraktion**, nie das SDK im Fachcode (Skill
  `neo-code`).
- **Ein zweiter Anbieter ist ein Betriebsthema**, kein Qualitätsthema:
  Rückfall bei Ausfall. Sein Modell durchläuft dieselben Goldfälle, sonst
  ist der Rückfall ein anderer Assistent.
- **Datenresidenz, Auftragsverarbeitung und Trainingsausschluss** sind
  vor der Modellwahl geklärt, nicht danach (Skill `neo-ki`,
  Skill `neo-recht`).
- **Was fremde Modelle sonst können, gehört nicht in eine Zusage.** Über
  ein Modell wird nur behauptet, was auf den eigenen Goldfällen gemessen
  wurde.
