# Abnahmeliste Arbeitsprozess

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". **Nicht Geprüftes gilt als nicht
erfüllt.**

Der Befehl `/neo-grundregeln:neo-selbstkontrolle` geht diese Liste am
aktuellen Arbeitsstand durch.

## Auftragsliste

- [ ] **Jeder Punkt der Auftragsliste ist erledigt oder gestrichen** —
      auch die, die zwischendurch nachgereicht wurden
      (`auftragsliste.md`).
- [ ] Kein Punkt steht auf **wartend**, ohne dass die Rückfrage offen
      sichtbar gestellt wurde.
- [ ] **Jede Anweisung zu Git wurde ausgeführt und belegt** — Merge,
      Commit, Push mit Kennung, nicht angekündigt.
- [ ] Die Liste steht in der Antwort, mit Stand je Punkt.

## Prozess

- [ ] Eine `CLAUDE.md` liegt vor, zählt die geltenden Skills namentlich
      auf und wurde eingehalten.
- [ ] **Zweigmodell, Zielgruppe je Bereich und Betriebsart stehen dort** —
      und wurden eingehalten, nicht aus einem anderen Projekt übernommen
      (Kernregeln 4, 16, 20).
- [ ] **Die Sprachstufe des Bereichs wurde eingehalten**, in dem gearbeitet
      wurde; die Wortliste ebenfalls (`zielgruppe.md`).
- [ ] Die Regelwerke des Projekts wurden gelesen, nicht nur die README.
- [ ] Umfang und Nicht-Umfang wurden benannt.
- [ ] Die Abhängigkeiten wurden **vor** der Umsetzung erhoben.
- [ ] **Jede Fachaufgabe lief über ihren Fachagenten**, nicht nebenbei in
      der Weiche (`orchestrierung.md`).
- [ ] **Die Konfiguration wurde gelesen**, nicht angenommen — `.env`,
      Konfigurationsdateien, `CLAUDE.md`. Keine Aussage über einen
      Schlüssel ohne die vier Schritte davor (`belegpflicht.md`).
- [ ] **Offene Zweige berichtet**, Zahl und Namen; gemergte gelöscht
      (`branch-check.py`, `git.md`).
- [ ] Zusammengefasst und die Freigabe **abgewartet**.
- [ ] Bei Oberflächen: Entwurf vorgelegt und freigegeben
      (Skill `neo-design`).
- [ ] Der Diff entspricht **exakt** dem freigegebenen Umfang. Alles
      darüber hinaus ist aufgelistet.
- [ ] Gewachsener Umfang wurde vorgelegt, nicht stillschweigend
      mitgenommen.

## Belege

- [ ] Jede Feststellung hat eine Fundstelle oder ist als Vermutung
      gekennzeichnet.
- [ ] Fremde Schnittstellen gegen die offizielle Spezifikation geprüft.
- [ ] Vorhandener Dokumentations-MCP wurde konsultiert.
- [ ] Referenzmaterial je Integration liegt im Repo.

## Selbstkontrolle

- [ ] Der eigene Diff wurde gelesen, Datei für Datei.
- [ ] Auswirkungsanalyse schriftlich, alle acht Bereiche beantwortet.
- [ ] Die Abhängigkeiten aus Schritt 2 wurden nach der Umsetzung
      einzeln geprüft, mit Ergebnis.
- [ ] Beim Debugging: Logs vor der Hypothese gelesen.
- [ ] Kein „das wird es beheben" ohne die drei Bedingungen.
- [ ] Was Laufzeit berührt, wurde zur Laufzeit geprüft — Neustart,
      Build, Probelauf.

## Tests

- [ ] Validierungsreihenfolge gelaufen: Abhängigkeiten, Lint, Tests,
      Build. **Zahlen genannt.**
- [ ] Neues Verhalten hat neue Tests.
- [ ] Jedes Bedienelement hat einen Oberflächen-Funktionstest.
- [ ] Keine abgeschwächte Zusicherung, kein übersprungener Test.
- [ ] Für jeden aufgetretenen Fehler existiert ein Regressionstest.
- [ ] Mock- und Demoschichten sind mitgezogen.
- [ ] Keine echten Kundendaten in Test und Entwicklung.

## Dokumentation

- [ ] Doku im selben Schritt nachgezogen (Skill `neo-doku`).
- [ ] Änderungsprotokoll ergänzt.
- [ ] Regeldatei für Agenten geprüft, wo Verhalten sich ändert.
- [ ] Tragende Entscheidung als Entscheidungsakte festgehalten.

## Hygiene

- [ ] **Die Liste der Dateien im Commit wurde angesehen**, nicht nur die
      Nachricht geschrieben (`git status --short`).
- [ ] **Kein Erzeugnis im Diff** — keine Bau-Ausgabe, kein
      Zwischenspeicher, keine Aufnahme, kein Bericht. Was neu entstanden
      ist, steht in der `.gitignore` (Kernregel 21).
- [ ] **Jedes neu eingeführte Werkzeug hat sein Muster in der
      `.gitignore`**, im selben Schritt eingetragen.
- [ ] Keine TODOs, keine temporären Dateien, kein auskommentierter Code.
- [ ] Keine Secrets im Diff.
- [ ] Deutsche Texte mit echten Umlauten — **auch die
      Commit-Nachricht**.
- [ ] Keine Emojis in Doku, Commits und Oberflächen.
- [ ] Keine leeren Ordner nach Refactorings.
- [ ] **Was in dieser Sitzung zum Ausprobieren entstand, ist weg** —
      Probeskripte, Zwischenstände, Aufnahmen, Protokolle
      (`altlasten.md`).
- [ ] Bei einer Durchsicht: `repo-hygiene.py` gelaufen, Geheimnisse und
      Reste **null**, die Vorschläge beantwortet statt übergangen.

## Abschluss

- „Geprüft: <n> von <m> Punkten, <k> nicht anwendbar."
- „Tests: <grün> von <gesamt>." — Zahlen, keine Einschätzung.
- „Bereit für Freigabe: ja/nein" mit Begründung. Ein roter Test, ein
  ungeprüfter Punkt oder ein Umfang über der Freigabe heißen nein.
