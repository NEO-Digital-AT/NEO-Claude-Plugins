---
name: neo-design
description: >
  NEO-Gestaltungs- und Bedienregeln. Diesen Skill laden, bevor eine
  Oberfläche entworfen, gebaut oder geändert wird: Seite, View, Screen,
  Dialog, Formular, Tabelle, Navigation, AppShell, Kopfzeile, Seitenleiste,
  Benutzermenü, Meldungsleiste. Ebenso bei Farb-, Layout-, Typografie- und
  Token-Arbeit, bei Fragen zu Kontrast, Hover, Fokus, Tastaturbedienung,
  Barrierefreiheit (BaFG, WZG, EN 301 549, WCAG), bei mobiler Ansicht,
  Umbruchpunkten und großen Bildschirmen sowie bei jeder Frage, welches
  Bedienelement für eine Eingabe richtig ist. Ebenso bei Webseiten-
  gestaltung, Animationen, Burgermenü, three.js und bei den Zielwerten
  aus PageSpeed Insights und Lighthouse (Leistung, Barrierefreiheit,
  Best Practices, SEO, agentisches Browsen). Zwingend, sobald ein Entwurf
  vorliegt und umgesetzt wird: Artboard aus Claude Design, Design-Set,
  Design-System, Klickprototyp — beim Bauen danach, beim Abgleichen
  dagegen und bei jeder Abweichung davon.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, belegt an bestehenden NEO-Projekten (Regeldateien, Entscheidungsakten zu Komponenten-Grundsatz und Logo/SVG, Token-Erzeugung), Stand 2026-08
---

# NEO-Gestaltungsregeln

Design ist nicht der Knopf. Design ist der ganze Weg durch die Anwendung:
Aufbau, Navigation, Verständlichkeit, Zurechtfinden, Sprache, Verhalten
bei Fehlern. Eine Oberfläche, die schön ist und in der sich niemand
zurechtfindet, ist nicht fertig. Eine, die funktioniert und eine
Anleitung braucht, auch nicht.

## Der Maßstab

Der Maßstab ist nicht „lässt sich bedienen", sondern **„lässt sich kaum
falsch bedienen"**. Vorbild ist die Schlichtheit von n8n und make.com:
sichtbare Struktur, geführte Eingabe, wenig Text an der richtigen Stelle.

Vier Fragen entscheiden über Fertig oder Nicht-fertig:

1. Weiß jemand ohne Anleitung, wo er ist und was hier geht?
2. Kann er hier etwas Falsches eingeben? Wenn ja: warum noch?
3. Trägt die Seite auf 320 px genauso wie auf 3840 px?
4. Ist jedes Element in jedem Zustand lesbar — auch beim Überfahren?

Eine Nein-Antwort ist ein Baumangel, keine Ausbaustufe.

## Zwei Betriebsarten

Alles in diesem Skill gilt für beide. Zwei Dinge unterscheiden sich:

- **Anwendung und Portal** — dicht, ruhig, arbeitsorientiert. Bewegung
  nur als Zustandswechsel. Muster sind gut: Wiedererkennung schafft
  Sicherheit.
- **Webseite** — großzügig, dynamisch, eigenständig. Bewegung ist Teil
  der Gestaltung. Muster sind schlecht: eine Seite, die wie jede andere
  aussieht, überzeugt niemanden. Regeln dafür, dazu die Liste der
  Muster, an denen man KI-gebaute Seiten erkennt:
  `references/webseiten.md`.

Welche Betriebsart gilt, steht in der Regeldatei des Projekts. Fehlt der
Eintrag: nachfragen, nicht annehmen.

## 1. Kein Bau ohne freigegebenen Entwurf

Oberflächen werden nicht „einfach gebaut". Reihenfolge ist verbindlich:
**mehrere Vorschläge → Skizze oder Screenshot → Änderungsrunden →
Freigabe → Bau.** Die Entscheidung, was und wie gebaut wird, liegt
ausnahmslos beim Projektinhaber. Eigenmächtige Gestaltung ist ein
Regelverstoß, auch wenn das Ergebnis gefällt.

**Liegt bereits ein Entwurf aus Claude Design vor, ist dieser Schritt
erledigt und die Gestaltung entschieden.** Dann gilt nicht „Vorschläge
machen", sondern Abschnitt 9: umsetzen, was da ist.

Ablauf, Format der Vorschläge und was eine Skizze zeigen muss:
`references/entwurfsverfahren.md`.

## 2. Aufbau vor Optik

