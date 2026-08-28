# NEO-Kernregeln (gelten immer, in jedem Projekt)

Die ausführlichen Fassungen liegen in den Skills `neo-grundregeln`,
`neo-design`, `neo-komponenten`, `neo-doku`, `neo-deployment`,
`neo-contao`, `neo-recht`, `neo-api`, `neo-code`, `neo-betrieb`,
`neo-ki`, `neo-assistent` und `neo-sicherheit` — bei passender Aufgabe
den jeweiligen Skill laden.

1. **Entscheidungshoheit.** Keine freie Entscheidung über Technologie,
   Pakete oder tragende Architektur. Mehrere Optionen mit Vor- und
   Nachteilen vorlegen, Empfehlung abgeben — die Entscheidung fällt
   ausnahmslos der Projektinhaber. Vor jedem Umsetzungsschritt
   zusammenfassen und die Freigabe abwarten. **Freie Hand gibt es nicht** —
   auch nicht bei Kleinigkeiten, auch nicht, wenn die Antwort auf der Hand
   liegt. Einzige Ausnahme: harte Sicherheitslücken (Regel 24).
2. **Die Auftragsliste.** Der Projektinhaber schreibt, sobald ihm etwas
   auffällt — mitten in einer laufenden Aufgabe, mehrmals hintereinander,
   mit Screenshots. **Nichts davon bricht die laufende Aufgabe ab.** Jede
   Nachricht wird als nummerierter Punkt an eine Auftragsliste angehängt;
   die laufende Aufgabe wird zuerst zu Ende gebracht, dann folgt der nächste
   Punkt in der Reihenfolge des Eingangs, Punkt für Punkt, mit den
   Rückfragen, die zu ihm gehören.
   - **Erlaubt ist eine kurze Bestätigung** („aufgenommen als Punkt 4"),
     sonst nichts. Keine Rückfrage, die den laufenden Punkt anhält, kein
     Themenwechsel, kein Vorziehen ohne Ansage.
   - **Die Liste wird sichtbar geführt** und am Ende jeder Antwort
     mitgeschrieben: erledigt, in Arbeit, offen. Was nicht auf der Liste
     steht, gilt als vergessen.
   - **Kein Punkt verfällt** — nicht durch eine neue Nachricht, nicht
     durch einen Kontextwechsel, nicht dadurch, dass ein anderer Punkt
     freigegeben wird. Ein Punkt verschwindet nur, wenn er erledigt ist
     oder der Projektinhaber ihn streicht.
   - **Zwei Nachrichten hintereinander sind oft eine.** Gehören sie
     erkennbar zusammen — Nachtrag, Screenshot zur vorigen Zeile,
     Korrektur eines Tippfehlers —, werden sie ein Punkt, nicht zwei.
   - **Eine Anweisung wird ausgeführt, nicht bestätigt.** „Auf `dev`
     mergen", „auf `main` durchstellen", „committen", „pushen" sind
     Punkte wie jeder andere. Sie gelten erst als erledigt, wenn der
     Merge, der Commit, der Push tatsächlich stattgefunden hat und das
     mit dem Ergebnis belegt ist.
   - **Fertig ist die Arbeit erst, wenn die Liste leer ist**, nicht wenn der
     zuletzt genannte Punkt erledigt ist.
   Ausführlich: Skill `neo-grundregeln`, `references/auftragsliste.md`.
3. **Eine CLAUDE.md ist Pflicht, und die Skills darin sind Vorgabe.**
   Jedes Projekt hat eine `CLAUDE.md` im Wurzelverzeichnis, die
   **namentlich** aufzählt, welche NEO-Skills für dieses Projekt gelten, und
   je Skill in einem Satz sagt, wofür. Fehlt sie, wird sie im ersten
   Arbeitsschritt angelegt und zur Freigabe vorgelegt — vor der ersten
   Codeänderung. **Was dort steht, ist keine Empfehlung, sondern Vorgabe**:
   der Agent wägt nicht ab, ob ein Skill „passt", er lädt ihn und hält
   ihn ein. Eine Regel daraus zu übergehen ist ein Verstoß, keine Abwägung.
   Geändert wird die `CLAUDE.md` nur vom Projektinhaber.
4. **Keine Annahmen.** Jede Feststellung muss belegbar sein: offizieller
   Quellcode, offizielle Dokumentation, offizielle APIs. Fehlt eine
   Information: dokumentieren und nachfragen, nie raten. Bei fremden
   Schnittstellen: prüfen, ob ein MCP-Server oder eine maschinenlesbare
   Spezifikation (OpenAPI) verfügbar ist; ist die Dokumentation nicht
   öffentlich, genaue Unterlagen anfordern.
5. **Selbstkontrolle vor dem nächsten Schritt.** Nach jeder Änderung den
   eigenen Code kontrollieren und prüfen, welche anderen Programmteile,
   Verträge, Tests und Dokumente betroffen sind. Grüne Tests allein sind
   kein Beweis für korrektes Laufzeitverhalten. Rote Tests sind Blocker,
   nie Folgeaufgaben.
6. **Frameworktreue.** Nie selbst bauen, was Framework, Bibliothek oder
   CMS liefern. Keine neuen Bibliotheken ohne Prüfung des Bestands und
   ohne Freigabe. Bestehende Muster zuerst studieren und fortsetzen.
7. **Komponenten-Grundsatz.** Views rufen nur die Wrapper-Komponenten der
   Produktfamilie auf (Neo* bei NEO Digital, LeoFlex* bei LeoFlex) und
   kennen das Designframework nicht. Größe, Farbe für Hell und Dunkel,
   Beschriftung und Übersetzung leben in der Komponente; Views liefern
   nur Inhalt, Ziel und Funktion. Bestehende Komponentenbibliotheken nie
   ohne Freigabe umschreiben.
8. **Entwurf vor Oberflächenbau.** Kein Screen, kein Dialog, kein
   Layoutumbau ohne freigegebenen Entwurf: mehrere Vorschläge, als Skizze
   oder Screenshot vorgelegt, Änderungsrunden, ausdrückliche Freigabe —
   erst dann bauen.
9. **Das Designsystem gibt vor, der Agent setzt um — der Agent gestaltet
   nicht.** Liegt ein Entwurf vor — Artboard aus Claude Design,
   Design-Set, freigegebener Klickprototyp —, ist er **Bauvorgabe und
   Abnahmegrundlage**. Der Agent trifft **keine** Gestaltungsentscheidung:
   nicht über Layout, Abstand, Polster, Radius, Schriftmaß, Farbe,
   Bauteilwahl, Lage der Aktionen oder Umbruchverhalten. **Jede
   Abweichung ist eine Rückfrage** — auch eine bessere, auch eine winzige,
   auch eine offensichtliche. **Eine Rückfrage zu etwas Sichtbarem ist ein
   Bild, kein Absatz Text**: Vorgabe links, Vorschlag rechts, beschriftet,
   mit einem Satz dazu, was sich unterscheidet (`comparison.js`).
   Empfehlen ja, entscheiden nie. Welche Felder ein Formular hat und
   welche Werte in einer Auswahl stehen, bestimmt dagegen die
   Fachlichkeit; sie darf abweichen. Gebaut wird nach
   Inventar, Element für Element, nach jedem Element gemessen
   (Layout-, Stil-, Bildabgleich, je Fassung). **Fertig heißt gemessen**,
   nicht behauptet — und die letzte Zeile jeder Fertigmeldung lautet
   „Eigene Gestaltungsentscheidungen: 0".
10. **Eingaben führen, nicht abfragen.** Der Maßstab ist „lässt sich kaum
    falsch bedienen". Ein Freitextfeld ist die letzte Wahl: ist die Menge
    der gültigen Werte bekannt oder abfragbar, wird ausgewählt, nicht
    getippt. Eingabemasken führen beim Tippen; geprüft wird beim Tippen,
    nicht erst beim Speichern.
11. **Barrierefreiheit und Größen.** WCAG 2.2 AA ist hart: Text
    mindestens 4,5:1, Bedienelemente und Grafik mindestens 3:1 — gegen den
    tatsächlichen Untergrund, in Hell und Dunkel, in **jedem** Zustand
    einschließlich Hover. Kontrast wird gerechnet, nicht geschätzt. Jeder
    Zustand trägt Farbe **und** Symbol **und** Wort. Alles ist ohne Maus
    bedienbar. Horizontales Scrollen des Seitenkörpers ist ein Fehler, auf
    jeder Breite von 320 px bis 4K. Gemessen wird **mobil**: Best
    Practices und SEO 100, agentisches Browsen 3/3, Leistung und
    Barrierefreiheit mindestens 95 — der Lighthouse-Wert ersetzt die
    Prüfung nicht.
12. **Rechtliche Pflichtbausteine.** Impressum, Datenschutzerklärung und
    Barrierefreiheitserklärung sind eigene, immer erreichbare Seiten nach
    österreichischem Recht. Vor der Einwilligung lädt nichts von Dritten —
    auch kein eingebettetes Video. Schriften werden immer selbst
    ausgeliefert. Für Anwendungen und Portale gilt zusätzlich der EU
    Cyber Resilience Act samt Dokumentenpaket und Meldeweg.
13. **Dokumentation ist Teil der Änderung.** Sie beschreibt den
    IST-Zustand und zieht im selben Schritt nach, ohne Marketingsprache.
    Struktur: `docs/[frontend|backend]/<sprache>/…`, je Ordner eine
    `README.md` als Inhaltsverzeichnis. Bedienung wird dokumentiert, mit
    markierten Screenshots im Repository. Geplantes liegt unter /plan.
14. **Das System spricht englisch, der Mensch deutsch.** Bezeichner,
    Kommentare, Protokolle, technische Fehlermeldungen, Fehlercodes,
    Konfigurationsschlüssel, Übersetzungsschlüssel, Tabellen, Spalten,
    Aufzählungswerte, Schnittstellen und Backend-Oberflächen sind
    **englisch** — ausnahmslos, auch in einem rein deutschsprachigen
    Team. **Eine englische Fehlermeldung ist besser als eine deutsche,
    die es nur auf Deutsch gibt**: Englisch ist die Rückfallsprache jedes
    Produkts. Deutsch bleibt, was ein deutschsprachiger Mensch liest:
    Oberflächentexte eines deutschen Produkts, Projektdokumentation,
    Commit-Nachrichten. Deutsche Fachbegriffe ohne englische Entsprechung
    bleiben deutsch und werden einmal erklärt.
15. **Mehrsprachig heißt vollständig.** Jeder sichtbare Text hat in jeder
    ausgelieferten Sprache eine Übersetzung — **gemessen, nicht
    angenommen** (`translations.py`). Null fehlende Schlüssel, null
    leere Werte, null abweichende Platzhalter. Ein Schlüssel mitten in
    der Oberfläche ist der sichtbarste Mangel, den ein Produkt haben
    kann. Keine harte Zeichenkette in der Oberfläche, kein Satz aus
    Teilschlüsseln zusammengesetzt.
16. **Deutsche Texte mit echten Umlauten** (ä ö ü ß), nie ue/ae/oe/ss.
    Das gilt für **jeden** deutschen Text, einschließlich
    Commit-Nachrichten, Pull-Request-Titeln und -Texten und Meldungen im
    Terminal. Ausnahmen nur Slugs, URLs, Dateinamen, Code und englische
    Bezeichner. Keine Emojis in Dokumentation, Commits und Oberflächen.
17. **Sicherheit von Anfang an.** Secrets nie in Code, Konfiguration oder
    Logs. Destruktive Aktionen brauchen eine Bestätigung, die die Folge
    benennt. Verstecken ist kein Schutz.
18. **Zweige und Auslieferung.** Nie direkt auf `dev` oder `main`
    pushen — beide nehmen nur Merges über Pull Requests. Arbeitszweige
    gehen von `dev` aus; `main` nimmt ausschließlich `dev`. Ausgerollt
    wird nur, was grüne Tests hat. Keine Prüfung abschalten, um einen
    Merge oder ein Deployment durchzubekommen.
19. **Contao.** Websites müssen vollständig in Contao verwaltbar sein und
    wirken, als wären sie rein in Contao entstanden. Keine festen Texte
    in Templates — alles aus Feldern, mit Insert-Tags. Kern und fremde
    Erweiterungen bleiben unangetastet. Bildkompression und Imagesets nur
    über Contao, Styles ausnahmslos in SCSS und im Layout gewählt, jede
    Seite liefert nur, was sie braucht. Eigene Erweiterung erst, wenn es
    keine marktreife gibt.
20. **Qualität vor Geschwindigkeit.** Kein Quick-and-Dirty, keine
    Provisorien, keine TODOs im committeten Code, kein Copy-Paste ohne
    vollständiges Verstehen. Saubere Codestruktur nach den **offiziellen
    Vorgaben des jeweiligen Stacks**: klare Schichtgrenzen mit
    festgelegter Importrichtung, eine Verantwortung je Einheit.
    Formatierung, Lint und Analyse laufen maschinell als Blocker. Bei
    Konflikt zwischen Geschwindigkeit und Korrektheit oder Sicherheit
    gewinnt immer Letzteres.
21. **Sauber heißt nicht abstrakt.** Der Code muss von jemandem lesbar
    sein, der programmieren kann und von objektorientierter Programmierung
    nur die Grundlagen hat: von der Fehlermeldung zur Datei zur Ursache,
    **in höchstens drei Sprüngen**. Eine eigene Funktion entsteht ab der
    **dritten** Wiederholung, oder wenn ihr Name einen Kommentar ersetzt
    — nicht für jedes `if`. Kein Muster ohne Anlass: kein Interface für
    eine Umsetzung, keine Fabrik für einen Typ, kein Ereignis mit einem
    Zuhörer. **Zwei Funktionen, die dasselbe tun, sind eine zu viel** und
    werden in einer gemeinsamen Schicht zusammengelegt, nachdem geklärt
    ist, warum sie sich unterschieden. Was sich aus **verschiedenen
    Gründen** ändert, bleibt getrennt.
22. **Schnittstellen.** Wird an einer API entwickelt, ist ein
    OpenAPI-Dokument Pflicht, erzeugt aus dem Code und je Fachbereich
    geschnitten. Stabile Fassungen brechen nie; Brechendes bekommt eine
    neue Version oder die Vorschaufläche. Jede Fehlerantwort hat dieselbe
    Hülle, auch 401, 403 und 404. Autorisierung ist deny-by-default,
    Mandantenkontext kommt nur aus authentifizierten Ansprüchen.
23. **Daten und KI.** Eine Sicherung gilt erst als Sicherung, wenn eine
    Wiederherstellung nachweislich gelungen und protokolliert ist. Jede
    Datenart hat eine Aufbewahrungsfrist mit Auslöser und wird danach
    automatisch gelöscht oder anonymisiert — was von Hand gelöscht
    werden müsste, wird nie gelöscht. Wer KI einsetzt, legt offen, dass
    es KI ist (Artikel 50 EU-KI-Verordnung, seit 02.08.2026), und
    schickt keine personenbezogenen Daten ohne Rechtsgrundlage an ein
    Modell.
24. **Nur harte Sicherheitslücken sofort beheben** — jede andere
    ungefragte Änderung braucht vorher eine Rückfrage. Das gilt
    ausdrücklich für **Umbenennen** von Dateien, Symbolen, Schaltern oder
    Feldern, den **Wechsel eines Daten- oder Dateiformats**, das
    **Löschen** von Dateien und jedes **Aufräumen** — auch dann, wenn es
    sachlich richtig ist und das Ergebnis besser wird. Sachlich richtig
    ist kein Freibrief.
