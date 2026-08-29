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

## Bauen nach dem Designsystem

Nur wenn ein Designsystem, ein Artboard oder ein freigegebener
Klickprototyp vorliegt. Verfahren: `claude-design.md`.

- [ ] **Eigene Gestaltungsentscheidungen: 0.** Kein Layout, kein Abstand,
      kein Radius, kein Schriftmaß, keine Farbe, kein Bauteil selbst
      gewählt.
- [ ] Das **Inventar** wurde vor der ersten Zeile Code geschrieben, aus
      dem Artboard **gemessen** und vorgelegt.
- [ ] Es listet **jedes** Element, nicht die wichtigen; offene Fragen
      stehen darin und wurden beantwortet, bevor gebaut wurde.
- [ ] Gebaut wurde **Element für Element** von oben nach unten, nach
      jedem Element gemessen — nicht die Seite gebaut und dann verglichen.
- [ ] Jedes Element hat einzeln bestanden, bevor das nächste begann.
- [ ] Kein Bauteil erfunden, wo der Entwurf keins zeigt; kein Bauteil des
      Entwurfs weggelassen.
- [ ] Abweichungen wurden **vorgelegt**, nicht entschieden: zwei Bilder
      nebeneinander, Maße, Grund, mindestens zwei Wege, Empfehlung.
- [ ] Bei einer bestehenden Seite wurde die Zusammenführung **vorgelegt**,
      nicht durchgeführt.
- [ ] Nach dem letzten Element wurde die Seite **im Ganzen** neben dem
      Artboard betrachtet — Rhythmus, Gewichtung, Eindruck.

## Abgleich mit dem Designsystem

- [ ] Marker (`data-compare`) auf beiden Seiten gesetzt, benennen die
      Rolle des Elements.
- [ ] Referenzmessung und Referenzaufnahme liegen unter
      `design/referenz/` im Repository.
- [ ] Referenz und gebaute Ansicht unter identischen Bedingungen
      gemessen (Sichtfeld, Bildmaßstab, Farbschema, Sprache, Schriften).
- [ ] **Layoutabgleich je Zustand und Fassung: 0 Abweichungen** bei 1 px
      Toleranz — Ruhe, Hover, Fokus, Deaktiviert, Fehler, hell und dunkel.
- [ ] Stilabgleich gelaufen: **null Funde**.
- [ ] Bildabgleich auf dem Bausteine-Artboard höchstens 0,5 Prozent; bei
      Ansichten mit echten Daten nur mit ausgenommenen Inhaltsbereichen.
- [ ] Das Unterschiedsbild wurde **angesehen**, nicht nur die Zahl
      gelesen; markierte Bauteile sind benannt.
- [ ] Kein Befund entsteht aus abweichendem **Inhalt** — Feldwerte und
      Listeneinträge sind dynamisch und werden nicht verglichen.
- [ ] Statische Oberflächentexte nur mitverglichen, wenn der
      Projektinhaber es verlangt hat.
- [ ] Tokens wurden übernommen, nicht abgetippt.
- [ ] Kein Code aus dem Designsystem in ein anderes Framework kopiert.

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

## Betriebsart Webseite

Nur bei Webseiten, nicht bei Anwendungen und Portalen.

- [ ] Die Seite könnte nicht ohne Änderung für ein anderes Unternehmen
      stehen.
- [ ] Keine Eyebrow-Zeile in der Standardform; entweder weg oder etwas
      Eigenes.
- [ ] Kein Dreikartenblock mit Symbolkreis, kein Verlaufstext, keine
      Milchglasfläche über Verlauf, keine Graustufen-Logoleiste.
- [ ] Die Seite bewegt sich: Erscheinen beim Scrollen, Übergänge,
      höchstens ein tragender Bühneneffekt.
- [ ] Bewegung nur über `transform` und `opacity`; kein Layoutsprung.
- [ ] Burgermenü animiert **und** bedienbar: `aria-expanded`, Fokus
      hinein, gefangen, zurück, Escape schließt.
