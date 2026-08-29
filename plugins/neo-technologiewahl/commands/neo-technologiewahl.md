---
description: Eine Systementscheidung vorbereiten — erfragen, belegen, rechnen, nachweisen, vorlegen. Die Entscheidung trifft der Projektinhaber.
---

Bereite eine Systementscheidung vor. **Du entscheidest nicht** — du legst
vor (Kernregel 1).

Lade zuerst den Skill `neo-technologiewahl`.

## 1. Erfragen, bevor du misst

Stelle diese sechs Fragen und **warte die Antworten ab**. Ohne sie misst
du am Ziel vorbei:

1. Welche Zielplattformen — heute und in 24 Monaten?
2. Ist das Designsystem verbindlich, und wie weit? Darf abgewichen werden?
3. Welche Hardware und welche Peripherie?
4. Wie lange soll das Ergebnis laufen?
5. Wer wartet es in zwei Jahren?
6. Was ist bereits entschieden und darf nicht wackeln?

Lies die vorhandenen Entscheidungsakten, bevor du fragst — und frage
nicht, was dort schon steht.

## 2. Bestand messen

Nicht schätzen. Zeilen je Schicht und Paket, Anteil Oberfläche gegen
Logik, Zahl der Plattformkanäle und fremden Pakete. Berichte die Zahlen.

## 3. Belegen

Je Alternative und je Kriterium eine Fundstelle **mit Datum**. Offizielle
Doku, Ticket des Anbieters, Anmerkungen zur Freigabe, API-Referenz. Keine
Vergleichsartikel. Was du nicht belegen kannst, kennzeichnest du als
Vermutung.

## 4. Rechnen

Wechselkosten nach `references/wechselkosten.md`: portiert, neu, bleibt,
wandert mit. Benenne die **teuerste Strecke** und ob sie schon gebaut
ist. Rechne auch die Kosten des Bleibens.

## 5. Nachweisen

Schlage einen **Nachbau** vor: ein Bildschirm oder ein Endpunkt, der
schwierigste, auf dem Zielgerät, mit Frist. Lege **vorher** fest, woran
erkannt wird, dass es besser ist. Ohne diesen Satz wird jedes Ergebnis
als Bestätigung gelesen.

## 6. Vorlegen

```
Voraussetzungen      <die sechs Antworten>
Bestand              <Zeilen je Schicht>
Alternativen         <n> verglichen, <n> ausgeschlossen mit Grund
Belege               <n> mit Fundstelle, <n> als Vermutung gekennzeichnet
Wechselkosten        portiert <n>, neu <n>, bleibt <n>
Teuerste Strecke     <benannt> — gebaut: ja/nein
Empfehlung           <eine, mit Begründung>
Nachweis             <Vorschlag mit Frist und Maßstab>
```

Dann **warten**. Die Entscheidung trifft der Projektinhaber.

## 7. Nach der Entscheidung

Entscheidungsakte schreiben (Skill `neo-doku`,
`references/entscheidungsakten.md`), mit den verworfenen Alternativen,
dem Abschnitt „Was dabei schiefging" und der Bedingung, bei der neu zu
prüfen ist. Abnahme nach `references/pruefliste.md`.
