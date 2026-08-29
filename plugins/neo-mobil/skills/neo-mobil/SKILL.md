---
name: neo-mobil
description: >
  NEO-Regeln für mobile Anwendungen mit Flutter und Material Design 3.
  Diesen Skill laden, sobald eine App entsteht oder geändert wird:
  Widget, Screen, Route, Zustandsverwaltung, Plattformkanal, Paket,
  Build, Signierung, Veröffentlichung im Store. Ebenso bei Fragen zu
  Stateless gegen Stateful, Zustandsverwaltung, Layout und Umbruch auf
  Telefon und Tablet, zu Themes und Material-Design-3-Tokens, zu
  Berechtigungen, Offline-Verhalten, Hintergrundarbeit und
  Benachrichtigungen, zu Barrierefreiheit auf Mobilgeräten und zu Tests
  mit Widget- und Integrationstests. Ebenso bei lokaler Datenhaltung,
  Schemaversionen und Migrationen, unveränderlichen Aufzeichnungen sowie
  bei Betriebsgeräten und Peripherie: Vollbild und Kiosk, Scanner und
  Kartenleser als Tastatur, Drucker, Lade, Kamera und Biometrie. Ebenso bei der Frage, ob eine
  Funktion nativ statt in Flutter gebaut werden sollte.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# Mobile Anwendungen

Lesekonvention siehe `README.md` des Regel-Repositorys.

**Flutter ist der aktuelle Weg für mobile Anwendungen bei NEO.** Nativ
ist nicht ausgeschlossen — die Wahl trifft der Projektinhaber, nicht der
Agent, und sie wird begründet (Abschnitt 7).

Schichten und Benennung: Skill `neo-code`. Der Komponenten-Grundsatz
steht im Skill `neo-komponenten` und gilt hier **ohne Abzug**.

## Der Satz vorweg

> **Die API wird nachgeschlagen, nicht erinnert.**

**Flutter:** <https://docs.flutter.dev/llms.txt> (geprüft 2026-08).
Flutter und seine Pakete bewegen sich schnell; eine erinnerte Signatur
stammt oft aus einer Fassung, die es im Projekt nicht gibt (Skill
`neo-grundregeln`, Belegpflicht).

## 1. Widgets bleiben klein

- **Ein Widget, ein Zweck.** Eine `build`-Methode über 60 Zeilen ist ein
  Hinweis, kein Stil.
- **Widgets statt Hilfsmethoden**, die Widgets zurückgeben — nur echte
  Widgets werden vom Rahmen wiederverwendet und übersprungen.
- **`const`, wo es geht.** Jedes `const` ist ein Neubau weniger.
- **`StatelessWidget` als Standard**; Zustand ist eine Entscheidung.
- **Keine Fachlogik in `build`.** `build` läuft oft und darf nichts tun,
  was Zeit kostet.

## 2. Zustand an einer Stelle

- **Eine Zustandsverwaltung je Projekt**, nicht drei nebeneinander. Die
  Wahl wird einmal getroffen, begründet und festgehalten (Skill
  `neo-doku`, Entscheidungsakte).
- **Zustand liegt über der Oberfläche**, nicht darin verstreut.
- **Kein `setState` in einer Anwendung, die schon eine
  Zustandsverwaltung hat.**
- **Jede Ressource wird freigegeben**: Controller, Zuhörer, Ströme,
  Zeitgeber. Das ist die häufigste Ursache für Speicherlecks in Flutter.

## 3. Material Design 3

- **Material 3 als System**, nicht als Farbtopf: Farbrollen,
  Typografiestufen, Formstufen, Höhenstufen, Zustandsdeckschichten.
- **Die Farbrollen werden gesetzt, nicht gerechnet.** Material 3 ist
  zweierlei: ein Komponentensystem **und** ein Farbsystem, das aus einer
  Saatfarbe Tonpaletten erzeugt. Das zweite ist **nicht verpflichtend**:
  `ColorScheme(...)` nimmt jede Rolle einzeln. Wo eine Markenfarbe exakt
  gelten muss — eine kräftige, gesättigte zumal —, wird sie **gesetzt**;
  die Erzeugung aus einer Saatfarbe würde sie harmonisieren und dämpfen.
  Ob gesetzt oder gerechnet, ist eine **Entscheidung des
  Projektinhabers** und gehört in die Entscheidungsakte.
- **Das Theme kommt aus Tokens**, hell und dunkel, an einer Stelle. Keine
  Farbe, kein Maß und kein Radius im Widget-Code.
- **Radien, Höhenstufen und Zustandsdeckschichten sind die des Systems**,
  nicht die aus dem Entwurfswerkzeug abgemessenen. Flutter führt diese
  Skalen nicht als Schnittstelle — das Projekt führt sie als Tokens und
  prüft sie maschinell (`md3-token-check.py`, Skill `neo-design`).
- **Wo das Designsystem von Material abweicht, gewinnt das
  Designsystem** — und die Abweichung ist eine **Rückfrage** (Skill
  `neo-design`, `references/claude-design.md`).
- **Material-Widgets hinter den Wrappern der Produktfamilie**, wie im
  Web (Skill `neo-komponenten`).

Was Flutter von Material 3 liefert und was nicht, die Größenklassen der
Tasten, die geschlossenen Skalen für Symbol, Radius und Textrolle sowie
die bekannten Lücken des Rahmens: `references/material3.md`.

## 4. Größen: Telefon ist nicht die einzige Größe

Es gilt Skill `neo-design`, `references/responsiv.md` sinngemäß — die
Prüfbreiten sind andere, die Regeln dieselben:

- **Kein Überlauf.** Ein `RenderFlex overflowed` ist ein Fehler, keine
  Warnung.
