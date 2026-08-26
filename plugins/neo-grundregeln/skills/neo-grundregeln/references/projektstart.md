# Projektstart — was ein neues Repo am ersten Tag mitbringt

Was am ersten Tag fehlt, fehlt in zwei Jahren immer noch. Diese Liste
wird beim Anlegen abgearbeitet, nicht später nachgezogen.

Der Befehl `/neo-grundregeln:neo-projektstart` prüft sie gegen ein
bestehendes Repository und berichtet, was fehlt.

## Vor der ersten Datei

Diese vier Punkte werden **erfragt**, nicht angenommen:

| Frage | Wirkt sich aus auf |
| --- | --- |
| Anwendung/Portal oder Webseite? | Betriebsart in `neo-design` |
| Rollt das Repo etwas aus? | Zweigmodell in `neo-deployment` |
| Frontend, Backend oder beides? | Doku-Struktur in `neo-doku` |
| Welche Sprachen werden ausgeliefert? | Sprachordner, Screenshots, Übersetzungen |

## Wurzelverzeichnis

| Datei | Inhalt |
| --- | --- |
| `README.md` | Was das Projekt ist, wie man es startet, wie man es testet, wohin die Doku zeigt |
| `CLAUDE.md` | Regeldatei für Agenten: Betriebsart, Stack, Besonderheiten, Verweis auf die NEO-Plugins. Projektregeln, die konkreter sind, gehen vor |
| `CHANGELOG.md` | Änderungsprotokoll ab dem ersten Eintrag |
| `.env.example` | Jeder Konfigurationsschlüssel mit Bedeutung, ohne echten Wert |
| `.gitignore` | Passend zum Stack; keine Erzeugnisse, keine Secrets, keine lokalen Ordner |
| `LICENSE` bzw. Lizenzhinweis | Auch bei geschlossenen Projekten: `proprietary` steht ausdrücklich da |
| `SECURITY.md` | Wie eine Schwachstelle gemeldet wird, an wen, mit welcher Reaktionszeit |

## Struktur

```
docs/            Doku nach neo-doku: [frontend|backend]/<sprache>/...
  README.md      Einstieg: Bereiche, Sprachen, Leitsprache
  adr/           Entscheidungsakten, sprachneutral
plan/            Geplantes und Oberflächen-Entwürfe
.github/
  workflows/     Prüfen und Ausrollen nach neo-deployment
  CODEOWNERS     Wer welchen Bereich freigeben muss
```

Bei Oberflächen zusätzlich der Ordner für die Komponenten der
Produktfamilie und der Wächter-Test (Skill `neo-komponenten`).

## Werkzeuge, ab dem ersten Commit

- Formatierer, Linter und Analyse eingerichtet, Konfiguration im Repo,
  Warnungen als Fehler (Skill `neo-code`).
- Testgerüst vorhanden, mit mindestens einem echten Test — nicht mit
  einem, der nur prüft, dass nichts geworfen wurde.
- CI läuft: Abhängigkeiten, Lint, Tests, Build. Grün, bevor der zweite
  Commit entsteht.

## Zweige und Ausrollung

- `dev` und `main` angelegt, beide geschützt, Rulesets gesetzt
  (Skill `neo-deployment`). Ohne Ausrollung: die Ausnahme wird begründet
  und im README festgehalten.
- Umgebungen mit Zweigrichtlinie, Secrets an der Umgebung.
- Pflichtprüfungen eingetragen, nachdem die Workflows einmal gelaufen
  sind.

## Betrieb

- Sicherung eingerichtet, hinnehmbarer Datenverlust und Wiederanlaufzeit
  festgelegt (Skill `neo-betrieb`).
- Erste Wiederherstellung durchgeführt und protokolliert — **vor** dem
  Livegang, nicht danach.
- Betriebshandbuch angelegt, auch wenn es zunächst kurz ist.
- Statusendpunkt und Überwachung, wo es eine laufende Anwendung gibt
  (Skill `neo-api`).
- SPF, DKIM und DMARC, sobald das Projekt Mail versendet.

## Recht

- Impressum, Datenschutzerklärung und Barrierefreiheitserklärung als
  eigene Seiten (Skill `neo-recht`).
- Consent-Dialog, bevor der erste Fremddienst eingebaut wird — nicht
  danach.
- Schriften selbst ausgeliefert.
- Löschkonzept angelegt, sobald personenbezogene Daten gespeichert
  werden.
- Bei Anwendungen: `docs/cra/` mit dem Dokumentenpaket.
- Bei KI-Funktionen: Offenlegung nach Artikel 50 (Skill `neo-ki`).

## Der erste Commit

Er enthält das Gerüst und läuft grün durch die CI. **Kein
„initial commit" mit 400 Dateien und rotem Test** — der Zustand wird nie
wieder aufgeräumt.

## Was ausdrücklich nicht am ersten Tag entsteht

- Ordner „für später".
- Abstraktionen ohne zweiten Anwendungsfall.
- Eine Komponentenbibliothek ohne die erste Ansicht, die sie braucht.
- Ein Modul ohne freigegebenen Entwurf (Skill `neo-design`).
