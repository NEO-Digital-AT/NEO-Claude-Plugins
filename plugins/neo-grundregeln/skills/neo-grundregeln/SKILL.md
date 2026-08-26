---
name: neo-grundregeln
description: >
  Verbindliche NEO-Arbeitsregeln für jede nicht-triviale Entwicklungsaufgabe:
  Prozess vor jeder Änderung (analysieren, begründen, Freigabe), Technologie-
  Entscheidungen (Optionen statt Alleingang), Belegpflicht statt Annahmen,
  Umgang mit fremden APIs und MCP, Selbstkontrolle und Auswirkungsanalyse,
  Testpflichten, Git-Hygiene, kein Direkt-Push auf dev oder main. Diesen
  Skill laden, bevor ein Feature, ein Bugfix, ein Refactoring oder eine
  Integration begonnen wird.
metadata:
  herkunft: NEO Digital — destilliert aus NEOcash- und LeoFlex-Regelwerken, Stand 2026-08
---

# NEO-Grundregeln

Es gelten Produktionsstandards, keine Prototyp-Standards (Leitsatz der
NEO-Regelwerke: „Sauberer als sauber. Besser als gut. Sicherer als
sicher."). Das gilt für Code, Architektur, Design und die Arbeitsweise —
auch beim Debugging. Es gibt kein Zeitlimit-Argument: langsam,
systematisch und sorgfältig arbeiten.

## 1. Prozess vor jeder Änderung

Verbindliche Reihenfolge — keine Änderung ohne ausdrückliche Freigabe.
Einzige Ausnahme: harte Sicherheitslücken sofort beheben, danach
unverzüglich melden (Abschnitt 5, Eskalationsregel).

1. **Analysieren** — was wird gebaut, was ist ausdrücklich nicht dabei.
   Zuerst die Regelwerke des Projekts lesen (CLAUDE.md/AGENTS.md →
   Architekturdokument → bereichsspezifisches Konzeptdokument). Wissen
   allein aus der README reicht nie.
2. **Abhängigkeiten prüfen** — welche bestehenden Funktionen, Verträge,
   Tests und Dokumente kann die Änderung treffen? Realistische
   Was-wäre-wenn-Fälle durchdenken, vor der Umsetzung.
3. **Begründen und belegen** — jede Feststellung mit Quelle (Fundstelle
   im Code, offizielle Dokumentation). Risiken benennen.
4. **Zusammenfassen und Freigabe einholen** — auch wenn der Inhaber
   „leg los" sagt: erst zusammenfassen, erst nach seinem Ok (oder mit
   seiner Korrektur) umsetzen. Nie blind loslegen.
5. **Umsetzen** — nur den freigegebenen Umfang.
6. **Testen und reparieren** — neue Tests für neues Verhalten; rote Tests
   beheben, nie umgehen oder abschwächen.
7. **Nachbarfunktionen mitprüfen** — die unter 2. gefundenen
   Abhängigkeiten nach der Umsetzung kontrollieren.
8. **Dokumentieren im selben Schritt** — Systemdoku, Änderungsprotokoll,
   betroffene Handbuch-/Regelseiten (Details: Skill `neo-doku`).
9. **Fertigmelden** — was sichtbar ist, was offen blieb, was als
   Nächstes ansteht. Ergebnisse ehrlich melden: rote Tests heißen rot.

**Bei Oberflächen kommt ein Schritt davor:** kein Screen, kein Dialog,
kein Layoutumbau ohne freigegebenen Entwurf. Mehrere Vorschläge bauen, als
Skizze oder Screenshot vorlegen, Änderungsrunden abwarten, Freigabe
einholen — erst dann Punkt 5. Einzelheiten im Skill `neo-design`,
`references/entwurfsverfahren.md`.

Bei großen Aufgaben zuerst einen Prüf- und Umsetzungsplan als Markdown
schreiben: Reihenfolge, betroffene Bereiche, benötigte Dokumentationen,
mögliche Live-Tests, fehlende Zugangsdaten, nur theoretisch prüfbare
Bereiche, Risiken. Erst danach mit der Arbeit beginnen.

## 2. Technologie-Entscheidungen

- Keine freie Entscheidung über Technologieeinsatz, Pakete, Datenformate
  oder schwer Umkehrbares. Immer mehrere Optionen vorlegen: je Option
  Vorteile, Nachteile, Risiken, Wartungsaufwand — dazu eine begründete
  Empfehlung. Die Entscheidung fällt ausnahmslos der Projektinhaber.
