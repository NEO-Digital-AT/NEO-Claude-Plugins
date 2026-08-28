---
description: Einen bestehenden KI-Assistenten vermessen — Prompt-Inventar, Ausgangsmessung, Umbauplan. Ohne Freigabe wird nichts umgebaut.
---

Nimm den bestehenden Assistenten auseinander und lege vor, was du
gefunden hast. **Du baust in diesem Befehl nichts um.** Am Ende steht ein
Plan mit Zahlen, keine geänderte Datei.

Lade zuerst den Skill `neo-assistent` und `references/umbau.md`.

## Schritt 0 — Zusammentragen

Kläre, falls es nicht im Projekt steht:

1. Wo liegen Systemprompt, Werkzeugdefinitionen und Absichtslogik?
2. Welche Werkzeuge sind angebunden, welche davon stammen aus einem
   fremden MCP-Server?
3. Welches Modell in welcher Fassung, je Stufe?
4. Welche Sprachen werden ausgeliefert, welche sind geplant?
5. Gibt es bereits Goldfälle oder einen Adapter?
6. Welche Werkzeuge sind **schreibend**? Diese Liste brauchst du für die
   Schwellen.

Friere den Ist-Zustand in einem Commit ein, bevor du misst.

## Schritt 1 — Inventar

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/prompt-inventory.py <promptdatei> --report inventory.json
```

Das Skript meldet Schlüsselwort-Verzweigung, Schemata in der Prosa,
wortgleiche Wiederholungen und zu große Abschnitte, jeweils mit
Zeilennummer. **Es urteilt nicht** — du gehst den Prompt danach von Hand
durch und ordnest jeden Zeilenbereich genau einer Klasse zu, nach der
Tabelle in `references/umbau.md`:

| Zeilen | Klasse | Ziel |
| --- | --- | --- |
| 1–12 | Rolle, Ton | bleibt |
| 34–58 | Werkzeugauswahl | in die Werkzeugbeschreibungen |
| 61–96 | Fachwissen | in ein Nachschlagewerkzeug |
| … | | |

Widersprüche und Doppelungen werden **benannt, nicht aufgelöst.** Welche
von zwei widersprechenden Zeilen gilt, entscheidet der Projektinhaber.

Prüfe zusätzlich, was das Skript nicht sehen kann:

- Wie viele Werkzeuge sieht das Modell **je Anfrage**?
- Grenzen sich ähnliche Werkzeuge in ihren Beschreibungen ab?
- Wie streng sind die Schemata — `enum`, `pattern`, `required`,
  `additionalProperties`?
- Steht `heute`, Mandant und Auswahl im Zustand oder wird geraten?
- Werden Vorbedingungen im Code geprüft oder nur im Prompt gebeten?

## Schritt 2 — Ausgangsmessung

Ohne sie ist jede spätere Verbesserung eine Behauptung.

1. **Adapter bauen**, falls keiner da ist: er fährt denselben Weg wie die
   Anwendung und führt schreibende Werkzeuge **nicht** wirklich aus.
2. **Goldfälle anlegen** — je Absicht der klare, der mehrdeutige und der
   Fall ohne Werkzeug, je Sprache, dazu Einschleusung, Datumsrechnung und
   je Vorbedingung ein Fall (`references/goldfaelle.md`).
   Vorlage: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/gold-run.py --example`
3. **Messen**, zehn Läufe:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/gold-run.py gold-cases.json \
  --adapter "<befehl>" --runs 10 --report baseline.json
```

Berichte die Zahlen **je Sprache und je Absicht**, nicht nur den
Mittelwert — ein Mittelwert verdeckt genau den Einbruch, der wehtut.

## Schritt 3 — Befunde ordnen

Ordne jeden Befund einer der vier Ursachen zu und nenne die Fundstellen:

| Ursache | Woran erkennbar |
| --- | --- |
| Keine Trennung | Absichten sehen einander; eine Änderung wirkt überall |
| Ablauf an Wörtern | Trefferquote bricht in genau einer Sprache ein |
| Prosa statt Schema | Argumentfehler, erfundene Werte, falsche Formate |
| Zu groß | Abschnitte über der Grenze, Regeln ohne Wirkung |

Nenne je Ursache, **was sie im Betrieb kostet** — nicht abstrakt: welcher
Goldfall fällt, in welcher Sprache, wie oft.

## Schritt 4 — Umbauplan vorlegen

Sechs Schritte in fester Reihenfolge, vom billigsten zum teuersten
(`references/umbau.md`). Je Schritt:

- was geändert wird,
- welche Goldfälle er verbessern soll,
- welches Risiko er trägt,
- wie er zurückgenommen wird.

Dazu die Frage, welche Schritte freigegeben werden. **Nichts umbauen,
solange der Umfang nicht freigegeben ist** (Skill `neo-grundregeln`).

## Berichten

```
Systemprompt          <n> Zeilen (Grenze 150)
Befunde               <n>× Schlüsselwort, <n>× Schema in Prosa, <n>× Wiederholung
Werkzeuge je Anfrage  <n>
Goldfälle             <n> in <n> Sprachen
Ausgangsmessung       de <x> %, en <y> %  ·  schreibend <z> %  ·  <n> von <n> bestanden
```

Am Ende ein Satz, keine Einschätzung: welche Ursache die teuerste ist und
welcher Schritt sie beseitigt. Die Entscheidung über den Umfang liegt
beim Projektinhaber.
