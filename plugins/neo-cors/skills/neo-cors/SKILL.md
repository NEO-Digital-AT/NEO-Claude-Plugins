---
name: neo-cors
description: >
  NEO-Regeln für Herkunftsgrenzen im Browser (CORS). Diesen Skill laden,
  **bevor** etwas gebaut wird, das eine Adresse außerhalb der eigenen
  Herkunft lädt oder aufruft: Bild, Video, Audio, Schrift, Symbolsatz,
  Textur, Karte, PDF, Datei-Download, Vorschaubild aus einem
  Medienspeicher oder CDN; `fetch`, `XMLHttpRequest`, `EventSource`,
  ein API-Aufruf aus der Oberfläche, ein Modul- oder Worker-Skript.
  Ebenso bei Canvas, `toDataURL`, `getImageData`, `captureStream`,
  WebGL, three.js-Texturen, Web-Audio und bei jeder Messung oder
  Aufnahme im Browser. Ebenso beim Einrichten eines Vorschauservers,
  eines Entwicklungsservers, eines Prüfstands oder einer CI, die eine
  Seite lädt. Und bei jeder Meldung, die nach CORS klingt:
  `Access-Control-Allow-Origin`, „blocked by CORS policy", „tainted
  canvas", `SecurityError` am Canvas, „Script error." ohne Zeile,
  Preflight, `OPTIONS` mit 401 oder 405, eine Schrift, die stumm
  zurückfällt, ein Aufruf, der mit curl geht und im Browser nicht.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, veranlasst durch wiederholte Ausfälle beim Testen und beim Messen von Oberflächen, Stand 2026-09
---

# NEO-CORS-Regeln

> **Wer etwas über eine Herkunftsgrenze lädt, klärt die Herkunftsfreigabe,
> bevor er baut — nicht, wenn der Browser sie verweigert.**

CORS ist keine Zusatzfrage am Ende. Es ist eine Eigenschaft der Quelle,
aus der geladen wird, und sie steht fest, bevor die erste Zeile
geschrieben ist. Wird sie nicht geklärt, fällt der Fehler **spät** an —
beim Testen, beim Messen, beim Vorführen — und er sieht dort nach etwas
anderem aus: nach einem kaputten Bild, einer fehlenden Schrift, einem
toten Knopf, einem leeren Diagramm.

**Der Prüfschritt kostet eine Minute. Die Fehlersuche kostet einen
Nachmittag, weil niemand an CORS denkt.**

## 1. Die Auslöser: wann geprüft wird

**Sobald eine dieser Stellen entsteht oder geändert wird, wird die
Herkunftsfrage beantwortet — vor dem Bauen, nicht danach:**

| Was gebaut wird | Was geklärt wird |
| --- | --- |
| Bild, Video, Audio, Schrift, Symbolsatz, Textur von einer fremden Adresse | Trägt die Quelle die Freigabe? Braucht das Element `crossorigin`? |
| Etwas davon landet in einem Canvas, in WebGL, in three.js, in Web-Audio | **Immer CORS** — sonst ist die Fläche vergiftet und jede Auswertung bricht |
| `fetch`, `XMLHttpRequest`, `EventSource` auf eine andere Adresse | Freigabe, Preflight, Anmeldedaten, sichtbare Antwortkopfzeilen |
| Die Oberfläche ruft die eigene API unter anderem Namen oder Port auf | Gleiche Herkunft herstellen statt CORS öffnen (Abschnitt 4) |
| Ein Modulskript, eine Quelltextkarte, ein Worker | Modul und Karte brauchen CORS, ein Worker lässt sich fremd gar nicht laden |
| Ein Medienspeicher, ein CDN, ein Objektspeicher wird angebunden | Dessen CORS-Regel ist Teil der Anbindung, nicht der Betrieb danach |
| Ein Vorschauserver, ein Entwicklungsserver, ein Prüfstand, eine CI-Seite | Unter welcher Herkunft läuft die Seite dort? (Abschnitt 6) |

**Die Antwort wird festgehalten**, nicht im Kopf behalten: welche Quelle,
welche Herkunft, welcher Weg, gemessen oder offen. Ein Satz je Quelle
genügt.

## 2. Was CORS ist — und was es nicht ist

CORS ist **keine Absicherung des Servers**. Ein Server, der nur mit CORS
geschützt ist, ist nicht geschützt: Jeder Aufruf ohne Browser — curl,
Skript, anderer Server — kommt ungehindert durch. CORS ist eine
**Lockerung** der Regel „eine Seite liest nur von ihrer eigenen
Herkunft", und der Browser setzt sie durch, niemand sonst. Autorisierung
gehört daneben und unabhängig (Skill `neo-sicherheit`, `neo-api`).