- [ ] Bei reduzierter Bewegung ist alles sofort da und vollständig
      bedienbar.
- [ ] Schriften werden selbst ausgeliefert, nicht von einem fremden
      Dienst geladen.

## Messwerte

- [ ] PageSpeed Insights **mobil** für **jede** Seitenvorlage gemessen,
      nicht nur für die Startseite.
- [ ] Best Practices 100, SEO 100, agentisches Browsen 3/3.
- [ ] Leistung und Barrierefreiheit mindestens 95, Ziel 100.
- [ ] Die drei Kernwerte für Ladezeit, Reaktion und Layoutstabilität
      berichtet.
- [ ] Bei einer **Webseite**: `llms.txt` und `llms-full.txt` an der
      Domain-Wurzel vorhanden, gültig und aus dem Bestand erzeugt. Bei
      Web-Anwendungen und APIs nicht verlangt.
- [ ] Klar benannt, dass der Barrierefreiheitswert ein Teilcheck ist —
      die Prüfung oben ersetzt er nicht.

## Brücke vom Entwurf in die Anwendung

Gilt, sobald das Ziel kein Browser ist (`entwurfsbruecke.md`).

- [ ] **Eine** Tokenquelle; die erzeugte Datei ist eingecheckt, der
      Erzeugungsschritt läuft in der CI und ist bei Abweichung rot.
- [ ] Kein Zahlenwert, keine Farbe in einer View. **Bedienhöhen sind
      Tokens.**
- [ ] Je Bildschirm eine goldene Aufnahme, **aus dem Entwurf** gelegt —
      nicht aus dem eigenen Bau.
- [ ] Aufnahmebedingungen in Entwurf und Test dieselben; Toleranz
      benannt; ausgenommene Bereiche benannt und begründet.
- [ ] Die Abweichung ist als **Zahl** berichtet.

## Größe und Gerät

Maschinell geprüft mit `overflow.js` auf 320, 390, 768, 1024, 1280,
1920, 2560 und 3840 px. **Null Befunde**, je Seite, je Sprache, in Hell
und Dunkel.

- [ ] **Kein horizontales Scrollen des Seitenkörpers** auf keiner Breite.
- [ ] **Kein `overflow-x: hidden` am Körper** — das versteckt den Fehler.
- [ ] **Nichts ragt über den sichtbaren Rand** — auch kein geöffnetes
      Menü, kein Dialog, kein klebender Kopf. Geöffnete Zustände wurden
      mitgemessen.
- [ ] **Jede Überlagerung wurde geöffnet und gemessen** — Auswahl, Menü,
      Datumswähler, Tooltip, Kontextmenü. Eine geschlossene Seite beweist
      über sie nichts.
- [ ] **Die Aufklapprichtung folgt dem Platz**: unten nach oben, oben
      nach unten, rechts nach links, links nach rechts. Entschieden wird
      beim Öffnen, nicht im Template.
- [ ] **Kein Vorfahre schneidet eine Überlagerung ab** (`overflow: hidden`
      an der Karte). Sonst gehört sie in eine eigene Ebene.
- [ ] **Keine Überlagerung höher als der Bildschirm** ohne eigenen
      Scrollbereich; auch bei **kleiner Höhe** geprüft (Telefon quer).
- [ ] **Tabellen nutzen 100 % des Inhaltsbereichs**, nie schmaler;
      breiter nur in einem ausdrücklichen Scrollbereich.
- [ ] **Keine Löcher in umgebrochenen Reihen** — entweder einspaltig oder
      das letzte Element füllt. Keine leere Platzhalterkachel.
- [ ] **Bedienziele**: bis 768 px mindestens 44 × 44 px, darüber
      24 × 24 px; mindestens 8 px Abstand zwischen zwei Zielen.
