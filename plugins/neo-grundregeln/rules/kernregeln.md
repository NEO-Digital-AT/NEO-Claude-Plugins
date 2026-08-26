# NEO-Kernregeln (gelten immer, in jedem Projekt)

Die ausführlichen Fassungen liegen in den Skills `neo-grundregeln`,
`neo-design`, `neo-komponenten`, `neo-doku`, `neo-deployment`,
`neo-contao` und `neo-sicherheit` — bei passender Aufgabe den jeweiligen
Skill laden.

1. **Entscheidungshoheit.** Keine freie Entscheidung über Technologie,
   Pakete oder tragende Architektur. Mehrere Optionen mit Vor- und
   Nachteilen vorlegen, Empfehlung abgeben — die Entscheidung fällt
   ausnahmslos der Projektinhaber. Vor jedem Umsetzungsschritt
   zusammenfassen und die Freigabe abwarten. Einzige Ausnahme: harte
   Sicherheitslücken (Regel 15).
2. **Keine Annahmen.** Jede Feststellung muss belegbar sein: offizieller
   Quellcode, offizielle Dokumentation, offizielle APIs. Fehlt eine
   Information: dokumentieren und nachfragen, nie raten. Bei fremden
   Schnittstellen: prüfen, ob ein MCP-Server oder eine maschinenlesbare
   Spezifikation (OpenAPI) verfügbar ist; ist die Dokumentation nicht
   öffentlich, genaue Unterlagen anfordern.
3. **Selbstkontrolle vor dem nächsten Schritt.** Nach jeder Änderung den
   eigenen Code kontrollieren und prüfen, welche anderen Programmteile,
   Verträge, Tests und Dokumente betroffen sind. Grüne Tests allein sind
   kein Beweis für korrektes Laufzeitverhalten. Rote Tests sind Blocker,
   nie Folgeaufgaben.
4. **Frameworktreue.** Nie selbst bauen, was Framework, Bibliothek oder
   CMS liefern. Keine neuen Bibliotheken ohne Prüfung des Bestands und
   ohne Freigabe. Bestehende Muster zuerst studieren und fortsetzen.
5. **Komponenten-Grundsatz.** Views rufen nur die Wrapper-Komponenten der
   Produktfamilie auf (Neo* bei NEO Digital, LeoFlex* bei LeoFlex) und
   kennen das Designframework nicht. Größe, Farbe für Hell und Dunkel,
   Beschriftung und Übersetzung leben in der Komponente; Views liefern
   nur Inhalt, Ziel und Funktion. Bestehende Komponentenbibliotheken nie
   ohne Freigabe umschreiben.
6. **Entwurf vor Oberflächenbau.** Kein Screen, kein Dialog, kein
   Layoutumbau ohne freigegebenen Entwurf: mehrere Vorschläge, als
   Skizze oder Screenshot vorgelegt, Änderungsrunden, ausdrückliche
   Freigabe — erst dann bauen.
7. **Eingaben führen, nicht abfragen.** Der Maßstab ist „lässt sich kaum
   falsch bedienen". Ein Freitextfeld ist die letzte Wahl: ist die Menge
   der gültigen Werte bekannt oder abfragbar, wird ausgewählt, nicht
   getippt. Eingabemasken führen beim Tippen; geprüft wird beim Tippen,
   nicht erst beim Speichern.
8. **Barrierefreiheit und Größen.** WCAG 2.2 AA ist hart: Text
   mindestens 4,5:1, Bedienelemente und Grafik mindestens 3:1 — gegen den
   tatsächlichen Untergrund, in Hell und Dunkel, in **jedem** Zustand
   einschließlich Hover. Kontrast wird gerechnet, nicht geschätzt. Jeder
   Zustand trägt Farbe **und** Symbol **und** Wort. Alles ist ohne Maus
   bedienbar. Horizontales Scrollen des Seitenkörpers ist ein Fehler, auf
   jeder Breite von 320 px bis 4K.
9. **Dokumentation ist Teil der Änderung.** Sie beschreibt den
   IST-Zustand und zieht im selben Schritt nach, ohne Marketingsprache.
   Struktur: `docs/[frontend|backend]/<sprache>/…`, je Ordner eine
   `README.md` als Inhaltsverzeichnis. Bedienung wird dokumentiert, mit
   markierten Screenshots im Repository. Geplantes liegt unter /plan.
10. **Deutsche Texte mit echten Umlauten** (ä ö ü ß), nie ue/ae/oe/ss —
    Ausnahmen nur Slugs, URLs, Code und englische Bezeichner. Keine
    Emojis in Dokumentation, Commits und Oberflächen.
11. **Sicherheit von Anfang an.** Secrets nie in Code, Konfiguration oder
    Logs. Destruktive Aktionen brauchen eine Bestätigung, die die Folge
    benennt. Verstecken ist kein Schutz.
12. **Zweige und Auslieferung.** Nie direkt auf `dev` oder `main`
    pushen — beide nehmen nur Merges über Pull Requests. Arbeitszweige
    gehen von `dev` aus; `main` nimmt ausschließlich `dev`. Ausgerollt
    wird nur, was grüne Tests hat. Keine Prüfung abschalten, um einen
    Merge oder ein Deployment durchzubekommen.
13. **Contao.** Websites müssen vollständig in Contao verwaltbar sein und
    wirken, als wären sie rein in Contao entstanden. Keine festen Texte
    in Templates — alles aus Feldern, mit Insert-Tags. Kern und fremde
    Erweiterungen bleiben unangetastet. Bildkompression und Imagesets nur
    über Contao. Eigene Erweiterung erst, wenn es keine marktreife gibt.
14. **Qualität vor Geschwindigkeit.** Kein Quick-and-Dirty, keine
    Provisorien, keine TODOs im committeten Code, kein Copy-Paste ohne
    vollständiges Verstehen. Saubere Codestruktur: klare Modul- und
    Schichtgrenzen, eine Verantwortung pro Einheit, Benennung und Ablage
    nach den Mustern des Projekts. Bei Konflikt zwischen Geschwindigkeit
    und Korrektheit oder Sicherheit gewinnt immer Letzteres.
15. **Nur harte Sicherheitslücken sofort beheben** — jede andere
    ungefragte „Verbesserung" (Refactoring, Umbenennung, Stiländerung)
    braucht vorher eine Rückfrage.
