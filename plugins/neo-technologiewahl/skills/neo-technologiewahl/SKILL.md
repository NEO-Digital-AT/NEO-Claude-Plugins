---
name: neo-technologiewahl
description: >
  NEO-Regeln für Systementscheidungen: welche Sprache, welches Rahmenwerk,
  welches Designsystem, welche Datenbank, welcher Anbieter. Diesen Skill
  laden, sobald eine Technologie gewählt, ersetzt, verworfen oder in Frage
  gestellt wird — bei einem neuen Projekt ebenso wie bei der Frage, ob ein
  laufendes Projekt umgestellt werden soll. Ebenso beim Vergleich von
  Alternativen, beim Abschätzen der Wechselkosten, beim Nachweis durch
  einen Prototyp und beim Schreiben der Entscheidungsakte.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# Systementscheidungen

Lesekonvention siehe `README.md` des Regel-Repositorys.

## Der Satz vorweg

> **Eine Systementscheidung wird einmal getroffen und jahrelang bezahlt.**

Deshalb ist sie keine Geschmacksfrage und kein Bauchgefühl, sondern ein
Verfahren mit Belegen. Und deshalb trifft sie **ausnahmslos der
Projektinhaber** (Kernregel 1). Der Agent legt vor: die Anforderungen, die
Belege, die Kosten, den Nachweis. Er entscheidet nicht — auch dann nicht,
wenn die Antwort eindeutig scheint.

## 1. Erst fragen, dann messen

**Der teuerste Fehler ist nicht die falsche Antwort. Es ist die richtige
Antwort auf die falsche Frage.**

Ein Repository beantwortet, was gebaut wurde. Es beantwortet **nicht**,
was vorgesehen ist. Diese sechs Punkte werden **erfragt**, bevor
irgendetwas gemessen wird — und die Antworten stehen in der
Entscheidungsakte:

| Frage | Warum sie alles dreht |
| --- | --- |
| **Welche Zielplattformen in den nächsten 24 Monaten?** | Eine zweite Plattform kippt jede Ein-Plattform-Empfehlung |
| **Ist das Designsystem verbindlich — und wie weit?** | „Wir folgen X" heißt selten „X ohne Abweichung" |
| **Welche Hardware, welche Peripherie?** | Entscheidet, wie viel Nähe zum Betriebssystem gebraucht wird |
| **Wie lange soll es laufen?** | Drei Jahre und zehn Jahre führen zu verschiedenen Antworten |
| **Wer wartet es in zwei Jahren?** | Nicht wer es baut |
| **Was ist bereits entschieden und darf nicht wackeln?** | Bestehende Akten binden |

**Wer diese Fragen überspringt, misst sauber am Ziel vorbei.** Das ist
kein hypothetischer Fehler: Er ist bei NEO nachweislich passiert und in
einer Entscheidungsakte festgehalten.

## 2. Die Reihenfolge der Kriterien

Kriterien sind nicht gleich schwer. Diese Reihenfolge gilt, bis der
Projektinhaber sie für ein Projekt ausdrücklich ändert:

1. **Ausschluss.** Kann es die harte Anforderung überhaupt? Rechtliche
   Pflicht, Fiskalisierung, Offlinebetrieb, Zertifizierung. Was hier
   durchfällt, wird nicht weiter verglichen.
2. **Zielplattformen**, heute und in 24 Monaten.
3. **Trägt es das Designsystem?** Nicht „hat es Bedienelemente", sondern:
   Lässt sich **das** entworfene Aussehen damit bauen — und wie viel
   Eigenbau kostet das?
4. **Nähe zur Hardware und zum Betriebssystem.** Peripherie, Sensoren,
   Hintergrundarbeit, Kiosk.
5. **Wer pflegt es.** Anbieter, Rhythmus der Fassungen, offene Tickets
   zum eigenen Bedarf, angekündigte Richtung.
6. **Bestand.** Was ist da, was portiert, was ist reines Wissen.
7. **Team und Werkzeuge.** Was können die, die es warten werden.
8. **Lizenz und Kosten**, einschließlich der Kosten des Ausstiegs.

**Punkt 3 wird regelmäßig unterschätzt.** Ein Rahmenwerk, das das
Designsystem nicht mitbringt, kostet bei jeder Komponente erneut — und
die Rechnung kommt in Monat neun, nicht in Woche eins.

## 3. Belege, nicht Meinungen

Es gilt Kernregel 5. Für Technologievergleiche im Besonderen:

| Zählt als Beleg | Zählt nicht |
| --- | --- |
| Offizielle Doku der **eingesetzten** Fassung | Erinnerung an eine frühere Fassung |
| Ticket im Projekt des Anbieters, **mit Datum und Status** | „man liest, dass" |
| Anmerkungen zur Freigabe, Fahrplan des Anbieters | Ein Blogartikel mit Jahreszahl im Titel |
| Eine eigene Messung, mit Bedingungen | Ein Gefühl aus einem früheren Projekt |
| Eine API-Referenz, die zeigt, dass es geht | Ein Beispiel, das etwas Ähnliches zeigt |

- **Jede Aussage über ein fremdes Rahmenwerk trägt ihre Fundstelle** —
  Link und Datum. Ohne Fundstelle ist es eine Vermutung und wird so
  gekennzeichnet.