**Herkunft** heißt: Schema, Name und Port zusammen. `https://neo.at` und
`https://api.neo.at` sind verschieden. `http://localhost:5173` und
`http://localhost:8000` sind verschieden. `https://neo.at` und
`http://neo.at` sind verschieden.

**Nicht CORS, sieht aber so aus** — wer hier falsch abbiegt, sucht in der
falschen Ecke:

| Fall | Wer es regelt |
| --- | --- |
| Ein `iframe` lädt nicht | `X-Frame-Options` bzw. CSP `frame-ancestors` |
| Die Seite im `iframe` lässt sich nicht auslesen | Same-Origin-Policy; der Weg ist `postMessage` |
| Eine WebSocket-Verbindung wird abgewiesen | Kein CORS — der Server prüft `Origin` selbst |
| Ein Aufruf wird blockiert, die Meldung nennt eine Richtlinie | CSP `connect-src`, `img-src`, `font-src` |
| Trotz richtiger Freigabe blockiert | `Cross-Origin-Resource-Policy` bzw. `-Embedder-Policy` |
| Ein Cookie reist nicht mit | `SameSite`, `Secure`, Domäne — zusätzlich zu CORS |
| Server ruft Server | Gar keine Herkunftsprüfung |

Einzelheiten und die Abgrenzung je Fall: `references/browser.md`.

## 3. Die Wirkungsrichtung: woran man erkennt, dass es CORS ist

**Jede dieser Beobachtungen zeigt auf etwas anderes, als sie ist.** Das
ist der Grund, warum die Suche so lange dauert:

| Beobachtung | Was es in Wahrheit ist |
| --- | --- |
| Das Bild ist **sichtbar**, aber `toDataURL()` oder `getImageData()` wirft `SecurityError` | Die Fläche ist vergiftet: das Bild kam ohne `crossorigin` |
| Die Schrift fällt stumm auf die Ersatzschrift zurück, Bilder daneben laden | Schriften werden **immer** mit Herkunftsprüfung geladen |
| Der Aufruf geht mit curl, im Browser nicht | Nur der Browser prüft — der Server ist unschuldig |
| Antwort ist 200, der Code kommt trotzdem nicht an den Inhalt | Freigabekopfzeile fehlt; der Browser reicht die Antwort nicht durch |
| `GET` geht, `POST` mit JSON nicht | Preflight: JSON ist keine einfache Anfrage |
| Es geht, bis jemand sich anmeldet | Anmeldedaten mit `*` als Freigabe — diese Kombination weist der Browser ab |
| Es geht mal, mal nicht, je nach Anwender oder Gerät | Zwischenspeicher ohne `Vary: Origin` liefert die falsche Freigabe |
| Ein Kopfzeilenwert der Antwort ist im Code `null` | Nicht freigegeben über `Access-Control-Expose-Headers` |
| `window.onerror` meldet nur „Script error." ohne Zeile | Fremdes Skript ohne `crossorigin` |
| Der Prüfstand zeigt ein leeres Bild, die Anwendung nicht | Der Prüfstand lädt über `file://` — Herkunft `null` |
| Video läuft, aber die Aufnahme daraus ist schwarz | Medienelement ohne `crossorigin` |
| Web-Audio liefert Stille statt Ton | Dasselbe: vergiftete Quelle wird stummgeschaltet |

## 4. Die Rangfolge: gleiche Herkunft schlägt jede Freigabe

**In dieser Reihenfolge, und eine Stufe wird erst genommen, wenn die
darüber nicht geht:**

1. **Gleiche Herkunft herstellen.** Die Oberfläche und was sie lädt
   liegen hinter demselben Namen — ein Pfad statt eines zweiten Namens,
   ein Reverse-Proxy davor, in der Entwicklung der Proxy des
   Entwicklungsservers. **Dann gibt es keine CORS-Frage.** Das ist der
   Regelfall für die eigene API.
2. **Freigabe mit benannten Herkünften**, aus der Konfiguration, nie im
   Code (Skill `neo-api`). Für alles, was tatsächlich von außen kommt.
3. **Die Quelle liefert die Freigabe selbst** — Medienspeicher, CDN,
   Objektspeicher: dort wird die CORS-Regel eingetragen, beim Anbinden.
4. **Geht nichts davon: Rückfrage.** Eine Quelle ohne Freigabe, die
   gebraucht wird, ist eine Entscheidung des Projektinhabers — eigener
   Spiegel, eigener Zwischenspeicher, andere Quelle. Nicht der Agent
   entscheidet das.

## 5. Die verbotenen Abkürzungen

