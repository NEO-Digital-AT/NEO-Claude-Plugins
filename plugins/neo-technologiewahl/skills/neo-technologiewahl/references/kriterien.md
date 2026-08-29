# Die Kriterien im Einzelnen

Lesekonvention siehe `SKILL.md`.

Je Kriterium: was gefragt wird, was als Antwort zählt, und woran man
merkt, dass die Antwort schlecht ist.

## 1. Ausschluss — kann es die harte Anforderung?

- Rechtliche Pflicht (Fiskalisierung, Barrierefreiheit, Aufbewahrung),
  Offlinebetrieb, Zertifizierung, Datenhaltung in einem Rechtsraum.
- **Antwort zählt nur mit Fundstelle**, dass es geht — nicht, dass nichts
  dagegen spricht.
- **Schlechte Antwort:** „Sollte machbar sein." Machbar ist alles.

Was hier durchfällt, kommt nicht in den Vergleich. Ein Kriterium, das
später doch aufweicht, wird als Änderung der Voraussetzung behandelt und
neu vorgelegt.

## 2. Zielplattformen

- **Heute** und **in 24 Monaten**, getrennt beantwortet.
- Web zählt mit. Ein Verwaltungsbereich im Browser ist eine Plattform.
- **Schlechte Antwort:** „Erst mal nur Android." Das „erst mal" ist die
  Entscheidung, und sie muss ausgesprochen sein.

| Lage | Was daraus folgt |
| --- | --- |
| Eine Plattform, dauerhaft | Nativ ist ernsthaft im Rennen |
| Zwei oder mehr, gleiches Aussehen gewünscht | Ein Rahmenwerk, das selbst zeichnet |
| Zwei oder mehr, jeweils plattformtypisch | Nativ je Plattform, geteilte Fachlogik |
| Web dabei | Das schließt manches aus — früh prüfen |

## 3. Trägt es das Designsystem?

Das am häufigsten unterschätzte Kriterium.

- **Nicht:** „Hat es Bedienelemente?" **Sondern:** „Lässt sich **dieses**
  Aussehen bauen, und was kostet der Rest?"
- **Geprüft wird an der Lücke, nicht am Katalog.** Welche Komponente des
  Designsystems fehlt, welche Größe, welcher Zustand, welche Bewegung?
- **Eine fehlende Komponente ist wiederkehrende Arbeit**, kein einmaliger
  Aufwand: Sie muss gebaut, gepflegt, getestet und bei jeder Fassung des
  Systems nachgezogen werden.
- **Zeichnet das Rahmenwerk selbst oder benutzt es die Bedienelemente der
  Plattform?** Für ein eigenes Designsystem ist Selbstzeichnen ein
  Vorteil, für eine plattformtypische Anwendung ein Nachteil.

**Schlechte Antwort:** „Man kann alles nachbauen." Kann man. Die Frage
ist, wie oft.

## 4. Nähe zur Hardware und zum Betriebssystem

- Peripherie (Drucker, Kartenleser, Lade, Scanner), Sensoren,
  Hintergrundarbeit, Kiosk, Sperrbildschirm, Zweitbildschirm.
- **Je Gerät benennen, wie es angebunden wird**: fertiges Paket,
  Plattformkanal, oder Eigenbau.
- **Ein Paket eines Dritten ist eine Abhängigkeit mit Lebensdauer.**
  Letzte Fassung, Anzahl offener Fehler, ein Betreuer oder mehrere.
- **Schlechte Antwort:** „Dafür gibt es ein Paket." Welches, wie alt, von
  wem?

## 5. Wer pflegt es

- **Der Anbieter, der Rhythmus, die Richtung.** Wie oft erscheint eine
  Fassung, wie lange wird eine gepflegt?
- **Die offenen Tickets zum eigenen Bedarf**, mit Datum und Status. Ein
  Ticket, das seit einem Jahr offen ist, ist eine Antwort.
- **Angekündigte Richtung zählt mehr als der heutige Stand**, wenn das
  Projekt Jahre laufen soll.
- **Schlechte Antwort:** „Große Firma dahinter." Große Firmen stellen
  Dinge ein.

## 6. Bestand

- **Zeilen je Schicht zählen**, nicht schätzen: Fachlogik, Datenzugriff,
  Oberfläche, Übersetzungen.
- **Was ist Wissen und was ist Code?** Fachwissen, Datenmodell, Pläne und
  Schnittstellenentwürfe wandern mit, unabhängig von der Sprache.
- Einzelheiten: `wechselkosten.md`.

## 7. Team und Werkzeuge

- **Wer wartet es in zwei Jahren**, nicht wer es baut.
- **Was gibt es an Werkzeug?** Fehlersuche, Profiler, Tests,
  Oberflächenprüfung, Ausrollung. Ein Rahmenwerk ohne brauchbare
  Testwerkzeuge kostet in jeder Abnahme.
- **Wird mit einem Agenten gebaut, zählt die Sprachkenntnis des Teams
  weniger** — aber die Lesbarkeit des Ergebnisses zählt mehr
  (Kernregel 24).

## 8. Lizenz und Kosten

- Lizenz des Rahmenwerks **und** der Pakete, die man dazu braucht.
- Kosten je Bau, je Gerät, je Nutzer, je Umgebung.
- **Die Kosten des Ausstiegs** gehören dazu: Was passiert, wenn es in
  drei Jahren nicht mehr geht?

## Die Gewichtung wird aufgeschrieben

Ein Vergleich ohne Gewichtung ist eine Tabelle, keine Entscheidung. Die
Reihenfolge aus `SKILL.md` gilt als Vorgabe; wird davon abgewichen, steht
das mit Begründung in der Akte.

**Kein Punktesystem mit erfundenen Zahlen.** Eine Bewertung „7 von 10"
sieht genau, ist aber geraten. Besser ist ein Satz je Kriterium, der die
Fundstelle nennt — und am Ende eine Empfehlung, die man begründen kann.
