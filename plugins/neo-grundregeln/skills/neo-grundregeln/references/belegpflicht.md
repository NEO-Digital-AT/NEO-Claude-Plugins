# Belegpflicht — keine Annahmen

Lesekonvention siehe `SKILL.md`.

**Keine Annahmen, keine Spekulationen.** Jede Feststellung ist entweder
belegt oder ausdrücklich als Vermutung gekennzeichnet. Es gibt keinen
dritten Zustand.

## Zulässige Quellen, in dieser Rangfolge

| Rang | Quelle | Beispiel |
| --- | --- | --- |
| 1 | Offizieller Quellcode | Das Repository selbst, die Bibliothek im `vendor`-Ordner |
| 2 | Maschinenlesbarer Vertrag | OpenAPI, JSON Schema, Typdefinitionen, `llms.txt` |
| 3 | Offizielle Dokumentation des Herstellers | docs.contao.org, die Herstellerseite |
| 4 | Offizielles SDK oder Beispiel des Herstellers | — |

**Nicht zulässig als Beleg:** Blogbeiträge, Forenantworten, Antworten
eines Sprachmodells, Erinnerung, Analogie zu einem anderen Produkt,
„das ist üblich".

**Maschinenlesbare Verträge haben Vorrang vor Prosa.** Wo eine OpenAPI
existiert, wird sie gelesen, nicht die Anleitung daneben.

## Bibliotheken: aus der Quelle, nicht aus dem Gedächtnis

**Die API einer Bibliothek wird nachgeschlagen, nie erinnert.** Frameworks
ändern sich schneller, als ein Modell trainiert wird; eine erinnerte
Signatur ist eine Vermutung mit gutem Ruf.

Viele Hersteller liefern ihre Dokumentation inzwischen maschinenlesbar
als `llms.txt` an der Domain-Wurzel — das ist Rang 2. **Vor dem
Schreiben von Code gegen eine dieser Bibliotheken wird sie gelesen:**

| Bibliothek | Quelle | Geprüft |
| --- | --- | --- |
| Nuxt | <https://nuxt.com/llms.txt> | 2026-08 |
| Nuxt UI | <https://ui.nuxt.com/llms.txt>, dazu `llms-full.txt` | 2026-08 |
| Vue | <https://vuejs.org/llms.txt>, dazu `llms-full.txt` | 2026-08 |
| Vuetify | <https://vuetifyjs.com/llms.txt> | 2026-08 |
| Angular | <https://angular.dev/llms.txt> | 2026-08 |
| Flutter | <https://docs.flutter.dev/llms.txt> | 2026-08 |

**Wo es keine gibt**, gilt die Rangfolge oben — offizielle Doku, offizielles
SDK. Für **Laravel** liefert der Hersteller stattdessen **Laravel Boost**:
einen MCP-Server mit Werkzeugen für die eigene Anwendung, mitgelieferten
KI-Richtlinien und einer Dokumentations-Schnittstelle. Wo Boost
verfügbar ist, ist es die Quelle (Skill `neo-php`). Für **.NET** und
**Angular Material** gibt es derzeit keine `llms.txt`; dort wird die
offizielle Dokumentation gelesen.

**Die Liste wird nachgeprüft, nicht geglaubt.** Eine Adresse, die heute
antwortet, kann morgen weg sein; eine, die es nicht gibt, kann dazukommen.
Wer eine neue findet, trägt sie mit Prüfdatum ein.

## Konfiguration wird gelesen, nicht geraten

> **Der Wert steht in der Datei. Es gibt keinen Grund, ihn zu erfinden.**

Vor **jeder** Aussage über eine Einstellung wird die Einstellung gelesen:

```
.env  und  .env.example        Endpunkte, Schlüssel, Regionen, Modelle
config/, appsettings*.json     Fassungen, Grenzwerte, Zeitzonen
CLAUDE.md                      was das Projekt festgelegt hat
```

- **Was dort steht, gilt.** Endpunkt, Router, Modellname, Region,
  Zeitzone, Grenzwert. Ein aus dem Gedächtnis ergänzter Wert ist ein
  erfundener Wert (Kernregel 2) — und er sieht richtig aus, das ist das
  Gefährliche daran.
- **Ein Standardwert des Anbieters ist nicht der Wert des Projekts.**
  Wer einen Endpunkt aus der Anbieterdokumentation nimmt, obwohl in der
  `.env` ein anderer steht, hat die Konfiguration übergangen.
- **Der Modellname ist Konfiguration**, keine Erinnerung. Modelle werden
  umbenannt, abgekündigt und regional getrennt.

### „Funktioniert nicht" ist erst eine Aussage, wenn geprüft wurde

Die Reihenfolge ist bindend, und sie endet **nicht** beim Schlüssel:

```
1  Steht der Wert in der Konfiguration?        lesen, nicht annehmen
2  Wird er vom Code gelesen?                   die Stelle zeigen
3  Kommt er beim Aufruf an?                    ausgeben, maskiert
4  Stimmt das Ziel?                            Endpunkt, Region, Modell
5  Erst dann: liegt es an den Zugangsdaten?
```

