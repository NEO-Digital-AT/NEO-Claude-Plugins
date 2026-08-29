# Texte in der Oberfläche

Der Text ist Teil der Bedienung, nicht die Beschriftung darüber. Eine
Oberfläche, die man ohne Handbuch versteht, verdankt das ihren Texten.

## Umfang: wenig, aber an der richtigen Stelle

- Ein Satz an der Stelle, an der die Frage entsteht, ersetzt einen Absatz
  weiter oben.
- **Nicht alles auf einmal erklären.** Die Oberfläche trägt, was jetzt
  gebraucht wird. Hintergrund, Zusammenhänge und Sonderfälle stehen in
  der Dokumentation und werden von dort verlinkt (Skill `neo-doku`).
- Einführungstexte, Willkommensabsätze und Erklärungen dessen, was man
  ohnehin sieht, werden gestrichen.
- Wer drei Sätze Hilfetext an einem Feld braucht, hat das falsche
  Bedienelement gewählt — siehe `eingaben.md`.

**Dieser Text regelt den Wortlaut.** Ob der Wortlaut in seinen Kasten
passt — Umbruch, Kürzung, zu schmale Bereiche, Schriftgrößen —, steht in
`textpassung.md`. Ob es ihn in jeder Sprache gibt, in
`uebersetzungen.md`. Eine gute Beschriftung, die abgeschnitten wird oder
nur auf Deutsch existiert, ist keine gute Beschriftung.

## Jeder Text hat eine Herkunft

> **Ein Satz, den niemand verlangt hat, gehört nicht in die Oberfläche —
> auch wenn er hilfreich klingt.**

Der teuerste Text ist der gut gemeinte: ein Hinweis unter einem Feld,
der erklärt, wo man das Ergebnis später findet. Er liest sich hilfreich,
er stand in keinem Entwurf, und er sagt etwas zu, das die Anwendung nicht
tut. Der Anwender glaubt ihn trotzdem — er hat keinen zweiten Ort, an dem
er nachsehen könnte.

**Zulässige Herkunft, sonst keine:**

| Herkunft | Woran man sie erkennt |
| --- | --- |
| Der freigegebene Entwurf | Der Text steht im Artboard, wörtlich |
| Eine freigegebene Textliste | Der Schlüssel steht in der Sprachdatei, freigegeben |
| Eine Anweisung des Projektinhabers | Nachricht, Ticket, Akte |

**Was die Oberfläche zusätzlich braucht, wird vorgelegt, nicht
geschrieben.** Fehlermeldungen, Leerzustände, Ladehinweise und
Bestätigungen fehlen in fast jedem Entwurf — sie sind trotzdem kein
Freibrief. Der Weg ist: Liste der fehlenden Texte, Vorschlag je Eintrag,
Freigabe, dann in die Sprachdatei. **Nicht: beim Bauen ausformulieren.**

- **Im Zweifel weglassen.** Ein fehlender Hinweis ist eine Rückfrage. Ein
  erfundener Hinweis ist ein Fehler im Produkt.
- **Kein Text „zur Sicherheit".** Wer nicht weiß, ob ein Hinweis nötig
  ist, fragt — er schreibt ihn nicht vorsorglich hin.
- **Kein Beispielwert, keine erfundene Zahl, keine erfundene Adresse.**
  Ein Platzhalter im Entwurf ist ein Platzhalter, kein Inhalt.

## Ein Satz in der Oberfläche ist eine Zusage

Sobald ein Text sagt, **was das System tut**, ist er kein Text mehr,
sondern eine Aussage über das Verhalten — und die kann falsch sein:

| Satzart | Beispiel | Was belegt sein muss |
| --- | --- | --- |
| Erreichbarkeit | „Die Statusseite ist unter dieser Adresse erreichbar" | Dass es die Seite gibt und dass sie unter **dieser** Adresse liegt |
| Automatik | „Der Bericht wird automatisch versendet" | Der Code, der versendet, und sein Auslöser |
| Frist | „Die Freigabe erfolgt innerhalb von 24 Stunden" | Wo diese Frist herkommt |
| Wahlfreiheit | „Sie können die Adresse frei wählen" | Dass das Feld überhaupt wählbar ist |
| Folge | „Löschen kann nicht rückgängig gemacht werden" | Dass es wirklich endgültig ist |

**Vor dem Schreiben wird am Code belegt, dass die Zusage stimmt** — mit
Fundstelle, und die Fundstelle wird berichtet. Ein Satz, der eine
Erreichbarkeit oder eine Wahlmöglichkeit behauptet, wird gegen die
Umsetzung geprüft, nicht gegen die Absicht.

**Der häufigste Fall ist die Adresse.** Wird eine Kennung erzeugt — GUID,
Zufallsschlüssel, laufende Nummer —, dann ist sie **nicht wählbar**, und
kein Text darf das Gegenteil nahelegen. Wer das prüfen will, sucht die
Stelle, die die Kennung erzeugt, nicht die Stelle, die sie anzeigt.

**Und der Test dazu:** Ein Test, der einen solchen Satz festhält, hält
die Zusage mit fest. Er ist nur zulässig, wenn der Satz eine Herkunft hat
(Kernregel 2, Skill `neo-grundregeln`, `references/tests.md`).

