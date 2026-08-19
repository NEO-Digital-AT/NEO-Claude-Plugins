---
description: Selbstkontrolle des aktuellen Arbeitsstands nach den NEO-Grundregeln (Diff, Auswirkungen, Tests, Doku, Umlaute)
---

Prüfe den aktuellen Arbeitsstand nach den NEO-Grundregeln und berichte
das Ergebnis als kompakte Liste. Nichts reparieren, nur prüfen und
berichten — Reparaturen erst nach Freigabe. Prüfe:

1. **Umfang:** Entspricht der aktuelle Diff exakt dem freigegebenen
   Umfang? Liste alles auf, was darüber hinausgeht.
2. **Auswirkungen:** Welche anderen Programmteile, Verträge, Tests und
   Dokumente sind von den Änderungen betroffen? Wurden sie mitgeprüft?
3. **Tests:** Laufen Lint/Analyse und die Test-Suiten des Projekts? Gibt
   es neues Verhalten ohne neuen Test? Gibt es abgeschwächte Assertions?
4. **Dokumentation:** Ist die Doku im selben Stand wie der Code
   (Systemdoku, Änderungsprotokoll, Handbuch, Regeldateien)? Behauptet
   ein Dokument etwas, das nicht mehr stimmt?
5. **Sprache:** Enthalten deutsche Texte ASCII-Ersatzschreibungen
   (ue/ae/oe/ss statt ü/ä/ö/ß) oder Emojis?
6. **Hygiene:** TODOs, Secrets, temporäre Dateien, leere Ordner,
   auskommentierter Code im Diff?

Am Ende: eine Zeile „Bereit für Freigabe: ja/nein" mit Begründung.
