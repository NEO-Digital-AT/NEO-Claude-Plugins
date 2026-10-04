# Verbotene Bauweisen

Lesekonvention siehe `SKILL.md`.

> **Jede dieser Bauweisen wurde gebaut, nachgebessert und wieder
> stillgelegt.** Einzeln wirkt jede vernünftig. Zusammen haben sie einen
> Assistenten ergeben, der an seinen eigenen Absicherungen gescheitert ist.

**Herkunft:** ein Hotel-Concierge im Betrieb, Juli bis September 2026 — Router mit
Fachagenten und Schreiber, ein über Monate gewachsener Prompt im Code,
Prüfungen der Antwort im Code und durch ein zweites Modell. Nach dem Umbau
vom 30.09.2026 arbeitet er mit einem Modell, Werkzeugen und Skills, und
das Buchen funktioniert, was es davor nicht tat. Die Absicherungen waren
nach Aussage des Projektinhabers der Grund, warum am Ende alles brach.

**Wer eine dieser Bauweisen vorschlägt, legt vorher dar, warum der Grund
hier nicht mehr gilt.** Ohne diese Darlegung ist der Vorschlag abgelehnt.

## 1. Router oder Klassifizierer vor dem Modell

**Was:** Ein Modell oder eine Wortliste ordnet die Nachricht vorab einem
Ablauf zu; das bearbeitende Modell sieht danach nur noch einen Ausschnitt.

**Woran es bricht:** An allem, was nicht in die Einteilung passt: zwei
Anliegen in einer Nachricht, ein Themenwechsel, eine kurze Antwort wie
„die zweite", eine Schrift ohne Leerzeichen. Eine Mindestlänge für
Textbelege ließ kurze chinesische und japanische Ortsnamen scheitern.

**Stattdessen:** Das Modell liest die Bedeutung, in jeder Sprache, mit
dem ganzen Regelwerk vor sich.

## 2. Fachagenten-Kette

**Was:** Ein Router reicht an Fachagenten weiter — Buchung, Zahlung,
Storno —, ein Schreiber formuliert am Ende, ein Fachagent meldet „nicht
mein Bereich" und gibt zurück.

**Woran es bricht:** An den Übergaben. Ein Fachagent scheiterte, oder der
Schreiber ließ weg, was die Werkzeuge geliefert hatten — beides stand im
alten Concierge als Grund, einen Auftrag aufzugeben.

**Stattdessen:** Ein Modell mit allen Skills und allen Werkzeugen.

## 3. Prüfagent, Antwortprüfer, Endredakteur

**Was:** Code oder ein zweites Modell prüft die fertige Antwort gegen
Belege, gibt sie frei, verwirft sie oder schreibt sie um.

**Woran es bricht:** Die Prüfung irrt selbst, und dann sicher und
unbemerkt. Ein korrektes Angebot über drei Zimmer wurde verworfen, weil
die Prüfung „1.038,00 €" als „038,00" las. Datumsteile eines Zeitstempels
galten als Preisbeleg. Verworfene Entwürfe wurden durch Servertext
ersetzt.

**Stattdessen:** Das Modell prüft die eigene Antwort nach dem Kern-Skill
gegen die Werkzeugergebnisse. Fakten kommen aus Werkzeugen, nicht aus
einer Nachkontrolle.

## 4. Fachliche Absicherung im Code

**Was:** Eine Regel, die ins Regelwerk gehört, steht als Prüfung im Code:
eine Pflichtbestätigung vor jedem Schreiben, eine vorgegebene
Bestätigungsformel, eine Wortliste für „ja", eine Mengen- oder
Reihenfolgeregel, die einen Aufruf zurückweist.

**Woran es bricht:** Sie kennt den Zusammenhang nicht. Die Zustimmung
eines Gastes in eigenen Worten galt nicht als Zustimmung; er wurde ein
zweites Mal gefragt; eine vorgegebene Formel landete bei ihm. Jede
Absicherung brachte die nächste Ausnahme mit sich.

**Stattdessen:** Die Regel steht im Skill, das Modell wendet sie an. Im
Code steht nur, was technisch ist: Mandant, Rechte, Eigentum, gültige
Angaben, keine Doppelausführung (`zugriff.md`, `werkzeuge.md`).

## 5. Text vom Server an den Kunden

**Was:** Ersatzantworten, feste Absagen und Vorlagentexte, die die
Anwendung schickt, wenn der Lauf scheitert oder eine Prüfung anschlägt.

