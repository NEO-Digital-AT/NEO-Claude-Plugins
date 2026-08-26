# Bestehende Bibliotheken, Migration, Frameworkwechsel

Lesekonvention siehe `SKILL.md`.

## Eine bestehende, produktive Bibliothek

**Eine bestehende Wrapper-Bibliothek wird nie ohne vorherige,
ausdrückliche Freigabe des Projektinhabers umgeschrieben.** Kein
Freigabeweg über den Umweg „ich habe es nur aufgeräumt".

Erlaubt ist ohne Freigabe:

- Einen Fehler in einer Komponente beheben.
- Eine fehlende Komponente ergänzen, wenn der Katalog sie vorsieht.
- Einen fehlenden Zustand ergänzen.

Erlaubt **nur mit Freigabe**:

- Den Vertrag einer Komponente ändern — Eigenschaften, Ereignisse, Slots.
- Eine Komponente umbenennen, zusammenlegen oder entfernen.
- Die Größenskala, die Tokens oder die Benennung ändern.
- Eine Komponente durch eine andere ersetzen.

**Nie erlaubt:** eine Komponente kopieren, um sie „für diese eine Seite"
anzupassen. Das ist der Anfang der zweiten Wahrheit.

## Ein bestehender Screen definiert das Muster

Definiert ein vorhandener Screen oder ein vorhandenes Modul das Muster
schon, wird **das Muster übernommen** — Struktur, Aufbau, Benennung,
Reihenfolge. Keine lokale Variante, kein „ich mache es diesmal besser".

Wer das Muster für falsch hält, legt eine Änderung für **alle** Stellen
vor, statt eine Ausnahme zu bauen.

Fehlt eine Komponenten-Definition: **nachfragen**, keinen generischen
Ersatz erfinden.

## Junge Anwendungen

In einer noch nicht weit fortgeschrittenen Anwendung darf nach Freigabe
umgebaut werden, was für den Grundsatz nötig ist. „Jung" heißt: die
Bibliothek ist noch nicht produktiv im Kundeneinsatz, und der Umbau
trifft eine überschaubare Zahl von Views.

Auch dann gilt: **erst der Plan, dann die Freigabe, dann der Umbau** —
und der Wächter wird im selben Schritt eingerichtet, nicht danach.

## Ein Projekt auf den Grundsatz bringen

Für Bestandsprojekte, die den Grundsatz nicht erfüllen. **Nie in einem
Zug, nie nebenbei in einem Feature-Zweig.**

1. **Messen, nicht schätzen.** Den Wächter schreiben und laufen lassen —
   mit allen Verstößen als Ausnahmeeinträge. Das Ergebnis ist die Liste
   der Arbeit, mit Zahlen.
2. **Vorlegen.** Anzahl der Verstöße je Regel und je View, Aufwand,
   Reihenfolge. Der Projektinhaber entscheidet über Umfang und Tempo.
3. **Den Katalog zuerst.** Die Komponenten, die alle Views brauchen
   (`katalog.md`), entstehen vor der ersten Umstellung.
4. **View für View umstellen**, je Umstellung ein Commit, je Umstellung
   ein Ausnahmeeintrag weniger. **Die Ausnahmeliste schrumpft
   monoton** — sie wächst nie wieder.
5. **Der Wächter läuft ab Tag eins als Blocker**, mit der Ausnahmeliste.
   Eine neue View darf nie einen neuen Eintrag erzeugen.

Der Fortschritt ist an der Länge der Ausnahmeliste ablesbar. Das ist die
Zahl, die berichtet wird.

## Frameworkwechsel

Das Ziel ist überprüfbar: **Beim Wechsel des Frameworks ändert sich
nichts unterhalb des Komponentenordners.**

Vor dem Wechsel wird gemessen, ob das stimmt:

1. **Kommt der Name des Frameworks außerhalb des Komponentenordners
   vor** — in einer View, einem Store, einem Test, einer Route, einer
   Konfiguration? Jedes Vorkommen ist eine Fessel. Der Wächter findet
   die in Views; die übrigen sucht eine einfache Textsuche.
2. **Steht ein Framework-Typ in der Signatur einer Komponente?** Dann
   wandert der Wechsel in die Views.

Der Ablauf:

1. Bestandsaufnahme nach 1. und 2., als Zahl.
2. Die Fesseln zuerst lösen, **vor** dem Wechsel.
3. Komponente für Komponente auf das neue Framework umbauen, mit
   unverändertem Vertrag nach außen.
4. **Nach jeder Komponente messen** — Layout- und Stilabgleich gegen das
   Designsystem (Skill `neo-design`). Ein Wechsel ohne Messung ist ein
   Neubau mit demselben Namen.
5. Die alte Bibliothek erst entfernen, wenn nichts mehr sie verwendet.

**Ein Frameworkwechsel ist eine tragende Entscheidung** und braucht eine
Entscheidungsakte vor der Umsetzung (Skill `neo-doku`).