- Jede tragende Entscheidung bekommt eine Entscheidungsakte (ADR) VOR der
  Umsetzung, im Format des jeweiligen Projekts.
- Neue Bibliothek oder neues Framework: zuerst prüfen, ob der bestehende
  Stack das Problem löst. Ein Neuzugang braucht Entscheidungsakte und
  Freigabe; erst dann Installation, Registereintrag und (wo vorhanden)
  Wächter-Test — im selben Commit.
- Bestehende Endpoints, Services und Komponenten bevorzugen. Neues nur,
  wenn das Bestehende den Ablauf nachweislich nicht tragen kann.

## 3. Belegpflicht — keine Annahmen

- Keine Annahmen, keine Spekulationen. Zulässige Quellen: offizieller
  Quellcode, offizielle Dokumentation, offizielle APIs und SDKs. Fehlt
  eine Information: dokumentieren und nachfragen, nie raten.
- **Fremde Schnittstellen:** jede Integration gegen die offizielle
  Dokumentation prüfen. Maschinenlesbare Verträge (OpenAPI, Postman,
  llms.txt) haben Vorrang vor Prosa-Anleitungen. Referenzmaterial je
  Integration im Repo ablegen und in der Regeldatei verlinken.
- Ist die Dokumentation einer fremden API nicht öffentlich verfügbar:
  genaue Unterlagen vom Anbieter oder Inhaber anfordern, bevor gebaut
  wird. Unsicheres Anbieterverhalten im Code-Kommentar und in der Doku
  festhalten statt eine Annahme zu implementieren.
- **MCP-Rollen trennen:** Prüfen, ob für die Technologie oder API ein
  MCP-Server verfügbar ist. Dokumentations-MCPs (z. B. einer UI-Library)
  VOR der Implementierung konsultieren — exakte Props, Parameter und
  Beispiele nachschlagen statt raten. Aktions-MCPs (Produktivsysteme)
  sind Werkzeuge für Laufzeit-Aktionen, keine Dokumentationsquelle.
  MCP-Zugangsdaten nie in Konfigurationsdateien ablegen.
- Für verteilte Systeme gilt eine „Nie annehmen"-Liste: kein gemeinsamer
  Host, kein localhost zwischen Diensten, kein gemeinsames Dateisystem,
  kein direkter Datenbankzugriff vom Frontend, keine fixe Topologie —
  alles läuft über definierte Schnittstellen.

## 4. Selbstkontrolle und Auswirkungsanalyse

- Nach jeder Änderung den eigenen Code noch einmal lesen und gegen den
  freigegebenen Umfang prüfen, BEVOR der nächste Schritt beginnt.
- Auswirkungsanalyse ist Pflicht: benennen, welche anderen Programmteile,
  Verträge, Tests, Dokumente und Betriebsaspekte betroffen sind —
  einschließlich Sicherheits- und Betriebs-Auswirkung.
- **Logs zuerst, dann Hypothese.** Beim Debugging vor jeder
  Ursachentheorie die Laufzeit-Logs lesen; sichtbare Fehlermeldungen
  sofort im Code verfolgen, nie als Nebeneffekt abtun.
- Nie behaupten „das wird es beheben", solange nicht: das Log den exakten
  Fehlerweg bestätigt, der Fix genau diesen Weg adressiert und der Nutzer
  das Ergebnis verifiziert hat. Bei Unsicherheit die Aussage als
  Vermutung kennzeichnen und Belege anfordern.
- **Grüne Tests sind keine Laufzeitverifikation.** Kann eine Änderung
  Laufzeitverhalten, Startvorgang, Migrationen, Routing, Auth oder extern
  sichtbares Verhalten berühren: das tatsächlich ausgelieferte Verhalten
  prüfen (Neustart, Build, Probelauf) — nicht nur die Tests.
- Feste Validierungsreihenfolge nach substanziellen Änderungen:
  Abhängigkeiten installieren → Lint/Analyse → Tests → Build. Rote Tests
  und Analysefehler sind Blocker.

## 5. Qualität

- Kein Quick-and-Dirty, kein „läuft erstmal", keine Workarounds, die
  Ursachen verstecken, kein Copy-Paste ohne vollständiges Verstehen.
- Keine TODOs im committeten Code — offene Punkte werden Issues oder
  stehen im Plan-Ordner.
- Bestehende Muster zuerst studieren und exakt fortsetzen. Definiert ein
  bestehender Screen oder ein bestehendes Modul das Muster schon: das
  Muster übernehmen statt eine lokale Variante zu erfinden.
