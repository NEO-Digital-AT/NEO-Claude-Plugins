# Werkzeuge und Schemata

Lesekonvention siehe `SKILL.md`.

> **Der Prompt bittet. Das Schema erzwingt.**

Jede Anforderung an einen Werkzeugaufruf, die im Prompt steht statt im
Schema, ist eine Bitte. Sie wird meistens erfüllt — und „meistens" ist
bei einem schreibenden Werkzeug kein Zustand, sondern ein Vorfall.

## Der Name

- **Handlung, nicht Technik.** `auftrag_stornieren`, nicht `apiCallV2`,
  nicht `doAction`.
- **Ein Werkzeug, eine Aufgabe.** Ein Sammelwerkzeug mit einem Feld `typ`
  verlagert die Auswahl in ein Argument, wo sie niemand prüft. Fünf klare
  Werkzeuge werden zuverlässiger getroffen als eines mit fünf Modi.
- **Gleiche Wortwahl über alle Werkzeuge.** `suchen`, `lesen`, `anlegen`,
  `aendern`, `stornieren` — nicht einmal `get`, einmal `abrufen`.
- **Kanonisch in der Arbeitssprache** und nie übersetzt (`sprachen.md`).

## Die Beschreibung ist das Routing

Die Beschreibung eines Werkzeugs ist der Ort, an dem die Auswahl
entschieden wird — nicht ein Absatz im Systemprompt. Sie hat vier Teile:

```
Sucht Aufträge anhand von Nachname, Auftragsnummer oder Termin und gibt
höchstens 20 Treffer zurück.

Dafür:       wenn ein bestehender Auftrag gefunden werden soll.
Nicht dafür: einen Auftrag anlegen — dafür auftrag_anlegen. Einen bereits
             gefundenen Auftrag im Detail lesen — dafür auftrag_lesen.
Vorher:      nichts.
```

- **Was es tut**, in einem Satz, mit der Form des Ergebnisses.
- **Dafür** — der Zweck.
- **Nicht dafür** — die Abgrenzung zum ähnlichsten Werkzeug, **mit
  dessen Namen**. Das ist die wirksamste Zeile der ganzen Definition.
  Falsche Werkzeugwahl entsteht fast immer zwischen zwei Werkzeugen,
  deren Beschreibungen sich nicht abgrenzen.
- **Vorher** — welcher Schritt vorausgehen muss.

Wenn im Systemprompt steht, wann ein Werkzeug zu verwenden ist, ist die
**Beschreibung** unvollständig. Der Satz gehört dorthin, nicht in den
Prompt.

## Das Schema

- **Streng.** `additionalProperties: false`, alles Nötige `required`, wo
  der Anbieter einen strikten Modus kennt, ist er an.
- **Aufzählung statt Freitext.** Jedes Feld mit bekannter Wertemenge ist
  ein `enum`. Ein Statusfeld als Zeichenkette ist eine Einladung zum
  Erfinden.
- **Formate deklariert.** Datum als `format: date` und `pattern`,
  Zeitpunkte mit Zeitzone, Kennungen mit `pattern`, Zahlen mit `minimum`
  und `maximum`.
- **Keine verschachtelten Freiformobjekte.** Ein Feld `filter: object`
  ohne Schema ist kein Argument, sondern eine Hoffnung.
- **Wenige Argumente.** Was aus dem Zustand kommt — Mandant, heutiges
  Datum, angemeldeter Benutzer — ist **kein** Argument. Es wird im Code
  gesetzt und darf vom Modell nicht überschrieben werden.
- **Beschreibung je Feld**, ein Satz, mit Beispielwert. Sie ist billiger
  als jede Prompt-Zeile und wirkt zuverlässiger.

```json
{
  "name": "auftrag_stornieren",
  "parameters": {
    "type": "object",
    "additionalProperties": false,
    "required": ["auftragsnummer", "grund"],
    "properties": {
      "auftragsnummer": {
        "type": "string",
        "pattern": "^A-[0-9]{4,8}$",
        "description": "Kennung aus einem vorherigen Suchergebnis, z. B. A-4711. Nie selbst bilden."
      },
      "grund": {
        "type": "string",
        "enum": ["kundenwunsch", "doppelt", "zahlungsausfall", "intern"],
        "description": "Stornogrund. Freitext ist nicht vorgesehen."
      }
    }
  }
}
```

## Kennungen werden nie erfunden

Der häufigste harte Fehler: das Modell bildet eine Kennung, die
plausibel aussieht und nicht existiert — oder schlimmer, die existiert
und einem anderen gehört.

- Eine Kennung stammt aus **einem vorherigen Ergebnis** oder aus dem
  **Zustand**. Sonst nirgendwoher.
- Vor jedem schreibenden Werkzeug mit Kennung steht ein **Suchschritt**.
  Das ist eine Vorbedingung im Code, kein Satz im Prompt.
