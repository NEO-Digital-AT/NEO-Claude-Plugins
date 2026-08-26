# Sicherung und Wiederherstellung

## Zwei Zahlen, bevor es live geht

| Zahl | Frage | Folge |
| --- | --- | --- |
| **Hinnehmbarer Datenverlust** | Wie viel Arbeit darf verloren gehen? | Bestimmt den Abstand zwischen zwei Sicherungen |
| **Wiederanlaufzeit** | Wie lange darf es dauern, bis wieder gearbeitet wird? | Bestimmt Art und Ort der Sicherung |

Beide Zahlen entscheidet der Projektinhaber, nicht die Technik. Sie
stehen im Betriebshandbuch und werden dem Kunden genannt — er soll
wissen, was er hat.

Eine Stunde Datenverlust ist etwas anderes als ein Tag. Wer täglich
sichert, verspricht damit einen Tag, auch wenn er es nie ausspricht.

## Was gesichert wird

- Die Datenbank, vollständig, mit Schema.
- **Hochgeladene Dateien und Medien.** Sie sind Kundendaten, kein
  Build-Ergebnis, und lassen sich nicht neu erzeugen.
- Konfiguration und Secrets — verschlüsselt, getrennt, aber gesichert.
  Eine wiederhergestellte Datenbank ohne Schlüssel ist wertlos.
- Die Zuordnung: welcher Stand gehört zu welcher Anwendungsversion.
  Eine Sicherung, die zu keinem Code mehr passt, spielt niemand ein.

## Wo sie liegt

- **Nicht auf demselben System.** Ein Ausfall, der die Produktion
  trifft, darf die Sicherung nicht mittreffen.
- **Nicht unter denselben Zugangsdaten.** Wer die Produktion übernimmt,
  darf die Sicherung nicht löschen können. Getrennte Rechte, möglichst
  nur schreibend, ohne Löschrecht.
- Mindestens eine Fassung an einem anderen Ort.
- Verschlüsselt im Ruhezustand und bei der Übertragung.

## Aufbewahrung

Gestaffelt statt gleichförmig: mehrere Tagesstände, mehrere
Wochenstände, mehrere Monatsstände. Die Staffel und die Höchstdauer
richten sich nach den Aufbewahrungsfristen — **eine Sicherung ist kein
Freibrief, Daten länger zu halten, als das Löschkonzept erlaubt**
(Skill `neo-recht`).

## Die Wiederherstellung ist der eigentliche Test

**Mindestens einmal je Quartal**, auf ein getrenntes System, mit
Protokoll:

1. Sicherungsstand wählen — auch einen älteren, nicht immer den
   neuesten.
2. Auf eine leere Umgebung einspielen.
3. Anwendung starten, Migrationen laufen lassen.
4. Fachlich prüfen: Anmeldung, ein Datensatz, eine Datei, ein Ablauf.
5. Zeit messen: wie lange hat es tatsächlich gedauert?
6. Protokollieren: Datum, Stand, Dauer, was fehlte, was auffiel.

Was dabei fehlt, ist der eigentliche Fund. Häufig: Dateien fehlen,
Secrets fehlen, eine Erweiterung fehlt, die Zeit reicht nicht.

**Ohne dieses Protokoll gilt die Sicherung als ungeprüft**, und das wird
so berichtet — nicht als „Sicherung vorhanden".

## Vor riskanten Änderungen

Vor Migrationen auf Bestandssystemen, vor Versionssprüngen und vor
Umbauten: eine Sicherung ziehen **und prüfen, dass sie lesbar ist**.
Eine Sicherung, die im selben Zug entsteht wie der Fehler, hilft nur,
wenn sie vorher fertig war.

## Was nicht als Sicherung gilt

- Eine Kopie im selben Dateisystem.
- Ein Schnappschuss des Speichers ohne getesteten Rückweg.
- Eine Replikation. Sie überträgt einen versehentlichen Löschbefehl
  zuverlässig mit.
- Der Papierkorb.
- Der letzte Stand im Versionsverwaltungssystem — der enthält keine
  Kundendaten.
