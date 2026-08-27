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
