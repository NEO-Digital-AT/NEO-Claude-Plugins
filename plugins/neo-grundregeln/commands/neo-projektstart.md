---
description: Ein Repository gegen die NEO-Projektstartliste prüfen (Gerüst, Werkzeuge, Zweige, Betrieb, Recht) und den Fehlbestand berichten
---

Prüfe das aktuelle Repository gegen die NEO-Projektstartliste.

**Nichts anlegen, nichts ändern. Nur prüfen und berichten.** Anlegen erst
nach Freigabe, und dann in der Reihenfolge, die der Projektinhaber
festlegt.

Lies zuerst den Skill `neo-grundregeln` und
`references/projektstart.md`. Kläre dann die vier Eingangsfragen — aus
dem Repository, wenn es dort steht, sonst durch Rückfrage:

1. Anwendung/Portal oder Webseite?
2. Rollt das Repo etwas aus?
3. Frontend, Backend oder beides?
4. Welche Sprachen werden ausgeliefert?

Prüfe danach diese Bereiche und belege jeden Punkt mit einer Fundstelle
oder mit „fehlt":

1. **Wurzelverzeichnis:** README, CLAUDE.md, CHANGELOG, `.env.example`,
   `.gitignore`, Lizenzhinweis, SECURITY.md. Bei vorhandenen Dateien
   auch prüfen, ob sie den IST-Zustand beschreiben oder veraltet sind.
2. **Struktur:** `docs/` nach der Struktur aus `neo-doku`
   (`[frontend|backend]/<sprache>/…`, `README.md` je Ordner), `docs/adr/`,
   `plan/`, `.github/workflows/`, `CODEOWNERS`. Bei Oberflächen
   zusätzlich der Komponentenordner und der Wächter-Test.
3. **Werkzeuge:** Formatierer, Linter, Analyse, Testgerüst — vorhanden,
   konfiguriert im Repo, Warnungen als Fehler? Läuft die CI, und läuft
   sie grün?
4. **Zweige:** Gibt es `dev` und `main`? Sind sie geschützt? Existieren
   die Workflows aus `neo-deployment` und die Herkunftsprüfung für
   `main`? Fehlt `dev`: steht die Begründung im README?
5. **Betrieb:** Sicherung eingerichtet, hinnehmbarer Datenverlust und
   Wiederanlaufzeit festgelegt, Wiederherstellung protokolliert,
   Betriebshandbuch vorhanden, Statusendpunkt, Mail-Einträge im DNS.
6. **Recht:** Impressum, Datenschutzerklärung, Barrierefreiheits-
   erklärung, Consent vor dem ersten Fremddienst, Schriften selbst
   ausgeliefert, Löschkonzept, bei Anwendungen `docs/cra/`, bei
   KI-Funktionen die Offenlegung nach Artikel 50.

Berichte das Ergebnis als Liste, gegliedert nach diesen sechs Bereichen,
je Eintrag: vorhanden, unvollständig oder fehlt — mit Fundstelle.

Am Ende drei Zeilen:

- „Vollständig: <n> von <m> Punkten."
- Die drei dringendsten Lücken, nach Schaden sortiert, mit einem Satz
  Begründung.
- „Livegang vertretbar: ja/nein" mit Begründung. Fehlende Pflichtseiten,
  eine ungeprüfte Sicherung oder eine rote CI heißen nein.
