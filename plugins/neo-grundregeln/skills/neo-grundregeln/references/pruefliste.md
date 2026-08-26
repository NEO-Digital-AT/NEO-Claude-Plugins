# Abnahmeliste Arbeitsprozess

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". **Nicht Geprüftes gilt als nicht
erfüllt.**

Der Befehl `/neo-grundregeln:neo-selbstkontrolle` geht diese Liste am
aktuellen Arbeitsstand durch.

## Prozess

- [ ] Die Regelwerke des Projekts wurden gelesen, nicht nur die README.
- [ ] Umfang und Nicht-Umfang wurden benannt.
- [ ] Die Abhängigkeiten wurden **vor** der Umsetzung erhoben.
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

- [ ] Keine TODOs, keine temporären Dateien, kein auskommentierter Code.
- [ ] Keine Secrets im Diff.
- [ ] Deutsche Texte mit echten Umlauten — **auch die
      Commit-Nachricht**.
- [ ] Keine Emojis in Doku, Commits und Oberflächen.
- [ ] Keine leeren Ordner nach Refactorings.

## Abschluss

- „Geprüft: <n> von <m> Punkten, <k> nicht anwendbar."
- „Tests: <grün> von <gesamt>." — Zahlen, keine Einschätzung.
- „Bereit für Freigabe: ja/nein" mit Begründung. Ein roter Test, ein
  ungeprüfter Punkt oder ein Umfang über der Freigabe heißen nein.
