# An der Quelle: Kopfzeilen, Vorabfrage, Zwischenspeicher

Lesekonvention siehe `SKILL.md`. Browserseite: `browser.md`. Wo die
Werte herkommen — Konfiguration, nie Code — steht im Skill `neo-api`.

## Die Kopfzeilen

**Die Anfrage bringt mit:**

| Kopfzeile | Wann |
| --- | --- |
| `Origin` | bei jeder herkunftsübergreifenden Anfrage; der Browser setzt sie, der Code kann sie nicht fälschen |
| `Access-Control-Request-Method` | nur in der Vorabfrage |
| `Access-Control-Request-Headers` | nur in der Vorabfrage |

**Die Antwort muss liefern:**

| Kopfzeile | Wofür | Ohne sie |
| --- | --- | --- |
| `Access-Control-Allow-Origin` | die Freigabe selbst | Der Browser reicht die Antwort nicht durch |
| `Access-Control-Allow-Credentials: true` | Cookies und Anmeldedaten | Anmeldung wirkt nicht, Antwort wird verworfen |
| `Access-Control-Allow-Methods` | Antwort auf die Vorabfrage | Die eigentliche Anfrage wird nie gesendet |
| `Access-Control-Allow-Headers` | dito, je gesendeter Kopfzeile | dito |
| `Access-Control-Expose-Headers` | welche Antwortkopfzeilen der Code sehen darf | Der Wert ist im Code `null`, obwohl er in den Werkzeugen steht |
| `Access-Control-Max-Age` | wie lange die Vorabfrage gilt | Vor **jeder** Anfrage eine zweite Runde |
| `Vary: Origin` | sobald die Freigabe je Herkunft verschieden ist | Zwischenspeicher liefern die falsche Freigabe |

## Einfach oder mit Vorabfrage

**Ohne Vorabfrage** läuft nur, was ein Formular auch könnte:

- `GET`, `HEAD` oder `POST`, **und**
- als `Content-Type` nur `application/x-www-form-urlencoded`,
  `multipart/form-data` oder `text/plain`, **und**
- keine eigenen Kopfzeilen außer den harmlosen.

**Alles andere löst eine Vorabfrage aus** — und das ist der Regelfall in
jedem echten Projekt:

- `application/json` als Inhaltstyp,
- eine `Authorization`-Kopfzeile,
- `PUT`, `PATCH`, `DELETE`,
- jede eigene Kopfzeile, etwa eine Mandanten- oder Korrelationskennung.

> **Daran scheitert der erste Aufruf fast immer:** `GET` läuft, der
> erste `POST` mit JSON nicht. Nicht der Aufruf ist falsch, die
> Vorabfrage wird nicht beantwortet.

**Die Vorabfrage ist eine `OPTIONS`-Anfrage ohne Anmeldedaten.** Daraus
folgt:

- Sie muss mit **2xx** beantwortet werden, `204` ist üblich.
- **Sie darf nicht durch die Anmeldeprüfung laufen.** Eine
  Sicherheitsschicht, die auf `OPTIONS` mit `401` antwortet, macht jeden
  angemeldeten Aufruf unmöglich — und genau das ist der Fall, der mit
  curl funktioniert und im Browser nicht.
- **Sie darf nicht weiterleiten.** Eine Umleitung in der Vorabfrage
  bricht ab; auch das Ziel einer späteren Umleitung braucht die
  Freigabe.
- Sie muss **jede** Methode und **jede** Kopfzeile nennen, die die echte
  Anfrage verwendet. Was fehlt, wird abgewiesen.

## Die Freigabe selbst

`Access-Control-Allow-Origin` trägt **genau einen** Wert: eine Herkunft
oder `*`. **Eine Liste ist ungültig**, auch mit Komma. Zwei Kopfzeilen
desselben Namens sind ebenfalls ungültig — der häufigste Fall, wenn
Anwendung **und** Reverse-Proxy beide die Freigabe setzen.

Praktisch heißt das: Die Anwendung prüft die Herkunft gegen eine Liste
aus der Konfiguration und **spiegelt die geprüfte Herkunft zurück**.
Dazu gehört zwingend `Vary: Origin`.

```
Access-Control-Allow-Origin: https://app.example.at
Vary: Origin
```

- **Nie ungeprüft spiegeln.** Wer jede ankommende Herkunft
  zurückschreibt, hat keine Regel: Jede fremde Seite liest dann im Namen
  des angemeldeten Anwenders mit.
- **`null` ist keine erlaubte Herkunft.** Sie entsteht bei `file://`,
  in Sandkästen und nach manchen Umleitungen — sie steht nie in der
  Liste.
