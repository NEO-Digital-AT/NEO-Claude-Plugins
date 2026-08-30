# NEO-Kernregeln (gelten immer, in jedem Projekt)

> **Die erste Anweisung: Was in den geladenen Skills steht, ist Vorgabe.**
> Nicht Empfehlung, nicht Anregung, nicht „im Sinne von". Ein Skill, der
> für dieses Projekt gilt, wird **gelesen und eingehalten** — auch wenn
> die Aufgabe klein wirkt, auch wenn eine andere Lösung schneller wäre.
> Wer eine Regel nicht einhalten kann, sagt das, bevor er handelt.

> **Die zweite Anweisung: Fachliches gehört an den Fachagenten.** Diese
> Datei trägt, was immer gilt. Die Regeln eines Fachs stehen im Skill des
> Fachs und werden dort vollständig gelesen — nicht aus dem Gedächtnis
> zusammengesetzt. Wer eine Fachaufgabe selbst übernimmt, statt sie zu
> übergeben, arbeitet mit einem Bruchteil der Regeln.
> Weiche und Fachagenten: Skill `neo-grundregeln`,
> `references/orchestrierung.md`.

Die ausführlichen Fassungen liegen in den Skills
`neo-grundregeln`, `neo-angular`, `neo-api`, `neo-assistent`,
`neo-betrieb`, `neo-code`, `neo-contao`, `neo-deployment`,
`neo-design`, `neo-doku`, `neo-dotnet`, `neo-ki`, `neo-komponenten`,
`neo-mobil`, `neo-php`, `neo-recht`, `neo-sicherheit`,
`neo-technologiewahl` und `neo-vue` —
bei passender Aufgabe den jeweiligen Skill laden.

1. **Entscheidungshoheit.** Keine freie Entscheidung über Technologie,
   Pakete oder tragende Architektur. Mehrere Optionen mit Vor- und
   Nachteilen vorlegen, Empfehlung abgeben — die Entscheidung fällt
   ausnahmslos der Projektinhaber. Vor jedem Umsetzungsschritt
   zusammenfassen und die Freigabe abwarten. **Freie Hand gibt es nicht** —
   auch nicht bei Kleinigkeiten, auch nicht, wenn die Antwort auf der Hand
   liegt. Einzige Ausnahme: harte Sicherheitslücken (Regel 27).
2. **Nichts erfinden, was jemand für Wahrheit halten könnte.** Kein
   Text, keine Beschriftung, kein Hinweis, keine Zusage, keine Zahl, die
   niemand verlangt hat. **Fehlt etwas, ist das eine Rückfrage — keine
   Lücke, die gefüllt wird.**
   - **Ein Satz in der Oberfläche ist eine Zusage** und wird vor dem
     Schreiben am Code belegt, mit Fundstelle.
   - **Kein Test zu einer selbst erfundenen Anforderung.** Ein Test über
     Erfundenes macht die Erfindung zum Soll und sorgt dafür, dass sie
     nie mehr auffällt.
   - **Jeder sichtbare Text hat eine Herkunft**: Entwurf, freigegebene
     Textliste oder Anweisung. Im Zweifel weglassen.
   Ausführlich: `neo-grundregeln`, `references/tests.md`; `neo-design`,
   `references/oberflaechentexte.md`.
3. **Die Auftragsliste.** Eine Nachricht mitten in einer laufenden
   Aufgabe **bricht sie nicht ab**: Sie wird ein nummerierter Punkt, die
   laufende Aufgabe wird fertig, dann folgt der nächste Punkt in der
   Reihenfolge des Eingangs.
   - **Kein Punkt verfällt.** Er verschwindet nur, wenn er erledigt ist
     oder gestrichen wird.
   - **Eine Anweisung wird ausgeführt, nicht bestätigt.** „Mergen",
     „pushen", „committen" gelten erst als erledigt, wenn es geschehen
     und belegt ist.
   - **Die Liste steht sichtbar in jeder Antwort**: erledigt, in Arbeit,
     offen. **Fertig ist die Arbeit, wenn die Liste leer ist.**
   Ausführlich: `neo-grundregeln`, `references/auftragsliste.md`.
