# Im Browser: was welche Quelle braucht

Lesekonvention siehe `SKILL.md`. Serverseite und Kopfzeilen:
`server.md`. Entwicklung, Vorschau und Prüfstand: `entwicklung.md`.

## Zwei Fragen, nicht eine

Bei jeder fremden Quelle stehen **zwei** Fragen nebeneinander, und die
zweite wird regelmäßig vergessen:

1. **Lädt es?** Erscheint das Bild, spielt das Video, kommt die Antwort
   an?
2. **Darf der Code hinein?** Darf JavaScript die Bildpunkte lesen, die
   Antwort auswerten, den Ton verarbeiten, die Kopfzeile sehen?

**Ein Ja auf Frage 1 sagt nichts über Frage 2.** Genau das ist die
Falle: Das Bild ist da, und trotzdem bricht die Auswertung.

## Je Quelle

| Quelle | Lädt ohne Freigabe | Code darf hinein | Was zu tun ist |
| --- | --- | --- | --- |
| `<img>`, `<video>`, `<audio>` nur zum Anzeigen | ja | — | nichts |
| dasselbe, aber der Inhalt wird ausgewertet | ja | **nein** | `crossorigin` **und** Freigabe an der Quelle |
| Schrift über `@font-face` | **nein** | — | Freigabe an der Quelle, immer |
| `fetch`, `XMLHttpRequest`, `EventSource` | — | **nein** | Freigabe, je nach Anfrage mit Vorabfrage |
| Klassisches `<script>` | ja | Fehler bleiben stumm | `crossorigin` für brauchbare Fehlermeldungen |
| `<script type="module">`, `import()` | **nein** | — | Freigabe, immer |
| Quelltextkarte einer fremden Datei | **nein** | — | Freigabe, sonst kein Debuggen |
| Worker-Skript | **nein** | — | CORS hilft nicht — siehe unten |
| Textur in WebGL oder three.js | ja, aber unbrauchbar | **nein** | `crossorigin` **und** Freigabe |
| Untertitelspur `<track>` | **nein** | — | `crossorigin` am Medienelement und Freigabe |

## Die vergiftete Fläche

Ein Bild von fremder Herkunft, das **ohne** Herkunftsprüfung geladen
wurde, **vergiftet** jede Zeichenfläche, in die es gezeichnet wird. Die
Fläche zeigt es weiterhin an — aber jeder Lesezugriff bricht:

```
DOMException: Failed to execute 'toDataURL' on 'HTMLCanvasElement':
Tainted canvases may not be exported.
```

Betroffen sind `toDataURL()`, `toBlob()`, `getImageData()`,
`captureStream()` und alles, was darauf aufbaut: Zuschneiden,
Vorschaubilder, Farbanalyse, Wasserzeichen, Aufnahmen, Diagrammexport.

**WebGL ist strenger:** Dort wirft schon das Hochladen der Textur
(`texImage2D`), nicht erst das Auslesen. Der Fehler kommt also früher,
aber an einer Stelle, die niemand mit dem Bild in Verbindung bringt.

## `crossorigin` richtig setzen

```html
<!-- Anzeige genügt: nichts zu tun -->
<img src="https://medien.example.at/foto.jpg" alt="…">

<!-- Der Inhalt wird ausgewertet: mit Herkunftsprüfung laden -->
<img src="https://medien.example.at/foto.jpg" crossorigin="anonymous" alt="…">
```

```js
// Reihenfolge ist Pflicht: erst crossOrigin, dann src.
const bild = new Image()
bild.crossOrigin = 'anonymous'   // danach gesetzt wirkt es nicht
bild.src = adresse
```

| Wert | Bedeutung |
| --- | --- |
| nicht gesetzt | keine Herkunftsprüfung; lädt, vergiftet die Fläche |
| `anonymous` (auch `crossorigin=""`) | Prüfung ohne Anmeldedaten; **ohne Freigabe lädt es gar nicht mehr** |
| `use-credentials` | Prüfung mit Cookies; die Quelle muss Herkunft **und** Anmeldedaten freigeben |

> **`crossorigin` macht das Laden strenger, nicht lockerer.** Wer es
> setzt und die Quelle liefert keine Freigabe, hat statt eines
> vergifteten Bildes gar keines. Beides wird gemessen, bevor es gebaut
> wird.

**Ein Bild, das an einer Stelle mit und an einer anderen ohne
Herkunftsprüfung geladen wird, ist für den Browser nicht dieselbe
Anfrage.** Es wird doppelt geholt, und welche Fassung im
Zwischenspeicher liegt, erklärt die Berichte „bei mir geht es". Die
Einstellung gehört deshalb an **eine** Stelle — in die Komponente, die
das Bild lädt (Skill `neo-komponenten`), nicht in jede View.

## Schriften

**Schriften werden immer mit Herkunftsprüfung geladen**, ohne dass
irgendwo `crossorigin` steht. Eine fremde Schrift ohne Freigabe fällt
deshalb **stumm** auf die Ersatzschrift zurück — keine Fehlermeldung im
Layout, nur ein anderes Schriftbild, das niemandem auffällt, der die
richtige nie gesehen hat.

- Die Freigabe muss an der Quelle der Schriftdatei stehen, nicht am
  Stylesheet.
