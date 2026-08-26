# Vorlagen

Lesekonvention siehe `SKILL.md`. Existiert im Projekt eine eigene
Vorlage (etwa `docs/VORLAGE.md`), **gilt sie wörtlich** und geht diesen
hier vor.

## Bedienungsseite (Anwenderdoku)

```markdown
---
titel: <Handlung>
kurzfassung: <ein Satz>
zielgruppe: anwender
bereich: frontend
sprache: de
stand: JJJJ-MM-TT
---

# <Handlung>

<Zwei bis drei Sätze: was diese Funktion tut und wann man sie braucht.>

## Voraussetzungen

- <Recht, Einstellung oder Datum, das vorher vorliegen muss>

## Schritte

1. <Handlung mit dem wörtlichen Namen des Bedienelements>
2. <…>

![<Beschreibung des Bildes samt Markierungen>](bilder/<name>.png)

Auf dem Bild markiert Rahmen 1 …, Rahmen 2 …

## Ergebnis

<Was danach sichtbar ist, woran man den Erfolg erkennt.>

## Felder

| Feld | Pflicht | Werte | Vorgabe | Bedeutung |
| --- | --- | --- | --- | --- |

## Häufige Fehler

| Meldung | Ursache | Abhilfe |
| --- | --- | --- |

## Was diese Funktion nicht tut

<Die Abgrenzung. Der Abschnitt, der die meisten Rückfragen erspart.>

## Verwandte Seiten

- [<Titel>](<pfad>) — <ein Satz>
```

## Entwicklerseite

```markdown
---
titel: <Gegenstand>
kurzfassung: <ein Satz>
zielgruppe: entwickler
bereich: backend
sprache: de
stand: JJJJ-MM-TT
---

# <Gegenstand>

## Wozu

<Wofür es da ist, in zwei Sätzen.>

## Aufbau

<Die Bausteine und wie sie zusammenhängen. Fundstellen im Code.>

## Das WARUM

<Warum es so und nicht anders gebaut ist. Verweis auf die
Entscheidungsakte, wo es eine gibt.>

## Eigenheiten

<Was überrascht. Was ein fremdes System falsch macht. Was schon einmal
schiefging.>

## Konfiguration

| Schlüssel | Bedeutung | Vorgabe | Pflicht |
| --- | --- | --- | --- |

## Grenzen

<Was es nicht kann, was es nicht abdeckt, wo es bricht.>

## Tests

<Was getestet ist, was nur theoretisch prüfbar ist, und warum.>
```

## Änderungsprotokoll

`CHANGELOG.md` im Wurzelverzeichnis. Je Eintrag: **was, wann, warum** —
aus Sicht dessen, der es merkt.

```markdown
# Änderungsprotokoll

## 2026-08-26

### Geändert
- Das Intervall eines Monitors lässt sich jetzt auf 30 Sekunden setzen.
  Vorher war 60 Sekunden die Untergrenze; Kunden mit kurzen
  Wartungsfenstern brauchten die feinere Stufe.

### Behoben
- Ein Monitor mit Umlaut im Namen erschien in der Suche nicht.
  Ursache war ein Vergleich ohne Normalisierung.

### Entfernt
- Die Tenant-Benutzerverwaltung unter `/platform/{version}/users`.
  Sie hatte keinen Aufrufer mehr, seit die Anmeldung über die
  eingebettete Oberfläche läuft.
```

- **Kein „diverse Verbesserungen"**, kein „Bugfixes". Wer das schreibt,
  schreibt nichts.
- Eine Änderung, die niemand merkt, gehört nicht hinein.
- Der Eintrag entsteht **im selben Commit** wie die Änderung.

## Übergabe

Als Datei im Repository, an der im Projekt vorgesehenen Stelle.

```markdown
# Übergabe <Datum> — <Thema>

## Stand
Zweig: <name>, letzter Commit: <kurz-hash>

## Erledigt und verifiziert
- <Punkt> — verifiziert durch <Beleg: Testzahl, Log, Screenshot>

## Nicht erledigt
- <Punkt> — <warum: blockiert wodurch, oder bewusst verschoben>

## Belege
- Tests: <grün> von <gesamt>
- <weitere Zahlen, Logauszüge, Messwerte>

## Nächster Schritt
<Was als Erstes zu tun ist, konkret genug zum Anfangen.>

## Offene Entscheidungen
- <Frage> — <Optionen> — <Empfehlung>
```

**Eine Übergabe ohne Belege ist eine Behauptung.** Zahlen gehören
hinein, keine Einschätzungen.

## Inhaltsverzeichnis eines Ordners

Aufbau und Regeln: `references/struktur.md`. Kurzfassung: Links mit je
einem Satz, Reihenfolge nach dem Arbeitsablauf, Unterordner verlinkt,
**eine neue Datei ohne Eintrag gilt als nicht angelegt.**