- [ ] Symbolknöpfe in Tabellenzeilen sind auf schmal bedienbar oder durch
      eine Zeilenaktion ersetzt.
- [ ] Unter dem Umbruchpunkt liegt das Hauptmenü hinter einem Knopf, mit
      `aria-expanded`, Fokusführung und Escape.
- [ ] **Höchstbreiten** aus Tokens für Inhaltsbereich, Textspalte und
      Eingabefelder — kein Feld über die halbe Wand auf 4K.
- [ ] Mit **langen Daten** geprüft: Name über 60 Zeichen, Kennung ohne
      Leerzeichen, achtstellige Zahl.

### Text im Layout (`text-fit.js`, null Befunde)

- [ ] **Kein Text abgeschnitten** — weder waagrecht hinter der Kante noch
      senkrecht bei fester Höhe.
- [ ] **Wo gekürzt wird, ist der volle Text erreichbar** (`title`,
      `aria-label`, Tooltip oder Detailansicht). Eine Auslassung ohne
      Volltext ist Datenverlust.
- [ ] **Nichts überlappt** — zwei Texte liegen nie übereinander.
- [ ] **Kein Bereich unter acht Zeichen je Zeile.** Zu schmale Spalten
      werden weggelassen oder zur Karte, nicht schmaler gemacht.
- [ ] **Fließtext trennt an Silbengrenzen**: `hyphens: auto` **und**
      `lang` am Dokument — ohne `lang` trennt der Browser nicht.
- [ ] `overflow-wrap: anywhere` nur für Kennungen, URLs und Prüfsummen;
      `word-break: break-all` nirgends im Fließtext.
- [ ] **Schriftgrößen** mindestens 12 px, auf schmalen Geräten 14 px;
      Text wird auf dem Telefon nicht kleiner als am Schreibtisch.
- [ ] Mitwachsende Größen über `clamp()` **mit Boden und Decke**, aus
      Tokens; kein reines `vw` als Schriftmaß.
- [ ] Bei **200 % Textvergrößerung** und **400 % Zoom** ist nichts
      abgeschnitten, nichts überlappt, nichts verschwunden.
- [ ] In der **längsten ausgelieferten Sprache** geprüft, nicht nur in
      Englisch.
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
- [ ] **Übersetzungen vollständig**: `translations.py` meldet null
      Blocker — nichts fehlt, nichts ist leer, keine Platzhalter- und
      keine Pluralabweichung. Abdeckung je Sprache **berichtet**.
- [ ] Rückfall auf **Englisch** konfiguriert und geprüft — nie ein
      Schlüssel, nie ein leerer Text in der Oberfläche.
- [ ] Kein Satz aus Teilschlüsseln zusammengesetzt; Platzhalter tragen
      sprechende Namen.
- [ ] Die Oberfläche wurde **in jeder Sprache bedient**, nicht nur in der
      Leitsprache.

## Recht

- [ ] Impressum, Datenschutzerklärung und Barrierefreiheitserklärung
      vorhanden, erreichbar und inhaltlich vollständig (Skill
      `neo-recht`).
- [ ] Vor der Einwilligung lädt nichts von Dritten — auch kein
      eingebettetes Video.
- [ ] Die Einwilligung lässt sich jederzeit widerrufen.

## Tests und Doku

- [ ] Jedes Bedienelement hat einen Oberflächen-Funktionstest, der die
      Bedienung auslöst und das beobachtbare Ergebnis prüft — **an jeder
      Stelle, an der es vorkommt** (Skill `neo-grundregeln`,
      `references/durchlauf.md`).
- [ ] Rauchtest je Route: lädt, rendert, keine Konsolenfehler, kein
      unerwarteter 4xx/5xx.
- [ ] Die Bedienungsdoku ist im selben Schritt nachgezogen, mit
      Screenshots und Markierungen (Skill `neo-doku`).
- [ ] Lint, Tests und Build laufen grün.