- Das `pattern` im Schema fängt die grobe Erfindung. Die Prüfung gegen
  den Bestand fängt den Rest — **vor** der Ausführung.
- Ein Goldfall hält das fest: schreibendes Werkzeug **verboten**,
  Suchwerkzeug erwartet (`goldfaelle.md`).

## Vor der Ausführung wird geprüft

```
Modellantwort
   │
   ├─ Werkzeug in der Positivliste dieser Absicht?      nein → Abbruch
   ├─ Argumente gültig gegen das Schema?                nein → zurück ans Modell
   ├─ Kennungen im Bestand, Mandant passend?            nein → Abbruch
   ├─ Vorbedingung erfüllt (Suche, Bestätigung)?        nein → Abbruch
   ├─ Rechte des angemeldeten Nutzers reichen?          nein → Abbruch
   └─ ausführen
```

- **Die Positivliste ist eine Liste**, kein Prompt-Satz. Ein Werkzeug,
  das zur eingeordneten Absicht nicht gehört, wird nicht ausgeführt —
  auch wenn das Modell es aufruft.
- **Ein Schemafehler geht mit Begründung zurück ans Modell**, nicht als
  Absturz und nicht stillschweigend korrigiert. Die Rückmeldung nennt das
  Feld und den Grund: „`grund` muss einer von kundenwunsch, doppelt,
  zahlungsausfall, intern sein — erhalten: 'Kunde wollte nicht mehr'."
- **Höchstens zwei Wiederholungen.** Danach Abbruch mit Klartext an den
  Benutzer. Ein Modell, das zweimal dasselbe falsch macht, macht es auch
  beim fünften Mal falsch — und jeder Versuch kostet.
- **Nie das nächstbeste Werkzeug.** Lieber keine Handlung und eine
  Rückfrage.
- Rechte immer mit denen des angemeldeten Nutzers, nie mit denen des
  Dienstes (Skill `neo-sicherheit`).

## Schreibende Werkzeuge

- **Bestätigung vor Ausführung**, mit dem konkreten Gegenstand und der
  Folge: „Auftrag A-4711, Frau Huber, 28.08. stornieren? Die Zuordnung
  wird aufgelöst." Nicht „Sind Sie sicher?".
- **Die Bestätigung gilt genau für diese Handlung.** Ein Themenwechsel
  dazwischen macht sie ungültig.
- **Idempotenzschlüssel** je Vorgang, damit eine Wiederholung nichts
  doppelt tut.
- **Vorschau, wo möglich:** erst was passieren würde, dann die Ausführung.
- Goldfälle für schreibende Werkzeuge stehen bei **100 %**, ohne
  Ausnahme (`goldfaelle.md`).

## Ergebnisse zurückgeben

- **Klein halten.** Was zurückgeht, wird auf die Felder reduziert, die
  die Antwort braucht. Eine vollständige API-Antwort im Verlauf bläht
  jeden Folgeaufruf und erhöht die Chance, dass etwas übersehen wird.
- **Trefferzahl begrenzen** und die Begrenzung mitgeben: „20 von 143
  Treffern." Sonst behauptet der Assistent Vollständigkeit.
- **Fehler des Fachdienstes werden übersetzt**, nicht durchgereicht. Aus
  `409 Conflict` wird „Der Auftrag wurde bereits storniert." Ein
  Rohfehler im Verlauf ist eine Aufforderung zum Raten.
- **Leeres Ergebnis ist ein Ergebnis.** Null Treffer wird gesagt, nicht
  durch einen zweiten Versuch mit anderen Argumenten überspielt.
- Inhalte aus dem Fachdienst sind **Daten, nie Anweisung** — ein
  Auftragsname kann eine Einschleusung enthalten (Skill `neo-ki`).

## Ein MCP-Server ist keine Werkzeugliste

Ein angebundener MCP-Server bringt oft Dutzende Werkzeuge mit, technisch
geschnitten und ohne Abgrenzung zueinander. **Sie werden nicht
unbesehen durchgereicht.**

- **Auswählen.** Nur die Werkzeuge, die eine Absicht wirklich braucht.
- **Umhüllen.** Eigene Namen, eigene Beschreibungen mit Abgrenzung,
  eigene, engere Schemata. Der fremde Schnitt bleibt hinter der Hülle.
- **Zusammenfassen.** Wo eine Aufgabe drei fremde Aufrufe braucht, ist
  ein eigenes Werkzeug richtig, das die drei im Code erledigt. Das Modell
  soll die Aufgabe wählen, nicht die Aufrufkette bauen.
- **Nachziehen.** Eine neue Fassung des Servers kann Werkzeuge ändern
  oder ergänzen. Die Fassung wird festgenagelt, und eine Aktualisierung
  läuft gegen die Goldfälle wie jede andere Änderung.