Jede davon macht die Messung grün und das Produkt kaputt:

- **`--disable-web-security`** oder ein Browserstart ohne Sicherheit,
  auch „nur zum Testen". **Was nur mit abgeschalteter Sicherheit läuft,
  läuft nicht.** Ein Prüfstand, der so gestartet wird, misst eine
  Anwendung, die es nicht gibt.
- **Eine Browsererweiterung**, die Kopfzeilen einfügt. Sie beweist
  nichts und steht auf keinem anderen Rechner.
- **Ein öffentlicher CORS-Weiterleitungsdienst.** Fremder Server,
  fremde Verfügbarkeit, fremde Einsicht in die Daten — bei
  Anmeldedaten ein Sicherheitsvorfall (Skill `neo-sicherheit`).
- **`Access-Control-Allow-Origin: *` „vorläufig"**, besonders zusammen
  mit Anmeldedaten. Vorläufig ist der Endzustand, den nie wieder jemand
  anfasst; mit Anmeldedaten weist der Browser die Kombination ohnehin ab.
- **Die Herkunft aus der Anfrage zurückspiegeln, ohne sie zu prüfen.**
  Das ist keine Freigabe, das ist keine Regel — jede fremde Seite darf
  dann im Namen des angemeldeten Anwenders lesen.
- **Das Bild über den eigenen Server durchreichen**, nur um CORS zu
  umgehen, ohne dass es jemand entschieden hat. Ein Spiegel ist eine
  Entscheidung mit Kosten, keine stille Abhilfe.

## 6. Prüfstand, Vorschau und Entwicklung

**Der Prüfstand hat seine eigene Herkunft, und sie ist nicht die der
Anwendung.** Wird über `file://` geladen, ist die Herkunft `null`, und
damit scheitert fast jede Freigabe. Gemessen wird deshalb über einen
Server, nicht über das Dateisystem — auch für eine einzelne HTML-Datei.

Das schließt an die Prüfstandsregeln des Skills `neo-design` an
(`references/pruefstand.md`): Ein Befund, der nur im Prüfstand auftritt,
ist ein Befund über den Prüfstand. **Ein leeres Bild, eine fehlende
Schrift und ein schwarzer Aufnahmeausschnitt sind zuerst
CORS-verdächtig**, bevor sie als Mangel der Anwendung gemeldet werden.

Entwicklungsserver, Proxy-Einträge je Rahmenwerk und der Weg für die CI:
`references/entwicklung.md`.

## 7. Gemessen statt angenommen

**„Die Freigabe ist eingetragen" ist keine Messung.** Gemessen wird
gegen die laufende Quelle, mit der Herkunft, unter der die Oberfläche
später läuft:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cors-check.py \
        https://medien.example.at/bild.jpg --origin https://app.example.at --media
```

Das Werkzeug stellt die Vorabfrage und die echte Anfrage, liest jede
Freigabekopfzeile und meldet die Fälle, die der Browser abweisen wird —
fehlende Freigabe, `*` mit Anmeldedaten, gespiegelte Herkunft ohne
`Vary`, nicht beantwortete Vorabfrage, nicht freigegebene
Antwortkopfzeilen. Rückgabewert ungleich null bei einem Blocker, also
als Tor in der CI verwendbar.

Und vor dem ersten Start, wenn noch nichts läuft:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cors-scan.py src/
```

Das liest den Quelltext und meldet, was sicher falsch ist —
abgeschaltete Browsersicherheit, `*` neben Anmeldedaten, ungeprüft
gespiegelte Herkunft, öffentliche Weiterleitungsdienste, fest
verdrahtete Freigaben — und getrennt davon, **was nachzusehen ist**:
Medien in einem Canvas ohne `crossorigin`, fremde Schriften, fremde
Modulskripte. Die zweite Gruppe sind Hinweise, keine Befunde; was das
Werkzeug nicht sehen kann, sagt es selbst.

Der Befehl `/neo-cors:neo-corspruefung` führt beides an einem Projekt
durch und berichtet je Quelle eine Zeile.

## 8. Abnahme

Vor jeder Fertigmeldung, in der etwas über eine Herkunftsgrenze geladen
wird: `references/pruefliste.md`. Nicht Gemessenes gilt als nicht
erfüllt.

Zugehörige Skills: `neo-api` (Freigaben und Cookies aus der
Konfiguration, Fehlerantworten mit Kopfzeilen), `neo-sicherheit`
(Autorisierung, Geheimnisse, Weiterleitungsdienste), `neo-design`
(Medien in der Oberfläche, Prüfstand), `neo-deployment` und `neo-betrieb`
(Reverse-Proxy, CDN, Zwischenspeicher).
