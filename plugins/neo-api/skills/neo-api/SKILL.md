---
name: neo-api
description: >
  NEO-API-Regeln. Diesen Skill laden bei jeder Arbeit an einer
  Schnittstelle: neuer oder geänderter Endpoint, Controller, Route,
  Vertrag, DTO, Swagger- oder OpenAPI-Dokument, Versionierung,
  Fehlerantworten, Statuscodes, PUT gegen PATCH, Paginierung,
  Idempotenz, Authentifizierung und Scopes, CORS und Cookies, Webhooks,
  Rate Limiting, Hintergrundaufträge, Datenbankmigrationen,
  Statusendpunkt und Überwachung. Ebenso beim Abkündigen einer
  Schnittstelle und beim Anbinden einer fremden API.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg; Struktur nach der API- und Betriebsdoku von LeoFlex (vom Projektinhaber übergeben), Stand 2026-08
---

# NEO-API-Regeln

## Pflicht: Swagger und OpenAPI

Wird an einer API entwickelt, **ist ein OpenAPI-Dokument Pflicht** —
keine Ausnahme, kein „später".

- Die Beschreibung entsteht **aus dem Code**, nicht daneben. Ein von Hand
  gepflegtes Dokument läuft auseinander, sobald es einmal jemand
  vergisst.
- Jeder Endpoint, jeder Parameter, jeder Rückgabetyp und **jede
  Fehlerantwort** ist beschrieben. Ein Endpoint, der nur 200 dokumentiert,
  ist nicht dokumentiert.
- Geschützte Operationen nennen ihren Authentifizierungsmodus und die
  benötigten Rechte in der Beschreibung.
- Die Oberfläche für die Anzeige ist abschaltbar und in Produktion nur
  dort erreichbar, wo es gewollt ist.
- **Das Dokument ist der Vertrag.** Wer die Beschreibung ändert, ändert
  den Vertrag — mit allem, was dazugehört (Versionierung, Abkündigung).

## Dokumente schneiden

Ein einziges Riesendokument findet niemand. Geschnitten wird nach
Fachbereich, mit je einer stabilen und einer Vorschau-Fassung:

```
Authentication
Billing V1              Billing NSFW
Inventory V1            Inventory NSFW
Modules V1              Modules NSFW
Module <Name> V1        Module <Name> NSFW
Onboarding V1           Onboarding NSFW
Platform V1             Platform NSFW
Administration          nur wenn ausdrücklich freigeschaltet
Development             nur in der Entwicklung
Frontend                nicht in der Kundenansicht
Webhooks
```

- **Ein neues Modul bekommt eigene Dokumente** — stabil und Vorschau —
  statt das gemeinsame Modul-Dokument wachsen zu lassen. Das gemeinsame
  Dokument trägt nur die Modulkern-Fläche.
- Verwaltungs- und Entwicklungsdokumente sind über Konfiguration
  geschaltet. Ohne den Schalter existiert die Adresse nicht.
- Innerhalb eines Dokuments wird mit **Tags** gruppiert, nach Sachgebiet,
  nicht nach Controller-Klasse.

Aufbau, Sichtbarkeitsschalter und die Regeln je Dokument:
`references/swagger-dokumente.md`.

## Versionierung

- **Stabil (`v1`)** ändert sich nie brechend. Wer brechen muss, macht
  eine neue Version.
- **Vorschau** (`v0-nsfw` nach der Konvention von apaleo) trägt alles,
  was noch wackelt. Sie ist ausdrücklich instabil und darf brechen.
- Beide Fassungen laufen nebeneinander und werden zusammen gepflegt: was
  in `v1` gefixt wird, wird in der Vorschau mitgefixt.
- Verwaltungsrouten (`/admin/...`) sind unversioniert, aber ihr Dokument
  muss mit den Routen übereinstimmen.
- Abkündigen heißt: ankündigen, Frist nennen, im Dokument markieren,
  dann entfernen — nie umgekehrt.

## Verträge

- **Wiederverwendbare Schemas statt kopierter Felder.** Adresse, Firma,
  Rechnungskontakt, Fehler — jedes davon existiert einmal und wird
  referenziert.
- Requests nie direkt an Entitäten binden; DTOs schützen vor
  Mass Assignment (Skill `neo-sicherheit`).
- Ungültige Nutzlast wird nie still angenommen.
- Felder, die ein Aufrufer nicht braucht, gehören nicht in die Antwort.
  Eine Liste bleibt schlank; Details holt man einzeln.

## Eine Fehlerhülle für alles

Jede Fehlerantwort hat dieselbe Gestalt — auch 401, 403 und 404:

```json
{
  "success": false,
  "errorCode": "E101",
  "message": "Lesbare Meldung",
  "sessionCode": "SESSION-ID"
}
```

