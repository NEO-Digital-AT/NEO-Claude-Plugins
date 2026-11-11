# Skills des Assistenten

Lesekonvention siehe `SKILL.md`.

> **Die Skills sind das ganze Regelwerk des Assistenten:** was er tun muss,
> wann und wie — und was nie. Was in keinem Skill steht, gilt für ihn nicht.

## Das Paket

```
skills/<assistent>/
  manifest.json          Verzeichnis: Kennung, Fassung, Abhängigkeiten, genutzte Werkzeuge
  core/SKILL.md          der Kern — gilt in jedem Schritt
  <bereich>/SKILL.md     je Fachbereich ein kleiner Skill
```

| Teil | Inhalt | Umfang |
| --- | --- | --- |
| **Kern** | wer der Assistent ist (aus den Einstellungen), Sprache des Kunden, Wahrheit, Zustimmung, Form der Antwort, Vorrang der Anweisungen, Umgang mit Fehlern und Grenzen, Übergabe, wie Skills und Werkzeuge geladen werden | streng und klein — er steht in jedem Aufruf |
| **Aufgaben-Skill** | ein Fachbereich: was der Kunde meint, die Standardabläufe, woher die Informationen kommen, was nie, wann das Team übernimmt | höchstens 2.800 Zeichen; wird er größer, wird er geteilt |
| **Manifest** | je Skill Kennung, Fassung, Zweck, Abhängigkeiten, genutzte Werkzeuge, betroffene Datenarten | keine Regeltexte |

Jeder Skill beginnt mit `name` und `description`. **Die Beschreibung sagt,
wann der Skill geladen wird** — sie steht im Katalog und ist alles, was das
Modell vor dem Laden von ihm sieht. Nie eine Liste von Wörtern, die ein
Kunde schreiben könnte.

## Wofür es einen Skill gibt

> **Je Fachbereich ein kleiner Skill** — Buchen, Zahlen, Stornieren,
> Rechnung, Nachweis, Wissen. Lieber mehr kleine als wenige große
> (Projektinhaber, 15.10.2026: „kürzer und dafür mehr Skills ist besser als
> weniger und dafür große Skills“).

- **Ein Skill übersetzt, was der Kunde schreibt**, beschreibt die
  Standardabläufe und sagt, woher das Modell die Informationen nimmt: aus
  dem Wissen, dem Fachsystem, der freigegebenen Website.
- **Standardfälle stehen im Skill, Sonderfälle gehen an das Team.** Ein
  Betrieb beschreibt eigene Abläufe in seinen Anweisungen.
- **Skills sperren nur, was gefährlich ist:** Daten, die der Kunde nicht
  sehen darf, und Handlungen, die nur der Betreiber darf (Projektinhaber,
  10.10.2026). Alles andere ist erlaubt.
- **Der Kern verbietet das Erfinden.** Gesagt wird nur, was ein
  Werkzeugergebnis, das Wissen oder das Gespräch belegt und nichts
  widerlegt. Ein Angebot, eine Leistung oder eine Möglichkeit — etwa ein
  Zimmer für wenige Stunden — wird erst genannt, wenn ein Werkzeug sie
  bestätigt hat.

## Form: kurz und streng

Ein Aufgaben-Skill besteht aus den Teilen, die sein Bereich braucht, je
als Liste mit einer Aussage pro Zeile. Üblich sind:

```
PURPOSE    ein Satz: wofür der Skill da ist
TOOLS      Werkzeugname — wann es gebraucht wird
STEPS      die Schritte des Ablaufs, nummeriert
NEVER      was nie geschieht
HANDOVER   wann das Team übernimmt — immer mit Nachricht an den Kunden
```

Ein Bereich kann eigene Teile brauchen, etwa PROOF und SCOPE beim
Nachweis.

- **Keine Begründungsprosa, keine Vorgeschichte.** Warum eine Regel gilt,
  steht in der Entscheidungsakte, nicht im Skill.
- **Was das Werkzeug erzwingt, beschreibt der Skill nicht nach.** Er sagt,
  welches Werkzeug mit welchen Angaben aufgerufen wird. Mandant, Nachweis,
  Eigentum und Doppelausführung prüft das Werkzeug, und dessen Fehler sagt
  dem Modell, was fehlt.
- **Die Längengrenze wird beim Start gemessen:** höchstens 2.800 Zeichen
  je Aufgaben-Skill, sonst wird ein Teil nicht mehr beachtet. Der Kern
  bleibt klein.

## Wie ein Skill geschrieben wird

- **Englisch** (Kernregel 16): Skills sind Systemtext für das Modell,
  keine Oberfläche.
