# Requesty als Modell-Zugang

Lesekonvention siehe `SKILL.md`.

**Modelle werden bei NEO grundsätzlich über Requesty angesprochen, über
den EU-Router.** Kein direkter Anbieterzugang, kein zweiter Weg neben dem
Router, keine Ausnahme ohne dokumentierte Freigabe.

| | Wert |
| --- | --- |
| Basisadresse (OpenAI-kompatibel) | `https://router.eu.requesty.ai/v1` |
| Basisadresse (Anthropic-kompatibel) | `https://router.eu.requesty.ai` |
| Schlüssel | Umgebungsvariable `REQUESTY_API_KEY` |
| Standort des Routers | Frankfurt, AWS `eu-central-1` |
| Modellkennung | `<anbieter>/<modell>`, Policy: `policy/<name>` |

Requesty ist OpenAI-kompatibel: derselbe Aufbau, dieselben Felder,
dieselbe Werkzeugform. Ein bestehender Client wird umgestellt, indem die
Basisadresse und der Schlüssel getauscht werden — sonst nichts.

## Der EU-Router allein reicht nicht

> **Der EU-Router hält die Verarbeitung nur bis zum Router in der EU.**
> Zeigt die Modellkennung auf ein Modell außerhalb der EU, wird die
> Anfrage von dort aus zur Inferenz hinausgeleitet.

Das ist die wichtigste Zeile dieses Textes, und sie wird übersehen, weil
die Adresse „eu" enthält und alles funktioniert.

- **EU-Modelle tragen eine Regionsangabe** in der Kennung — etwa
  `@eu-central-1`, `@eu-west-1`, `@eu-north-1` bei Bedrock, `@eu` bei
  Vertex, `@francecentral` oder `@swedencentral` bei Azure. Modelle eines
  Anbieters, der ohnehin in der EU betreibt, brauchen keine.
- **Eine Kennung ohne Regionsangabe ist ein Befund**, kein Detail. Sie
  gehört vorgelegt, bevor personenbezogene Daten durchlaufen.
- Welche Modelle EU-fähig sind, steht in der Modell-Liste des Anbieters
  (`GET /v1/models`) und im Modellkatalog der Konsole — **nachsehen, nicht
  annehmen**.
- Verarbeitet der Assistent personenbezogene Daten, gehören Standort,
  Auftragsverarbeitung und Trainingsausschluss in die Erklärung, bevor
  gebaut wird (Skill `neo-recht`, Skill `neo-ki`).

Der Adapter `scripts/requesty_adapter.py` warnt bei `--check`, wenn die
Basisadresse nicht der EU-Router ist oder die Modellkennung weder
Regionsangabe noch Policy trägt. Die Warnung ersetzt die Prüfung nicht.

## Der Schlüssel

- **Nur aus der Umgebung**, `REQUESTY_API_KEY`. Nie in der Konfiguration,
  nie im Repository, nie in einer Ausgabe, nie in einem Protokoll (Skill
  `neo-sicherheit`).
- Der Adapter **weist eine Konfiguration ab**, in der ein Schlüsselfeld
  steht — auch ein leeres. Das ist Absicht.
- Für die CI ein **eigener Schlüssel** mit eigener Kostengrenze, getrennt
  vom Betriebsschlüssel. Ein Goldlauf mit fünf Läufen über hundert Fälle
  ist eine spürbare Zahl von Modellaufrufen.
- Der Schlüssel eines Entwicklers liegt lokal in der Umgebung, nicht in
  einer Datei im Projekt.

## Modell festnageln

- **Kennung mit Fassung**, nie ein gleitender Alias. Der Anbieter kann
  hinter einem Alias tauschen; der Assistent ändert sein Verhalten ohne
  eine Codeänderung (`modellwahl.md`).
- **Aus der Konfiguration**, nie aus dem Code (Skill `neo-ki`).
- **Eine Policy ist erlaubt und meist besser**: `policy/<name>` verweist
  auf eine Kette aus Modellen, die der Reihe nach versucht werden. Sie
  fängt Ausfälle und Ratenbegrenzungen ab, ohne dass der Code es merkt.
- **Jedes Kettenglied einer Policy ist ein eigenes Modell** und wird wie
  eines behandelt: EU-fähig, festgenagelt, **gegen dieselben Goldfälle
  gemessen**. Ein Rückfallmodell, das die Goldfälle nicht besteht, ist
  kein Rückfall, sondern ein zweiter, ungeprüfter Assistent.
- Die Kennung — Modell oder Policy — steht in **jedem** Goldfall-Bericht.

