# Abnahmeliste Oberfläche

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.
Was bewusst nicht erfüllt ist, wird benannt, mit Grund.

## Verfahren

- [ ] Es gab Vorschläge, eine Skizze und eine ausdrückliche Freigabe.
- [ ] Gebaut wurde genau das Freigegebene. Abweichungen sind gemeldet.
- [ ] Der freigegebene Entwurf liegt unter `/plan`, die Entscheidung als
      Entscheidungsakte (ADR).

## Aufbau

- [ ] Die erste Bildschirmhöhe beantwortet: wo bin ich, welcher Zustand,
      was ist die nächste Handlung.
- [ ] Eine Hauptaufgabe, eine Hauptaktion je Ansicht.
- [ ] Gleiche Elemente stehen an derselben Stelle wie in den übrigen
      Ansichten.
- [ ] Aktionen stehen am Ort ihrer Wirkung, nicht im Kopf.
- [ ] Höchstens zwei Verschachtelungsebenen.

## Komponenten

- [ ] Die View verwendet ausschließlich Komponenten der Produktfamilie
      (`Neo*`, `LeoFlex*`) — kein rohes Framework-Element.
- [ ] Kein Farbliteral, kein `style`, keine erfundene Maßzahl in der View.
- [ ] Keine neue lokale Variante einer bestehenden Komponente.
- [ ] Der Wächter-Test läuft grün.

## Eingaben

- [ ] Jedes Freitextfeld ist begründet — es gibt keine bekannte Menge
      gültiger Werte.
- [ ] Auswahllisten stammen aus der Quelle, nicht aus einer Kopie.
- [ ] Masken führen beim Tippen; Einfügen aus der Zwischenablage klappt.
- [ ] Geprüft wird beim Tippen und beim Verlassen, nicht erst beim
      Speichern.
- [ ] Sinnvolle Voreinstellungen; Pflichtfelder gekennzeichnet.
- [ ] Destruktives bestätigt die Folge; Umkehrbares bietet Rückgängig.
- [ ] Serverseitige Prüfung ist vorhanden — die Oberfläche ist Komfort,
      keine Autorität (Skill `neo-sicherheit`).

## Zustände

- [ ] Ruhe, Hover, Fokus, Gedrückt, Aktiv, Deaktiviert, Fehler, Ladend
      sind für jedes Bedienelement gebaut und angesehen.
- [ ] Hover verschiebt um eine Stufe; der Text nähert sich nicht der
      Fläche an.
- [ ] Deaktiviert ist erkennbar und erklärt sich.
- [ ] Jede Fläche hat einen Leer-Zustand mit nächster Handlung, getrennt
      nach „nichts angelegt" und „Filter ohne Treffer".
- [ ] Jede Aktion endet in einer sichtbaren Rückmeldung.

## Barrierefreiheit (WCAG 2.2 AA, hart)

- [ ] Kontrastwerte **gerechnet** und als Zahl berichtet: Text ≥ 4,5:1,
      Bedienelemente und Grafik ≥ 3:1 — in Hell und Dunkel, in jedem
      Zustand einschließlich Hover.
- [ ] Vollständig ohne Maus bedienbar, sinnvolle Reihenfolge, keine
      Falle, sichtbarer Fokus, Fokus nirgends verdeckt.
- [ ] Jeder Zustand trägt Farbe **und** Symbol **und** Wort; in
      Graustufen bleibt alles unterscheidbar.
- [ ] Bedienziele mindestens 24 × 24 px.
- [ ] Überschriftenhierarchie ohne Sprünge, Beschriftungen verknüpft,
      jedes Symbol mit Namen.
- [ ] Statusänderungen werden angesagt, der Meldungstext steht in der
      Live-Region.
- [ ] Ziehen hat eine Tastaturalternative.
- [ ] `prefers-reduced-motion` wird beachtet.
- [ ] 200 % Textvergrößerung und 400 % Zoom ohne Verlust.

## Größe und Gerät

- [ ] Kein horizontales Scrollen des Seitenkörpers auf 320, 390, 768,
      1024, 1280, 1920, 2560 und 3840 px — maschinell geprüft.
- [ ] In jeder ausgelieferten Sprache geprüft, nicht nur in einer.
- [ ] Auf großen Bildschirmen wird verteilt, nicht gedehnt; Textzeile
      bleibt unter 90 Zeichen.
- [ ] Tabellen auf schmalen Geräten nach der Rangfolge behandelt.
- [ ] Klebende Köpfe fressen auf 390 × 660 px nicht die halbe Höhe.

## Texte

- [ ] Knöpfe tragen Verb plus Objekt; Bestätigungsknöpfe die Folge.
- [ ] Fehlermeldungen nennen Ursache und nächsten Schritt.
- [ ] Kein Platzhalter als Beschriftung.
- [ ] Jeder sichtbare Text kommt aus der Sprachdatei; keine
      zusammengesetzten Sätze.
- [ ] Zahlen, Datum und Währung über die Formatierung der Sprache.
- [ ] Echte Umlaute, Sie-Form, keine Emojis, keine Marketingsprache.

## Tests und Doku

- [ ] Jedes Bedienelement hat einen Oberflächen-Funktionstest, der die
      Bedienung auslöst und das beobachtbare Ergebnis prüft.
- [ ] Die Bedienungsdoku ist im selben Schritt nachgezogen, mit
      Screenshots und Markierungen (Skill `neo-doku`).
- [ ] Lint, Tests und Build laufen grün.
