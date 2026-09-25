# Inhaltsänderungen an einer bestehenden Seite

Lesekonvention siehe `SKILL.md`.

> **Eine Inhaltsänderung ist eine Migration, kein SQL zum Eintippen.**

Am Server gibt niemand etwas von Hand ein. Kein SQL-Schnipsel mit
Anleitung, kein „bitte im Backend ändern", kein „das einmal am Server
ausführen". Eine Textänderung, die live gehen soll, ist eine Migration im
Projekt-Bundle und läuft beim Ausrollen mit `contao:migrate`.

Bisher regelte dieser Skill nur **Schema**migrationen und den idempotenten
Seed (`betrieb.md`). Diese Datei regelt die Änderung von **Inhalt**: Text,
Titel, Meta-Angaben, FAQ-Einträge, Listeneinträge, Symbole, Links.

## 1. Jede Inhaltsänderung ist eine Migration

- **Im Projekt-Bundle**, mit dem Tag `contao.migration`. Sie läuft beim
  Ausrollen, zusammen mit den Schemamigrationen.
- **Nie SQL zum Eintippen**, nie eine Anleitung für das Backend, nie ein
  Befehl, den jemand auf dem Server absetzt.
- Was dazugehört: Text, Titel, `pageTitle`, Beschreibung, FAQ-Frage und
  -Antwort, Einträge eines `listWizard`, Symbolnamen, Links, Alternativtexte.

## 2. Die Datenbank ist die Wahrheit

**Ein Schritt ändert ein Feld nur, solange es exakt den alten Wert hat**
oder den zu entfernenden Satz noch enthält.

- **Dieselbe Bedingung steht an zwei Stellen**: in der Prüfung, ob der
  Schritt offen ist, und im `WHERE` des `UPDATE`. Zwei verschiedene
  Bedingungen sind ein Fehler, auch wenn sie sich gleich lesen.
- **Was die Redaktion seither geändert hat, bleibt unangetastet** — bei
  diesem Ausrollen und bei jedem künftigen. Die Migration überschreibt
  keine redaktionelle Arbeit, niemals.
- Ein Feld, das den alten Wert nicht mehr trägt, ist **nicht offen**. Das
  ist kein Fehler, sondern der Normalfall nach einer Redaktionsänderung.

## 3. Serialisierte Felder werden entpackt, nicht ersetzt

Betrifft `listWizard`, die Blog-FAQ in der Form `Frage | Antwort` und
jedes Blob-Array.

**Nie per SQL-`REPLACE`.** `serialize()` schreibt die Länge jeder
Zeichenkette mit; ein `REPLACE` verändert den Text, nicht die Länge, und
das Feld ist danach unlesbar — für Contao und für jeden anderen.

Der Ablauf:

```
1  unserialize($roh, ['allowed_classes' => false])
2  in den Werten ersetzen
3  serialize(...) neu packen
4  UPDATE ... SET feld = :neu WHERE feld = :alterRohwert
```

- **`allowed_classes => false` ist Pflicht.** Ein serialisiertes Objekt aus
  der Datenbank wird nicht instanziiert.
- **Das `WHERE` vergleicht den alten Rohwert**, nicht den entpackten.
- **Ein Feld, das sich nicht entpacken lässt, gilt als nicht offen.** Es
  wird übersprungen und gemeldet, nicht repariert.

## 4. Nach dem Ausführen ist der Schritt nicht mehr offen

`contao:migrate` wiederholt offene Migrationen, auch zwischen den
Schema-Abgleichen, bis nichts mehr offen ist — und bricht erst bei seiner
Schleifengrenze ab.

> **Ein Schritt, der nach dem Ausführen noch offen meldet, dreht den
> Deploy im Kreis. Die Seite bleibt beim Containerstart unten.**

- **Pflichttest: Die Migration läuft zweimal hintereinander.** Der zweite
  Lauf meldet „Nichts zu tun". Ohne diesen Test gilt die Migration als
  nicht geprüft.
- Die Prüfung „ist offen" wird deshalb **gegen das Ergebnis** formuliert:
  Ist der neue Wert da, ist nichts offen.

## 5. Zeilen über stabile Merkmale finden

- **Nie über IDs aus einer lokalen Kopie.** Die IDs unterscheiden sich
  zwischen Entwicklung, Vorschau und Live.
- **Stabil ist**: Seiten-Alias plus Elementtyp plus ein eindeutiges
  Merkmal des Eintrags — etwa dessen Titel oder der Anfang seines Textes.
- Findet die Bedingung **mehr als eine** Zeile, ist sie nicht eindeutig
  genug: Der Schritt bricht ab und meldet es, statt zu raten.

## 6. Der Seed kommt im selben Commit mit

Die Vorlage wird auf denselben Text gebracht, damit neue Projekte und
Neuaufbauten stimmen.

- **Der Seed überschreibt die Datenbank nie** (`betrieb.md`). Er legt an,
  was fehlt.
