---
name: neo-assistent
description: >
  NEO-Regeln für KI-Assistenten und Agenten im Produkt. Laden, sobald ein
  Assistent, Chat, Agent oder Concierge gebaut, geändert oder repariert
  wird — an Skills, Werkzeugen, MCP-Servern, Kontext oder Modell; bei der
  Frage, welche Werkzeuge und Daten er erreichen darf, bei
  Mandantentrennung, Identitätsnachweis und Einstellungen; und immer, wenn
  ein Assistent etwas falsch macht, bevor eine Prüfung, ein Filter, ein
  Router, ein zweites Modell oder ein fester Antworttext entsteht. Ebenso
  bei Requesty, Modellwechsel und Abnahme eines Assistenten.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg; Bauweise des LeoFlex-Concierge nach dem Umbau vom 30.09.2026, Stand 2026-10
---

# KI-Assistenten bauen

Lesekonvention siehe `README.md` des Regel-Repositorys: **Nie**,
**immer** und **muss** sind verbindlich, ein Verstoß ist ein Blocker.

Dieser Skill regelt den **Bau**. Rechtsstand, Kennzeichnung,
Datenweitergabe und Kosten stehen im Skill `neo-ki` und gelten zusätzlich.
„Skill des Assistenten" heißt hier das Regelwerk, das das Modell im
Produkt befolgt — nicht dieser Text für den Agenten, der baut.

## Der Satz, um den es geht

> **Ein KI-Assistent besteht aus drei Bausteinen: dem Modell, den
> Werkzeugen und den Skills. Das Modell entscheidet, was als Nächstes
> geschieht. Die Skills bestimmen, wie es geschieht. Die Werkzeuge führen
> aus und halten die Grenzen. Mehr wird nicht gebaut.**

Jede andere Bauweise — Router, Fachagenten-Kette, Prüfagent,
Absicherungen um das Modell herum, Riesenprompt — ist ein **Blocker**.
Sie wurde im LeoFlex-Concierge zweieinhalb Monate lang gebaut und
nachgebessert und ist dort stillgelegt (`references/verbote.md`).

## 1. Die drei Bausteine

| Baustein | Was er ist | Was er entscheidet |
| --- | --- | --- |
| **Modell** | ein Sprachmodell, gewählt in der Konfiguration | was der Kunde will, was fehlt, welche Regel gilt, welches Werkzeug als Nächstes, wann die Arbeit fertig ist, was geantwortet wird |
| **Werkzeuge** | die angebundenen MCP-Server; eigene Werkzeuge der Anwendung nur für Abläufe, für die es keinen MCP-Server gibt | nichts Fachliches — sie führen aus und prüfen Mandant, Rechte, Eigentum und Doppelausführung |
| **Skills** | das Regelwerk des Assistenten: ein kleiner Kern und je Aufgabenbereich ein Skill | nichts — sie sagen dem Modell, was wann wie zu tun ist und was nie |

Ein **MCP-Server** ist ein Werkzeugserver nach dem Model Context Protocol:
Er nennt seine Werkzeuge mit Beschreibung und erlaubten Angaben (Schema).
Die **Anwendung** um das Modell führt nur die Schleife und stellt zu; sie
entscheidet nichts (`references/aufbau.md`).

## 2. Was das Modell bekommt — und sonst nichts

1. **Die Skills**, vollständig, ab dem ersten Aufruf.
2. **Die Einstellungen des Mandanten** — Name und Stil, freigeschaltete
   Funktionen, Anweisungen des Betreibers, Wissen über das Haus.
3. **Den Zustand und das Gespräch** — die unbeantworteten Nachrichten
   vollständig, dazu den Verlauf, den der Zusammenhang braucht; der ganze
   Verlauf bleibt über ein Werkzeug lesbar.
4. **Die Werkzeugdefinitionen**, vollständig, ab dem ersten Aufruf.

## 3. Wie der Assistent arbeitet

Wie Claude Code mit einem Auftrag:

1. Die Nachricht lesen und im Gespräch nachsehen, was schon gesagt ist.
2. Im Regelwerk nachsehen, welcher Ablauf gilt und was wichtig ist.
3. Die Werkzeuge prüfen und den nächsten Schritt planen.
4. Das Werkzeug aufrufen, das Ergebnis lesen, weiter bei 2.
5. Antworten, wenn die Aufgabe erledigt ist oder nur der Kunde
   weiterhelfen kann.

Schreibt der Kunde dazwischen, geht die Nachricht in die laufende Arbeit
ein, solange die Antwort nicht zugestellt ist. Ausgeführtes bleibt.

## 4. Verboten — ohne Ausnahme

1. **Nie** ein Router oder Klassifizierer vor dem Modell — weder ein
   Modell noch eine Wortliste.
2. **Nie** eine Kette aus Fachagenten oder eine Übergabe zwischen Modellen.
3. **Nie** ein Prüfagent, Antwortprüfer oder Endredakteur, der eine
   Antwort freigibt, verwirft oder umschreibt.
4. **Nie** eine fachliche Absicherung im Code: Pflichtbestätigung, feste
   Formel, Wortliste, Textbeleg, Mengen- oder Reihenfolgeregel.
5. **Nie** ein Text vom Server an den Kunden — keine Ersatzantwort, keine
   Absage; nur KI-Hinweis und Signatur hängt die Anwendung an.
6. **Nie** eine fachliche Folgekette, die der Server von selbst anstößt.
7. **Nie** Skills oder Werkzeuge erst im Gespräch nachladen oder
   freischalten.