- **Eine Aussage über die Zukunft ist ein Zitat oder gar nichts.** „Wird
  wohl kommen" ist keine Grundlage; ein datiertes Wort des Anbieters
  schon.
- **Suchergebnisse aus Rangfolgen-Texten sind keine Quelle.** Wer nur
  Vergleichsartikel findet, hat nichts gefunden.

## 4. Wechselkosten ehrlich rechnen

Einzelheiten: `references/wechselkosten.md`.

Ein Wechsel wirkt immer teurer als er ist, weil man die Zeilen sieht —
und immer billiger, weil man die Wiederholung des Lernens vergisst.
Beides wird mit Zahlen aufgelöst:

| Was | Wohin |
| --- | --- |
| **Fachlogik** | wird **portiert**, mit ihren Tests — Zeilen zählen |
| **Oberfläche** | entsteht neu — und wäre in jedem Fall neu entstanden |
| **Pläne, Datenmodell, Schnittstellenentwurf, Fachwissen** | **bleibt** |
| **Übersetzungen, Testdaten, Aufnahmen** | sind Daten und wandern mit |

**Der günstigste Zeitpunkt für einen Schnitt liegt vor der teuersten
Strecke.** Wer die Peripherie noch nicht gebaut hat, wechselt billig; wer
sie gebaut hat, zahlt sie zweimal. Diese Frage wird ausdrücklich
beantwortet, nicht überschlagen.

## 5. Der Nachweis schlägt die Debatte

**Eine Systementscheidung wird nicht ausdiskutiert, sondern
nachgewiesen.**

Wo eine begründete Unsicherheit bleibt — und die bleibt fast immer —,
entscheidet ein **kleiner, echter Nachbau** statt eines weiteren
Arguments:

- **Ein Bildschirm**, nicht die App. Der schwierigste, nicht der
  einfachste.
- **Gegen dieselbe Vorlage** wie das Original, mit denselben Tokens.
- **Auf dem Zielgerät**, nicht im Emulator, wenn das Gerät die Frage ist.
- **Mit einer Frist**: ein bis zwei Tage. Wer länger braucht, hat die
  Antwort auch schon.
- **Mit einem vorher festgelegten Maßstab**: Woran wird erkannt, dass es
  besser ist? Ohne diesen Satz wird jedes Ergebnis als Bestätigung
  gelesen.

Das Ergebnis ist ein Beleg, kein Eindruck — und es kostet weniger als die
dritte Diskussionsrunde.

## 6. Die Entscheidungsakte

**Ohne Akte hat die Entscheidung nicht stattgefunden.** Format und Ablage
regelt Skill `neo-doku`, `references/entscheidungsakten.md`. Für
Systementscheidungen gilt zusätzlich:

- **Die erfragten Antworten aus Abschnitt 1 stehen drin** — sie sind die
  Voraussetzungen, unter denen die Entscheidung gilt.
- **Die verworfenen Alternativen stehen drin**, je mit dem Grund und mit
  Zahlen. Eine Akte ohne Verworfenes ist eine Bekanntmachung.
- **Der Abschnitt „Was dabei schiefging"** ist Pflicht, auch wenn nichts
  schiefging — dann steht das da.
- **Die Akte nennt, wann sie neu zu prüfen ist**: bei welcher geänderten
  Voraussetzung.

## 7. Wann neu entschieden wird

- **Wenn sich eine Voraussetzung ändert.** Eine neue Zielplattform, ein
  Anbieter, der die Richtung wechselt, eine rechtliche Änderung.
- **Nicht, weil jemand unzufrieden ist.** Unzufriedenheit ist ein Anlass
  zu prüfen, ob die Ursache wirklich beim Rahmenwerk liegt — häufig liegt
  sie im fehlenden Vertrag zwischen Entwurf und Umsetzung (Skill
  `neo-design`, `references/entwurfsbruecke.md`).
- **Die alte Akte wird nicht gelöscht.** Sie bekommt einen Status und
  einen Verweis auf die neue.

**Die häufigste falsche Systementscheidung ist die, die ein Problem
lösen soll, das an einer anderen Stelle entsteht.** Bevor ein Rahmenwerk
in Frage gestellt wird, wird die Ursache benannt und belegt.

## 8. Abnahme

Vor jeder Vorlage `references/pruefliste.md` durchgehen. Nicht Geprüftes
gilt als nicht erfüllt.

| Bereich | Referenz |
| --- | --- |
| Die Kriterien im Einzelnen, je mit Prüffragen | `references/kriterien.md` |
| Wechselkosten, Zeitpunkt, was bleibt und was portiert | `references/wechselkosten.md` |
| Abnahme vor der Vorlage | `references/pruefliste.md` |

Zugehörige Skills: `neo-grundregeln` (Entscheidungshoheit, Belegpflicht),
`neo-doku` (Entscheidungsakten), `neo-design`
(`references/entwurfsbruecke.md` — warum ein Rahmenwerk oft
fälschlich beschuldigt wird), `neo-code`, `neo-dotnet`, `neo-php`,
`neo-vue`, `neo-angular`, `neo-mobil` (was NEO tatsächlich einsetzt).