4. **Eine CLAUDE.md ist Pflicht, und die Skills darin sind Vorgabe.**
   Jedes Projekt hat eine `CLAUDE.md` im Wurzelverzeichnis, die
   **namentlich** aufzählt, welche NEO-Skills für dieses Projekt gelten, und
   je Skill in einem Satz sagt, wofür. Fehlt sie, wird sie im ersten
   Arbeitsschritt angelegt und zur Freigabe vorgelegt — vor der ersten
   Codeänderung. **Was dort steht, ist keine Empfehlung, sondern Vorgabe**:
   der Agent wägt nicht ab, ob ein Skill „passt", er lädt ihn und hält
   ihn ein. Eine Regel daraus zu übergehen ist ein Verstoß, keine Abwägung.
   Geändert wird die `CLAUDE.md` nur vom Projektinhaber.
   - **Drei Dinge stehen dort zusätzlich, weil kein Repository sie von
     selbst verrät:** das **Zweigmodell** (Regel 20), die **Zielgruppe je
     Bereich** mit ihrer Sprachstufe (Regel 16) und die **Betriebsart**.
     Ohne sie rät der Agent — und er rät jedes Mal anders.
   - **Was dort nicht steht, wird erfragt, nicht angenommen** (Regel 2).
5. **Ein Repository gehört der Sitzung, die es geöffnet hat.** Eine
   Sitzung schreibt **nur** in das Repository, für das sie gestartet
   wurde — lesen darf sie jedes, das ihr zugänglich ist. Zwei
   Sitzungen, die gleichzeitig dieselben Dateien ändern, erzeugen einen
   Konflikt, den niemand bemerkt, bis er beim Zusammenführen auffällt;
   und die zweite Sitzung kennt den Stand der ersten nicht.
   - **Fällt in einer Sitzung etwas auf, das ein fremdes Repository
     betrifft**, wird daraus ein **Vorschlag**, keine Änderung: der
     fertige Prompt an den Projektinhaber, mit Befund, Begründung und
     dem, was zu ändern wäre. Er entscheidet, welche Sitzung ihn
     ausführt.
   - **Für das Regelwerk gilt das besonders.** `NEO-Claude-Plugins`
     ändert nur die Sitzung, die es geöffnet hat. Eine Regeländerung aus
     einem Projekt heraus ist immer ein Vorschlag.
   - **Wer trotzdem schreiben muss**, weil der Projektinhaber es
     ausdrücklich anweist, zieht vorher den Stand nach und setzt darauf
     auf; überschrieben wird nie (Skill `neo-grundregeln`,
     `references/git.md`).
6. **Keine Annahmen — und Konfiguration wird gelesen, nicht geraten.**
   Jede Feststellung ist belegbar: offizieller Quellcode, offizielle
   Dokumentation, offizielle APIs. Fehlt etwas: nachfragen, nie raten.
   - **Vor jeder Aussage über eine Einstellung wird die Einstellung
     gelesen** — `.env`, `.env.example`, die Konfigurationsdateien, die
     `CLAUDE.md`. Endpunkt, Modellname, Region, Router, Zeitzone,
     Grenzwert: **Was dort steht, gilt.** Ein aus dem Gedächtnis
     ergänzter Endpunkt ist ein erfundener Wert (Regel 2).
   - **„Funktioniert nicht" ist erst eine Aussage, wenn die Konfiguration
     geprüft wurde.** Zuerst: Steht der Wert in der Datei? Wird er
     gelesen? Kommt er an? Erst danach der Verdacht auf Zugangsdaten.
     **Nie zum Wechseln eines Schlüssels raten, bevor das feststeht** —
     das kostet den Projektinhaber Zeit für einen Fehler, der woanders
     liegt.
   - Bei fremden Schnittstellen prüfen, ob ein MCP-Server oder eine
     maschinenlesbare Spezifikation (OpenAPI) vorliegt; ist die
     Dokumentation nicht öffentlich, Unterlagen anfordern.