## Beschriftungen

- Knöpfe tragen **Verb plus Objekt**: „Auftrag anlegen", „Änderungen
  speichern", „Einladung senden". Nicht „OK", nicht „Absenden", nicht
  „Weiter" ohne Ziel.
- Die Beschriftung sagt, was **passiert**, nicht was man tut. Im
  Bestätigungsdialog steht auf dem Knopf die Folge: „Auftrag löschen",
  nicht „Ja".
- Abbrechen heißt „Abbrechen". Ein zweites Wort dafür verwirrt.
- Feldbeschriftungen stehen **über** dem Feld und bleiben stehen. Ein
  Platzhalter ist keine Beschriftung: er verschwindet beim Tippen, und
  wer dann unterbrochen wird, weiß nicht mehr, was er füllt.
- Der Platzhalter zeigt das **Format**, nicht die Aufforderung:
  „TT.MM.JJJJ", nicht „Bitte Datum eingeben".
- Gleiche Dinge heißen überall gleich. Ein Begriff, ein Wort — im
  Backend, im Frontend, in der Doku und in der API-Beschreibung.

## Fehlermeldungen

Muster: **was ist passiert — warum — was jetzt zu tun ist.** In ganzen
Sätzen, in der Sprache des Anwenders.

| Statt | Besser |
| --- | --- |
| „Fehler 422" | „Die Datei ist 8,4 MB groß. Erlaubt sind bis zu 5 MB. Bitte eine kleinere Datei wählen." |
| „Ungültige Eingabe" | „Diese Kennung ist bereits vergeben. Bitte eine andere wählen." |
| „Ein Fehler ist aufgetreten" | „Der Dienst antwortet gerade nicht. Der Vorgang wurde nicht gespeichert. In einer Minute erneut versuchen." |

- Nie den Anwender beschuldigen. Keine Ausrufezeichen, kein „Sie haben
  falsch …".
- Technische Kennungen dürfen dabeistehen — klein, kopierbar, für den
  Support. Sie ersetzen den Satz nicht.
- Die Meldung steht **am Feld**, das sie betrifft. Eine Zusammenfassung
  oben ersetzt das nicht, sie ergänzt es.
- Was nicht gespeichert wurde, wird gesagt. Ein Fehler, nach dem unklar
  ist, ob die Daten weg sind, ist der schlimmste Fall.

## Leere Flächen

Jede Liste, Tabelle und Fläche hat einen Leer-Zustand mit drei Teilen:
was hier normalerweise steht, warum gerade nichts da ist, und die
nächste Handlung als Knopf.

Zwei Fälle werden unterschieden: **noch nichts angelegt** (mit Einladung
zum Anlegen) und **Filter ohne Treffer** (mit Knopf zum Zurücksetzen).
Derselbe Text für beides ist ein Fehler.

## Laden und Warten

- Skelette in der Form des echten Inhalts statt Ladekreisel.
- Dauert es länger als etwa zehn Sekunden, wird gesagt, was läuft und wie
  weit es ist. „Bitte warten" allein ist keine Auskunft.
- Nach jeder Aktion eine sichtbare Rückmeldung. Erfolg als Kurzmeldung,
  die von selbst geht; Information bleibt stehen, bis sie geschlossen
  wird; harte Fehler blockieren.

## Bestätigungen

Der Dialog benennt **das Objekt** und **die Folge**: „Auftrag
‚Kundenportal' löschen? Die Verlaufsdaten der letzten 90 Tage werden mit
gelöscht und lassen sich nicht wiederherstellen."

Kein „Sind Sie sicher?" ohne Inhalt. Bei großer Tragweite den Namen
abtippen lassen. Wo Rückgängig möglich ist, ist Rückgängig besser als
ein Dialog.

## Sprache

- Sie-Form, echte Umlaute (ä ö ü ß), keine Emojis, keine
  Marketingsprache, keine Füllwörter.
- Sentence case in Beschriftungen und Überschriften, keine
  Versalienschreibung.
- Kurze Sätze, Aktiv statt Passiv, ein Verb pro Handlung.
- Zahlen, Datum, Uhrzeit und Währung immer über die Formatierung der
  eingestellten Sprache — nie roh interpoliert. Sonst fehlt das
  Dezimalkomma.

## Mehrsprachigkeit

- **Jeder sichtbare Text kommt aus der Sprachdatei**, auch der eine, der
  „sowieso nie übersetzt wird". Der Text lebt in der Komponente, nicht
  in der View (Skill `neo-komponenten`).
- Sätze werden **nicht aus Teilen zusammengesetzt**. Wortstellung und
  Beugung unterscheiden sich je Sprache; zusammengesetzte Sätze werden
  in der zweiten Sprache falsch.
- Platzhalter tragen Namen, keine Nummern: `{anzahl}`, nicht `{0}`.
- Mehrzahl über die Pluralregeln der Sprache, nicht über `if (n === 1)`.
- Das Layout hält längere Übersetzungen aus. Deutsche Beschriftungen sind
  gegenüber englischen etwa ein Drittel länger — daran bricht das Layout
  zuerst (siehe `responsiv.md`).
- Bei rechtsläufigen Sprachen kommen Richtungen aus logischen
  Eigenschaften (`start`/`end`), nicht aus `left`/`right`.
