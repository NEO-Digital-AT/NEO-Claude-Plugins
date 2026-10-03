# Modell und Modellzugang

Lesekonvention siehe `SKILL.md`.

> **Ein Modellwechsel ist keine Reparatur.** Bricht etwas, liegt die
> Ursache in Skill, Werkzeug oder Kontext — dort wird sie behoben.

## Ein Modell

- **Ein Modell trägt das Gespräch:** Es versteht, plant, ruft Werkzeuge
  auf und antwortet.
- **Hilfsdienste mit eigenem Modell sind erlaubt**, wenn das Modell sie
  als Werkzeug aufruft oder sie nur Daten liefern: eine Sprachnachricht
  abschreiben, ein Bild beschreiben, einen alten Verlauf zusammenfassen.
  **Sie entscheiden nichts, prüfen nichts und schreiben dem Kunden
  nichts.**

## Zugang über Requesty

| | Wert |
| --- | --- |
| Basisadresse, OpenAI-kompatibel | `https://router.eu.requesty.ai/v1` |
| Basisadresse, Anthropic-kompatibel | `https://router.eu.requesty.ai` |
| Standort des Routers | Frankfurt, AWS `eu-central-1` |
| Schlüssel | nur aus der Umgebung — nie in Konfiguration, Repository oder Protokoll |

> **Der EU-Router allein hält die Verarbeitung nicht in der EU.** Er hält
> nur die Verarbeitung bei Requesty dort. Das Modell muss ebenfalls in der
> EU laufen; seine Kennung trägt dann eine Regionsangabe — bei Bedrock
> `@eu-central-1`, `@eu-west-1` oder `@eu-north-1`, bei Vertex `@eu`, bei
> Azure `@francecentral` oder `@swedencentral`.

- **Eine Kennung ohne Regionsangabe ist ein Befund**, bevor
  personenbezogene Daten durchlaufen.
- Beleg: <https://docs.requesty.ai/features/eu-routing>, geprüft am
  03.10.2026. Vor dem Verlassen auf eine dieser Angaben erneut nachsehen.

## Fassung und Konfiguration

- **Eine festgenagelte Fassung**, nie ein gleitender Alias.
- **Modell, Basisadresse und Denktiefe (reasoning effort) stehen in der
  Konfiguration**, nie im Code (Skill `neo-ki`).
- **Eine Zeitgrenze je Modellaufruf** ist gesetzt.
- **Je Lauf wird festgehalten, welches Modell angefragt und welches
  geliefert wurde.** Ein Router kann umleiten.

## Ein Modell wechseln

1. **Erst die Ursache, dann das Modell.** Ein Fehler, der sich im Lauf auf
   Skill, Werkzeug oder Kontext zurückführen lässt, wird dort behoben.
2. **Dieselben Abläufe** mit dem alten und dem neuen Modell im Staging,
   sonst nichts geändert (`abnahme.md`).
3. **Gemessen wird der erledigte Auftrag:** Erfolgsquote und Kosten je
   erledigtem Anliegen, einschließlich Wiederholungen — nicht der Preis je
   Token.
4. **Werkzeugaufrufe über mehrere Schritte werden auf der tatsächlichen
   Route geprüft.** Dass ein Anbieter etwas kann, belegt nicht, dass es
   über den Router mit dem eigenen Client geht.
5. **Die Entscheidung trifft der Projektinhaber**, festgehalten als
   Entscheidungsakte (Skill `neo-doku`).