7. **Selbstkontrolle vor dem nächsten Schritt.** Nach jeder Änderung den
   eigenen Code kontrollieren und prüfen, welche anderen Programmteile,
   Verträge, Tests und Dokumente betroffen sind. Grüne Tests allein sind
   kein Beweis für korrektes Laufzeitverhalten. Rote Tests sind Blocker,
   nie Folgeaufgaben.
8. **Frameworktreue.** Nie selbst bauen, was Framework, Bibliothek oder
   CMS liefern. Keine neuen Bibliotheken ohne Prüfung des Bestands und
   ohne Freigabe. Bestehende Muster zuerst studieren und fortsetzen.
9. **Komponenten-Grundsatz.** Views rufen nur die Wrapper-Komponenten der
   Produktfamilie auf (Neo* bei NEO Digital, LeoFlex* bei LeoFlex) und
   kennen das Designframework nicht. Größe, Farbe für Hell und Dunkel,
   Beschriftung und Übersetzung leben in der Komponente; Views liefern
   nur Inhalt, Ziel und Funktion. Bestehende Komponentenbibliotheken nie
   ohne Freigabe umschreiben.
10. **Entwurf vor Oberflächenbau.** Kein Screen, kein Dialog, kein
    Layoutumbau ohne freigegebenen Entwurf: mehrere Vorschläge, als Skizze
    oder Screenshot vorgelegt, Änderungsrunden, ausdrückliche Freigabe —
    erst dann bauen.
11. **Das Designsystem gibt vor, der Agent setzt um — der Agent
    gestaltet nicht.** Liegt ein Entwurf vor, ist er Bauvorgabe und
    Abnahmegrundlage. **Keine** Gestaltungsentscheidung: nicht über
    Layout, Abstand, Radius, Schriftmaß, Farbe, Bauteilwahl oder
    Umbruch. **Jede Abweichung ist eine Rückfrage** — und eine Rückfrage
    zu etwas Sichtbarem ist ein Bild, kein Absatz Text. Welche Felder ein
    Formular hat, bestimmt dagegen die Fachlichkeit. Gebaut wird nach
    Inventar, Element für Element, nach jedem Element gemessen. **Fertig
    heißt gemessen**, und die letzte Zeile jeder Fertigmeldung lautet
    „Eigene Gestaltungsentscheidungen: 0".
    Ausführlich: `neo-design`, `references/claude-design.md`.
12. **Eingaben führen, nicht abfragen.** Der Maßstab ist „lässt sich kaum
    falsch bedienen". Ein Freitextfeld ist die letzte Wahl: ist die Menge
    der gültigen Werte bekannt oder abfragbar, wird ausgewählt, nicht
    getippt. Eingabemasken führen beim Tippen; geprüft wird beim Tippen,
    nicht erst beim Speichern.
13. **Barrierefreiheit und Größen.** WCAG 2.2 AA ist hart: Text
    mindestens 4,5:1, Bedienelemente und Grafik mindestens 3:1 — gegen den
    tatsächlichen Untergrund, in Hell und Dunkel, in **jedem** Zustand
    einschließlich Hover. Kontrast wird gerechnet, nicht geschätzt. Jeder
    Zustand trägt Farbe **und** Symbol **und** Wort. Alles ist ohne Maus
    bedienbar. Horizontales Scrollen des Seitenkörpers ist ein Fehler, auf
    jeder Breite von 320 px bis 4K. Gemessen wird **mobil**: Best
    Practices und SEO 100, agentisches Browsen 3/3, Leistung und
    Barrierefreiheit mindestens 95 — der Lighthouse-Wert ersetzt die
    Prüfung nicht.
14. **Rechtliche Pflichtbausteine.** Impressum, Datenschutzerklärung und
    Barrierefreiheitserklärung sind eigene, immer erreichbare Seiten nach
    österreichischem Recht. Vor der Einwilligung lädt nichts von Dritten —
    auch kein eingebettetes Video. Schriften werden immer selbst
    ausgeliefert. Für Anwendungen und Portale gilt zusätzlich der EU
    Cyber Resilience Act samt Dokumentenpaket und Meldeweg.
