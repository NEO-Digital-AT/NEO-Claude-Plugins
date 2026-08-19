# NEO-Kernregeln (gelten immer, in jedem Projekt)

Die ausführlichen Fassungen liegen in den Skills `neo-grundregeln`,
`neo-doku`, `neo-komponenten` und `neo-sicherheit` — bei passender
Aufgabe den jeweiligen Skill laden.

1. **Entscheidungshoheit.** Keine freie Entscheidung über Technologie,
   Pakete oder tragende Architektur. Mehrere Optionen mit Vor- und
   Nachteilen vorlegen, Empfehlung abgeben — die Entscheidung fällt
   ausnahmslos der Projektinhaber. Vor jedem Umsetzungsschritt
   zusammenfassen und die Freigabe abwarten. Einzige Ausnahme: harte
   Sicherheitslücken (Regel 10).
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
4. **Frameworktreue.** Nie selbst bauen, was Framework oder Bibliothek
   liefern. Keine neuen Bibliotheken ohne Prüfung des Bestands und ohne
   Freigabe. Bestehende Muster zuerst studieren und fortsetzen.
5. **Komponenten-Grundsatz.** Views rufen nur die Wrapper-Komponenten der
   Produktfamilie auf (Neo* bei NEO Digital, LeoFlex* bei LeoFlex), nie
   rohe Framework-Widgets. Stil, Größe und Farbe leben in der Komponente;
   Views liefern nur Inhalt, Ziel und Funktion. Bestehende
   Komponentenbibliotheken nie ohne Freigabe umschreiben.
6. **Dokumentation ist Teil der Änderung.** Sie beschreibt den
   IST-Zustand, zieht im selben Schritt nach und enthält keine
   Marketingsprache. Geplantes liegt unter /plan bzw. /plans.
7. **Deutsche Texte mit echten Umlauten** (ä ö ü ß), nie ue/ae/oe/ss —
   Ausnahmen nur Slugs, URLs, Code und englische Bezeichner. Keine
   Emojis in Dokumentation, Commits und Oberflächen.
8. **Sicherheit von Anfang an.** Secrets nie in Code, Konfiguration oder
   Logs. Destruktive Aktionen brauchen eine Bestätigung, die die Folge
   benennt. Verstecken ist kein Schutz.
9. **Qualität vor Geschwindigkeit.** Kein Quick-and-Dirty, keine
   Provisorien, keine TODOs im committeten Code, kein Copy-Paste ohne
   vollständiges Verstehen. Saubere Codestruktur: klare Modul- und
   Schichtgrenzen, eine Verantwortung pro Einheit, Benennung und Ablage
   nach den Mustern des Projekts. Bei Konflikt zwischen Geschwindigkeit
   und Korrektheit oder Sicherheit gewinnt immer Letzteres.
10. **Nur harte Sicherheitslücken sofort beheben** — jede andere
    ungefragte „Verbesserung" (Refactoring, Umbenennung, Stiländerung)
    braucht vorher eine Rückfrage.