- Der `sessionCode` ist **immer** dabei. Er ist das, was ein Anwender dem
  Support nennt.
- Für die konfigurierten Frontend-Herkünfte werden Fehlerantworten
  **mit den CORS-Kopfzeilen** ausgeliefert. Sonst sieht der Browser nur
  einen Transportfehler und der Anwender eine leere Meldung statt der
  echten Ursache.
- Die Meldung ist für Menschen, der Code für Maschinen. Kein Stacktrace,
  keine internen Pfade, keine Datenbankfehler nach außen.

## PUT und PATCH

- **PUT** für vollständiges Ersetzen und für stabile Anlege-oder-Ändern-
  Operationen.
- **PATCH** nur für sichere Teiländerungen, bei denen das Backend die
  erlaubten Pfade ausdrücklich prüft.
- **Arbeitsabläufe sind kein PATCH.** Zyklus erzeugen, Zahlung
  auslösen, Wiederholung anstoßen — das sind eigene Kommandos auf
  eigenen Routen, meist verwaltungsseitig.

## Autorisierung: deny-by-default

- Eine globale Rückfallregel verlangt auf **jedem** Endpoint einen
  authentifizierten Aufrufer, sofern er nichts anderes deklariert.
- Absichtlich anonyme Endpoints tragen die Freigabe **ausdrücklich** —
  Onboarding, Token- und Abmeldewege, Webhooks, signierte Links,
  Gesundheitsprüfungen.
- Folge, die man kennen muss: anonyme Anfragen auf unbekannte Routen
  antworten `401`, nicht `404`. Authentifizierte Aufrufer bekommen
  weiterhin `404`.
- **Zwei Wege auf dieselben Fachrouten:** Sitzungscookie für die eigene
  Oberfläche, Bearer-Token für Integrationen. Beide erzwingen dieselbe
  Mandantentrennung aus dem authentifizierten Kontext.
- Token tragen feingliedrige Lese- und Schreibrechte. Ein pauschales
  Recht ist höchstens ein Altbestand mit Ablaufdatum.
- Bootstrap-Routen der eigenen Oberfläche sind **keine**
  Integrationsendpoints und werden nicht als solche behandelt.

## Betrieb

Migrationen, Webhooks, Rate Limiting, Hintergrundarbeit, Statusendpunkt,
Überwachung und Konfiguration: `references/betrieb.md`. Die harten
Punkte in Kurzform:

- **Nur EF-Core-Migrationen**, kein `EnsureCreated()`. Automatische
  Migration beim Start ist kein Freibrief, Mandantendaten neu anzulegen
  oder zu löschen.
- **Webhooks nach dem Store-First-Modell:** Signatur prüfen, Eintrag samt
  Idempotenzschlüssel speichern, Auftrag einreihen, antworten. Die
  Fachlogik läuft danach im Hintergrund.
- **Rate Limiting nach dem authentifizierten Aufrufer**, nie nach
  Angaben aus Query oder Route. Der Begrenzer läuft nach der
  Authentifizierung.
- **CORS und Cookies kommen ausschließlich aus der Konfiguration.** Keine
  Herkunft, keine Cookie-Domäne, keine Adresse fest im Code.
- **Ein abgesicherter Statusendpunkt** für die externe Überwachung, mit
  Geheimnis im Kopf statt in der Query, ohne Swagger-Eintrag, und nur
  gemappt, wenn das Geheimnis konfiguriert ist.

## Tests

- Endpointverhalten wird geprüft, nicht nur der Statuscode: Struktur und
  Bedeutung der Antwort, bei ändernden Operationen die beobachtbare
  Zustandsänderung.
- Fremde Anbieter werden gefälscht. Keine interaktive Anmeldung, keine
  Mehrfaktor-Abhängigkeit in der CI. Ein echter Anmeldelauf ist ein
  manueller Rauchtest, keine Teststrategie.
- Jede neue Schnittstellenfunktion bekommt ihre Mock-Entsprechung.

## Dokumentation

Das OpenAPI-Dokument beschreibt den Vertrag. Es ersetzt **nicht** die
Backend-Doku unter `docs/backend/<sprache>/` (Skill `neo-doku`): dort
stehen Zusammenhänge, Entscheidungen, Betriebsverhalten und Eigenheiten
fremder APIs — alles, was ein Schema nicht ausdrückt.

**Jeder Endpunkt wird getestet, und zwar auf das, was er liefert** —
sechs Pflichtfälle je Endpunkt, die Antwort gegen das OpenAPI-Schema, und
für schreibende Endpunkte der gelesene Zustand danach:
`references/tests.md`.

Zugehörige Skills: `neo-sicherheit` (Auth, Secrets, Härtung, CRA),
`neo-doku` (Backend-Doku), `neo-deployment` (Ausrollung),
`neo-code` (Aufbau des Codes dahinter), `neo-grundregeln` (Prozess).