- **Nichts ragt hinaus**, auch nicht bei größter Schrifteinstellung des
  Systems.
- **Keine Löcher beim Umbrechen** auf Tablet und Querformat.
- **Bedienziele mindestens 44 × 44 px**, mit Abstand dazwischen.
- **Text passt**: kein abgeschnittener Text, kein Bereich, der zu schmal
  für seinen Inhalt ist (Skill `neo-design`, `references/textpassung.md`).
- **Sichere Bereiche** beachten: Kerbe, Statusleiste, Gestenleiste,
  Tastatur.
- **Geprüft wird auf Telefon hoch und quer, Tablet hoch und quer**, bei
  kleinster und größter Systemschrift, hell und dunkel.

## 5. Barrierefreiheit gilt auch auf dem Telefon

- **Jedes Bedienelement hat einen Namen** für Vorlesegeräte.
- **Kontraste gerechnet**, nicht geschätzt (`contrast.py`, Skill
  `neo-design`).
- **Die Systemschrift wird respektiert** — eine App, die bei 200 %
  Schrift bricht, ist nicht fertig.
- **Bewegung reduzierbar**, wo das System es verlangt.
- Geprüft mit dem Vorlesegerät des Systems, nicht nur mit dem Prüfwerkzeug.

## 6. Betrieb

- **Keine Geheimnisse im Paket.** Was in der App liegt, ist öffentlich —
  auch in einem obfuskierten Paket (Skill `neo-sicherheit`).
- **Berechtigungen sparsam**, jede begründet, jede zum Zeitpunkt des
  Bedarfs erklärt. Eine abgelehnte Berechtigung ist ein vorgesehener
  Zustand, kein Absturz.
- **Offline ist ein Zustand, kein Fehler**: was ohne Netz geht, geht ohne
  Netz; was nicht geht, sagt es.
- **Kein Datenverlust beim Beenden.** Das System beendet Apps ohne
  Vorwarnung.
- **Pakete werden vorgelegt** — Zweck, Alternative, Pflegezustand,
  Lizenz, Plattformabdeckung (Skill `neo-grundregeln`).
- **Signierung und Veröffentlichung sind dokumentiert und
  reproduzierbar**; Schlüssel liegen nicht im Repository.

## 7. Lokale Daten

Eine mobile Anwendung ist offline-fähig oder sie ist es nicht.
Gerätestellungen, Bewegungsdaten und Stammdaten bleiben getrennt; jede
Schemaänderung erhöht die Version und bekommt ihren Migrationsschritt
samt Test; Aufzeichnungen, die lückenlos sein müssen, werden nur
angehängt und nie geändert. Geschrieben wird, BEVOR die Oberfläche
aufräumt. Einzelheiten: `references/persistenz.md`.

## 8. Geräte und Peripherie

Betriebsgeräte stehen in einer Halterung und hängen an Drucker, Scanner
oder Lade: Vollbild und Kiosk, Fremdgeräte, die wie eine Tastatur
sprechen, Ausgabegeräte hinter einer Schnittstelle mit Attrappe,
Berechtigungen zum Zeitpunkt des Bedarfs, Offline als Normalfall.
Einzelheiten: `references/geraete.md`.

## 9. Flutter oder nativ

Die Frage wird **gestellt, nicht stillschweigend beantwortet**. Für nativ
spricht: tiefe Systemintegration, Hardwarezugriff jenseits verfügbarer
Pakete, Anforderungen der Plattform, die Flutter nicht erfüllt. Für
Flutter spricht: eine Oberfläche für beide Plattformen, ein Team, ein
Testlauf.

**Die Entscheidung trifft der Projektinhaber**, mit Vor- und Nachteilen
vorgelegt, und sie wird als Entscheidungsakte festgehalten (Skill
`neo-doku`). Ein Wechsel mitten im Projekt ist eine Änderung mit
Auswirkung, kein Detail.

## 10. Tests

Es gilt Skill `neo-grundregeln`, `references/tests.md`. Zusätzlich:

- **Widget-Tests** für jedes Bedienelement: auslösen und das
  **beobachtbare Ergebnis** prüfen.
- **Integrationstests** für die Abläufe, mit dem Oberflächendurchlauf
  über jedes Bedienelement an **jeder** Stelle (Skill `neo-grundregeln`,
  `references/durchlauf.md`).
- **Goldene Aufnahmen je Bildschirm — gelegt aus dem Entwurf, nicht aus
  dem eigenen Bau.** Das ist die Brücke vom Designset in die App: Der
  Test ist rot, solange der Bildschirm dem Entwurf nicht entspricht.
  Bedingungen (Gerätegröße, Bildmaßstab, Farbschema, geladene Schriften,
  abgeschaltete Bewegung, feste Testdaten) sind in Entwurf und Test
  dieselben, die Toleranz ist benannt. Wer die Aufnahme aus dem eigenen
  Bau erzeugt, hat sich selbst bestätigt und nichts gemessen (Skill
  `neo-design`, `references/entwurfsbruecke.md`).
- Derselbe Vorbehalt wie beim Bildabgleich: Bereiche mit veränderlichem
  Inhalt werden ausgenommen, und die Ausnahme wird benannt.
- **Auf beiden Plattformen geprüft**, nicht nur auf der des Entwicklers.

## 11. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.

Zugehörige Skills: `neo-design` (Gestaltung, Größen, Barrierefreiheit),
`neo-komponenten` (Wrapper), `neo-code` (Schichten), `neo-api`
(Verträge), `neo-sicherheit` (Geheimnisse, Berechtigungen),
`neo-grundregeln` (Belegpflicht, Tests).
