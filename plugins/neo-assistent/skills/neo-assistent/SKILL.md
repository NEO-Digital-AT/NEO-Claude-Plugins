---
name: neo-assistent
description: >
  NEO-Regeln für den Bau von KI-Assistenten mit Werkzeugzugriff. Diesen
  Skill laden, sobald ein Assistent, ein Chatbot, ein Agent oder ein
  Copilot gebaut, erweitert oder umgebaut wird, und bei jeder Änderung an
  seinem Systemprompt, an seinen Werkzeugen, an seinem Werkzeugschema
  oder an seinem Modell. Ebenso bei Anbindung eines MCP-Servers oder
  einer Fach-API an ein Sprachmodell, bei der Frage, welches Werkzeug ein
  Modell wann aufruft, bei falschen oder ausbleibenden Werkzeugaufrufen,
  bei falschen Argumenten oder Datenformaten, bei mehrsprachigen
  Assistenten und beim Dazuschalten einer Sprache. Ebenso bei einem
  Prompt, der zu groß geworden ist, bei Änderungen, die an anderer Stelle
  etwas kaputt machen, bei der Wahl und beim Wechsel des Modells und
  immer dann, wenn die Zuverlässigkeit eines Assistenten gemessen werden
  soll.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# KI-Assistenten bauen

Lesekonvention siehe `README.md` des Regel-Repositorys.

Dieser Skill regelt den **Bau**. Rechtsstand, Kennzeichnungspflicht,
Datenweitergabe, Prompt Injection, Protokollierung und Kosten stehen im
Skill `neo-ki` und gelten zusätzlich.

## Der Satz, um den es geht

> **Ein Assistent ist eine Architektur, kein Prompt.**

Ein Assistent, der aus einem großen Systemprompt besteht, wird ab einer
gewissen Größe unwartbar — und zwar mit Ansage, an denselben vier
Stellen:

| Symptom | Ursache |
| --- | --- |
| Eine Änderung bricht eine andere Stelle | Alle Anweisungen sehen einander. Es gibt keine Trennung. |
| Auf Deutsch geht es, auf Englisch nicht | Der Ablauf hängt an Wörtern. Wörter überleben keine Übersetzung. |
| Das falsche Werkzeug, falsche Argumente | Die Auswahl steht in Prosa statt im Schema. Prosa erzwingt nichts. |
| „Mit dem größeren Modell geht es besser" | Der Prompt ist zu groß. Das Modell kauft Zeit, es löst nichts. |

**Ein größeres Modell ist nie die Antwort auf eine dieser vier
Ursachen.** Es verschiebt die Grenze und bringt sie später zurück.

## 1. Fünf Schichten, getrennt

Was heute in einem Prompt steht, gehört auf fünf Orte verteilt. Die
Trennung ist der eigentliche Gewinn: was getrennt ist, kann einander
nicht mehr kaputt machen.

| Schicht | Inhalt | Ort |
| --- | --- | --- |
| **Systemprompt** | Rolle, Ton, Grenzen, Eskalation | eine Datei, **unter 150 Zeilen** |
| **Absichten** | geschlossene Liste; je Absicht Zweck, Werkzeuge, Zusatzanweisung | Katalog, je Absicht ein Abschnitt |
| **Werkzeuge** | Name, Beschreibung, Schema | Schemadatei, nicht Prosa |
| **Zustand** | was bereits bekannt ist: Mandant, Datum, Auswahl | Code, als Daten übergeben |
| **Ablauf** | Vorbedingung, Bestätigung, Wiederholung, Abbruch | Code, nicht Text |

**Die Obergrenze wird gemessen, nicht geschätzt.** Was den Systemprompt
sprengt, gehört in eine der anderen Schichten. Die wichtigste Grenze
läuft zwischen Prompt und Code: **ein Prompt bittet, ein Schema
erzwingt, eine Vorbedingung im Code entscheidet.**

Schichten, Zweistufigkeit und wann ein Router nötig wird:
`references/architektur.md`.

## 2. Kein natürlichsprachiges Wort steuert den Ablauf

**Nie** so:

```
Wenn der Benutzer „stornieren" oder „cancel" schreibt, rufe das
Werkzeug auftrag_stornieren auf.
```

Das ist der teuerste Fehler im ganzen Skill. Er bricht bei der nächsten
Sprache, bei jeder Umschreibung und bei jedem Tippfehler.

Stattdessen: eine **Absicht** mit einem Zweck, und ein **Werkzeug**,
dessen Beschreibung sagt, wofür es da ist. Die Zuordnung macht das
Modell — semantisch, in jeder Sprache.

> **Die Prüffrage: Eine neue Sprache dazuschalten darf keine einzige
> Prompt-Zeile ändern.** Muss sie es doch, gibt es Schlüsselwort-Routing,
> und es muss weg.

Absichtskatalog, Zuschnitt, Mehrdeutigkeit und Rückfallabsicht:
`references/absichten.md`. Sprachen, kanonische Arbeitssprache und das
Dazuschalten: `references/sprachen.md`.

## 3. Das Werkzeug trägt seine Auswahl selbst

