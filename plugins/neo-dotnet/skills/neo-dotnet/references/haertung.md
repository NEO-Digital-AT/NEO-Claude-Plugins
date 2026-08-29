# Härtung der Serveranwendung

Lesekonvention siehe `SKILL.md`.

Was Sicherheit grundsätzlich heißt, steht im Skill `neo-sicherheit`;
Verträge und Autorisierungsregeln der Schnittstelle im Skill `neo-api`.
Hier steht, **womit** das in ASP.NET Core durchgesetzt wird — die
Stellen, an denen eine richtige Regel ohne den passenden Schalter
wirkungslos bleibt.

## Autorisierung: die Rückfallregel entscheidet

**Deny-by-default ist kein Vorsatz, sondern eine Zeile im Start.**

Ohne eine globale Rückfallregel ist jeder Endpunkt offen, an den niemand
ein Attribut geschrieben hat — und genau der wird vergessen. Die Regel
verlangt auf **jedem** Endpunkt einen authentifizierten Aufrufer; was
öffentlich sein soll, wird **einzeln** und sichtbar freigegeben.

- **Die Ausnahmen sind zählbar** und stehen an einer Stelle: Anmeldung,
  Health, Impressum. Wächst die Liste, ist das ein Befund.
- **Ein Test beweist die Rückfallregel**: ein Aufruf ohne Anmeldung
  gegen einen beliebigen Fachendpunkt bekommt 401, nicht 200.
- Rollen und Rechte gehören in **Richtlinien**, nicht als Zeichenkette in
  jedes Attribut verstreut.
- **Der Mandant kommt aus dem Anspruch des Angemeldeten**, nie aus einem
  Feld der Anfrage (Skill `neo-sicherheit`).

## Ratenbegrenzung

ASP.NET Core bringt sie mit; sie muss nur eingeschaltet und zugeordnet
werden.

- **Nach dem authentifizierten Aufrufer**, nicht nach der Adresse —
  hinter einem Zwischenserver teilen sich sonst alle eine Grenze.
- **Anmeldung, Kennwortrücksetzung und alles, was Kosten auslöst,
  bekommen eine eigene, engere Grenze.**
- **Die Antwort ist 429 mit `Retry-After`**, in derselben Fehlerhülle wie
  alles andere (Skill `neo-api`).
- **Die Grenze wird protokolliert**, sonst merkt niemand, dass sie greift.

## Grenzen der Anfrage

Eine Anwendung ohne Grenzen kippt am ersten Tag, an dem jemand sie
ausprobiert.

- **Höchstgröße des Rumpfes** gesetzt, ausdrücklich — auch bei Uploads,
  und dort zusätzlich je Teil.
- **Höchstzahl und Höchstgröße hochgeladener Dateien**, dazu die
  erlaubten Typen als **Positivliste**, geprüft am Inhalt und nicht an
  der Endung.
- **Zeitgrenzen für das Lesen der Anfrage**, damit ein langsamer Sender
  keinen Platz belegt.
- **Tiefe und Länge bei der Deserialisierung begrenzt.**

## Serialisierung

- **`System.Text.Json`** mit ausdrücklichen Einstellungen, nicht mit dem,
  was zufällig voreingestellt ist.
- **Keine Typinformationen aus der Anfrage**, unter keinen Umständen —
  daraus wird Codeausführung.
- **Eigene Eingabetypen je Endpunkt**, nie die Entität. Sonst setzt eine
  Anfrage ein Feld, das niemand gemeint hat (Überposten) — der Grund,
  warum ein Endpunkt seine Eingabe als eigenen Typ annimmt und nicht als
  Modell aus der Datenbank.
- **Was hinausgeht, ist ebenfalls ein eigener Typ**: keine Entität mit
  allen Beziehungen und keine internen Felder in einer Antwort.

## CORS und Kopfzeilen

- **CORS ausdrücklich**, mit benannten Ursprüngen. `AllowAnyOrigin`
  zusammen mit Anmeldedaten ist verboten und wird vom Rahmenwerk zu
  Recht abgelehnt.
- **Sicherheitskopfzeilen** nach Skill `neo-sicherheit`,
  `references/haertung.md` — die Liste steht dort, sie wird hier nicht
  wiederholt.
- **Antiforgery**, wo mit Cookies angemeldet wird. Bei reiner
  Token-Anmeldung entfällt es — das ist eine Entscheidung, die benannt
  wird, keine Auslassung.

## Zeit

- **Die Zeit kommt aus `TimeProvider`**, nicht aus `DateTime.Now`.

Zwei Gründe, beide praktisch: `DateTime.Now` liefert im Container die
Zeitzone des Containers, nicht die des Anwenders — und ein Test, der ein
Verhalten „am Monatsersten" prüfen will, kann die Uhr nicht stellen. Mit
`TimeProvider` schon (`FakeTimeProvider` aus
`Microsoft.Extensions.Time.Testing`).

- **Gespeichert wird UTC**, angezeigt wird in der Zeitzone des Anwenders.
- **`DateTimeOffset` für Zeitpunkte**, `DateOnly` für Datumsangaben ohne
  Uhrzeit.
- Ein `DateTime.Now` im Fachcode ist ein Befund.

## Geheimnisse und Protokolle

Gilt Skill `neo-sicherheit`, `references/secrets-und-logging.md`.
Zusätzlich für .NET:

- **Keine Verbindungszeichenfolge in `appsettings`**, auch nicht die zur
  Testdatenbank.
- **Ausnahmen werden mit Kontext protokolliert**, nicht mit dem ganzen
  Objekt — ein serialisiertes Anfrageobjekt im Protokoll ist die
  häufigste Art, Personendaten zu verlieren.
- **Der ausführliche Health-Zustand ist abgesichert.** Er nennt
  Datenbanknamen, Fassungen und erreichbare Dienste — für einen
  Angreifer ein Lageplan.

## Abnahme

- [ ] Globale Rückfallregel setzt Authentifizierung durch; die
      öffentlichen Endpunkte sind **einzeln benannt und gezählt**.
- [ ] Ein Test belegt: unangemeldeter Aufruf eines Fachendpunkts → 401.
- [ ] Ratenbegrenzung nach dem authentifizierten Aufrufer, engere Grenze
      für Anmeldung und kostenauslösende Endpunkte, Antwort 429 mit
      `Retry-After`.
- [ ] Höchstgröße für Rumpf und Uploads gesetzt, Dateitypen als
      Positivliste am Inhalt geprüft.
- [ ] Eigene Ein- und Ausgabetypen je Endpunkt; keine Entität am Rand.
- [ ] CORS mit benannten Ursprüngen; kein `AllowAnyOrigin` mit
      Anmeldedaten.
- [ ] Antiforgery gesetzt oder die Entscheidung dagegen benannt.
- [ ] Kein `DateTime.Now` im Fachcode; Zeit über `TimeProvider`,
      gespeichert in UTC.
- [ ] Keine Geheimnisse in Konfiguration oder Protokoll; ausführlicher
      Health-Zustand abgesichert.