- Wird die Schrift vorgeladen, trägt auch das Vorladen die Prüfung:
  `<link rel="preload" as="font" crossorigin>` — ohne das Attribut wird
  sie **zweimal** geholt und das Vorladen ist wirkungslos.
- NEO liefert Schriften ohnehin selbst aus, nicht von einem fremden
  Dienst (Skill `neo-design`, `references/webseiten.md`). Dann stellt
  sich die Frage nicht — und genau deshalb fällt sie auf, wenn doch
  jemand eine fremde einbindet.

## Skripte, Module und Quelltextkarten

- **Klassisches `<script src>`** läuft auch ohne Freigabe. Aber jeder
  Laufzeitfehler daraus erreicht die Fehlerbehandlung nur als
  `Script error.` ohne Datei, Zeile und Kontext. Wer fremde Skripte
  überwacht, setzt `crossorigin="anonymous"` und braucht dafür die
  Freigabe.
- **Prüfsummen (`integrity`) an einer fremden Adresse verlangen
  `crossorigin`.** Ohne das Attribut wird die Prüfsumme nicht angewandt
  und das Skript abgelehnt.
- **Modulskripte werden immer geprüft** — `<script type="module">` und
  jedes dynamische `import()`. Ohne Freigabe lädt nichts.
- **Quelltextkarten** einer fremden Adresse brauchen ebenfalls die
  Freigabe, sonst zeigen die Entwicklerwerkzeuge nur die gebaute Datei.

## Worker

**Ein Worker-Skript wird nicht von fremder Herkunft geladen.** Das ist
keine CORS-Frage, das ist eine Grenze: `new Worker('https://fremd/…')`
scheitert, mit oder ohne Freigabe.

Der Weg ist, das Skript aus der eigenen Herkunft auszuliefern. Der
verbreitete Umweg über einen Blob (`fetch` mit Freigabe →
`createObjectURL`) funktioniert, ist aber eine Entscheidung mit Folgen
für Inhaltsrichtlinie und Fehlersuche — also vorlegen, nicht
stillschweigend einbauen.

## three.js und WebGL

- Der Texturlader von three.js lädt mit Herkunftsprüfung
  (`crossOrigin`); eine Quelle ohne Freigabe wirft beim Hochladen der
  Textur, nicht beim Zeichnen.
- **Vor der ersten Szene steht die Frage, woher die Texturen, Modelle,
  Umgebungskarten und Schriftatlanten kommen** — aus dem eigenen Bestand
  oder von fremder Adresse. Kommt etwas von fremd, gehört die Freigabe
  in die Anbindung, nicht in die Fehlersuche.
- Eine Aufnahme der Szene (`toDataURL`, `readPixels`) bricht, sobald
  **eine einzige** Quelle ungeprüft war. Der Fehler nennt die Quelle
  nicht.

## Video, Untertitel, Aufnahme

- Ein Video anzuzeigen braucht keine Freigabe. **Ein Bild daraus zu
  nehmen** — `drawImage` in eine Fläche, `captureStream`, ein
  Vorschaubild — braucht `crossorigin` und Freigabe.
- **Untertitelspuren von fremder Adresse brauchen beides**, sonst
  bleiben sie leer.
- Bereichsanfragen (Sprünge im Video) brauchen die Freigabe ebenfalls,
  sobald mit Prüfung geladen wird; die Quelle muss `Range` zulassen
  (`server.md`).

## Web-Audio

- Ein Medienelement ohne Herkunftsprüfung, das in den Audiograph geht
  (`createMediaElementSource`), liefert **Stille**. Kein Fehler, kein
  Hinweis — der Ton ist einfach weg.
- `decodeAudioData` arbeitet auf einem geholten Puffer; die Freigabe
  braucht dann die Abfrage, nicht das Element.

## Was **nicht** CORS ist

| Beobachtung | Zuständig |
| --- | --- |
| Ein `iframe` bleibt leer, die Konsole spricht von Einbettung | `X-Frame-Options`, CSP `frame-ancestors` |
| Der Inhalt eines `iframe` lässt sich nicht lesen | Same-Origin-Policy; Weg: `postMessage` mit geprüftem Absender |
| Eine WebSocket-Verbindung wird abgewiesen | Kein CORS; der Server prüft `Origin` selbst und muss es auch |
| „Refused to connect/load … violates Content Security Policy" | CSP des Projekts, nicht die Quelle |
| Freigabe stimmt, es wird trotzdem blockiert | `Cross-Origin-Resource-Policy` an der Quelle, oder die Seite läuft unter `Cross-Origin-Embedder-Policy: require-corp` |
| Ein Formular sendet an eine fremde Adresse und wird nicht blockiert | Formularabsenden ist eine Navigation, keine Leseanfrage — CORS greift hier nicht, die Absicherung liegt am Server |
| Das Cookie reist nicht mit | `SameSite=None; Secure`, Domäne, Pfad — **zusätzlich** zu `use-credentials` |

Der letzte Punkt ist der häufigste Doppelfehler: Anmeldedaten brauchen
**beide** Seiten — die Freigabe im CORS-Sinn und ein Cookie, das
überhaupt mitreisen darf.
