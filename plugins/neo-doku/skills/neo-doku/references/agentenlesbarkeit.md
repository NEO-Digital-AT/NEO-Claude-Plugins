# Doku, die auch ein Agent versteht

Ein generatives Modell liest eine Doku-Datei oft **allein** — ohne den
Rest des Repositories, ohne die Nachbarseiten, ohne den Verlauf. Was in
dieser einen Datei nicht steht, existiert für die Antwort nicht.

Dieselben Regeln machen die Doku auch für Menschen besser: wer nur eine
Seite öffnet, hat dieselbe Lage.

## Kopfdaten

Jede Doku-Datei beginnt mit einem Kopf. Er beantwortet ohne Lesen, worum
es geht, für wen und ob der Inhalt noch gilt.

```yaml
---
titel: Monitor anlegen
kurzfassung: Einen neuen Monitor einrichten, vom Typ bis zum ersten Testlauf.
zielgruppe: anwender          # anwender | entwickler | betrieb
bereich: frontend             # frontend | backend
sprache: de
stand: 2026-08-26
gilt_fuer: ab Version 2.4
verwandt:
  - regeln.md
  - ../benachrichtigungen/README.md
---
```

`stand` wird bei jeder inhaltlichen Änderung mitgezogen. Ein Datum, das
nicht gepflegt wird, ist schlimmer als keines.

## Aufbau

- **Ein Thema je Datei.** Wer zwei Abläufe in eine Datei legt, bekommt
  Antworten, die beide vermischen.
- **Die Überschrift benennt die Sache**, nicht die Kategorie: „Monitor
  anlegen", nicht „Anleitung" oder „Allgemeines".
- **Überschriften sind stabil.** Sie sind Anker; wer sie umbenennt,
  bricht Verweise. Keine Nummerierung in der Überschrift, die sich beim
  Einfügen verschiebt.
- **Eine Hierarchie ohne Sprünge**, eine H1 je Datei.
- **Der erste Absatz beantwortet die Frage**, die auf die Seite geführt
  hat — vor jeder Vorrede.

## Formulierung

- **Namen ausschreiben, nicht verweisen.** „Das Auswahlfeld ‚Typ' im
  Formular ‚Monitor anlegen'" statt „das erwähnte Feld". Kein „siehe
  oben", kein „wie bereits beschrieben" über Dateigrenzen hinweg.
- **Keine mehrdeutigen Pronomen.** „Er wird dann geprüft" — wer? Den
  Gegenstand wiederholen, auch wenn es sich hölzern liest.
- **Exakte Zeichenketten in Anführung**: Beschriftungen genau so, wie sie
  in der Oberfläche stehen; Pfade, Befehle, Feldnamen und Werte genau so,
  wie sie eingegeben werden.
- **Ein Begriff je Sache**, im ganzen Projekt. Nicht „Prüfung",
  „Check" und „Monitor" für dasselbe. Wo Synonyme im Umlauf sind, werden
  sie einmal in einer Begriffsliste zugeordnet.
- **Bedingungen ausschreiben:** „Wenn das Intervall unter 60 Sekunden
  liegt, verlangt die Anwendung eine Begründung." Nicht: „ggf. mit
  Begründung."
- **Zahlen mit Einheit und Grenze**: „höchstens 5 MB", nicht „nicht zu
  groß".

## Was in Tabellen gehört

Parameter, Felder, Rückgabewerte, Fehlercodes und Optionen als Tabelle,
nicht als Fließtext. Eine Tabelle ist für ein Modell eindeutig, ein
Absatz mit Kommas nicht.

| Feld | Pflicht | Werte | Vorgabe | Bedeutung |
| --- | --- | --- | --- | --- |
| Bezeichnung | ja | Text, 1–80 Zeichen | — | Name in Listen und Meldungen |
| Typ | ja | HTTP-Prüfung, TCP-Port, Zertifikat | HTTP-Prüfung | Legt fest, welche Felder darunter erscheinen |
| Intervall | ja | 30 s, 60 s, 5 min, 15 min | 60 s | Abstand zwischen zwei Prüfungen |

## Bilder

- **Jede Aussage steht im Text.** Das Bild bestätigt sie. Eine Angabe,
  die nur im Screenshot steht, geht verloren.
- Der Alternativtext beschreibt den Inhalt und die Markierungen.
- Nach dem Bild ein Satz, was darauf zu sehen ist — nicht nur die
  Bildunterschrift.

## Verweise

- Relative Links innerhalb der Doku, mit sprechendem Linktext: „siehe
  [Regeln festlegen](regeln.md)", nicht „siehe [hier](regeln.md)".
- Beim Verweis auf eine andere Sprache oder einen anderen Bereich den
  vollen Pfad angeben.
- Jede Datei ist im Inhaltsverzeichnis ihres Ordners verlinkt. Was nicht
  verlinkt ist, findet niemand — auch kein Agent.

## Vorlage für eine Bedienungsseite

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

## Verwandte Seiten

- [<Titel>](<pfad>) — <ein Satz>
```

## Was Agenten am häufigsten fehlt

1. Der genaue Wortlaut einer Beschriftung — sie steht sinngemäß statt
   wörtlich in der Doku.
2. Die Vorgabe eines Feldes und was passiert, wenn man es leer lässt.
3. Die vollständige Liste zulässiger Werte statt „unter anderem".
4. Der Fehlerfall: was die Anwendung meldet und was dann zu tun ist.
5. Die Abgrenzung: was diese Funktion **nicht** tut.

Diese fünf Punkte gehören in jede Bedienungsseite, auch wenn sie kurz
ausfallen.