- Teilmuster („alles unter `.example.at`") werden **ausgeschrieben**
  oder sauber geprüft; ein Vergleich mit „endet auf" lässt
  `example.at.angreifer.tld` durch.

## Anmeldedaten

Sobald der Browser mit `use-credentials` oder
`credentials: 'include'` fragt, gilt:

| Kopfzeile | Mit Anmeldedaten |
| --- | --- |
| `Access-Control-Allow-Origin` | konkrete Herkunft — **`*` weist der Browser ab** |
| `Access-Control-Allow-Credentials` | `true`, sonst wird die Antwort verworfen |
| `Access-Control-Allow-Headers` / `-Methods` / `-Expose-Headers` | `*` gilt hier **wörtlich**, nicht als Platzhalter — alles einzeln nennen |

Dazu die zweite Hälfte, die nichts mit CORS zu tun hat und trotzdem
gebraucht wird: Das Cookie selbst muss herkunftsübergreifend mitreisen
dürfen — `SameSite=None; Secure`, passende Domäne, passender Pfad.
**Beide Hälften fehlen typischerweise einzeln**, und das Fehlerbild ist
dasselbe.

## Sichtbare Antwortkopfzeilen

Der Code sieht von Haus aus nur eine kurze Liste (Inhaltstyp, Länge,
Sprache, Änderungsdatum und ein paar Zwischenspeicherangaben). **Alles
andere ist unsichtbar, bis es freigegeben wird** — auch wenn es in den
Entwicklerwerkzeugen steht.

Die Fälle, die regelmäßig auflaufen:

```
Access-Control-Expose-Headers: Content-Disposition, Location, ETag,
                               X-Total-Count, Content-Range, Accept-Ranges
```

- **`Content-Disposition`** — der Dateiname eines Downloads.
- **`Location`** — die Adresse eines neu angelegten Objekts.
- **`X-Total-Count`** oder wie die Gesamtzahl im Projekt heißt — sonst
  bleibt die Blätterung leer.
- **`ETag`** — ohne ihn kein bedingtes Schreiben.
- **`Content-Range` und `Accept-Ranges`** — für Sprünge in Medien.

## Fehlerantworten tragen die Kopfzeilen mit

Eine `401`, `403`, `422` oder `500` **ohne** Freigabe kommt im Browser
als Transportfehler an: Der Anwender sieht eine leere Meldung statt der
echten Ursache, und im Protokoll steht nichts Brauchbares. Die
Freigabekopfzeilen gehören deshalb an **jede** Antwort, auch an die aus
der Fehlerbehandlung und aus der Ratenbegrenzung (Skill `neo-api`).

## Zwischenspeicher, Reverse-Proxy und CDN

- **`Vary: Origin` ist Pflicht**, sobald die Freigabe je Herkunft
  verschieden ausfällt. Ohne sie liefert ein gemeinsamer
  Zwischenspeicher die Freigabe des vorigen Anwenders — das ist das
  Fehlerbild „geht mal, geht mal nicht".
- **Nur eine Stelle setzt die Kopfzeilen.** Anwendung **oder** Proxy,
  nicht beide; doppelte Freigaben sind ungültig.
- **Ein Proxy, der Kopfzeilen filtert**, entfernt sie manchmal auch:
  Was die Anwendung nachweislich sendet, muss am Ziel noch ankommen —
  gemessen wird deshalb von außen, nicht am Anwendungsprotokoll.
- **Objektspeicher und Medien-CDN führen eine eigene CORS-Regel.** Sie
  gehört in den Anbindungsschritt. Eine signierte Adresse ersetzt sie
  nicht: Die Signatur regelt, **ob** geladen werden darf, die Freigabe,
  **wer im Browser** hineinsehen darf.
- **Bilder für eine Zeichenfläche brauchen die Freigabe am Bild**, nicht
  an der HTML-Seite.

## Vorabfrage zwischenspeichern

`Access-Control-Max-Age` erspart die zweite Runde vor jeder Anfrage.
Die Browser deckeln den Wert unterschiedlich hoch — ein sehr großer
Wert bringt nichts, ein fehlender kostet bei jedem Aufruf eine volle
Umlaufzeit. Wer misst, sieht es sofort: doppelt so viele Anfragen wie
erwartet, jede zweite eine `OPTIONS`.

## Ein Sonderfall in der Entwicklung

Ruft eine öffentlich ausgelieferte Seite eine Adresse im **privaten
Netz** auf — `localhost`, ein Gerät im Hausnetz —, verlangt Chromium
dafür eine zusätzliche Vorabfrage mit eigener Freigabe. Das trifft
Werkstattseiten, Geräteanbindungen und Vorführaufbauten, und es sieht
aus wie ein gewöhnlicher CORS-Fehler, ist aber einer mit anderer
Ursache. Wer so etwas baut, klärt es vorher (`entwicklung.md`).

## Die häufigsten Falscheinstellungen

| Einstellung | Was wirklich passiert |
| --- | --- |
| `Access-Control-Allow-Origin: *` mit Anmeldedaten | Der Browser weist die Kombination ab — es geht **gar nicht** |
| Herkunft ungeprüft gespiegelt | Keine Regel; fremde Seiten lesen im Namen des Anwenders |
| Freigabe gespiegelt, `Vary: Origin` fehlt | Falsche Freigabe aus dem Zwischenspeicher |
| `OPTIONS` läuft durch die Anmeldeprüfung | Jeder angemeldete Aufruf scheitert, curl aber nicht |
| Freigabe nur am Erfolgsfall | Fehler kommen als leere Meldung an |
| Anwendung und Proxy setzen beide | Doppelte Kopfzeile, ungültig |
| Liste in einer einzigen `Allow-Origin`-Zeile | Ungültig, wirkt wie gar keine Freigabe |
| Kopfzeile gesetzt, aber nicht freigegeben | Im Code `null`, in den Werkzeugen sichtbar |
| Freigabe im Code statt in der Konfiguration | Für jede Umgebung ein neuer Bau (Skill `neo-api`) |