## Werkzeugaufrufe und strenge Ausgaben

- Werkzeuge werden im OpenAI-Format übergeben (`tools`, `tool_choice`),
  Ergebnisse als Nachrichten der Rolle `tool` mit `tool_call_id`.
- **Strenge Ausgaben** über `response_format` mit `json_schema` und
  `strict: true` werden unterstützt, aber **nicht von jedem Modell**. Die
  Modell-Liste weist das aus. Für die Einordnung (`absichten.md`) ist das
  die Stelle, an der es zählt.
- Ein strenges Schema hat Bedingungen: alle Felder `required`,
  `additionalProperties: false`, verschachtelte Objekte ebenso. Ein
  Schema, das dagegen verstößt, wird mit **400** abgewiesen — nicht
  stillschweigend gelockert.
- **Wo ein Modell strenge Ausgaben nicht kann**, bleibt nur die lose
  Form: gültiges JSON ohne Schemazwang. Dann prüft der Code das Ergebnis
  selbst, und ein Wert außerhalb der Liste führt zur Rückfallabsicht.
- **Die Prüfung im eigenen Code entfällt nie**, auch bei strengem Modus
  nicht. Der Adapter prüft die Argumente jedes Werkzeugaufrufs gegen das
  Schema und meldet jeden Verstoß als Mangel — genau das fängt, was der
  Anbieter durchgelassen hat.

## Fehler vom Router

| Code | Bedeutung | Was zu tun ist |
| --- | --- | --- |
| 400 | Schema oder Parameter abgewiesen | **Kein Wiederholen.** Das Schema oder der Aufruf ist falsch |
| 401 | Schlüssel ungültig oder gilt nicht für diese Adresse | Umgebung prüfen, nicht wiederholen |
| 404 | Modellkennung gibt es dort nicht | Kennung und Basisadresse prüfen |
| 429 | Ratenbegrenzung | Wiederholen mit wachsendem Abstand, Obergrenze; sonst Policy |
| 5xx | Anbieter gestört | Wiederholen mit wachsendem Abstand; Policy fängt es sauberer ab |

Ratenbegrenzung ist im Betrieb der häufigste Fehler, Schemaabweisung der
zweithäufigste. Beides gehört behandelt, nicht abgewartet: **429 durch
eine Policy und eine Warteschlange, 400 durch ein Schema, das erst gar
nicht abgewiesen wird.**

Zeitüberschreitung, Längengrenze, Ratenbegrenzung je Nutzer und
Kostengrenze sind gesetzt (Skill `neo-ki`).

## Die Konfiguration

```json
{
  "base": "https://router.eu.requesty.ai/v1",
  "model": "policy/assistent-eu",
  "system_prompt": "prompts/system.md",
  "tools": "prompts/tools.json",
  "temperature": 0,
  "max_steps": 8,
  "timeout": 90
}
```

Kein Schlüssel darin. `REQUESTY_BASE_URL` übersteuert die Basisadresse,
wo eine Umgebung das braucht.

```
export REQUESTY_API_KEY="…"
python3 tools/requesty_adapter.py --config assistant.json --check
```

`--check` nennt Router, Modell, Promptgröße und Werkzeugzahl, warnt bei
fehlender EU-Kennung und führt einen echten Aufruf aus. Das ist der erste
Befehl bei jedem Verdacht, dass „irgendetwas mit der Verbindung nicht
stimmt".

**Temperatur 0 für Goldläufe.** Ein Modell bleibt trotzdem nicht
deterministisch — deshalb der Mehrfachlauf (`goldfaelle.md`) —, aber die
Streuung wird kleiner und die Messung damit aussagekräftiger.

## Belege

- EU-Routing, Basisadressen, Regionsangaben und der Hinweis, dass der
  EU-Endpunkt allein die Datenhaltung nicht sichert:
  <https://docs.requesty.ai/features/eu-routing>
- OpenAI-Kompatibilität, Schlüssel aus der Umgebung, Kennungsform:
  <https://docs.requesty.ai/quickstart>
- Strenge Ausgaben, `strict: true`, Bedingungen an das Schema:
  <https://docs.requesty.ai/features/structured-outputs>
- Policies, Rückfallketten, Regionsangaben in der Kette:
  <https://docs.requesty.ai/features/fallback-policies>

Stand der Prüfung: 2026-08. **Vor dem Verlassen auf eine dieser Angaben
nachsehen** — ein Anbieter ändert Adressen und Fähigkeiten (Skill
`neo-grundregeln`, Belegpflicht).
