# Einen bestehenden Assistenten umbauen

Lesekonvention siehe `SKILL.md`.

Für den häufigen Fall: der Assistent läuft, der Prompt ist über Monate
gewachsen, niemand fasst ihn gern an. **Er wird nicht neu geschrieben.**
Ein Neuschrieb verliert alles, was in den gewachsenen Zeilen an
Erfahrung steckt, und niemand kann beweisen, dass die neue Fassung besser
ist.

Umgebaut wird in Schritten, jeder einzeln gemessen, jeder für sich
zurücknehmbar.

## Schritt 0 — Nichts anfassen

Zuerst wird der Ist-Zustand festgehalten. Ein Umbau, der ohne
Ausgangsmessung beginnt, kann am Ende nicht zeigen, dass er etwas
verbessert hat.

- Prompt, Werkzeugdefinitionen, Absichtslogik und Modellfassung in einem
  Commit einfrieren.
- Alles Weitere in Zweigen davon.

## Schritt 1 — Inventar

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/promptinventar.py prompts/assistent.md
```

Das Skript zählt und findet Muster; es urteilt nicht. Es meldet
Schlüsselwort-Verzweigung, Schemata in der Prosa, wortgleiche
Wiederholungen und zu große Abschnitte, jeweils mit Zeilennummer.

Danach wird der Prompt **von Hand** durchgegangen und jede Zeile genau
einer Klasse zugeordnet:

| Klasse | Wohin sie gehört |
| --- | --- |
| Rolle, Ton, Anrede | bleibt im Systemprompt |
| Grenze, Eskalation, Verweigerung | bleibt im Systemprompt |
| Werkzeugauswahl („wenn …, dann rufe …") | in die Werkzeugbeschreibung |
| Argumentregel, Format, erlaubte Werte | ins Schema |
| Reihenfolge, Vorbedingung, Bestätigung | in den Code |
| Fachwissen, Listen, Codes, Preise | in Daten oder ein Nachschlagewerkzeug |
| Beispieldialog | weg oder je Sprache |
| Wiederholung | weg |
| Widerspruch zu einer anderen Zeile | **vorlegen** |

Das Ergebnis ist eine Tabelle: Zeilenbereich, Klasse, Ziel. **Sie wird
vorgelegt, bevor etwas verschoben wird.** Widersprüche werden nicht
selbst aufgelöst — welche der beiden Zeilen gilt, entscheidet der
Projektinhaber.

## Schritt 2 — Ausgangsmessung

Goldfälle für den heutigen Stand, mindestens die klaren Fälle je Absicht
und je Sprache, dazu die schreibenden Werkzeuge (`goldfaelle.md`).
**Zehn Läufe**, Bericht als Datei.

Diese Zahl ist der Maßstab für alles Weitere. Sie wird oft unangenehm
sein — das ist ihr Zweck.

## Schritt 3 bis 6 — Umbau, in dieser Reihenfolge

Vom billigsten zum teuersten Eingriff. **Nach jedem Schritt messen und
die Zahl berichten**, vor dem nächsten.

### 3. Schemata härten

Größter Ertrag, geringstes Risiko, keine Prompt-Änderung nötig.

- `additionalProperties: false`, Pflichtfelder, `enum` statt Zeichenkette,
  `pattern` für Kennungen, Formate für Datum und Zeit.
- Schemaprüfung **vor** der Ausführung, Fehler mit Begründung zurück ans
  Modell, höchstens zwei Wiederholungen.
- Abgrenzung in jede Werkzeugbeschreibung: „Nicht dafür — dafür `…`".
- Was jetzt im Schema steht, wird aus dem Prompt gelöscht. Doppelt
  gepflegt heißt bald widersprüchlich.

Erwartung: die Argumentfehler verschwinden fast vollständig, die
Werkzeugwahl wird besser, ohne dass am Prompt etwas geändert wurde.

### 4. Fachwissen herausziehen

Listen, Codes, Zustände, Preise, Häuser, Öffnungszeiten. Alles, was
veraltet, gehört nicht in einen Prompt.

- In ein Nachschlagewerkzeug oder in den Zustand.
- `heute`, Zeitzone, Mandant und Auswahl kommen als Daten
  (`architektur.md`).

Erwartung: der Prompt schrumpft deutlich, die Datumsfehler hören auf.

### 5. Absichten schneiden

Erst jetzt, wenn der Prompt klein genug ist, um ihn zu überblicken.

- Katalog aufstellen, mit Abgrenzung und den drei Pflichtabsichten
  (`absichten.md`).
- Je Absicht die erlaubten Werkzeuge als **Positivliste im Code**.
- Die Schlüsselwort-Verzweigungen aus Schritt 1 ersatzlos löschen — die
  Absichten übernehmen ihre Aufgabe.

Erwartung: die Sprachen gleichen sich an. Wo eine Sprache vorher
deutlich schlechter war, ist der Unterschied hier weg.

### 6. Zweite Stufe

**Nur, wenn die Messung sie verlangt** — wenn die Werkzeugwahl trotz
Schritt 3 bis 5 unter der Schwelle bleibt oder mit jedem weiteren
Werkzeug sinkt (`architektur.md`).

Erwartung: Absichten stören einander nicht mehr. Ab hier bricht eine
Änderung an einer Absicht keine andere mehr — das eigentliche Ziel des
ganzen Umbaus.

## Regeln für den ganzen Umbau

- **Eine Änderung je Commit**, mit der Messung davor und danach in der
  Commit-Nachricht (Skill `neo-grundregeln`).
- **Nie zwei Schritte gleichzeitig.** Sonst weiß niemand, welcher gewirkt
  hat — und bei einem Rückschritt muss beides zurück.
- **Kein Modellwechsel während des Umbaus.** Er verfälscht jede Messung
  (`modellwahl.md`).
- **Keine Verhaltensänderung nebenbei.** Fällt beim Umbau etwas
  Fachliches auf, wird es vorgelegt, nicht miterledigt.
- **Ein Schritt, der die Zahl verschlechtert, wird zurückgenommen**, nicht
  nachgebessert. Zurücknehmen ist billig, Nachbessern selten.
- Der Umbau endet mit einer Entscheidungsakte: Ausgangslage, Schritte,
  Zahlen vorher und nachher, was offen bleibt (Skill `neo-doku`).

## Woran man erkennt, dass es reicht

- Der Systemprompt ist unter 150 Zeilen und enthält keine Werkzeugauswahl.
- Eine neue Sprache braucht keine Prompt-Änderung.
- Eine neue Absicht berührt keine bestehende.
- Alle Goldfälle liegen über der Schwelle, schreibende bei 100 %.
- Ein neues Werkzeug hinzuzufügen dauert eine Stunde, nicht einen Tag.
