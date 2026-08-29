# NEO-Kernregeln (gelten immer, in jedem Projekt)

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
2. **Nichts erfinden, was jemand für Wahrheit halten könnte.** Der Agent
   schreibt keinen Inhalt, den niemand verlangt hat: keinen Satz in die
   Oberfläche, keine Beschriftung, keinen Hilfetext, keinen Hinweis unter
   einem Feld, keine Zusage, keine Zahl, keinen Beispielwert. **Fehlt an
   einer Stelle ein Text, ist das eine Rückfrage — keine Lücke, die
   gefüllt wird.**
   - **Ein Satz in der Oberfläche ist eine Zusage.** Steht dort, wo etwas
     erreichbar ist, wie lange etwas dauert, was automatisch geschieht
     oder was der Anwender auswählen kann, dann sagt das Produkt sein
     eigenes Verhalten zu. **Vor dem Schreiben wird am Code belegt, dass
     es stimmt**, mit Fundstelle. Ohne Beleg ist es keine unglückliche
     Formulierung, sondern eine Falschaussage gegenüber dem Kunden des
     Kunden — und sie steht in der Oberfläche, nicht im Protokoll.
   - **Kein Test zu einer selbst erfundenen Anforderung.** Ein Test hält
     fest, was **verlangt** wurde, nie, was der Agent beschlossen hat.
     Ein Test über Erfundenes ist schlimmer als die Erfindung: Er erklärt
     sie zum Soll, macht sie grün und sorgt dafür, dass sie nie mehr
     auffällt. Lässt sich zu einem Test die Anforderung nicht benennen —
     Entwurf, Ticket, Satz des Projektinhabers —, wird er nicht
     geschrieben, sondern gefragt.
   - **Jeder sichtbare Text hat eine Herkunft**: der Entwurf, eine
     freigegebene Textliste oder eine Anweisung des Projektinhabers. Was
     die Oberfläche zusätzlich braucht — Fehlermeldung, Leerzustand,
     Ladehinweis —, wird **vorgelegt und freigegeben**, bevor es in die
     Sprachdatei kommt. Es entsteht nicht beim Bauen.
   - **Im Zweifel weglassen.** Ein fehlender Hinweis ist eine Rückfrage.
     Ein erfundener Hinweis ist ein Fehler im Produkt.
   - **Eine Entschuldigung hinterher stellt nichts wieder her.** Der
     Anwender hat den Satz gelesen, der Test hat ihn bestätigt, die
     Dokumentation hat ihn übernommen. Deshalb gilt die Regel vorher.
   Ausführlich: Skill `neo-grundregeln`, `references/tests.md`; Skill
   `neo-design`, `references/oberflaechentexte.md`.
3. **Die Auftragsliste.** Der Projektinhaber schreibt, sobald ihm etwas
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
6. **Keine Annahmen.** Jede Feststellung muss belegbar sein: offizieller
   Quellcode, offizielle Dokumentation, offizielle APIs. Fehlt eine
   Information: dokumentieren und nachfragen, nie raten. Bei fremden
   Schnittstellen: prüfen, ob ein MCP-Server oder eine maschinenlesbare
   Spezifikation (OpenAPI) verfügbar ist; ist die Dokumentation nicht
   öffentlich, genaue Unterlagen anfordern.
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
11. **Das Designsystem gibt vor, der Agent setzt um — der Agent gestaltet
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
   - **Wie technisch der Mensch angesprochen wird, bestimmt das Projekt —
     je Bereich, nicht je Projekt.** Ein Kassensystem spricht am Tresen
     mit Kellnern und in den Einstellungen mit dem Betreiber, der eine
     Registrierkasse hinterlegt. Drei Stufen: **1 ohne Vorkenntnisse**
     (keine Technik, keine Abkürzungen, Sprache des Berufs), **2 kundig**
     (Fachbegriffe der Sache ja, Technik nur wo unvermeidbar und dort
     erklärt), **3 technisch** (Fachausdrücke ohne Erklärung). Welche
     Stufe wo gilt, steht in der `CLAUDE.md`; **fehlt der Eintrag, wird
     gefragt**. Im Zweifel die niedrigere. Ein technischer Satz in einem
     Bereich der Stufe 1 ist ein Fehler, auch wenn er stimmt.
     Ausführlich: Skill `neo-grundregeln`, `references/zielgruppe.md`.
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
20. **Zweige und Auslieferung — welches Modell gilt, sagt das Projekt.**
    Es steht in der `CLAUDE.md` (Regel 4). **Fehlt der Eintrag, gilt das
    strengste Modell**, und es wird nachgefragt — nicht angenommen, dass
    das Modell des letzten Projekts auch hier gilt.
    - **Modell `dev`** — der Regelfall bei NEO und LeoFlex: Ein
      Arbeitszweig geht von `dev` aus und wird **nach `dev` gemerged**;
      `main` nimmt **ausschließlich** `dev`. Kein direkter Push auf
      `dev`, kein Merge nach `main` aus irgendetwas anderem als `dev`,
      kein Arbeitszweig direkt nach `main`.
    - **Modell `main` mit Arbeitszweig** — Projekte ohne `dev`: Der
      Arbeitszweig geht von `main` aus und wird nach `main` gemerged.
      Kein direkter Push auf `main`.
    - **Modell `main` direkt** — nur, wo der Projektinhaber es
      ausdrücklich festgelegt hat, und nur für dieses Projekt.
    - **Ausgerollt wird nur, was grüne Tests hat.** Keine Prüfung
      abschalten, um einen Merge oder ein Deployment durchzubekommen.
    - **Historie eines fremden Zweigs wird nie umgeschrieben** — kein
      Rebase, kein Amend, kein Force-Push.
