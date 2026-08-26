# EU-KI-Verordnung in der Praxis

Verordnung (EU) 2024/1689. Dieser Text ist eine **Bau- und
Prüfanleitung, keine Rechtsberatung** — die Einstufung des Systems und
die rechtliche Abnahme macht der Rechtsbeistand (Skill `neo-recht`).

## Welche Rolle man hat

| Rolle | Wer das ist |
| --- | --- |
| **Anbieter** | Wer ein KI-System entwickelt und unter eigenem Namen oder eigener Marke in Verkehr bringt |
| **Betreiber** | Wer ein KI-System unter eigener Verantwortung einsetzt |

**Die Falle:** Wer ein fremdes Modell nimmt, es unter dem eigenen Namen
als Assistent auf die eigene Seite stellt und ihm einen eigenen Namen
gibt, kann damit vom Betreiber zum **Anbieter** werden — mit weiter
reichenden Pflichten. Das ist keine technische, sondern eine rechtliche
Frage. Sie wird je Produkt geklärt und im Projekt festgehalten, bevor
gebaut wird.

## Die vier Transparenzfälle aus Artikel 50

| Fall | Pflicht | Wen es trifft |
| --- | --- | --- |
| System interagiert direkt mit Menschen | Der Mensch erfährt, dass er mit KI spricht — spätestens bei der ersten Interaktion, klar und unterscheidbar. Entfällt nur, wenn es ohnehin offensichtlich ist | Anbieter |
| System erzeugt Ton, Bild, Video oder Text | Die Ausgabe wird **maschinenlesbar** markiert und als erzeugt erkennbar | Anbieter |
| Emotionserkennung, biometrische Kategorisierung | Offenlegung gegenüber den Betroffenen | Betreiber |
| Täuschend echte Inhalte von Personen, Orten, Ereignissen | Offenlegung, dass der Inhalt erzeugt oder verändert wurde | Betreiber |

Dazu: Wer KI-erzeugten **Text veröffentlicht, um die Öffentlichkeit über
Angelegenheiten von öffentlichem Interesse zu unterrichten**, legt das
offen. Ein Kundenchat fällt nicht darunter, ein automatisch erzeugter
Nachrichtenbeitrag schon.

## Wie eine ausreichende Offenlegung aussieht

Musterbeispiel aus den eigenen Produkten: die Assistenten **Nova**
(NEO Digital) und **Leo** (LeoFlex).

Was sie richtig machen:

- **Die Kennzeichnung steht im Kopf des Fensters**, direkt neben dem
  Namen: „KI-Assistentin" bzw. „KI-Assistent". Sie ist da, **bevor**
  jemand etwas eingibt.
- Sie ist **klar und unterscheidbar**, nicht in einem Fließtext
  versteckt und nicht in der Datenschutzerklärung.
- Die Begrüßung wiederholt es in eigenen Worten.
- Nova ergänzt unten: „Antworten können Fehler enthalten."

Das erfüllt Absatz 1. Drei Punkte, die trotzdem zu beachten sind:

1. **Ein Hinweis auf Fehlbarkeit gehört dazu, kein Genauigkeitsversprechen.**
   „Antworten können Fehler enthalten" ist die richtige Form. Ein Satz
   wie „nennt nur gesicherte Informationen" ist ein **Versprechen**, an
   dem man gemessen wird — und es ist bei einem Sprachmodell nicht
   haltbar. Beide Produkte eines Hauses sollen hier dieselbe Haltung
   zeigen.
2. **Der Hinweis darf nicht abgeschnitten sein.** Eine Kopfzeile, die
   mit „…" endet, ist ein Baumangel (Skill `neo-design`). Was
   rechtlich gefordert ist, muss vollständig lesbar sein — auf jeder
   Breite.
3. **Übernimmt ein Mensch, wechselt die Kennzeichnung sichtbar mit.**
   Ein Weiterleitungsknopf allein genügt nicht; nach der Übergabe darf
   der Kopf nicht weiter „KI-Assistent" sagen, wenn dort ein Mensch
   antwortet — und umgekehrt.

**Was die sichtbare Kennzeichnung nicht abdeckt:** die
**maschinenlesbare** Markierung erzeugter Inhalte aus Absatz 2. Ob und
wie weit sie für einen Chat gilt, hängt an der Rollenfrage oben und ist
je Produkt zu klären — nicht vom Agenten zu entscheiden.

## Verbotene Praktiken

Seit 02.02.2025 verboten, unter anderem: Bewertung von Menschen nach
sozialem Verhalten, Ausnutzen von Schutzbedürftigkeit, ungezieltes
Auslesen von Gesichtsbildern zum Aufbau von Datenbanken,
Emotionserkennung am Arbeitsplatz und in Bildungseinrichtungen.

Bußgeldrahmen: bis **35 Mio. Euro oder 7 %** des weltweiten
Jahresumsatzes. Fällt eine Anforderung auch nur in die Nähe, wird sie
nicht gebaut, sondern vorgelegt.

## Hochrisiko — die Abgrenzung

Hochrisiko sind unter anderem KI-Systeme für Bewerbung und
Personalauswahl, Kreditwürdigkeit, Zugang zu Bildung, kritische
Infrastruktur, Strafverfolgung. Sie bringen ein eigenes Pflichtenpaket
mit: Risikomanagement, Datenqualität, technische Dokumentation,
Protokollierung, menschliche Aufsicht, Genauigkeit und Robustheit.

**Ein Kundenchat, ein Textvorschlag oder eine Zusammenfassung sind das
in der Regel nicht.** Sobald eine KI-Funktion über Menschen entscheidet
oder eine solche Entscheidung vorbereitet, ist die Einstufung
ausdrücklich zu klären, bevor gebaut wird.

## KI-Kompetenz

Seit 02.02.2025 müssen Anbieter und Betreiber für ausreichende
KI-Kompetenz der Personen sorgen, die mit den Systemen arbeiten. Das ist
keine Prüfung, aber eine Bringschuld: wer KI einsetzt, muss wissen, was
das System kann, wo es scheitert und was mit den Daten passiert.

Im Projekt heißt das: eine kurze, gepflegte Seite in der Doku, die den
Einsatz, die Grenzen und den Umgang mit falschen Ausgaben beschreibt
(Skill `neo-doku`).

## Prüfliste

- [ ] Rolle geklärt und festgehalten: Anbieter oder Betreiber.
- [ ] Einstufung geklärt: verboten, hochrisiko, Transparenzfall, keines
      davon.
- [ ] Offenlegung sichtbar vor der ersten Eingabe, vollständig lesbar,
      auf jeder Breite, barrierefrei.
- [ ] Hinweis auf Fehlbarkeit vorhanden; kein Genauigkeitsversprechen.
- [ ] Wechsel Mensch/Maschine sichtbar gekennzeichnet.
- [ ] Maschinenlesbare Markierung erzeugter Inhalte geklärt.
- [ ] Datenweitergabe an das Modell in der Datenschutzerklärung und, bei
      Drittanbietern, im Consent (Skill `neo-recht`).
- [ ] Doku-Seite zu Einsatz, Grenzen und Fehlerumgang vorhanden.
