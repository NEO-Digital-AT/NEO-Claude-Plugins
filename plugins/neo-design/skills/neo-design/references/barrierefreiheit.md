# Barrierefreiheit — Maßstab, Rechnung, Prüfung

## Rechtsgrundlage in Österreich

| Regelwerk | Wen es trifft | Seit |
| --- | --- | --- |
| **BaFG** — Barrierefreiheitsgesetz (Umsetzung der Richtlinie (EU) 2019/882, European Accessibility Act) | Produkte und Dienstleistungen am Markt, unter anderem elektronischer Geschäftsverkehr, Bankdienste, E-Books, Personenverkehr | 28.06.2025 |
| **WZG** — Web-Zugänglichkeits-Gesetz (Umsetzung der Richtlinie (EU) 2016/2102) | Websites und Apps öffentlicher Stellen | 2019 |
| **BGStG** — Bundes-Behindertengleichstellungsgesetz | Diskriminierungsverbot allgemein | 2006 |

Technisch führt beides auf **EN 301 549**. Der heute harmonisierte Stand
ist **V3.2.1 (2021-03)** und verweist auf **WCAG 2.1 AA**. Die Fassung
**V4.1.1** mit **WCAG 2.2 AA** wird für Oktober 2026 im Amtsblatt der EU
erwartet und löst V3.2.1 dann ab.

**Arbeitsmaßstab dieses Regelwerks: WCAG 2.2 AA, hart.** WCAG 2.2 AA ist
eine Obermenge von 2.1 AA — damit ist die heutige Rechtslage erfüllt und
beim Wechsel der Norm nichts nachzuziehen.

Eine Ausnahme gilt ausschließlich, wenn der Projektinhaber sie
ausdrücklich erteilt. Sie wird an der betroffenen Stelle im Code und in
der Doku vermerkt, mit Grund und Datum.

**Ehrlichkeitsregel.** „Barrierefrei", „BaFG-konform" oder „WCAG-konform"
nie behaupten. Ohne Prüfbericht einer unabhängigen Stelle ist es eine an
der Norm ausgerichtete Umsetzung. Wo eine Barrierefreiheitserklärung
verlangt ist, nennt sie den geprüften Stand und die bekannten Lücken.

## Kontrast

| Was | Mindestens | Kriterium |
| --- | --- | --- |
| Fließtext, Beschriftungen, Hilfetexte, Fehlertexte | **4,5:1** | 1.4.3 |
| Großtext (ab 24 px, oder ab 18,66 px fett) | **3:1** | 1.4.3 |
| Ränder von Bedienelementen, Zustandsmarkierungen, Symbole mit Bedeutung, Diagrammfarben, Fokusring | **3:1** | 1.4.11 |
| Ziel: Fließtext, wo die Marke es zulässt | 7:1 | 1.4.6 (AAA) |
| Rein dekorative Flächen, deaktivierte Elemente, Logos | keine Vorgabe | — |

Regeln zur Rechnung:

- Gerechnet wird gegen den **tatsächlichen Untergrund** — nicht gegen
  Weiß, weil das Element „meistens auf Weiß steht". Bei durchsichtigen
  Flächen wird die Zusammensetzung gerechnet, nicht geschätzt.
- Gerechnet wird in **beiden Themes** und in **jedem Zustand**: Ruhe,
  Hover, Fokus, Gedrückt, Aktiv, Fehler.
- **Deaktiviert ist von der Vorgabe befreit, aber nicht von der
  Verständlichkeit.** Ein deaktiviertes Element muss als solches erkennbar
  bleiben und sagen, warum es deaktiviert ist.
- Text über Bild oder Verlauf braucht eine deckende Trägerfläche. Ein
  Schatten hinter Text ist keine Lösung.

### Hover — der häufigste Fehler

Ein Knopf, dessen Schrift beim Überfahren fast die Farbe seiner Fläche
annimmt, ist unbrauchbar, auch wenn er im Ruhezustand jede Prüfung
besteht. Deshalb:

- Beim Überfahren wird **Vordergrund gegen die Hover-Fläche** gerechnet,
  nicht gegen die Ruhefläche.
- Hover verschiebt um **genau eine Stufe** — eine Aufhellung, eine
  Randverstärkung. Kein Farbwechsel des Textes, der ihn der Fläche
  annähert. Keine Umkehrung von Vorder- und Hintergrund.
- Hover ist nie die **einzige** Anzeige einer Bedienbarkeit: was
  anklickbar ist, ist auch ohne Zeiger erkennbar. Auf Berührungsgeräten
  gibt es kein Hover.
- Inhalte, die bei Hover oder Fokus erscheinen (Tooltip, Menü), müssen
  ohne Mausbewegung schließbar sein, mit dem Zeiger erreichbar bleiben
  und stehen bleiben, bis sie geschlossen werden (1.4.13).

### Kontrast rechnen

```
# Ein Paar
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kontrast.py "#5C5470" "#FFFFFF"

# Durchsichtige Hover-Fläche über einer Grundfarbe
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kontrast.py "#FFFFFFCC" "#2A025F" --grund "#0F0524"

# Alle Paare eines Projekts, als Tor in der CI
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kontrast.py --paare design/kontrastpaare.json
```

Die Paardatei gehört ins Projekt und wächst mit ihm. Sie ist der Beleg,
dass geprüft wurde — nicht der Satz „sieht gut aus". Beispiel für den
Aufbau liefert `--beispiel`.

## Tastatur

