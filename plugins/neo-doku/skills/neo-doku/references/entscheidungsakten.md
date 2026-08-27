# Entscheidungsakten (ADR)

Lesekonvention siehe `SKILL.md`.

Eine Entscheidungsakte hält fest, **warum** etwas so und nicht anders
gebaut wurde. Ohne sie wiederholt in einem Jahr jemand die verworfene
Variante — meist derselbe Mensch.

## Wann eine entsteht

**Vor der Umsetzung**, nicht danach. Eine Akte, die eine bereits gebaute
Lösung begründet, ist eine Rechtfertigung, keine Entscheidung.

Pflicht bei:

- Wahl oder Wechsel einer Technologie, eines Frameworks, einer
  Bibliothek
- Einer neuen Abhängigkeit (Skill `neo-grundregeln`)
- Datenmodell und Datenhaltung an tragender Stelle
- Authentifizierung, Autorisierung, Mandantentrennung
- Schnittstellenverträgen nach außen
- Zweigmodell, Ausrollung, Umgebungen
- Dem Komponenten-Grundsatz und seinem Wächter
- Jedem riskanten Umbau am Bestand (Skill `neo-sicherheit`)
- Jeder Abweichung von einer NEO-Regel

**Nicht nötig bei:** einer Fehlerbehebung, einer Umbenennung, dem
Einsetzen einer bereits entschiedenen Lösung an einer weiteren Stelle.

Im Zweifel: **eine Akte zu viel kostet zwanzig Minuten, eine zu wenig
kostet eine Woche.**

## Ablage und Nummerierung

```
docs/adr/0001-frontend-stack.md
docs/adr/0002-komponenten-grundsatz.md
docs/adr/0003-backend-stack.md
```

- **`docs/adr/`, sprachneutral.** Akten sind Entwicklerinhalt und werden
  **nicht übersetzt** — auch nicht in Projekten mit mehreren
  Doku-Sprachen.
- Vierstellige, fortlaufende Nummer, **nie neu vergeben**. Eine Nummer
  gehört für immer ihrer Akte.
- Slug im Dateinamen: klein, mit Bindestrich, ohne Umlaute.
- **Eine Akte wird nie gelöscht.** Wird sie überholt, bekommt sie den
  Status „ersetzt" und einen Verweis auf die neue.

## Der Aufbau

```markdown
# ADR <Nummer> — <Titel: die Entscheidung, nicht das Thema>

- **Status:** vorgeschlagen | angenommen | ersetzt durch ADR <n> | verworfen
- **Datum:** JJJJ-MM-TT
- **Grundlage:** worauf sie aufbaut — andere Akten, Regeldateien,
  eine ausdrückliche Anforderung des Projektinhabers (wörtlich zitiert)

## Frage

Die Frage in ein bis drei Sätzen. Nicht die Lösung, die Frage.

## Entscheidung

Was entschieden wurde, im Präsens und in ganzen Sätzen. Mit den
konkreten Werten, Namen und Grenzen — nicht „wir nehmen etwas
Passendes".

## Warum

Die tragenden Gründe. Was den Ausschlag gab.

## Verworfene Möglichkeiten

Je Möglichkeit: was sie gewesen wäre, und warum sie es nicht wurde.
Dieser Abschnitt ist der Grund, warum die Akte in einem Jahr gelesen
wird. Er fehlt nie.

## Folgen

Was sich dadurch ändert — auch das Unangenehme. Was jetzt teurer ist,
was nicht mehr geht, wer davon betroffen ist.

## Was dabei schiefging, damit es nicht wieder passiert

Wird nachgetragen, sobald etwas schiefging. Konkret, mit Fundstelle.
Der wertvollste Abschnitt der ganzen Akte.
```

Der Titel benennt die **Entscheidung**, nicht das Thema: „Das Logo im
Kopfbereich, und warum SVG hier erlaubt ist" statt „Logo".

## Der Abschnitt „Was dabei schiefging"

Ein NEO-Eigenes, aus der Praxis bestehender Projekte. Er wird
**nachgetragen**, wenn beim Bauen oder im Betrieb etwas an dieser
Entscheidung hängen blieb.

Beispiel aus einer solchen Akte:

> **Angelegt wird über das DbSet, nicht über die Navigation.** Der
> Schlüssel steht schon im Initialisierer, und eine nur über
> `page.Assets` gefundene Zeile hält EF für eine bestehende: sie ging
> als UPDATE hinaus, traf null Zeilen und riss die Anfrage mit einer
> Nebenläufigkeitsausnahme ab. **Dritter Fall derselben Falle** — und
> wieder erst im Laufzeitlauf aufgefallen, nicht im Test.

Was ihn wertvoll macht: er nennt das Symptom, die Ursache, die
Fundstelle und dass es **nicht das erste Mal** war. Wer das liest, tappt
nicht hinein.

## Status pflegen

| Status | Bedeutung |
| --- | --- |
| `vorgeschlagen` | Liegt vor, wartet auf die Entscheidung des Projektinhabers |
| `angenommen` | Gilt. Der Code muss ihr entsprechen |
| `ersetzt durch ADR <n>` | Überholt. Bleibt liegen, mit Verweis |
| `verworfen` | Wurde vorgelegt und abgelehnt. Bleibt liegen — auch eine Ablehnung ist eine Information |

**Eine angenommene Akte, der der Code widerspricht, ist ein Befund** —
entweder ist der Code falsch oder die Akte überholt. Beides wird
gemeldet, nichts bleibt stehen.

## Verweise

- Die Akte wird dort verlinkt, wo sie wirkt: in der Regeldatei, in der
  Entwicklerdoku, im Kommentar an der Stelle, die sie betrifft.
- `docs/adr/README.md` listet alle Akten mit Nummer, Titel, Status und
  einem Satz.
- Andere Skills verlangen Akten für ihre Bereiche: `neo-grundregeln`
  (Technologie), `neo-komponenten` (Grundsatz, Frameworkwechsel),
  `neo-sicherheit` (riskante Umbauten), `neo-design` (Entwurf nach der
  Freigabe), `neo-contao` (Erweiterungswahl), `neo-api` (Verträge).