- **Im Befehlston, konkret, ohne Begründungsprosa.** „Fetch offers before
  collecting personal data." — nicht „Es wäre sinnvoll, zuerst …".
- **Werkzeugnamen genau so, wie sie definiert sind.** Ein Name, den es
  nicht gibt, lässt die Prüfung des Pakets scheitern.
- **Was nie geschieht, steht ausdrücklich da:** erfundene Preise,
  Verfügbarkeiten, Verweise, Kontaktdaten, Nummern, erledigte Handlungen.
- **Zustimmung wird in jeder Sprache verstanden.** Kein Satz, den der
  Kunde tippen muss, keine feste Formel. Eine Zustimmung zu einer
  unveränderten Zusammenfassung wird nicht noch einmal abgefragt.
- **Zustände werden unterschieden:** angefragt, vorbereitet, ausgeführt,
  ungewiss, zugestellt. Unfertiges wird nie als erledigt beschrieben.

## Jede Regel genau einmal

- **Eine Regel steht in dem Skill, dem der Bereich gehört.** Braucht ein
  anderer Skill sie, nennt er die Abhängigkeit im Manifest; er kopiert sie
  nicht.
- **Eine Regel steht nicht zugleich im Code.** Was im Skill steht, prüft
  kein Code nach. Was technisch ist — Mandant, Rechte, Eigentum,
  Doppelausführung —, steht im Werkzeug und nicht als Bitte im Skill.
- **Der Skill enthält die Standards, die Einstellungen die Ausnahmen.** Die
  Anweisung des Betreibers geht dem Standard im Skill vor (`zugriff.md`).

## Katalog zuerst, Inhalte auf Abruf

- **Ab dem ersten Schritt stehen der Kern und der Katalog im Kontext:** je
  Skill die Kennung und ein Satz, je Werkzeug der Name und ein Satz.
- **Das Modell lädt einen Skill selbst** (`load_module`), bevor es in
  dessen Bereich handelt; die Abhängigkeiten aus dem Manifest und die
  Werkzeuge des Skills kommen mit. Eine einzelne Werkzeugdefinition lädt
  es mit `load_tools`. Keine Vorstufe wählt für das Modell aus.
- **Geladenes bleibt für den Lauf.** Nichts wird entladen oder ersetzt. Die
  Anwendung fügt die Skills offener Vorgänge selbst hinzu, etwa einer
  vorbereiteten Buchung.
- **Die Größe wird gemessen**, je Skill und für Kern und Katalog. Ein
  Skill, der zu lang wird, wird geteilt — nicht gekürzt, bis eine Regel
  fehlt. Nichts wird still weggelassen.

## Woher das Paket kommt

- **Im Repository, versioniert, als Dateien** — nicht als Zeichenkette im
  Code, nicht in einer beschreibbaren Ablage.
- **Produkte, die der Kunde selbst einrichtet,** dürfen zusätzlich Skills
  aus Quellen wie GitHub installieren (Projektinhaber, 08.11.2026). Beim
  Installieren wird eine feste Fassung abgelegt und wie unten geprüft; zur
  Laufzeit wird nichts aus dem Netz geladen; aktualisiert wird nur durch
  den Administrator, mit Anzeige der Änderungen. Mitgelieferte Skills des
  Produkts sind eingebettet wie bei eigenen Assistenten.
- **In die Anwendung eingebettet und beim Start geprüft:** Fehlt eine
  Datei, ist ein Werkzeug oder eine Abhängigkeit unbekannt, gibt es einen
  Kreis in den Abhängigkeiten oder ist ein Skill zu groß, startet die
  Anwendung nicht mit diesem Paket.
- **Nie aus einer Kundennachricht, einer besuchten Webseite oder einem
  Anhang.** Die Anweisungen des Betreibers sind Einstellungen, keine
  Skills.
- **Ein Skill gewährt keine Rechte.** Ein Werkzeugname im Skill macht kein
  Werkzeug ausführbar.

## Ändern

1. **Den Skill ändern, dem der Bereich gehört** — nicht den Code.
2. **Die Fassung im Manifest heben.**
3. **Die Tests laufen lassen** (Belegart 1, `abnahme.md`).
4. **Den betroffenen Ablauf im Staging mit dem echten Modell
   durchspielen** (Belegart 2).

Eine neue Kombination bestehender Fähigkeiten braucht nur Skills und
Tests. Eine neue Fähigkeit braucht dazu ein Werkzeug, mit Vertrag, Rechten
und Tests — ein Satz im Skill erzeugt keine.