- **Alles ist ohne Maus bedienbar**, in sinnvoller Reihenfolge, ohne
  Falle. Was mit der Maus geht, geht mit der Tastatur.
- Der Fokus ist immer sichtbar: mindestens 2 px, 3:1 gegen die Umgebung,
  mit Abstand zum Element. Ein zweiteiliger Ring (Akzentfarbe plus
  Flächenfarbe versetzt) bleibt auch auf farbigen Flächen sichtbar.
- Das fokussierte Element wird von nichts verdeckt — nicht von einem
  klebenden Kopf, nicht von einer Fußleiste (2.4.11).
- Dialoge fangen den Fokus, geben ihn beim Schließen an den Auslöser
  zurück und schließen auf Escape.
- Ein Sprunglink „Zum Inhalt" steht vor der Navigation.
- Ziehen ist nie der einzige Weg: jede Sortierung per Ziehen hat eine
  Tastaturalternative (2.5.7).
- Tastaturkürzel aus einzelnen Buchstaben sind abschaltbar oder
  umbelegbar.

## Ziele und Zeigergenauigkeit

- Bedienziele mindestens **24 × 24 px** (2.5.8), auf Berührungsgeräten
  44 × 44 px anstreben. Kleinere Symbole bekommen eine größere Fläche.
- Zwischen zwei Zielen genug Abstand, dass der Daumen nicht das falsche
  trifft.

## Vorlesegeräte und Struktur

- Eine Überschriftenhierarchie ohne Sprünge, eine H1 je Seite.
- Bedeutung steckt in der Auszeichnung, nicht nur im Aussehen: Listen
  sind Listen, Tabellen haben Kopfzellen, Formulare haben verknüpfte
  Beschriftungen.
- Jedes Symbol, das eine Handlung auslöst, trägt einen Namen — nicht
  ableitbar, nicht optional.
- Zustandsänderungen werden angesagt: höfliche Live-Region für Erfolg
  und Information, bestimmte nur für Ausfälle (4.1.3). Der Meldungstext
  steht **in** der Region, nicht daneben.
- Dekorative Grafik bleibt für Vorlesegeräte unsichtbar. Ein Diagramm ist
  nicht dekorativ: es braucht eine Textfassung oder eine Tabelle.
- Ein Balken aus vielen Segmenten braucht eine vorlesbare Zusammenfassung
  davor und eine Möglichkeit, ihn zu überspringen.

## Bewegung, Zeit und Zoom

- `prefers-reduced-motion` wird beachtet: keine Einflüge, kein Bounce,
  keine Dauerschleifen. Übrig bleibt ein Farbwechsel.
- Nichts blinkt mehr als dreimal je Sekunde.
- Automatisch Wechselndes lässt sich anhalten. Zeitgrenzen lassen sich
  verlängern; eine Sitzung läuft nicht ohne Vorwarnung ab.
- Text lässt sich auf 200 % vergrößern, ohne dass Inhalt verloren geht
  (1.4.4). Bei 400 % Zoom bricht die Seite auf eine Spalte um, ohne
  horizontales Scrollen (1.4.10) — siehe `responsiv.md`.
- Erhöhte Zeichen-, Wort- und Zeilenabstände zerstören kein Layout
  (1.4.12). Feste Höhen an Textbehältern sind deshalb verboten.

## Neu in WCAG 2.2 — Punkte, die hier oft fehlen

| Kriterium | Bedeutung |
| --- | --- |
| 2.4.11 Fokus nicht verdeckt | Der Fokus liegt nie unter einem klebenden Kopf oder einer Leiste |
| 2.5.7 Ziehbewegungen | Alles, was gezogen wird, geht auch per Knopf oder Tastatur |
| 2.5.8 Zielgröße | Mindestens 24 × 24 px |
| 3.2.6 Gleichbleibende Hilfe | Hilfe und Kontakt stehen auf jeder Seite an derselben Stelle |
| 3.3.7 Keine doppelte Eingabe | Was im Ablauf schon eingegeben wurde, wird nicht erneut verlangt |
| 3.3.8 Zugängliche Anmeldung | Keine Anmeldung, die ein Gedächtnisrätsel verlangt; Einfügen aus dem Kennwortspeicher muss erlaubt sein |

## Sprache und Verständlichkeit

- Die Seitensprache ist ausgezeichnet, abweichende Abschnitte ebenfalls.
- Fehlermeldungen benennen Ursache und nächsten Schritt in ganzen Sätzen.
- Fachbegriffe werden beim ersten Auftreten erklärt oder vermieden.
- Abkürzungen und Einheiten ausgeschrieben, wo Platz ist.

## Prüfung vor der Fertigmeldung

1. Kontrastrechnung für alle neuen Paare, **einschließlich Hover**, in
   beiden Themes — Ergebnis als Zahl berichten, nicht als Einschätzung.
2. Ansicht ohne Maus vollständig bedienen, einmal durch, Fokus dabei
   ansehen.
3. Ansicht in Graustufen ansehen: bleibt jeder Zustand unterscheidbar?
4. Auf 400 % zoomen: entsteht horizontales Scrollen?
5. Vorlesegerät über die Ansicht laufen lassen: hat jedes Bedienelement
   einen Namen, wird jede Statusänderung angesagt?
6. Automatische Prüfung laufen lassen, wo das Projekt eine hat (axe,
   Lighthouse, Pa11y). Sie ersetzt die Punkte 1 bis 5 nicht — sie findet
   erfahrungsgemäß nur einen Teil der Verstöße.
