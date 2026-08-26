# Entwurfsverfahren — vom Vorschlag zur Freigabe

Gilt für jede neue Ansicht, jeden Umbau einer bestehenden Ansicht, jede
neue Komponente mit sichtbarer Wirkung und jede Änderung an Layout,
Farbsystem, Typografie oder Navigation.

Nicht dafür gilt es: Textkorrekturen, Fehlerbehebungen ohne sichtbare
Änderung, das Einsetzen einer bereits freigegebenen Komponente an einer
weiteren Stelle.

## Reihenfolge

1. **Aufgabe klären.** Wer benutzt die Ansicht, in welcher Lage, mit
   welchem Wissen, unter welchem Druck? Welche Daten liegen wirklich vor?
   Ohne diese Antworten wird nicht entworfen.
2. **Bestand lesen.** Gibt es die Ansicht schon in ähnlicher Form? Dann
   ist ihr Muster die Vorgabe, nicht der eigene Geschmack. Vorhandene
   Komponenten, Tokens und Design-Referenzen des Projekts durchsehen.
3. **Mehrere Vorschläge bauen.** Zwei bis drei, die sich in der Struktur
   unterscheiden — nicht in der Farbe des Knopfes. Ein Vorschlagspaar,
   das dieselbe Anordnung in zwei Tönungen zeigt, ist kein Vorschlagspaar.
4. **Vorlegen.** Als Skizze oder Screenshot, nie als Beschreibung allein.
   Dazu je Vorschlag: was er löst, was er kostet, wo er unangenehm wird —
   und eine begründete Empfehlung.
5. **Änderungsrunden.** Der Projektinhaber korrigiert, der Entwurf wird
   überarbeitet und erneut vorgelegt. So oft, wie er es verlangt.
   Zwischen den Runden wird **nicht** gebaut.
6. **Freigabe abwarten.** Erst ein ausdrückliches Ja startet die
   Umsetzung. „Sieht gut aus" ist kein Ja, solange nicht klar ist, welcher
   Vorschlag gemeint ist.
7. **Bauen — genau das Freigegebene.** Abweichungen, die beim Bauen
   nötig werden, werden gemeldet, nicht entschieden.

## Was eine Skizze zeigen muss

Eine Skizze ist keine Stimmung, sondern eine Entscheidungsgrundlage.
Jeder Vorschlag zeigt:

- **Echte Inhalte.** Reale Feldnamen, plausible Werte, deutsche Texte in
  der Sie-Form. Kein Lorem Ipsum, keine Platzhalterbalken.
- **Den unangenehmen Fall**, nicht den schönen: die lange Bezeichnung,
  die volle Tabelle, den Fehlerzustand, die leere Liste.
- **Beide Fassungen**, hell und dunkel.
- **Mindestens zwei Breiten**, mobil (390 px) und Arbeitsbreite.
- **Die Zustände der Bedienelemente**, mindestens Ruhe, Hover, Fokus,
  Deaktiviert — nebeneinander auf einem eigenen Blatt.

## Format

Vorrang in dieser Reihenfolge:

1. **Klickprototyp als eigenständige HTML-Datei** mit den echten Tokens
   des Projekts. Er lässt sich anfassen, im Browser umschalten und
   später als Referenz für die Umsetzung verwenden. Für Oberflächen mit
   Zuständen und Abläufen ist er die einzige ehrliche Form.
2. **Entwurfsfläche (`/design`)** für frühe Struktursuche, wenn noch
   nicht feststeht, wie die Ansicht überhaupt geschnitten ist.
3. **Screenshot** einer bestehenden Ansicht mit eingezeichneter Änderung,
   wenn es um einen Umbau geht — Werkzeug und Markierungsregeln:
   Skill `neo-doku`, `references/screenshots.md`.

Von jedem Klickprototyp wird zusätzlich ein Screenshot erzeugt und
mitgeliefert, damit der Vorschlag ohne Browser beurteilbar ist.

## Ablage

Entwürfe liegen unter `/plan` bzw. `/plans` — nie in `/docs`, denn sie
beschreiben keinen IST-Zustand (Skill `neo-doku`). Empfohlen:
`plan/entwuerfe/<datum>-<thema>/` mit den Varianten, den Screenshots und
einer kurzen Seite, die Vorschläge, Empfehlung und die getroffene
Entscheidung festhält.

Nach der Umsetzung: Entscheidung in eine Entscheidungsakte (ADR)
überführen, Bedienung in die Anwenderdoku, Entwurf als umgesetzt
markieren. Freigegebene Klickprototypen bleiben als Referenz liegen —
die gebaute Oberfläche muss ihnen entsprechen, nicht ungefähr ähneln.

## Verbotene Abkürzungen

- Bauen und hinterher fragen.
- Einen einzigen Vorschlag vorlegen und ihn als alternativlos darstellen.
- Eine Beschreibung statt eines Bildes liefern.
- Beim Bauen „noch schnell" etwas verbessern, das nicht freigegeben war.
- Eine Variante zeigen, die man selbst nicht bauen würde, nur damit die
  bevorzugte besser aussieht.
