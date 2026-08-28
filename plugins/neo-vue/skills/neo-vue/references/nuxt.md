# Nuxt und Nuxt UI

Lesekonvention siehe `SKILL.md`.

> **Vor dem Schreiben lesen:** <https://nuxt.com/llms.txt> und
> <https://ui.nuxt.com/llms.txt> (ausführlich `llms-full.txt`).
> Geprüft 2026-08. Dieser Text sagt nicht, wie Nuxt funktioniert — er
> sagt, **wie NEO es verwendet**.

## Die Grenze zwischen Server und Browser

Die wichtigste Grenze im ganzen Framework, und die, an der die
gefährlichsten Fehler passieren.

| Gehört auf den Server | Gehört in den Browser |
| --- | --- |
| Schlüssel, Geheimnisse, Zugangsdaten | Darstellung |
| Direkter Datenbankzugriff | Bedienung |
| Aufrufe fremder Dienste mit Anmeldung | Zustand der Ansicht |
| Rechteprüfung, die zählt | Rechteprüfung, die nur die Anzeige steuert |

- **Was im geteilten Code steht, landet im Browser.** Auch wenn es nur in
  einem `if (import.meta.server)` steht — das Bündel enthält es.
- **Serverrouten für alles, was ein Geheimnis braucht.** Der Browser ruft
  die eigene Route, nicht den fremden Dienst.
- **Laufzeitkonfiguration**: öffentlich und privat getrennt. Was privat
  ist, verlässt den Server nicht.
- **Rechteprüfung im Browser ist Komfort, keine Autorität** (Skill
  `neo-sicherheit`).

## Datenabruf

- **Über die vorgesehenen Wege**, nicht mit einem nackten `fetch` in
  einer Komponente. Sonst wird auf dem Server geladen und im Browser
  gleich noch einmal.
- **Schlüssel setzen**, sonst kann Nuxt nichts wiederverwenden.
- **Fehler behandeln**, nicht nur den Erfolgsfall: jeder Abruf hat einen
  Fehlerzustand in der Ansicht (Skill `neo-design`).
- **Ladezustände sind Teil der Gestaltung**, kein Nachtrag.
- **Nur laden, was die Ansicht braucht.** Ein vollständiges Objekt „für
  später" ist eine Übermittlung zu viel (Skill `neo-ki` für Daten).

## Rendermodus

Je Route bewusst gewählt und **begründet** — daran hängen Ladezeit,
Auffindbarkeit und Kosten.

| Modus | Wofür | Nicht |
| --- | --- | --- |
| Statisch erzeugt | Inhalte, die sich selten ändern | personalisierte Ansichten |
| Auf dem Server gerendert | Inhalte, die Suchmaschinen sehen sollen | reine Arbeitsoberflächen hinter der Anmeldung |
| Nur im Browser | Arbeitsoberflächen hinter der Anmeldung | öffentliche Seiten |

**Hydration-Warnungen sind Fehler.** Sie bedeuten, dass Server und
Browser verschiedene Bäume erzeugt haben — meist wegen Datum, Zufall oder
`window`. Sie werden behoben, nicht weggeklickt.

## Nuxt UI

- **Hinter den `Neo*`-Wrappern**, nie direkt in einer View (Skill
  `neo-komponenten`). Ein Bibliothekswechsel darf keine View anfassen.
- **Das Theme kommt aus Tokens**, über die vorgesehene Konfiguration —
  nicht aus überschriebenem CSS und nie aus `!important`.
- **Die Komponente wird gelesen, bevor sie verwendet wird.** Die
  `llms-full.txt` nennt Props, Slots und Ereignisse; eine erinnerte Prop
  ist der Grund, warum etwas „fast" funktioniert.
- **Barrierefreiheit wird geprüft, nicht angenommen.** Die Bibliothek
  bringt viel mit; Kontrast, Fokusreihenfolge und Bedienziele werden
  trotzdem gemessen (Skill `neo-design`).
- **Keine zweite UI-Bibliothek daneben.** Nuxt UI **oder** Vuetify.

## Module

- **Jedes Modul ist eine Abhängigkeit** und wird vorgelegt: Zweck,
  Alternative, Pflegezustand, Lizenz (Skill `neo-grundregeln`).
- **Kein Modul für etwas, das drei Zeilen wären.**
- Module, die zur Bauzeit Code erzeugen, werden verstanden, bevor sie
  eingebaut werden — sie sind schwer zu debuggen.

## Auslieferung

- **Bündelgröße wird gemessen** und berichtet, nicht geschätzt.
- **Bilder über die Bildkomponente** mit Maßen, damit nichts springt
  (Skill `neo-design`, agentisches Browsen).
- **Schriften selbst ausgeliefert**, nicht von einem fremden Dienst
  (Skill `neo-recht`).
- Die PageSpeed-Zielwerte gelten je Seitenvorlage, mobil (Skill
  `neo-design`, `references/messwerte.md`).