- Jede Ansicht beantwortet in der ersten Bildschirmhöhe: wo bin ich, was
  ist der Zustand, was ist die nächste Handlung.
- Eine Ansicht hat **eine** Hauptaufgabe und **eine** Hauptaktion. Alles
  andere ist nachgeordnet und sieht auch so aus.
- Gleiche Dinge stehen überall an derselben Stelle. Der Speichern-Knopf
  wandert nicht von Seite zu Seite.
- Im Kopf steht, **wo** man ist, nicht was man tun kann. Aktionen stehen
  am Ort ihrer Wirkung: Tabellenaktionen über der Tabelle, Speichern am
  Fuß des Bereichs, Rückwege als Brotkrume im Inhalt.
- Verschachtelung höchstens zwei Ebenen tief. Wer eine dritte braucht,
  hat die Ansicht falsch geschnitten.
- Nicht alles auf einmal erklären. Die Oberfläche trägt den Satz, den man
  jetzt braucht; alles Weitere steht in der Dokumentation und wird von
  dort verlinkt (Skill `neo-doku`).

## 3. Eingaben führen, nicht abfragen

**Gilt überall und ohne Ausnahme.** Sie steht über Bequemlichkeit, über
Aufwand und über „das reicht fürs Erste".

Ein Freitextfeld ist die letzte Wahl, nicht die erste. Wo die Anwendung
weiß, was gültig ist, bietet sie es an — und was sie nicht weiß, holt sie
sich, bevor sie fragt.

- **Was nicht eingegeben werden kann, kann nicht falsch sein.** Ist die
  Menge der gültigen Werte bekannt, ist Auswahl, Schieber, Liste oder
  Maske dem Textfeld vorzuziehen.
- **Erst holen, dann anbieten.** Felder, Pfade, Klassen, Zeitzonen und
  Kennungen werden aus der Quelle gelesen und zur Auswahl gestellt, nicht
  eingetippt und beim Speichern zurückgewiesen.
- **Prüfen, während getippt wird.** Eine Rückmeldung nach dem Speichern
  ist eine Fehlermeldung; eine Rückmeldung beim Tippen ist eine Hilfe.
- **Ein erweiterter Modus für die Ausnahme.** Wer einen Wert braucht, den
  die Anwendung nicht kennt, bekommt ihn — hinter einem ausdrücklichen
  Schalter, nie als Standardweg.
- Ein Textfeld als Zwischenlösung ist keine Zwischenlösung, sondern der
  Endzustand, den nie wieder jemand anfasst.

Welches Bedienelement zu welchem Datentyp gehört, mit Masken, Formaten
und Grenzfällen: `references/eingaben.md`.

## 4. Ein Farb- und Layoutsystem, keine Seitenvarianten

- Farben ausschließlich über Design-Tokens bzw. Theme-Rollen. Kein
  Hex-Wert, kein rgba, kein Opacity-Trick in einer View.
- Abstände, Radien und Schriftgrößen nur aus der Skala des Systems. Keine
  erfundene Maßzahl.
- Farbe ist bedeutungstragend, nicht dekorativ. Die Fehlerfarbe ist für
  Zerstörendes reserviert. Höchstens eine Akzentfläche je Ansicht.
- Zustand nie nur über Farbe: immer **Farbe plus Symbol plus Wort**. Die
  Seite muss in Graustufen und bei Rot-Grün-Schwäche verständlich
  bleiben.
- Tiefe kommt aus Rändern, nicht aus Schatten. Keine dekorativen
  Verläufe, keine Muster, keine Ad-hoc-Designexperimente. **Dieser Punkt
  gilt für Anwendungen und Portale**; auf Webseiten darf die Marke
  tragen, nach `references/webseiten.md`.
- Hell- und Dunkelfassung sind gleichwertig. Ein Entwurf ohne geprüfte
  Dunkelfassung ist ein halber Entwurf.

Die Umsetzung dieser Regeln liegt in den Wrapper-Komponenten der
Produktfamilie, nie in der View — Skill `neo-komponenten`.

## 5. Jeder Zustand wird geprüft

Jedes Bedienelement hat mindestens diese Zustände, und **jeder einzelne
wird angesehen und gemessen**: Ruhe, Überfahren (Hover), Fokus,
Gedrückt, Aktiv/Ausgewählt, Deaktiviert, Fehler, Ladend.