- Saubere Codestruktur ist Pflicht: klare Modul- und Schichtgrenzen mit
  festgelegten Importrichtungen, eine Verantwortung pro Einheit,
  konsistente Benennung und Ablage nach den Mustern des Projekts, keine
  toten oder auskommentierten Pfade.
- Eskalationsregel: harte Sicherheitslücken sofort beheben und
  unverzüglich melden; jede andere ungefragte „Verbesserung" braucht
  vorher eine Rückfrage.
- Veraltete Werkzeuge und Abhängigkeiten erkennen und Updates auf die
  neueste stabile Version vorschlagen; eingespielt wird nach Freigabe —
  klein, nachvollziehbar und getestet (Skill `neo-sicherheit`,
  Lieferkette).

## 6. Tests

- Tests sind Pflicht für neue Funktionen, Bugfixes und geänderte Logik.
  Kein Abschluss ohne Abdeckung.
- **Oberflächen-Funktionstests (UI-Tests):** jedes Bedienelement — jeder
  Knopf, Schalter, Menüpunkt, jede Dialogaktion — hat einen Test, der
  die Bedienung auslöst und das beobachtbare Ergebnis prüft (Flutter:
  Widget-/Integrationstests; Web: Component-/E2E-Tests). Ein
  Bedienelement ohne solchen Test gilt als ungetestet, auch wenn die
  dahinterliegende Logik getestet ist.
- Keine fake-grünen Tests: Nur-Statuscode-Prüfungen reichen nicht —
  Struktur und Bedeutung der Antwort prüfen. Mutierende Operationen
  prüfen die beobachtbare Zustandsänderung.
- Für jeden real aufgetretenen Fehler existiert ein Regressionstest,
  bevor er als erledigt gilt.
- Externe Anbieter in Tests faken; keine Abhängigkeit von interaktiven
  Anmeldungen in der CI. Mock- und Demo-Schichten mitpflegen: jede neue
  Schnittstellenfunktion braucht ihre Mock-Entsprechung.
- Testdaten isolieren oder aufräumen.

## 7. Git und Commits

- Vor jedem Commit: Tests laufen lassen, deutsche Texte auf echte Umlaute
  prüfen (kein ue/ae/oe/ss), keine Secrets, keine TODOs, keine
  temporären Dateien, keine leeren Ordner nach Refactorings.
- **Die Commit-Nachricht selbst ist ein deutscher Text.** Sie trägt echte
  Umlaute, keine Ersatzschreibung — ebenso Titel und Text eines Pull
  Requests. Ein Dateiname oder ein Slug in der Nachricht bleibt
  ASCII (`references/loeschkonzept.md`), der Fließtext daneben nicht.
- Ein abgeschlossener, freigegebener Schritt = ein sauberes Commit-Paket.
  Querschnitts-Refactorings nie auf einem unfertigen Feature-Branch.
- Committen und pushen nur, wenn der Projektinhaber es verlangt oder das
  Projekt es so festlegt.
- **Nie direkt auf `dev` oder `main` pushen.** Beide Zweige nehmen
  Änderungen ausschließlich über einen Pull Request entgegen.
  Arbeitszweige gehen von `dev` aus, `main` nimmt ausschließlich Merges
  aus `dev`. Zweigmodell, Schutzregeln, Pflichtprüfungen und Ausrollung:
  Skill `neo-deployment`.

## 8. Projektstart

Was ein neues Repository am ersten Tag mitbringt — Gerüst, Werkzeuge,
Zweige, Betrieb, Recht — steht in `references/projektstart.md`. Was dort
am ersten Tag fehlt, fehlt in zwei Jahren immer noch. Der Befehl
`/neo-grundregeln:neo-projektstart` prüft ein bestehendes Repository
dagegen und berichtet den Fehlbestand.

Zugehörige Skills: `neo-design` (Gestaltung, Bedienung,
Barrierefreiheit), `neo-komponenten` (Wrapper-Komponenten),
`neo-doku` (Dokumentation), `neo-deployment` (Zweige, Auslieferung),
`neo-contao` (Contao-Websites), `neo-betrieb` (Sicherung, Notfall,
Umzug), `neo-ki` (KI im Produkt), `neo-recht` (Pflichtseiten,
Löschkonzept), `neo-api` (Schnittstellen), `neo-code` (Codeaufbau),
`neo-sicherheit` (Sicherheit, Release, riskante Umbauten).