21. **Das Repository bleibt sauber: die `.gitignore` davor, der Rückbau
    danach.** Ein Repository ist ein Werkzeug, kein Archiv. Jede Datei
    darin kostet Aufmerksamkeit — jemand liest sie, jemand hält sie für
    aktuell, jemand pflegt sie mit.
    - **Die `.gitignore` gehört zum ersten Commit**, nicht zum
      Aufräumen: **bevor** die erste Datei entsteht, die nicht
      hineingehört — Abhängigkeiten, Bau-Ausgaben, Zwischenspeicher,
      Aufnahmen und Berichte aus Werkzeugen, Editor- und
      Betriebssystemreste, alles Lokale.
    - **Das Muster wird eingetragen, bevor die Datei entsteht.** Wer ein
      Werkzeug einführt, das schreibt, trägt im selben Schritt ein, was
      es schreibt. Sonst liegen nach dem nächsten Lauf tausend Dateien im
      Verlauf, und niemand sieht mehr, was die Änderung war.
    - **Nachträglich eintragen entfernt nichts.** Was einmal eingecheckt
      ist, steht im Verlauf; es muss zusätzlich aus der Verwaltung
      genommen werden (`git rm --cached`), und ein Geheimnis gilt ab dann
      als kompromittiert (Regel 19).
    - **Vor jedem Commit wird die Liste der Dateien angesehen**, nicht nur
      die Nachricht geschrieben. `git add -A` ohne diesen Blick ist der
      Weg, auf dem Erzeugnisse hineinkommen.
    - **`git add -f` nur mit Grund und Vermerk.**
    - **Jede Änderung nimmt ihre Rückstände mit.** Was der Agent anlegt,
      um etwas herauszufinden — Probeskript, Zwischenstand, Aufnahme,
      Protokoll —, räumt er im selben Schritt weg; es taucht gar nicht
      erst im Commit auf. Vorübergehendes entsteht **außerhalb** des
      Repositories.
    - **Von Zeit zu Zeit die Durchsicht**, Datei für Datei mit einer
      Frage: Wird das noch gebraucht? Reste, Screenshots, einmal
      benutzte Skripte und **abgeschlossene Planungen** gehen; was daran
      wissenswert war, wird eine Entscheidungsakte. **Gelöscht wird nach
      Freigabe** — der Agent legt die Liste vor, mit Grund je Datei
      (Regel 1). Ausgenommen ist nur, was er selbst zum Ausprobieren
      angelegt hat.
    - **Was aussieht wie Müll und keiner ist:** Sperrdateien der
      Abhängigkeiten (`package-lock.json`, `composer.lock`,
      `packages.lock.json`) gehören eingecheckt, ebenso die
      Dokumentation fremder Schnittstellen und Entscheidungsakten.
    Ausführlich: Skill `neo-grundregeln`, `references/altlasten.md`.
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