- **Hover ist der häufigste Fehler.** Ein Knopf, dessen Schrift beim
  Überfahren fast die Farbe seiner Fläche annimmt, ist unbrauchbar. Der
  Kontrast wird gegen die **tatsächliche Hover-Fläche** gerechnet, nicht
  gegen den Ruhezustand. Hover verschiebt um genau eine Stufe.
- Deaktiviert heißt gedämpft, nicht unsichtbar, und sagt warum.
- Jede Fläche kennt einen Leer-Zustand mit Satz und nächster Handlung —
  eine leere Tabelle ohne Text sieht kaputt aus.
- Jede Aktion bestätigt sich sichtbar. Ein Formular, das auf Speichern
  hin still bleibt, sieht aus wie ein defektes.
- Destruktive Aktionen nie still: Bestätigungsdialog, der die Folge
  benennt.

## 6. Barrierefreiheit ist nicht verhandelbar

Rechtsgrundlage in Österreich: **BaFG** (in Kraft seit 28.06.2025) und
**WZG** für öffentliche Stellen, technisch über **EN 301 549**.

**Verbindlicher Arbeitsmaßstab: WCAG 2.2 AA — hart.** Fließtext
mindestens **4,5:1**, Großtext sowie Bedienelemente, Ränder, Symbole und
Diagrammfarben mindestens **3:1**, jeweils gegen den tatsächlichen
Untergrund, in Hell und Dunkel und in **jedem** Zustand einschließlich
Hover. AAA (7:1) anstreben, wo die Marke es zulässt. Eine Ausnahme gilt
nur, wenn der Projektinhaber sie ausdrücklich erteilt; sie wird an Ort
und Stelle vermerkt.

Ehrlichkeitsregel wie bei CRA: „barrierefrei" oder „BaFG-konform" nie
behaupten — ohne Prüfbericht ist es eine an der Norm ausgerichtete
Umsetzung, mehr nicht.