**Woran es bricht:** Ein Gast wählte einen Tarif, nannte seinen Namen und
bekam eine Absage. Ein erschöpfter Lauf erzeugte einen festen Text oder
beauftragte ein Modell, eine Absage zu schreiben. Umgekehrt gab ein Lauf
ein Gespräch still an das Team ab: Der Gast bekam keine Antwort mehr und
erfuhr nicht, warum.

**Stattdessen:** Jeder Text an den Kunden kommt vom Modell; die Anwendung
hängt nur KI-Hinweis und Signatur an, immer gleich. Kommt ein Lauf
nicht zu Ende, arbeitet er mit den festgehaltenen Ergebnissen weiter; ein
voller Kontext wird komprimiert. Übergibt das Modell an das Team, schreibt
es dem Kunden selbst, dass ein Mitarbeiter übernimmt (`aufbau.md`).

## 6. Fachliche Folgekette

**Was:** Nach einem Schritt stößt der Server den nächsten selbst an —
nach der Buchung die Zahlung, eine automatische Wiederherstellung, eine
automatische Zusammenfassung mehrerer Zahlungen.

**Woran es bricht:** Die Kette handelt ohne Auftrag und ohne das
Regelwerk. Die Zahlungsauswahl stand teilweise fest im Server und überging
die Anweisung des Betreibers, keine Vorauszahlung zu verlangen.

**Stattdessen:** Jeder fachliche Schritt ist ein Werkzeugaufruf, den das
Modell wählt. Hintergrundarbeit führt nur zu Ende, was das Modell
ausgelöst hat (`aufbau.md`).

## 7. Nachladen und Freischalten

**Was:** Das Modell sieht anfangs nur eine Liste der Skills und muss den
passenden erst laden; Werkzeuge erscheinen erst nach dem Laden oder nach
einem bestimmten Schritt.

**Woran es bricht:** Lädt das Modell den Skill nicht, fehlen Regel und
Werkzeug. Eine Korrektur schickte das Modell zu Werkzeugen, die es nicht
sehen konnte.

**Stattdessen:** Alle Skills und alle Werkzeugdefinitionen ab dem ersten
Aufruf. Ob ein Aufruf ausgeführt wird, entscheidet das Werkzeug.

## 8. Laufzeitprompt im Code

**Was:** Die Anweisungen an das Modell stehen als Zeichenketten im
Programmcode, über Monate gewachsen und an vielen Stellen ergänzt.

**Woran es bricht:** Niemand sieht das Ganze. Eine Änderung an einer
Stelle bricht eine andere, und Code, Doku und Prompt widersprechen sich.

**Stattdessen:** Ein Skill-Paket als Dateien, jede Regel genau einmal
(`skills.md`).

## 9. Grenze mit Absage

**Was:** Eine knappe Höchstzahl an Schritten oder an verworfenen
Antworten beendet den Lauf — mit einem Text an den Kunden.

**Woran es bricht:** 16 Modellschritte reichten für einen gewöhnlichen
Buchungsablauf nicht. Drei verworfene Antworten beendeten den Lauf, auch
wenn er zwischendurch vorankam.

**Stattdessen:** Großzügige, einstellbare Grenzen; am Ende Fortsetzung.
Ein voller Kontext wird komprimiert — nie eine Absage, nie eine stille
Abschaltung (`aufbau.md`).

## Woran man einen Rückfall erkennt

- Eine Änderung baut eine Prüfung der Antwort, eine Wortliste oder einen
  zweiten Modellaufruf ein, der entscheidet, prüft oder antwortet, „damit
  das nicht wieder passiert". (Ein Hilfsaufruf, der nur für den Kontext
  zusammenfasst, ist erlaubt — `aufbau.md`.)
- Eine Regel steht im Code und im Skill, mit verschiedenem Wortlaut.
- Ein Werkzeug gibt einen fertigen Satz für den Kunden zurück.
- Ein Test prüft Code, der im echten Lauf nicht aufgerufen wird.
- Ein Kommentar beschreibt Router, Fachagenten oder Schreiber.
- Ein Gespräch endet beim Team, ohne dass der Kunde es vom Modell erfahren
  hat.
- Ein Skill erklärt eine reine Informationsfrage oder begründet seine
  Regeln in Prosa.

Jeder dieser Funde wird gemeldet und vorgelegt, nicht nebenbei gebaut und
nicht nebenbei entfernt (Kernregel 3).
