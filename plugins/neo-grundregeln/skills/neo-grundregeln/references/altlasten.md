# Altlasten: was im Repository liegen bleibt

Lesekonvention siehe `SKILL.md`.

> **Ein Repository ist ein Werkzeug, kein Archiv.**

Jede Datei, die darin liegt, kostet Aufmerksamkeit: Jemand liest sie,
jemand hält sie für aktuell, jemand pflegt sie mit. Ein Screenshot aus
einer Fehlersuche, eine Protokolldatei, ein Skript, das einmal zum
Ausprobieren geschrieben wurde, eine Planung, die vor einem halben Jahr
abgeschlossen wurde — für sich genommen ist nichts davon schlimm.
Zusammen ergeben sie ein Repository, dem niemand mehr traut, weil
niemand mehr weiß, was davon gilt.

## Zwei Wege, und der erste ist der wichtige

### 1. Beim Arbeiten: jede Änderung nimmt ihre Rückstände mit

**Wer etwas anlegt, um etwas herauszufinden, räumt es im selben Schritt
weg.** Nicht „später", nicht „könnte man noch brauchen".

- **Der Agent räumt weg, was er für sich selbst angelegt hat** —
  Probeskripte, Zwischenstände, Aufnahmen, Protokolle. Das war nie
  bestellt und braucht keine Freigabe. Es taucht gar nicht erst im Commit
  auf.
- **Vorübergehendes gehört nicht ins Repository**, sondern in ein
  Arbeitsverzeichnis außerhalb. Was nur für einen Versuch entsteht, wird
  dort angelegt und dort gelassen.
- **Was bleiben soll, bekommt einen Platz und einen Zweck** — oder es
  bleibt nicht.

### 2. Von Zeit zu Zeit: die Durchsicht

Einmal je Fassung, je Meilenstein oder wenn es unübersichtlich wird:
**Datei für Datei die eine Frage** — wird das noch gebraucht?

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/repo-hygiene.py
```

Das Werkzeug liest die **verfolgten** Dateien und meldet vier Gruppen:
Geheimnisse, Reste, nirgends Erwähntes und liegen gebliebene Planungen.
**Es löscht nichts.** Die letzten beiden Gruppen sind Vorschläge, keine
Urteile: Eine Datei kann gebraucht werden, ohne dass eine andere sie
nennt.

## Was geht, was bleibt

| Geht | Warum |
| --- | --- |
| Protokolle, Zwischenspeicher, Bau-Ausgaben | entstehen neu |
| Screenshots aus einer Sitzung | waren für einen Moment |
| Skripte, die einmal etwas ausprobiert haben | erfüllen keinen Zweck mehr |
| Dateien aus einem Temp-Ordner | sind versehentlich hier |
| Abgeschlossene Planungen | tragen eine Aufgabe, keine Entscheidung |
| Zweite Fassungen: `datei-alt.md`, `datei-neu-final.md` | Git ist die Fassungsverwaltung |
| Auskommentierter Code, tote Zweige | der Verlauf hebt sie auf |

| Bleibt | Warum |
| --- | --- |
| **Dokumentation fremder Schnittstellen** | genau dafür hat man ein Repository — sie ist auf jedem Rechner da |
| **Entscheidungsakten** | halten fest, warum etwas so ist (Skill `neo-doku`) |
| **Sperrdateien der Abhängigkeiten** (`package-lock.json`, `composer.lock`, `pubspec.lock`, `packages.lock.json`) | machen den Bau wiederholbar; sie gehören **eingecheckt** |
| **Erzeugte Dateien mit Absicht**, mit Kopf „nicht von Hand ändern" | etwa die Tokendatei aus dem Erzeugungsschritt (Skill `neo-design`) |
| **Testdaten und Aufnahmen, auf die ein Test zeigt** | sie sind Teil des Tests |

**Die Sperrdatei ist der häufigste Fehlgriff beim Aufräumen.** Sie sieht
aus wie ein Erzeugnis und ist das Gegenteil: Ohne sie baut morgen jeder
etwas anderes.

## Die abgeschlossene Planung

Ein Plan trägt eine **Aufgabe**, eine Entscheidungsakte trägt eine
**Entscheidung**. Ist die Aufgabe erledigt, hat der Plan seinen Zweck
erfüllt:

- **Was daran wissenswert war, wird eine Entscheidungsakte** — warum es
  so gebaut wurde, was verworfen wurde (Skill `neo-doku`,
  `references/entscheidungsakten.md`).
- **Der Rest geht.** Ein Plan, der drei Fassungen alt ist und
  Zwischenstände beschreibt, die es nicht mehr gibt, führt in die Irre.
- **Ein Plan, der noch läuft, bleibt** — und ist daran erkennbar, dass
  jemand ihn anfasst.

## Gelöscht wird nach Freigabe

**Der Agent legt vor, der Projektinhaber entscheidet** (Kernregel 1). Die
Vorlage ist eine Liste: Datei, warum sie als Altlast gilt, und was
verloren ginge. Keine Sammellöschung, kein „habe gleich mit aufgeräumt".

**Zwei Ausnahmen, beide eng:**

1. **Was der Agent selbst in dieser Sitzung angelegt hat** und was nie
   bestellt war — das räumt er ohne Rückfrage weg.
2. **Ein Geheimnis** wird sofort aus der Verfolgung genommen und gemeldet
   (Kernregel 27). Es aus dem Verlauf zu entfernen und zu wechseln ist
   dann eine eigene Aufgabe.

## Geheimnisse gehören nie hinein

- **Nie ein Zugangsdatum, ein Token, ein Schlüssel, ein Zertifikat mit
  privatem Teil** — auch nicht „nur für die Testumgebung", auch nicht
  auskommentiert.
- **Was einmal im Verlauf steht, gilt als kompromittiert.** Die Datei zu
  löschen genügt nicht: Das Geheimnis wird **gewechselt**. Der Verlauf
  ist auf jedem Rechner, der jemals geklont hat.
- **Eine `.env.example` mit leeren Werten** ist der richtige Weg, die
  Felder zu dokumentieren.
- Einzelheiten: Skill `neo-sicherheit`.

## Abnahme

- [ ] `repo-hygiene.py` gelaufen; Geheimnisse und Reste: **null**.
- [ ] Die Vorschläge wurden **angesehen** und beantwortet — behalten mit
      Grund oder gelöscht mit Freigabe.
- [ ] Was in dieser Sitzung zum Ausprobieren entstand, ist weg.
- [ ] Kein Vorübergehendes im Commit; das Arbeitsverzeichnis lag
      außerhalb des Repositories.
- [ ] Abgeschlossene Planungen sind Entscheidungsakten geworden oder
      gelöscht.
- [ ] Sperrdateien der Abhängigkeiten sind **nicht** gelöscht worden.
