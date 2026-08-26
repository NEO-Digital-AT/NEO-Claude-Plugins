# Datenmodell

## Benennung

- **Englisch, einheitlich, ohne Abkürzungen.** Ein Feld heißt
  `created_at`, nicht `crdt`.
- Ein Schreibstil je System: entweder durchgehend `snake_case` oder
  durchgehend die Konvention des ORM. Gemischt ist der Zustand, den
  niemand mehr repariert.
- Tabellennamen im **Plural** oder durchgehend im Singular — einmal
  entscheiden, festhalten, nie mischen.
- Ein Begriff je Sache, gleich wie im Code und in der API: heißt es dort
  `property`, heißt die Tabelle nicht `location`.
- Fremdschlüsselfelder tragen den Namen der Zieltabelle plus `_id`.
- Zeitfelder enden auf `_at` und sind Zeitpunkte in UTC; reine Daten
  enden auf `_on` und haben keine Uhrzeit (Skill `neo-code`,
  `references/querschnitt.md`).
- Wahrheitsfelder werden positiv benannt: `is_active`, nicht
  `is_not_disabled`. Doppelte Verneinung im Datenmodell rächt sich in
  jeder Abfrage.

## Schemata

- **Ein Schema je Modul bzw. Fachbereich**, dazu ein Kernschema für das,
  was alle brauchen. Das hält Zuständigkeit und Rechte sauber trennbar
  und macht sichtbar, wer wem gehört.
- Ein Modul liest nicht direkt in den Tabellen eines anderen Moduls. Der
  Weg führt über dessen Dienst oder über eine ausdrücklich vereinbarte
  Sicht.
- Erzeugte oder gespiegelte Daten eines Fremdsystems werden nicht
  gehortet: gespeichert wird, was zur Wiedererkennung und Idempotenz
  nötig ist, nicht der ganze fremde Bestand.

## Mandantentrennung

- **Jede mandantenbezogene Tabelle trägt die Mandantenkennung**, und
  jeder Zugriff filtert darauf — ausnahmslos.
- Die Kennung kommt aus den authentifizierten Ansprüchen, nie aus einem
  Parameter (Skill `neo-sicherheit`).
- Wo das ORM es hergibt, erzwingt ein globaler Filter die Trennung, damit
  eine vergessene Bedingung nicht zum Datenabfluss wird. Der Filter ist
  die zweite Verteidigungslinie, nicht die erste.
- Eindeutigkeiten gelten **je Mandant**, nicht global: eine Kundennummer
  darf bei zwei Mandanten gleich sein.
- Ein Test prüft, dass ein Mandant die Daten eines anderen nicht sieht —
  für jede neue Tabelle.

## Schlüssel und Indizes

- Ein technischer Primärschlüssel. Fachliche Werte sind kein
  Primärschlüssel, auch wenn sie heute eindeutig sind.
- Nach außen sichtbare Kennungen sind nicht hochzählbar
  (`references/querschnitt.md`).
- **Fremdschlüssel werden gesetzt**, mit ausdrücklich gewählter Regel für
  Löschen und Ändern. Eine Beziehung ohne Fremdschlüssel ist eine
  Beziehung ohne Garantie.
- **Jeder Fremdschlüssel bekommt einen Index.** Ohne ihn wird jedes
  Löschen in der Elterntabelle zum vollen Tabellendurchlauf.
- Indizes entstehen aus tatsächlichen Abfragen, nicht auf Verdacht. Ein
  unbenutzter Index kostet bei jedem Schreiben.
- Eindeutigkeiten stehen als Bedingung in der Datenbank, nicht nur in der
  Anwendung. Zwei gleichzeitige Anfragen umgehen jede Prüfung im Code.

## Löschen: weich oder hart

| Art | Wann | Worauf zu achten ist |
| --- | --- | --- |
| **Hart** | Der Datensatz soll wirklich weg sein — und muss es rechtlich | Kaskaden bewusst festlegen; Verweise vorher auflösen |
| **Weich** (Kennzeichen plus Zeitpunkt) | Rückgängig soll möglich sein, oder Historie hängt daran | **Jede** Abfrage muss filtern; Eindeutigkeiten müssen den gelöschten Stand ausschließen |

- **Weiches Löschen ist kein Löschen im Sinne des Datenschutzes.** Wo
  eine Frist abgelaufen ist, wird hart gelöscht oder anonymisiert
  (Skill `neo-recht`, `references/loeschkonzept.md`).
- Wer weich löscht, muss den Weg zum harten Löschen mitbauen — sonst
  wächst ein Bestand, den niemand mehr anfassen will.
- Ein weich gelöschter Datensatz darf in keiner Auswertung, keinem
  Export und keiner Zählung auftauchen.

## Historie und Archiv

- Was fachlich nachvollziehbar sein muss (Preise, Steuersätze,
  Vertragsstände), wird **mit dem Vorgang gespeichert**, nicht bei der
  Anzeige neu geholt. Sonst ändert sich eine alte Rechnung rückwirkend.
- Änderungsprotokolle sind aus Anwendungssicht unveränderlich
  (Skill `neo-sicherheit`).
- Große, alte Bestände wandern in eine Archivtabelle, statt jede Abfrage
  zu bremsen — mit demselben Löschkonzept wie die Ursprungsdaten.

## Migrationen

- Nur Migrationen, nie Handarbeit, nie Neuaufbau (Skill `neo-api`,
  `references/betrieb.md`).
- **Trennen, was trennbar ist:** erst die Spalte hinzufügen, dann füllen,
  dann umschalten, dann die alte entfernen. Vier kleine Schritte laufen
  ohne Ausfall; ein großer nicht.
- Eine Migration, die Daten verändert, wird gegen eine Kopie des Bestands
  gefahren, bevor sie in die Produktion geht.
- Vor der Migration eine geprüfte Sicherung (Skill `neo-betrieb`).

## Testdaten

- Isoliert oder aufgeräumt — nie im Produktivbestand.
- **Keine echten Kundendaten in Entwicklung und Test.** Wird ein
  Produktivstand für eine Fehlersuche gebraucht, wird er vorher
  anonymisiert, und der Vorgang ist freigegeben und dokumentiert.
- Demodaten sind als solche erkennbar und plausibel, damit Oberflächen
  damit beurteilbar sind (Skill `neo-design`).