- **Die Beschreibung ist das Routing.** Sie sagt, wann das Werkzeug zu
  verwenden ist **und wann nicht** — mit Abgrenzung zum ähnlichsten
  Werkzeug, unter dessen Namen. Zwei Werkzeuge ohne Abgrenzung sind die
  häufigste Ursache für die falsche Wahl.
- **Ein Werkzeug, eine Aufgabe.** Kein `aktion(typ, nutzlast)`. Der Name
  ist eine Handlung: `auftrag_stornieren`, nicht `apiCallV2`.
- **Aufzählungen statt Freitext**, Formate deklariert,
  `additionalProperties: false`, Pflicht ist Pflicht.
- **Kennungen werden nie erfunden.** Sie stammen aus einem Ergebnis oder
  aus dem Zustand; davor gehört ein Suchschritt.
- **Geprüft wird vor der Ausführung.** Ein ungültiger Aufruf geht mit
  Begründung zurück ans Modell, höchstens zweimal, dann Abbruch mit
  Klartext. Nie stillschweigend das nächstbeste Werkzeug.
- **Schreibende Werkzeuge bestätigen**, sind idempotent und laufen mit
  den Rechten des angemeldeten Nutzers (Skill `neo-sicherheit`).

Schemata, Beschreibungen, Abgrenzung, Fehlerrückgabe und Vorbedingungen:
`references/werkzeuge.md`.

## 4. Fertig heißt gemessen

**Keine Änderung an Prompt, Absicht, Werkzeug, Schema oder Modell ohne
Goldfall-Lauf davor und danach.** „Es wirkt besser" ist keine Zahl.

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/goldlauf.py goldfaelle.json \
  --adapter "python3 tools/assistent_adapter.py" --laeufe 5
```

Der Prüfer läuft jeden Fall mehrfach, weil ein Modell nicht
deterministisch antwortet, und bewertet die Trefferquote.

| Fallart | Schwelle |
| --- | --- |
| Schreibende Werkzeuge | **100 %** |
| Verweigerung, Einschleusung, Zuständigkeitsgrenze | **100 %** |
| Alles Übrige | **95 %** |

Je Absicht mindestens drei Fälle: der klare, der mehrdeutige und der,
der **kein** Werkzeug auslösen darf. Jeder Fall in **jeder**
ausgelieferten Sprache.

**Eine Änderung je Lauf.** Zwei gleichzeitig, und niemand weiß, welche
gewirkt hat.

Format, Abdeckung, Schwellen, CI und das Vorgehen bei einem Rückschritt:
`references/goldfaelle.md`.

## 5. Das Modell ist ein gemessener Parameter

- **Festgenagelte Version**, nie „latest". Ein stiller Modellwechsel
  bricht den Assistenten ohne eine einzige Codeänderung.
- **Je Stufe ein Modell**: klein und schnell für die Einordnung, stark
  für die Bearbeitung — genauer und billiger als ein Modell für alles.
- **Ein Modellwechsel wird gemessen wie jede andere Änderung**: dieselben
  Goldfälle, Zahlen vorher und nachher, sonst nichts verändert, Ergebnis
  als Entscheidungsakte (Skill `neo-doku`).
- **Nie als Reparatur einer Strukturschwäche.** Erst Struktur, dann
  messen, dann Modelle vergleichen. Der Modellname steht in der
  Konfiguration, nie im Code (Skill `neo-ki`).

Vergleich, Wechsel und was billiger ist als hochrüsten:
`references/modellwahl.md`.

## 6. Ein bestehender Assistent wird nicht neu geschrieben

Ein gewachsener Assistent wird **in Schritten** umgebaut, jeder einzeln
gemessen, vom billigsten zum teuersten Eingriff: **Inventar**
(`scripts/promptinventar.py`) → **Ausgangsmessung** → **Schemata
härten** → **Fachwissen herausziehen** → **Absichten schneiden** →
**Router**, letzterer erst, wenn die Messung ihn nötig macht.

**Nie alles auf einmal**, **nie ohne Freigabe des Umfangs** (Skill
`neo-grundregeln`), und ein Schritt, der die Zahl verschlechtert, wird
zurückgenommen statt nachgebessert. Vorgehen je Schritt:
`references/umbau.md`. Der Befehl
`/neo-assistent:neo-assistentpruefung` führt Inventar und
Ausgangsmessung durch und legt den Umbauplan vor.

## 7. Mehrere Assistenten teilen ein Skelett

Gemeinsam sind Schichtung, Router, Schemaprüfung, Fehlerrückgabe,
Sprachbehandlung, Goldfall-Prüfer, Adapter und Protokollierung. Eigen
sind nur Absichten, Werkzeuge, Ton und Goldfälle. Wer den zweiten
Assistenten als Kopie des ersten anlegt, pflegt ab dem Tag zwei
Fassungen jeder Regel.

## 8. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.
Der Befehl `/neo-assistent:neo-goldlauf` führt die Messung durch.

Zugehörige Skills: `neo-ki` (Recht, Kennzeichnung, Daten, Injection,
Kosten), `neo-api` (Schnittstellen), `neo-sicherheit` (Rechte, Secrets),
`neo-code` (Abstraktion, Schichten), `neo-doku` (Entscheidungsakten),
`neo-grundregeln` (Freigabe, eine Änderung je Commit).