**Nie zum Wechseln eines Schlüssels raten, bevor Schritt 4 erledigt
ist.** Ein Schlüssel wird gesperrt, neu erzeugt, überall nachgetragen —
das kostet den Projektinhaber eine halbe Stunde für einen Fehler, der
woanders liegt.

**Der Fall, aus dem diese Regel entstanden ist:** Ein Aufruf schlug fehl.
Gemeldet wurde „der API-Schlüssel funktioniert nicht". Tatsächlich waren
zwei andere Dinge falsch — ein Modellname, den es unter diesem Anbieter
nicht gab, und ein Endpunkt, der **erraten** statt aus der `.env` gelesen
wurde; dort stand der regionale Router, den das Projekt bewusst benutzt.
Der Schlüssel war die ganze Zeit gültig. Er wurde trotzdem gewechselt,
und danach ging es immer noch nicht — weil der Fehler nie dort lag.

## Wenn eine Information fehlt

1. **Dokumentieren, dass sie fehlt** — an der Stelle, an der sie
   gebraucht wird.
2. **Nachfragen.**
3. **Nie raten.** Ein geratener Wert, der zufällig funktioniert, ist
   schlimmer als ein Fehler: er wird nie wieder überprüft.

Ist die Dokumentation einer fremden API nicht öffentlich verfügbar,
werden **genaue Unterlagen vom Anbieter oder vom Projektinhaber
angefordert, bevor gebaut wird**. Unsicheres Anbieterverhalten wird im
Code-Kommentar und in der Doku festgehalten, statt als Annahme
implementiert.

## Fremde Schnittstellen

Vor jeder Integration:

- [ ] Gibt es eine offizielle, maschinenlesbare Spezifikation?
- [ ] Gibt es ein offizielles SDK?
- [ ] Gibt es einen Dokumentations-MCP für diese Technologie?
- [ ] Liegt die Fassung vor, die tatsächlich angesprochen wird?
- [ ] Sind die Fehlerfälle dokumentiert, nicht nur der Erfolgsfall?
- [ ] Sind Grenzen dokumentiert: Ratenbegrenzung, Größen, Zeitüberschreitungen?

**Referenzmaterial je Integration wird im Repository abgelegt** und in
der Regeldatei verlinkt. Eine Integration, deren Grundlage nur im Kopf
existiert, ist beim nächsten Anbieterwechsel verloren.

An der Grenze wird das fremde Modell in das eigene übersetzt. **Kein
fremder Typ wandert bis in die Fachlogik** (Skill `neo-code`).

## MCP-Rollen trennen

| Art | Zweck | Regel |
| --- | --- | --- |
| **Dokumentations-MCP** | Props, Parameter, Beispiele nachschlagen | **Vor** der Implementierung konsultieren, nicht danach |
| **Aktions-MCP** | Werkzeug für Laufzeit-Aktionen an Produktivsystemen | **Keine Dokumentationsquelle.** Wer daraus Verhalten ableitet, rät mit zusätzlichen Schritten |

**MCP-Zugangsdaten nie in Konfigurationsdateien** (Skill
`neo-sicherheit`).

Vor der Implementierung gegen eine fremde Technologie wird geprüft, ob
ein Dokumentations-MCP verfügbar ist. Ist einer da und wird nicht
genutzt, ist das ein Befund.

## Verteilte Systeme: die „Nie annehmen"-Liste

Keine dieser Annahmen ist zulässig, auch wenn sie heute stimmt:

- Kein gemeinsamer Host.
- Kein `localhost` zwischen Diensten.
- Kein gemeinsames Dateisystem.
- Kein direkter Datenbankzugriff vom Frontend.
- Keine feste Topologie, keine feste Anzahl von Instanzen.
- Keine Reihenfolge zwischen Nachrichten.
- Keine Einmalzustellung — alles kann doppelt kommen.
- Keine gemeinsame Uhr.
- Kein gemeinsamer Zwischenspeicher.

**Alles läuft über definierte Schnittstellen.** Wer eine dieser
Annahmen braucht, legt sie als Entscheidung vor.

## Wie eine Behauptung belegt wird

Nicht: „Das Feld ist optional."
Sondern: „Das Feld ist optional — `openapi.json`, `components.schemas.Auftrag`,
`required` enthält es nicht."

Nicht: „Contao kann das."
Sondern: „Contao liefert dafür das Inhaltselement `gallery` —
docs.contao.org/5.x/manual/de/, Abschnitt Inhaltselemente."

**Eine Fundstelle ist eine Datei mit Position oder eine Adresse mit
Abschnitt.** „Steht in der Doku" ist keine Fundstelle.

## Vermutungen kennzeichnen

Wo etwas nicht belegbar ist, wird die Aussage gekennzeichnet und der
Beleg angefordert:

> **Vermutung:** Der Anbieter dürfte bei 429 einen `Retry-After`-Kopf
> senden. In der Dokumentation nicht erwähnt, im Beispiel nicht
> enthalten. Zum Prüfen brauche ich einen echten 429 aus dem Testkonto.

**Nie behaupten „das wird es beheben"**, solange nicht drei Dinge
zutreffen (`selbstkontrolle.md`).