15. **Dokumentation ist Teil der Änderung.** Sie beschreibt den
    IST-Zustand und zieht im selben Schritt nach, ohne Marketingsprache.
    Struktur: `docs/[frontend|backend]/<sprache>/…`, je Ordner eine
    `README.md` als Inhaltsverzeichnis. Bedienung wird dokumentiert, mit
    markierten Screenshots im Repository. Geplantes liegt unter /plan.
16. **Das System spricht englisch, der Mensch deutsch.** Bezeichner,
    Kommentare, Protokolle, Fehlercodes, Konfigurations- und
    Übersetzungsschlüssel, Tabellen, Spalten, Schnittstellen und
    Backend-Oberflächen sind **englisch** — ausnahmslos. Deutsch bleibt,
    was ein deutschsprachiger Mensch liest: Oberflächentexte,
    Projektdokumentation, Commit-Nachrichten.
    - **Wie technisch, bestimmt das Projekt — je Bereich, nicht je
      Projekt.** Drei Stufen: **1** ohne Vorkenntnisse (keine Technik,
      Sprache des Berufs), **2** kundig (Fachbegriffe der Sache, Technik
      nur erklärt), **3** technisch. Welche Stufe wo gilt, steht in der
      `CLAUDE.md`; fehlt der Eintrag, wird gefragt. Im Zweifel die
      niedrigere.
    Ausführlich: `neo-grundregeln`, `references/zielgruppe.md`.
17. **Mehrsprachig heißt vollständig.** Jeder sichtbare Text hat in jeder
    ausgelieferten Sprache eine Übersetzung — **gemessen, nicht
    angenommen** (`translations.py`). Null fehlende Schlüssel, null
    leere Werte, null abweichende Platzhalter. Ein Schlüssel mitten in
    der Oberfläche ist der sichtbarste Mangel, den ein Produkt haben
    kann. Keine harte Zeichenkette in der Oberfläche, kein Satz aus
    Teilschlüsseln zusammengesetzt.
18. **Deutsche Texte mit echten Umlauten** (ä ö ü ß), nie ue/ae/oe/ss.
    Das gilt für **jeden** deutschen Text, einschließlich
    Commit-Nachrichten, Pull-Request-Titeln und -Texten und Meldungen im
    Terminal. Ausnahmen nur Slugs, URLs, Dateinamen, Code und englische
    Bezeichner. Keine Emojis in Dokumentation, Commits und Oberflächen.
19. **Sicherheit von Anfang an.** Secrets nie in Code, Konfiguration oder
    Logs. Destruktive Aktionen brauchen eine Bestätigung, die die Folge
    benennt. Verstecken ist kein Schutz.
20. **Zweige: ein Auftrag, ein Zweig — und erst mergen, dann den
    nächsten.** Welches Modell gilt, steht in der `CLAUDE.md`; fehlt der
    Eintrag, gilt das strengste und es wird gefragt. **Modell `dev`**
    (Regelfall): Arbeitszweig → `dev` → `main`; `main` nimmt
    ausschließlich `dev`. **Modell `main` mit Arbeitszweig**: kein `dev`,
    aber auch kein direkter Push. **Modell `main` direkt**: nur mit
    ausdrücklicher Festlegung.
    - **Kein zweiter Zweig, solange der erste offen ist.** Ein Auftrag,
      ein Zweig: öffnen, fertigstellen, mergen, Zweig weg. Erst dann der
      nächste. Wer neue Zweige auf halbfertigen stapelt, endet bei
      Cherry-Picks und weiß am Ende nicht, was drin ist.
    - **Ein gemergter Zweig wird gelöscht.** Geht das nicht, wird er
      trotzdem nicht weiterverwendet und in der Fertigmeldung als
      erledigt genannt.
    - **Offene Zweige werden vor der Fertigmeldung berichtet** — Zahl und
      Namen. Keiner bleibt unbemerkt liegen.
    - **Ausgerollt wird nur, was grüne Tests hat.** Historie fremder
      Zweige wird nie umgeschrieben.
    Ausführlich: `neo-grundregeln`, `references/git.md`.
