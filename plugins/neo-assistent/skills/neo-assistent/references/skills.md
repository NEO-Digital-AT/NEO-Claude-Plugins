# Skills des Assistenten

Lesekonvention siehe `SKILL.md`.

> **Die Skills sind das ganze Regelwerk des Assistenten:** was er tun muss,
> wann und wie — und was nie. Was in keinem Skill steht, gilt für ihn nicht.

## Das Paket

```
skills/<assistent>/
  manifest.json          Verzeichnis: Kennung, Fassung, Abhängigkeiten, genutzte Werkzeuge
  core/SKILL.md          der Kern — gilt in jedem Schritt
  <aufgabe>/SKILL.md     je Aufgabenbereich ein Skill
```

| Teil | Inhalt | Umfang |
| --- | --- | --- |
| **Kern** | wer der Assistent ist (aus den Einstellungen), Sprache des Kunden, Wahrheit, Zustimmung, Form der Antwort, Vorrang der Anweisungen, Umgang mit Fehlern und Grenzen, Übergabe | streng und klein — er steht in jedem Aufruf |
| **Aufgaben-Skill** | ein komplexer Ablauf mit Folgen: Zweck, Werkzeuge, Schritte, was nie, wann das Team übernimmt | kurz; wird er größer, wird er geteilt |
| **Manifest** | je Skill Kennung, Fassung, Zweck, Abhängigkeiten, genutzte Werkzeuge, betroffene Datenarten | keine Regeltexte |

Jeder Skill beginnt mit `name` und `description`. **Die Beschreibung sagt,
wofür der Skill da ist** — nie eine Liste von Wörtern, die ein Kunde
schreiben könnte.

## Wofür es einen Skill gibt

> **Einen Skill gibt es nur für einen Ablauf, der komplex ist und Folgen
> hat** — Buchen, Zahlen, Stornieren, eine Rechnung, eine Änderung am
> Vorgang. Für eine Information braucht es keinen.

- **Informationsfragen beantwortet das Modell mit Kern und Werkzeugen.**
  Es sucht selbst: im Wissen, im Fachsystem, auf der freigegebenen Website.
- **Der Kern verbietet das Erfinden.** Gesagt wird nur, was ein
  Werkzeugergebnis, das Wissen oder das Gespräch belegt und nichts
  widerlegt. Ein Angebot, eine Leistung oder eine Möglichkeit — etwa ein
  Zimmer für wenige Stunden — wird erst genannt, wenn ein Werkzeug sie
  bestätigt hat.

## Form: kurz und streng

Jeder Aufgaben-Skill hat fünf Teile, in dieser Reihenfolge, je als Liste
mit einer Aussage pro Zeile:

```
PURPOSE    ein Satz: wofür der Skill da ist
TOOLS      Werkzeugname — wann es gebraucht wird
STEPS      die Schritte des Ablaufs, nummeriert
NEVER      was nie geschieht
HANDOVER   wann das Team übernimmt — immer mit Nachricht an den Kunden
```

- **Keine Begründungsprosa, keine Vorgeschichte.** Warum eine Regel gilt,
  steht in der Entscheidungsakte, nicht im Skill.
- **Was das Werkzeug erzwingt, beschreibt der Skill nicht nach.** Er sagt,
  welches Werkzeug mit welchen Angaben aufgerufen wird. Mandant, Nachweis,
  Eigentum und Doppelausführung prüft das Werkzeug, und dessen Fehler sagt
  dem Modell, was fehlt.
- **Die Längengrenze legt das Projekt fest** und misst sie beim Start.
  Richtwert: Kern höchstens 4.000, Aufgaben-Skill höchstens 2.000 Zeichen.

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

## Alles im Kontext

- **Kern und alle Aufgaben-Skills stehen ab dem ersten Aufruf im
  Kontext.** Kein Nachladen, keine Auswahl durch eine Vorstufe.
- **Die Größe wird gemessen**, je Skill und für das Paket. Ein Skill, der
  zu lang wird, wird geteilt — nicht gekürzt, bis eine Regel fehlt.
- **Passt das Paket nicht mehr**, wird das dem Projektinhaber vorgelegt.
  Nichts wird still weggelassen.

## Woher das Paket kommt

- **Im Repository, versioniert, als Dateien** — nicht als Zeichenkette im
  Code, nicht in einer beschreibbaren Ablage.
- **In die Anwendung eingebettet und beim Start geprüft:** Fehlt eine
  Datei, ist ein Werkzeug oder eine Abhängigkeit unbekannt, gibt es einen
  Kreis in den Abhängigkeiten oder ist ein Skill zu groß, startet die
  Anwendung nicht mit diesem Paket.
- **Nie aus einer Kundennachricht, einer Webseite, einem Anhang oder einer
  beschreibbaren Einstellung.** Die Anweisungen des Betreibers sind
  Einstellungen, keine Skills.
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
