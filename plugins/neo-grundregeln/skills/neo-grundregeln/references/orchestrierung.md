# Die Weiche und die Fachagenten

Lesekonvention siehe `SKILL.md`.

> **Ein Agent, der alle Regeln gleichzeitig tragen soll, trägt keine
> davon zuverlässig.**

Das ist kein Vorwurf an ein Modell, sondern eine Eigenschaft der Sache:
Je mehr Regeln in einem Kontext liegen, desto weniger Gewicht hat jede
einzelne. Man merkt es daran, dass eine neu geschärfte Regel greift und
gleichzeitig eine alte durchrutscht. Wer dann nachschärft, macht es
schlimmer — der Kontext wird länger, das Gewicht je Regel kleiner.

**Die Antwort ist nicht: weniger Regeln. Sie ist: weniger Regeln
gleichzeitig.**

## Wer was trägt

| Wer | Was er trägt | Wie viel |
| --- | --- | --- |
| **Die Weiche** (Hauptsitzung) | Kernregeln, Auftragsliste, Freigaben, Git, Weiterleitung | wenig, dafür immer |
| **Der Fachagent** | genau einen Skill, vollständig, mit seinen Referenzen | viel, dafür nur in seinem Fach |

Ein Fachagent hat ein **eigenes Kontextfenster**. Er erbt weder den
Gesprächsverlauf noch die Skills der Hauptsitzung; sein Skill wird beim
Start vollständig geladen (`skills:` in seiner Definition). Damit sind
seine Regeln nicht ein Zwanzigstel des Kontexts, sondern der Kontext.

## Was die Weiche tut — und was nicht

**Sie tut:**

- Die **Auftragsliste** führen (Kernregel 3) und die Punkte zuordnen.
- Den Auftrag so übergeben, dass er ohne Vorgeschichte verständlich ist:
  Ziel, Dateien, Randbedingungen, was schon entschieden wurde.
- **Rückfragen des Fachagenten an den Projektinhaber weiterreichen** —
  der Fachagent spricht nicht mit ihm.
- Ergebnisse zusammenführen, Widersprüche zwischen zwei Fächern
  auflösen, indem sie vorgelegt werden.
- Git: Zweig, Commit, Merge (Kernregeln 20 und 21).

**Sie tut nicht:**

- **Fachliche Arbeit selbst**, für die es einen Fachagenten gibt. Wer
  „schnell noch" eine Oberfläche baut, baut sie mit den Kernregeln
  statt mit `neo-design` — und das sind die falschen Regeln.
- Entscheiden. Das tut ausnahmslos der Projektinhaber (Kernregel 1).

## Die Weiche: welche Aufgabe an wen

| Aufgabe | Fachagent |
| --- | --- |
| Screen, Dialog, Formular, Tabelle, Farben, Zustände, Barrierefreiheit, responsive Ansicht, Oberflächentexte | `neo-design:oberflaeche` |
| Eine Komponente der Produktfamilie anlegen oder ändern, Wächter-Test | `neo-komponenten:komponenten` |
| Struktur, Benennung, Lesbarkeit, Refactoring | `neo-code:code` |
| Vue, Nuxt | `neo-vue:vue` |
| Angular | `neo-angular:angular` |
| PHP, Laravel, Symfony | `neo-php:php` |
| .NET, C# | `neo-dotnet:dotnet` |
| Flutter, native App, Geräte und Peripherie | `neo-mobil:mobil` |
| API, OpenAPI, Verträge, Fassungen | `neo-api:api` |
| Contao | `neo-contao:contao` |
| Eingabeprüfung, Rechte, Geheimnisse, Lücken | `neo-sicherheit:sicherheit` |
| Zweigmodell, Pull Requests, Workflows, Ausrollung | `neo-deployment:deployment` |
| Überwachung, Sicherungen, Störungen | `neo-betrieb:betrieb` |
| Dokumentation, Entscheidungsakten, Screenshots | `neo-doku:doku` |
| Impressum, Datenschutz, Barrierefreiheitserklärung | `neo-recht:recht` |
| Datenhaltung, Migrationen, KI-Modelle, Prompts, Kosten | `neo-ki:ki` |
| Assistent oder Agent im Produkt | `neo-assistent:assistent` |
| Sprache, Rahmenwerk, Anbieter wählen oder verwerfen | `neo-technologiewahl:technologiewahl` |

**Zwei Fächer in einer Aufgabe sind zwei Übergaben**, nacheinander, mit
einem Ergebnis dazwischen. Nicht ein Agent, der beides „mitmacht".

## Wie übergeben wird

- **Automatisch**: Die Beschreibung des Fachagenten entscheidet. Sie ist
  deshalb kein Titel, sondern eine Auslöserliste.
- **Ausdrücklich**: `@"oberflaeche (agent)"` — wenn es genau dieser sein
  muss.
- **Der Auftrag steht für sich.** Der Fachagent kennt das Gespräch
  nicht: Was er wissen muss, steht im Auftrag oder in der `CLAUDE.md`.

## Die Grenzen — damit niemand mehr erwartet, als es kann

- **Ein Fachagent kann nicht nachfragen.** Was eine Entscheidung
  braucht, gibt er zurück; die Weiche legt es vor.
- **Er sieht den Verlauf nicht.** Ein halber Auftrag wird ein halbes
  Ergebnis.
- **Er ersetzt die Regeln nicht, er konzentriert sie.** Ein schlechter
  Skill wird durch einen Fachagenten nicht besser.
- **Mehr Agenten sind nicht besser.** Ein Fach, das keine eigenen Regeln
  hat, braucht keinen eigenen Agenten.

## Wann die Aufteilung wieder geprüft wird

Wenn ein Skill so lang wird, dass sein Fachagent ihn nicht mehr
zuverlässig einhält, wird **der Skill geteilt**, nicht die Regel
gestrichen. Der Maßstab ist das Verhalten, nicht die Zeilenzahl: Eine
Regel, die nachweislich zweimal übergangen wurde, steht im falschen
Zusammenhang.

## Abnahme

- [ ] Jede Fachaufgabe lief über ihren Fachagenten, nicht über die
      Weiche.
- [ ] Der Auftrag war ohne Vorgeschichte verständlich.
- [ ] Rückfragen des Fachagenten wurden vorgelegt, nicht selbst
      beantwortet.
- [ ] Zwei Fächer waren zwei Übergaben.
- [ ] Die Fertigmeldung nennt, welcher Agent was gemacht hat.