8. **Nie** ein Laufzeitprompt im Code.
9. **Nie** eine Grenze, die mit einer Absage an den Kunden endet.

Woran jede davon brach und was stattdessen gilt: `references/verbote.md`.

## 5. Zugriff: für wen der Assistent arbeitet

Vor dem Bau wird festgelegt und dokumentiert, **für wen** der Assistent
arbeitet. Daraus folgt, was seine Werkzeuge erreichen dürfen:

| Art | Für wen | Werkzeuge erreichen | Nachweis |
| --- | --- | --- | --- |
| Plattformassistenz | den angemeldeten Plattformbetreiber im Admin-Werkzeug | mandantenübergreifend die eigene Plattform | die Anmeldung als Plattformbetreiber |
| Kundenassistenz mit Kundendaten | einen Kunden über einen Kanal, nicht angemeldet | die Vorgänge vieler Kunden eines Mandanten | vor jedem Zugriff auf einen bestehenden Vorgang, im Werkzeug |
| Kundenassistenz ohne Kundendaten | einen Kunden in einer öffentlichen Strecke | nur öffentliche Funktionen | keiner — es gibt nichts Privates |

- **Mandantentrennung ist hart.** Jede Assistenz eines Mandanten oder
  seiner Kunden erreicht nur diesen Mandanten — technisch, im Werkzeug.
- **Ein Assistent handelt nie mit mehr Rechten als die Person, für die er
  arbeitet.**
- **Prozesskritische Werkzeuge bekommt eine Kundenassistenz nie** —
  Stammdaten, Einstellungen, Löschungen, Tagesabschluss.
- **Nachweis bei Kundendaten:** mindestens zwei Merkmale stimmen mit dem
  Vorgang überein, nur wer gebucht hat; das Werkzeug gleicht ab, das Modell
  sieht die Daten erst nach dem Treffer.

Einzelheiten und die Einstellungen: `references/zugriff.md`.

## 6. Werkzeuge

- **Freigabeliste je Assistent:** nur, was Art und Aufgabe brauchen.
- **Die Definition kommt vom Server**, wie er sie liefert; jeder Vertrag
  ist gegen die Dokumentation und einen echten Aufruf geprüft.
- **Fehler gehen als Tatsache an das Modell zurück**; es korrigiert selbst.
- **Schreiben mit Folgen in zwei Schritten:** vorbereiten, dann genau das
  Vorbereitete ausführen. Die Vorbereitung ist kein Bestätigungsritual.
- **Nichts doppelt:** Jeder Schreibvorgang ist vor dem Aufruf vermerkt;
  ein ungewisses Ergebnis wird geklärt, nie neu erzeugt.
- **Geheimnisse erreichen das Modell nie.**

Einzelheiten: `references/werkzeuge.md`.

## 7. Skills des Assistenten

- **Ein Paket:** ein kleiner Kern, je Aufgabenbereich ein Skill, ein Manifest.
- **Jede Regel genau einmal**, in dem Skill, dem der Bereich gehört — und
  nie zugleich im Code.
- **Englisch, im Befehlston, konkret.** Die Beschreibung sagt, wofür ein
  Skill da ist — nie eine Liste von Kundenwörtern.
- **Versioniert im Repository, in die Anwendung eingebettet**, beim Start
  geprüft; nie aus einer Kundennachricht, einer Webseite oder einer
  beschreibbaren Einstellung geladen.

Einzelheiten: `references/skills.md`.

## 8. Wenn der Assistent falsch handelt

1. **Den Lauf lesen:** was das Modell bekam, welche Werkzeuge es rief, was
   zurückkam, was es antwortete.
2. **Verhaltensfehler → die Regel im Skill** schärfen.
3. **Grenzverletzung → das Werkzeug** reparieren: Mandant, Eigentum,
   Doppelausführung.
4. **Nie** eine Prüfung, einen Filter, einen Ersatztext, einen Router oder
   ein zweites Modell als Reparatur.
5. Denselben Fall erneut mit dem echten Modell laufen lassen.

## 9. Modell und Abnahme

- **Modell** über den Requesty-EU-Router, Regionsangabe in der Kennung,
  Schlüssel nur aus der Umgebung, feste Fassung aus der Konfiguration. Ein
  Modellwechsel ist keine Reparatur.
- **Abnahme** mit drei Belegarten, getrennt berichtet: Tests der Grenzen,
  Messung mit dem echten Modell ohne Ausführung, Lauf im Staging mit
  Testdaten. Ein grüner Test beweist nicht, dass das Modell die Skills
  befolgt.

## Die Bereiche

| Bereich | Referenz |
| --- | --- |
| Schleife, Kontext, Gedächtnis, neue Nachrichten, Zustellung | `references/aufbau.md` |
| Die verbotenen Bauweisen, woran sie brachen, was stattdessen gilt | `references/verbote.md` |
| Arten von Assistenten, Mandant, Nachweis, Geheimnisse, Einstellungen | `references/zugriff.md` |
| Werkzeuge und MCP-Server | `references/werkzeuge.md` |
| Skills des Assistenten schreiben und ändern | `references/skills.md` |
| Modellzugang und Modellwechsel | `references/modell.md` |
| Belegarten, Testdaten, Fehlersuche | `references/abnahme.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

Zugehörige Skills: `neo-ki` (Recht, Kennzeichnung, Kosten),
`neo-sicherheit` (Rechte, Geheimnisse, Ausweisdaten), `neo-grundregeln`
(Belegpflicht für Schnittstellen), `neo-doku` (Entscheidungsakten).