Kontrast rechnen statt schätzen:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kontrast.py "#5A6273" "#FFFFFF"
```

Vollständige Anforderungen, Tastaturbedienung, Fokus, Vorlesegeräte,
Bewegung und die Prüfliste: `references/barrierefreiheit.md`.

## 7. Von 320 px bis 4K

**Gilt für Anwendungen und Portale genauso wie für Webseiten.** Eine
Web-Anwendung ist keine Ausnahme, weil sie „am Schreibtisch bedient
wird". Der Funktionsumfang darf auf schmalen Geräten kleiner sein — **das
Aussehen nie**. Was weggelassen wird, entscheidet der Projektinhaber,
nicht der Umbruchpunkt.

Fünf harte Regeln, alle **maschinell geprüft** auf acht Breiten mit
`scripts/ueberlauf.js`, erlaubt sind **null Befunde**:

1. **Kein waagrechtes Scrollen des Seitenkörpers** — auf keiner Breite,
   auch nicht am Schreibtisch. Breite Inhalte scrollen in ihrem eigenen
   Bereich. `overflow-x: hidden` am Körper ist keine Behebung.
2. **Nichts ragt hinaus.** Kein Element steht über dem sichtbaren
   Bereich — auch kein geöffnetes Menü, kein klebender Kopf, kein Dialog.
3. **Tabellen füllen die Inhaltsbreite**, 100 %, nie schmaler. Breiter
   nur in einem ausdrücklichen Scrollbereich.
4. **Keine Löcher beim Umbrechen.** Drei Kacheln auf zwei Spalten lassen
   in der zweiten Reihe eine halbe Fläche frei — entweder gleich
   einspaltig, oder das letzte Element nimmt die volle Breite.
5. **Bedienziele wachsen zum schmalen Gerät hin**: bis 768 px mindestens
   44 × 44 px, darüber 24 × 24 px. Symbolknöpfe in Tabellenzeilen sind
   der häufigste Verstoß.
6. **Kein Text verschwindet** — und wo er nicht ganz passt, ist
   entschieden, wie. Nichts abgeschnitten, nichts überlappt, kein Bereich
   unter acht Zeichen je Zeile, kein Bruch mitten im Wort.

Dazu: unter dem Umbruchpunkt liegt das Hauptmenü hinter einem Knopf;
Inhaltsbereich, Textspalte und Eingabefelder haben **Höchstbreiten** aus
Tokens, damit ein Formular auf 4K nicht über die halbe Wand läuft.

**Der Überlauf ist nur die Hälfte.** Ein Kasten kann richtig sitzen und
der Text darin abgeschnitten, zwei Zeichen breit oder falsch umgebrochen
sein — das erzeugt keinen Balken. Deshalb misst `scripts/textpassung.js`
zusätzlich, was **innen** nicht passt. Für Fließtext gilt `hyphens: auto`
mit gesetzter Sprache — **ohne `lang` trennt der Browser nicht**;
`overflow-wrap: anywhere` ist für Kennungen richtig und für Fließtext
falsch. Wer kürzt, bietet den vollen Text an; eine Auslassung ohne
Volltext ist Datenverlust.

Gemessen wird je Seite, je Sprache, in Hell und Dunkel, mit **langen
Testdaten** und bei 200 % Textvergrößerung — ein Layout, das nur mit
kurzen Daten hält, hält nicht.

Umbruchpunkte, Tabellenrangfolge, Lückenregel mit Beispielcode,
Höchstbreiten und Navigation: `references/responsiv.md`. Umbruch, Kürzen,
zu schmale Bereiche und mitwachsende Schriftgrößen:
`references/textpassung.md`. Der Befehl
`/neo-design:neo-responsivpruefung` führt beide Messungen durch.

## 8. Texte in der Oberfläche

Beschriftungen sagen, was passiert („Auftrag anlegen", nicht „OK").
Fehlermeldungen benennen Ursache und nächsten Schritt, nie einen Code
allein. Hilfetexte stehen am Feld, nicht im Handbuch. Sentence case,
Sie-Form, echte Umlaute, keine Emojis, keine Marketingsprache.

**In einem mehrsprachigen Produkt hat jeder sichtbare Text in jeder
ausgelieferten Sprache eine Übersetzung — gemessen, nicht angenommen**
(`scripts/uebersetzungen.py`): null fehlende Schlüssel, null leere Werte,
null abweichende Platzhalter. Ein Schlüssel mitten in der Oberfläche ist
der sichtbarste Mangel, den ein Produkt haben kann. Rückfall ist
**Englisch**, nie der Schlüssel und nie ein leerer Text.

Formulierungen, Fehlertext-Muster, Leerzustände und Ladehinweise:
`references/oberflaechentexte.md`. Vollständigkeit, Platzhalter,
Pluralformen und was das Werkzeug **nicht** sieht:
`references/uebersetzungen.md`.

## 9. Liegt ein Designsystem vor: es gibt vor, der Agent setzt um

> **Claude Design gibt vor. Der Agent setzt um. Der Agent gestaltet
> nicht.**

Ein Designsystem — Artboards aus Claude Design, ein Design-Set, ein
freigegebener Klickprototyp — ist **die Bauvorgabe und die
Abnahmegrundlage**, keine Anregung. Der Projektinhaber hat den Entwurf
gemacht und hat ein Ergebnis im Kopf. Gebaut wird **dieses** Ergebnis —
nicht ein ähnliches, nicht ein besseres.

**Der Agent trifft keine Gestaltungsentscheidung.** Nicht über Layout,
Abstand, Polster, Radius, Schriftmaß, Farbe, Bauteilwahl, Lage der
Aktionen oder Umbruchverhalten. Jede Abweichung — auch eine bessere,
auch eine winzige, auch eine offensichtliche — ist eine **Rückfrage**.
Eine Empfehlung ist erlaubt, eine Entscheidung nicht.

**Die Trennlinie läuft zwischen Gestaltung und Fachlichkeit:**

| Vorgegeben — nur nach Rückfrage anders | Von der Aufgabe bestimmt — frei |
| --- | --- |
| Seitenaufbau, Raster, Karten, Abstände, Typografie, Farben, Zustände, Aufbau von Formular und Tabelle, Lage der Aktionen | **Welche** Felder ein Formular hat, **welche** Werte in Auswahl und Combobox stehen, Pflicht/optional, Prüfregeln, Verhalten, Zeilenzahl aus Daten |

> **Ein Feld mehr ist normal. Ein Feld, das anders aussieht als die
> Felder im Designsystem, ist ein Fehler.**

**Kein Bau ohne Inventar.** Vor der ersten Zeile wird jedes Element des
Artboards von oben nach unten mit seinen **gemessenen** Maßen gelistet
und vorgelegt. Dann wird **Element für Element** gebaut und nach jedem
Element gemessen — nicht die Seite bauen und am Ende vergleichen. Zum
Schluss der Durchgang über die ganze Seite, auch als Gesamteindruck.

**Fertig heißt gemessen.** Drei Prüfungen, in dieser Reihenfolge:

| Prüfung | Werkzeug | Antwort | Erlaubt |
| --- | --- | --- | --- |
| **1. Layout** | `scripts/layoutabgleich.js` | Sind Maße, Lage und Abstände gleich? | 0 Abweichungen bei 1 px |
| **2. Stil** | `scripts/stilabgleich.js` | Stammt jeder Wert aus den Tokens? | 0 Funde |
| **3. Bild** | `scripts/bildabgleich.py` | Sieht es gleich aus? | 0,5 % auf dem Bausteine-Artboard |

Der Layoutabgleich ist der wichtigste: er misst das **Aussehen** und
liest die Feldinhalte nicht. Der Bildabgleich ist der schwächste — er
schlägt bei abweichenden Feldwerten an, und das ist kein Befund, sondern
ein falsch angesetztes Werkzeug. Gemessen wird je Fassung und Zustand:
hell, dunkel, mobil; Ruhe, Hover, Fokus, Deaktiviert, Fehler.

**Das Designsystem ist Quelle für Aussehen und Werte, nicht für Code.**
Claude Design liefert React-nahes HTML; dieser Code wird nie in ein Vue-,
Nuxt-, Flutter- oder Contao-Projekt kopiert. Übernommen werden Tokens,
Maße, Zustände und Anordnung — gebaut wird in den Wrapper-Komponenten
der Produktfamilie (Skill `neo-komponenten`).

**Trifft eine Designänderung eine bestehende Seite**, entscheidet der
Agent **nie**, wie alt und neu zusammengeführt werden. Er legt die
Unterschiede mit Maßen dar, zeigt mindestens zwei Wege mit
Gegenüberstellung, empfiehlt — und wartet.

**Selbstkontrolle ist Pflicht.** Nach jeder Korrektur erneut messen und
die Zahl nennen; „sieht gut aus" ist keine Zahl. Die letzte Zeile jeder
Fertigmeldung lautet: **„Eigene Gestaltungsentscheidungen: 0."** Steht
dort etwas anderes, ist die Arbeit nicht abnahmefähig.

Bauverfahren, Inventar, verbotene Entscheidungen und die vierteilige
Rückfrage mit Gegenüberstellungsbild: `references/claude-design.md` —
**vor dem ersten Bauschritt lesen**. Messverfahren, Marker, Schwellen und
Ursachen typischer Abweichungen: `references/designsystem-abgleich.md`.
Befehle: `/neo-design:neo-designumsetzung` baut nach Entwurf,
`/neo-design:neo-designabgleich` misst eine bestehende Ansicht.

## 10. Messwerte

Gemessen wird **mobil**, mit PageSpeed Insights bzw. Lighthouse, für
jede Seitenvorlage — nicht nur für die Startseite.

| Kategorie | Ziel | Untergrenze |
| --- | --- | --- |
| Leistung | 100 | 95 |
| Barrierefreiheit | 100 | 95 |
| Best Practices | 100 | 100 |
| SEO | 100 | 100 |
| Agentisches Browsen | 3/3 | 3/3 |

Agentisches Browsen prüft drei Dinge: sauberer Accessibility-Tree,
stabiles Layout, gültige `llms.txt` an der Domain-Wurzel. **Die
`llms.txt` ist bei Webseiten Pflicht** — zusammen mit `llms-full.txt`.
Bei Web-Anwendungen, Portalen und APIs ist sie es nicht; dort ist OpenAPI
der maschinenlesbare Vertrag (Skill `neo-api`).

**Der Wert für Barrierefreiheit ist kein Nachweis.** Er prüft
automatisch, was sich automatisch prüfen lässt — ein Bruchteil der
WCAG-Kriterien. 100 dort ersetzt die Prüfung aus Abschnitt 6 nicht.

Berichtet werden Zahlen je Seite und Kategorie. Einzelheiten, Ursachen
und der Unterschied zwischen Feld- und Laborwerten:
`references/messwerte.md`.

## 11. Abnahme

Vor jeder Fertigmeldung die Liste in `references/pruefliste.md`
durchgehen und das Ergebnis berichten. Nicht Geprüftes gilt als nicht
erfüllt. Der Befehl `/neo-design:neo-oberflaechenpruefung` führt die
Prüfung an einer bestehenden Ansicht durch.

Zugehörige Skills: `neo-komponenten` (Wrapper-Komponenten, Katalog),
`neo-doku` (Bedienungsdoku, Screenshots), `neo-grundregeln` (Prozess,
Freigabe, Tests), `neo-sicherheit` (Eingabeprüfung serverseitig).