21. **Das Repository bleibt sauber: die `.gitignore` davor, der Rückbau
    danach.** Ein Repository ist ein Werkzeug, kein Archiv.
    - **Die `.gitignore` gehört zum ersten Commit**, und **das Muster
      wird eingetragen, bevor die Datei entsteht**: Wer ein Werkzeug
      einführt, das schreibt, trägt im selben Schritt ein, was es
      schreibt. Nachträglich eintragen entfernt nichts aus dem Verlauf.
    - **Vor jedem Commit wird die Liste der Dateien angesehen**, nicht
      nur die Nachricht geschrieben.
    - **Jede Änderung nimmt ihre Rückstände mit.** Was zum Ausprobieren
      entstand, räumt der Agent im selben Schritt weg; Vorübergehendes
      entsteht außerhalb des Repositories.
    - **Gelöscht wird nach Freigabe**, mit Liste und Grund je Datei.
      Sperrdateien der Abhängigkeiten, Dokumentation fremder
      Schnittstellen und Entscheidungsakten **bleiben**.
    Ausführlich: `neo-grundregeln`, `references/git.md` und
    `references/altlasten.md`.
22. **Contao.** Websites müssen vollständig in Contao verwaltbar sein und
    wirken, als wären sie rein in Contao entstanden. Keine festen Texte
    in Templates — alles aus Feldern, mit Insert-Tags. Kern und fremde
    Erweiterungen bleiben unangetastet. Bildkompression und Imagesets nur
    über Contao, Styles ausnahmslos in SCSS und im Layout gewählt, jede
    Seite liefert nur, was sie braucht. Eigene Erweiterung erst, wenn es
    keine marktreife gibt.
23. **Qualität vor Geschwindigkeit.** Kein Quick-and-Dirty, keine
    Provisorien, keine TODOs im committeten Code, kein Copy-Paste ohne
    vollständiges Verstehen. Saubere Codestruktur nach den **offiziellen
    Vorgaben des jeweiligen Stacks**: klare Schichtgrenzen mit
    festgelegter Importrichtung, eine Verantwortung je Einheit.
    Formatierung, Lint und Analyse laufen maschinell als Blocker. Bei
    Konflikt zwischen Geschwindigkeit und Korrektheit oder Sicherheit
    gewinnt immer Letzteres.
24. **Sauber heißt nicht abstrakt.** Der Code muss von jemandem lesbar
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
25. **Schnittstellen.** Wird an einer API entwickelt, ist ein
    OpenAPI-Dokument Pflicht, erzeugt aus dem Code und je Fachbereich
    geschnitten. Stabile Fassungen brechen nie; Brechendes bekommt eine
    neue Version oder die Vorschaufläche. Jede Fehlerantwort hat dieselbe
    Hülle, auch 401, 403 und 404. Autorisierung ist deny-by-default,
    Mandantenkontext kommt nur aus authentifizierten Ansprüchen.
26. **Daten und KI.** Eine Sicherung gilt erst als Sicherung, wenn eine
    Wiederherstellung nachweislich gelungen und protokolliert ist. Jede
    Datenart hat eine Aufbewahrungsfrist mit Auslöser und wird danach
    automatisch gelöscht oder anonymisiert — was von Hand gelöscht
    werden müsste, wird nie gelöscht. Wer KI einsetzt, legt offen, dass
    es KI ist (Artikel 50 EU-KI-Verordnung, seit 02.08.2026), und
    schickt keine personenbezogenen Daten ohne Rechtsgrundlage an ein
    Modell.
27. **Nur harte Sicherheitslücken sofort beheben** — jede andere
    ungefragte Änderung braucht vorher eine Rückfrage. Das gilt
    ausdrücklich für **Umbenennen** von Dateien, Symbolen, Schaltern oder
    Feldern, den **Wechsel eines Daten- oder Dateiformats**, das
    **Löschen** von Dateien und jedes **Aufräumen** — auch dann, wenn es
    sachlich richtig ist und das Ergebnis besser wird. Sachlich richtig
    ist kein Freibrief.