- **Migration und Seed im selben Commit.** Sonst steht in der Vorlage der
  alte Text, und der nächste Neuaufbau bringt ihn zurück.

## 7. Geprüft wird gegen eine Kopie des Live-Bestands

Nicht gegen eine leere Datenbank, nicht gegen die Entwicklungsdaten:

```
1  Kopie des Live-Bestands einspielen
2  contao:migrate                      erster Lauf
3  contao:migrate                      zweiter Lauf: „Nichts zu tun"
4  betroffene Seiten rendern
5  alte Texte suchen                   null Treffer
6  neue Texte suchen                   gefunden
```

**Nach dem Ausrollen wird dieselbe Prüfung auf der Live-Seite
wiederholt** — Schritt 4 bis 6. Ein Ausrollen ohne diese Wiederholung
gilt als nicht abgeschlossen.

## 8. Das Ergebnis nennt jeden ausgeführten Schritt

Die Migration gibt je ausgeführtem Schritt dessen **Bezeichnung** zurück.
So steht im Deploy-Protokoll, was sich geändert hat — nicht „Migration
gelaufen", sondern welche Texte auf welchen Seiten.

## 9. Felder aus Erweiterungen werden vorher geprüft

Vor dem Zugriff: Gibt es die Tabelle? Gibt es die Spalte? Eine
Erweiterung kann in einer Umgebung fehlen oder eine andere Fassung haben.
Fehlt sie, ist der Schritt **nicht offen** — kein Fehler, keine Ausnahme.

## Das Muster: ein Schritt ist ein Tripel

Bewährt in einem NEO-Projekt, hier so beschrieben, dass es ohne dieses
Projekt nachgebaut werden kann. Eine abstrakte Basisklasse hält die
Mechanik, die konkrete Migration nur ihre Schritte.

**Ein Schritt besteht aus dreierlei:**

| Teil | Bedeutung |
| --- | --- |
| **Bezeichnung** | Ein Satz, der im Deploy-Protokoll steht |
| **offen()** | `true`, solange der Schritt noch etwas zu tun hat |
| **ausführen()** | Führt genau diesen Schritt aus |

Die Basisklasse stellt drei Bausteine bereit, und jeder trägt die
Bedingung aus Regel 2 in sich:

| Baustein | Was er tut |
| --- | --- |
| `setIfOld(Tabelle, Zeile, Feld, alteWerte, neuerWert)` | Setzt das Feld nur, solange es einen der alten Werte trägt |
| `replaceIn(Tabelle, Zeile, Feld, Suchtext, Ersatz)` | Ersetzt einen Textteil, solange der Suchtext noch enthalten ist |
| `replaceInSerialized(Tabelle, Zeile, Feld, Suchtext, Ersatz)` | Wie oben, aber entpackt und packt neu (Regel 3) |

Und zwei Methoden nach außen:

| Methode | Verhalten |
| --- | --- |
| `shouldRun()` | Wahr, solange **ein** Schritt offen ist |
| `run()` | Führt **nur die offenen** Schritte aus und gibt deren Bezeichnungen zurück |

**Die Reihenfolge ist wichtig:** `shouldRun()` fragt jeden Schritt, ob er
offen ist, ohne etwas zu ändern. `run()` fragt erneut und führt nur aus,
was noch offen ist. Damit ist ein zweiter Lauf von sich aus leer, und
Regel 4 ist strukturell erfüllt statt durch Disziplin.

**Eine Migration mit einem Schritt ist der Normalfall.** Die Basisklasse
lohnt sich ab dem zweiten, weil die Mechanik dann nicht doppelt
geschrieben und doppelt geprüft wird.

## Abnahme

- [ ] Kein SQL zum Eintippen, keine Backend-Anleitung, kein Befehl für den
      Server — die Änderung ist eine Migration im Bundle.
- [ ] Jeder Schritt hat eine **Bezeichnung**, die im Protokoll erscheint.
- [ ] **Dieselbe Bedingung** in „ist offen" und im `WHERE`.
- [ ] Serialisierte Felder entpackt und neu gepackt, nie per `REPLACE`;
      `allowed_classes => false` gesetzt.
- [ ] **Zweimal hintereinander gelaufen**, der zweite Lauf meldet „Nichts
      zu tun".
- [ ] Zeilen über stabile Merkmale gefunden, **keine IDs** aus einer Kopie.
- [ ] Mehrdeutige Bedingung bricht ab, statt zu raten.
- [ ] Der Seed trägt denselben Text, im **selben Commit**.
- [ ] Gegen eine **Kopie des Live-Bestands** geprüft: alte Texte null
      Treffer, neue Texte gefunden.
- [ ] Nach dem Ausrollen **auf der Live-Seite wiederholt**.
- [ ] Felder aus Erweiterungen vor dem Zugriff geprüft.
- [ ] Redaktionelle Änderungen sind unangetastet geblieben.
