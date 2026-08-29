---
name: neo-grundregeln
description: >
  Verbindliche NEO-Arbeitsregeln für jede nicht-triviale
  Entwicklungsaufgabe: Prozess vor jeder Änderung (analysieren,
  begründen, Freigabe abwarten), Technologie-Entscheidungen mit Optionen
  statt Alleingang, Belegpflicht statt Annahmen, Umgang mit fremden APIs
  und MCP, Selbstkontrolle und Auswirkungsanalyse, Debugging mit Logs
  vor Hypothese, Testpflichten einschließlich Oberflächen-Funktionstests,
  Git-Hygiene und Commit-Nachrichten, kein Direkt-Push auf dev oder main,
  Projektstart-Gerüst. Diesen Skill laden, bevor ein Feature, ein Bugfix,
  ein Refactoring oder eine Integration begonnen wird.
metadata:
  herkunft: NEO Digital — destilliert aus NEOcash- und LeoFlex-Regelwerken, Stand 2026-08
---

# NEO-Grundregeln

Es gelten **Produktionsstandards, keine Prototyp-Standards**. Leitsatz
der NEO-Regelwerke: „Sauberer als sauber. Besser als gut. Sicherer als
sicher." Das gilt für Code, Architektur, Design und die Arbeitsweise —
auch beim Debugging.

**Es gibt kein Zeitlimit-Argument.** Langsam, systematisch und sorgfältig
arbeiten. Wer Geschwindigkeit gegen Korrektheit tauscht, hat die Regel
verletzt, nicht abgekürzt.

## Wie diese Regeln zu lesen sind

| Wort | Bedeutung |
| --- | --- |
| **Nie**, **immer**, **muss** | Verbindlich. Ein Verstoß ist ein **Blocker**: die Arbeit gilt als nicht fertig, ein Merge wird zurückgewiesen. |
| **Ausnahme** | Nur mit ausdrücklicher Freigabe des Projektinhabers, festgehalten an der betroffenen Stelle mit Grund und Datum. **Ohne Vermerk gibt es keine Ausnahme**, auch wenn sie mündlich erteilt wurde. |
| **Sollte** | Begründet abweichbar. Die Abweichung wird gemeldet, nicht stillschweigend genommen. |

Diese Konvention gilt in allen Referenzdateien dieses Skills.

## Die sieben Sätze, die alles tragen

1. **Die Entscheidung fällt ausnahmslos der Projektinhaber.** Der Agent
   legt Optionen vor und empfiehlt. Er entscheidet nicht.
2. **Keine Änderung ohne vorherige Freigabe.** Einzige Ausnahme: eine
   harte Sicherheitslücke — sofort beheben, unverzüglich melden.
3. **Keine Annahme, keine Spekulation.** Jede Feststellung ist belegt
   oder wird als Vermutung gekennzeichnet.
4. **Nichts erfinden.** Kein Text, keine Zusage, keine Zahl, die niemand
   verlangt hat — und **kein Test zu einer selbst erfundenen
   Anforderung** (`references/tests.md`).
5. **Eine neue Nachricht bricht die laufende Aufgabe nicht ab.** Sie wird
   ein Punkt auf der Auftragsliste. Kein Punkt verfällt, und eine
   Anweisung gilt erst als erledigt, wenn sie ausgeführt und belegt ist
   (`references/auftragsliste.md`).
6. **Grüne Tests sind kein Beweis.** Was Laufzeit berührt, wird zur
   Laufzeit geprüft.
7. **Rote Tests sind Blocker, nie Folgeaufgaben.**

## Der Prozess in Kürze

Verbindliche Reihenfolge. Kein Schritt wird übersprungen, keiner
getauscht:

```
1 Analysieren        was wird gebaut, was ausdrücklich nicht
2 Abhängigkeiten     was kann die Änderung treffen
3 Begründen          jede Feststellung mit Quelle, Risiken benannt
4 Zusammenfassen     und die Freigabe ABWARTEN
  ── bei Oberflächen davor: Entwurf vorlegen und freigeben lassen
5 Umsetzen           nur den freigegebenen Umfang
6 Testen             neue Tests für neues Verhalten, rote Tests beheben
7 Nachbarn prüfen    die unter 2 gefundenen Abhängigkeiten
8 Dokumentieren      im selben Schritt
9 Fertigmelden       ehrlich: was offen blieb, was rot ist
```

**„Leg los" hebt Schritt 4 nicht auf.** Auch dann wird erst
zusammengefasst und die Bestätigung abgewartet.

