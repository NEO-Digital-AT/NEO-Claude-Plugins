---
description: Oberfläche gegen die NEO-Gestaltungsregeln prüfen (Aufbau, Eingabeführung, Zustände, Kontrast, Barrierefreiheit, Größen, Texte)
---

Prüfe die angegebene Ansicht — oder, wenn nichts angegeben ist, die im
aktuellen Diff geänderten Ansichten — gegen die NEO-Gestaltungsregeln.

**Nichts reparieren. Nur prüfen, messen und berichten.** Reparaturen erst
nach Freigabe.

Lade zuerst den Skill `neo-design` und die Abnahmeliste
`references/pruefliste.md`. Arbeite dann diese Punkte ab und belege jeden
mit einer Fundstelle (Datei und Zeile) oder einer Zahl:

1. **Komponenten.** Verwendet die View ausschließlich Komponenten der
   Produktfamilie (`Neo*`, `LeoFlex*`)? Liste jedes rohe
   Framework-Element, jedes Farbliteral, jedes `style`-Attribut und jede
   erfundene Maßzahl mit Fundstelle auf.

2. **Aufbau.** Eine Hauptaufgabe, eine Hauptaktion? Stehen Aktionen am
   Ort ihrer Wirkung? Weicht die Anordnung von vergleichbaren Ansichten
   des Projekts ab?

3. **Eingabeführung.** Liste jedes Freitextfeld auf und beurteile je
   Feld, ob die Menge der gültigen Werte bekannt oder abfragbar ist.
   Jedes Feld, bei dem sie es ist, ist ein Befund. Prüfe außerdem:
   Masken, Prüfzeitpunkt, Voreinstellungen, Bestätigung bei
   Destruktivem.

4. **Zustände.** Sind Ruhe, Hover, Fokus, Gedrückt, Aktiv, Deaktiviert,
   Fehler und Ladend gebaut? Fehlt ein Leer-Zustand? Bleibt eine Aktion
   ohne sichtbare Rückmeldung?

5. **Kontrast — gerechnet, nicht geschätzt.** Sammle alle
   Farbkombinationen der Ansicht einschließlich der Hover- und
   Fokusfassungen, in Hell und Dunkel, und rechne sie:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/contrast.py <vorne> <hinten> [--grund <grund>] [--usage element]
   ```

   Berichte jeden Wert als Zahl. Text unter 4,5:1 sowie Bedienelement
   oder Grafik unter 3:1 ist ein Befund. Achte besonders auf Hover, wo
   sich Schrift und Fläche annähern.

6. **Barrierefreiheit.** Tastaturweg vollständig? Fokus sichtbar und
   nirgends verdeckt? Jeder Zustand mit Farbe **und** Symbol **und**
   Wort? Bedienziele mindestens 24 × 24 px? Symbole mit Namen?
   Statusänderungen angesagt? Ziehen mit Tastaturalternative?

7. **Größen.** Prüfe auf 320, 390, 768, 1024, 1280, 1920, 2560 und
   3840 px, ob der Seitenkörper waagrecht scrollt, und in jeder
   ausgelieferten Sprache. Nenne je Breite den Überstand in Pixeln.
   Gibt es keinen Test dafür, ist das selbst ein Befund.

8. **Texte.** Knöpfe mit Verb und Objekt? Fehlermeldungen mit Ursache
   und nächstem Schritt? Platzhalter als Beschriftung missbraucht?
   Sichtbarer Text außerhalb der Sprachdatei? Zusammengesetzte Sätze?
   ASCII-Ersatz statt echter Umlaute? Emojis?

9. **Tests und Doku.** Hat jedes Bedienelement einen
   Oberflächen-Funktionstest? Ist die Bedienungsdoku auf dem Stand der
   Ansicht?

Ergebnis als Liste, nach Schwere sortiert, je Befund: Fundstelle,
Feststellung, gemessener Wert, verletzte Regel, Vorschlag zur Behebung.

Am Ende zwei Zeilen:

- „Gemessen: <n> Kontrastpaare, <n> Breiten, <n> Sprachen."
- „Abnahmefähig: ja/nein" mit Begründung.

Was nicht geprüft werden konnte, wird als ungeprüft benannt — nie als
erfüllt.
