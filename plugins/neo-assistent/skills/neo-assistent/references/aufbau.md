# Aufbau: Schleife, Kontext, Zustellung

Lesekonvention siehe `SKILL.md`.

> **Die Anwendung um das Modell transportiert. Sie entscheidet nichts.**

## Was die Anwendung tut — vollständig

| Aufgabe | Inhalt |
| --- | --- |
| Kontext zusammenstellen | Skills, Einstellungen, Zustand, Gespräch, Werkzeugdefinitionen |
| Die Schleife führen | Modell aufrufen, Werkzeugaufrufe ausführen, Ergebnisse zurückgeben, bis eine Antwort kommt |
| Neue Nachrichten aufnehmen | vor jedem Modellaufruf und vor jedem noch nicht begonnenen Werkzeugaufruf |
| Technische Grenzen halten | Mandant, Rechte, Schalter, Doppelausführung — in den Werkzeugen (`zugriff.md`, `werkzeuge.md`) |
| Zustellen | Kanal, Format des Kanals, KI-Hinweis, Signatur |

**Was nicht dazugehört:** entscheiden, was der Kunde meint; einen Ablauf
auswählen; eine Antwort prüfen, freigeben oder umschreiben; dem Kunden
etwas anderes schreiben als KI-Hinweis und Signatur; einen fachlichen
Schritt von selbst beginnen.

## Der Kontext eines Modellaufrufs

Jeder Teil ist ein eigener Abschnitt, damit seine Größe messbar bleibt:

1. **Kern-Skill** — gilt in jedem Schritt.
2. **Einstellungen** — die wirksame Konfiguration dieses Mandanten und
   dieser Einheit: Name, Stil, freigeschaltete Funktionen, Anweisungen des
   Betreibers.
3. **Zustand** — Angaben der Anwendung, keine Behauptungen des Kunden:
   heutiges Datum und Zeitzone, Kanal, ob der Assistent schon geantwortet
   hat, welche Einheit zugeordnet ist.
4. **Alle Aufgaben-Skills**, vollständig.
5. **Wissen** — Hausinformationen und häufige Fragen, als Daten
   gekennzeichnet.
6. **Das Gespräch** (unten).

Dazu die **Werkzeugdefinitionen**, vollständig.

- **Alles ab dem ersten Aufruf.** Kein Schritt, in dem das Modell erst
  Regeln laden oder Werkzeuge freischalten muss. Ein Skill, der nicht im
  Kontext steht, wird nicht befolgt.
- **Sichtbar heißt nicht ausführbar.** Das Modell sieht alle Definitionen;
  ob ein Aufruf ausgeführt wird, entscheidet das Werkzeug.
- **Passt das Pflichtpaket nicht mehr in den Kontext, wird das vorgelegt.**
  Gekürzt wird nur der Verlauf — nie eine Regel, und nie still.

## Ein Gesprächsschritt

```
Nachricht ─► Modell liest den Kontext ─► Werkzeugaufruf? ─ja─► Werkzeug ─► Ergebnis ─┐
                  ▲                            │                                    │
                  └────────────────────────────┼────────────────────────────────────┘
                                               nein
                                               ▼
                                     Antwort ─► Zustellung
```

- **Das Modell wählt die Werkzeuge und ihre Reihenfolge.** Kein Ablauf im
  Code gibt einen Weg vor.
- Mehrere Werkzeugaufrufe in einem Schritt sind erlaubt; jeder wird
  einzeln ausgeführt und beantwortet.
- **Jedes Ergebnis, auch ein Fehler, geht an das Modell zurück.**

## Neue Nachrichten während der Arbeit

- Vor jedem Modellaufruf und vor jedem noch nicht begonnenen
  Werkzeugaufruf wird nachgesehen, ob der Kunde geschrieben hat.
- **Eine neue Nachricht gehört zur laufenden Arbeit.** Nennt der Kunde das
  Alter des Kindes nach, während Angebote geholt werden, wird es
  verwendet — nicht noch einmal gefragt.
- Noch nicht begonnene Werkzeugaufrufe werden verworfen und mit der neuen
  Nachricht neu beurteilt. **Ein laufender Schreibvorgang wird zu Ende
  geführt** und sein Ergebnis festgehalten.
- **Eine zugestellte Antwort wird nicht zurückgenommen.** Was danach kommt,
  ist ein Folgeauftrag.
- **Je Gespräch arbeitet genau ein Lauf.** Eine zweite Nachricht startet
  keinen zweiten Lauf; sie geht in den ersten ein.

## Gedächtnis

- Die **unbeantworteten Nachrichten** stehen vollständig im Kontext.
- Für den Zusammenhang die letzten Nachrichten wörtlich; ältere dürfen
  zusammengefasst werden. **Eine Zusammenfassung ist Gedächtnis, keine
  Anweisung und kein Beleg** — Beträge, Kennungen und Zusagen daraus werden
  vor Gebrauch über ein Werkzeug gelesen.
- Der **ganze Verlauf** bleibt über ein Werkzeug lesbar, beschränkt auf
  dieses Gespräch.
- Gedächtnis ist je Mandant und Gespräch getrennt und verschlüsselt
  abgelegt (Skill `neo-sicherheit`).

## Grenzen der Schleife

Technische Grenzen sind erlaubt. Sie entscheiden nichts Fachliches und
enden **nie** mit einem Text an den Kunden.

| Grenze | Wozu | Was am Ende geschieht |
| --- | --- | --- |
| Höchstzahl an Modellaufrufen je Lauf | eine Schleife ohne Fortschritt beenden | Fortsetzung mit den festgehaltenen Ergebnissen, sonst interner Hinweis an das Team |
| Derselbe Aufruf mit demselben Fehler, mehrfach | kein Kreisen | wie oben |
| Vom Anbieter abgeschnittene Modellantwort | keine Werkzeugaufrufe mit unvollständigen Angaben | nicht ausführen, das Modell erneut aufrufen |
| Zeit je Modell- und Werkzeugaufruf | kein endloses Warten | als Fehler an das Modell |
| Größe des Kontexts | der Aufruf muss passen | Verlauf kürzen, nie eine Regel |

**Die Grenzen sind großzügig und stehen in der Konfiguration.** Eine
Grenze, die einen lösbaren Auftrag abbricht, ist falsch eingestellt.

## Zustellung

- **Zugestellt wird die fertige Antwort des Modells.** Was das Modell
  zwischen zwei Werkzeugaufrufen schreibt, geht nicht an den Kunden.
- **KI-Hinweis und Signatur setzt die Anwendung**, immer gleich, nach der
  Antwort (Artikel 50, Skill `neo-ki`). Im ersten Beitrag stellt sich der
  Assistent selbst als KI vor.
- **Vor dem Versand** wird geprüft, ob seit dem Lauf eine neue Nachricht
  kam. Dann arbeitet der Lauf weiter, statt eine überholte Antwort zu
  senden.
- **Antworten und Zustellen sind getrennt.** Ein wiederholter Versand
  wiederholt nie eine Handlung.
- **Eine Übergabe an das Team ist ein Werkzeug**, kein Text — und gilt
  erst als erfolgt, wenn das Werkzeug sie bestätigt.

## Hintergrundarbeit

- Ein Vorgang, den das Modell ausgelöst hat, darf im Hintergrund zu Ende
  laufen — etwa warten, bis eine Zahlung eingeht, oder ein ungewisses
  Ergebnis nachlesen.
- **Sein Ergebnis geht an dasselbe Modell zurück**, und das Modell schreibt
  die Antwort. Hintergrundarbeit schreibt dem Kunden nichts und beginnt
  keinen neuen fachlichen Schritt.