Einzelheiten, was eine Freigabe ist und was nicht, und was ein
Umsetzungsplan enthält: `references/prozess.md`.

## Technologie-Entscheidungen

- **Keine freie Entscheidung** über Technologieeinsatz, Pakete,
  Datenformate oder schwer Umkehrbares.
- **Immer mehrere Optionen** vorlegen: je Option Vorteile, Nachteile,
  Risiken, Wartungsaufwand — dazu eine begründete Empfehlung.
- Jede tragende Entscheidung bekommt eine **Entscheidungsakte (ADR) vor
  der Umsetzung** (Skill `neo-doku`, `references/entscheidungsakten.md`).
- Neue Bibliothek: zuerst prüfen, ob der bestehende Stack das Problem
  löst. Ein Neuzugang braucht Entscheidungsakte und Freigabe; erst dann
  Installation, Registereintrag und Wächter-Test — im selben Commit.
- **Bestehende Endpoints, Dienste und Komponenten haben Vorrang.** Neues
  nur, wenn das Bestehende den Ablauf nachweislich nicht trägt.

## Qualität

- Kein Quick-and-Dirty, kein „läuft erstmal", keine Workarounds, die
  Ursachen verstecken, **kein Copy-Paste ohne vollständiges Verstehen**.
- **Keine TODOs im committeten Code.** Offene Punkte werden Aufgaben
  oder stehen im Plan-Ordner.
- **Bestehende Muster zuerst studieren und exakt fortsetzen.** Definiert
  ein bestehender Screen oder ein bestehendes Modul das Muster schon,
  wird es übernommen — keine lokale Variante.
- Saubere Codestruktur nach den offiziellen Vorgaben des Stacks
  (Skill `neo-code`): klare Schichtgrenzen mit festgelegter
  Importrichtung, eine Verantwortung je Einheit, keine toten oder
  auskommentierten Pfade.
- **Eskalationsregel:** harte Sicherheitslücken sofort beheben und
  unverzüglich melden; **jede andere ungefragte „Verbesserung"** —
  Refactoring, Umbenennung, Stiländerung — braucht vorher eine Rückfrage.
- Veraltete Werkzeuge erkennen und Updates vorschlagen; eingespielt wird
  nach Freigabe, klein und getestet (Skill `neo-sicherheit`).

## Die Bereiche

| Bereich | Referenz |
| --- | --- |
| Die Auftragsliste: Punkte bilden, abarbeiten, belegen | `references/auftragsliste.md` |
| Werkzeug `scripts/rules-update.py`: hält die Regel-Plugins auf dem Stand des Marktplatzes, läuft aus dem SessionStart-Hook | — |
| Der Prozess im Detail, was Freigabe heißt, der Umsetzungsplan | `references/prozess.md` |
| Belegpflicht, Quellen, fremde APIs, MCP-Rollen, verteilte Systeme | `references/belegpflicht.md` |
| Selbstkontrolle, Auswirkungsanalyse, Debugging, Laufzeitverifikation | `references/selbstkontrolle.md` |
| Tests: Arten, Oberflächen-Funktionstests, fake-grüne Tests, Mocks | `references/tests.md` |
| Git, Commits, Zweigmodelle, `.gitignore`, Hygiene | `references/git.md` |
| Zielgruppe je Bereich, die drei Sprachstufen, die Wortliste | `references/zielgruppe.md` |
| Altlasten: was liegen bleibt, was geht, was bleiben muss | `references/altlasten.md` |
| Werkzeug `scripts/repo-hygiene.py`: findet Geheimnisse, Reste, nirgends Erwähntes und liegen gebliebene Planungen | — |
| Was ein neues Repository am ersten Tag mitbringt | `references/projektstart.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

## Befehle

- `/neo-grundregeln:neo-selbstkontrolle` — den aktuellen Arbeitsstand
  gegen diese Regeln prüfen und berichten.
- `/neo-grundregeln:neo-projektstart` — ein Repository gegen die
  Projektstartliste prüfen und den Fehlbestand berichten.

Zugehörige Skills: `neo-design` (Gestaltung, Bedienung,
Barrierefreiheit), `neo-komponenten` (Wrapper-Komponenten), `neo-doku`
(Dokumentation), `neo-deployment` (Zweige, Auslieferung), `neo-contao`
(Contao-Websites), `neo-betrieb` (Sicherung, Notfall, Umzug), `neo-ki`
(KI im Produkt), `neo-recht` (Pflichtseiten, Löschkonzept), `neo-api`
(Schnittstellen), `neo-code` (Codeaufbau), `neo-sicherheit` (Sicherheit,
Release, riskante Umbauten).
