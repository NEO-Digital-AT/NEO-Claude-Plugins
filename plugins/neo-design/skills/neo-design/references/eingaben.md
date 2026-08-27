# Eingaben führen — welches Bedienelement wofür

Grundsatz: **Was nicht eingegeben werden kann, kann nicht falsch sein.**
Ein Freitextfeld ist zulässig, wenn die Menge der gültigen Werte weder
bekannt noch abfragbar noch beschreibbar ist. Sonst nicht.

Rangfolge der Fehlervermeidung, von oben nach unten anzuwenden:

1. Den Wert **gar nicht erfragen** — herleiten, voreinstellen, merken.
2. Den Wert **auswählen lassen** aus dem, was gültig ist.
3. Die Eingabe **während des Tippens führen** (Maske, Zeichenfilter,
   Vervollständigung, Sofortprüfung).
4. Erst danach: prüfen und melden.

Eine Fehlermeldung ist der vierte Platz, nicht der erste.

## Wahl des Bedienelements

| Was eingegeben wird | Richtig | Nie |
| --- | --- | --- |
| Zwei Zustände, sofort wirksam | Schalter mit Beschriftung des Ergebnisses | Kontrollkästchen ohne Speichern |
| Zwei Zustände, mit Speichern | Kontrollkästchen | Schalter, der erst später wirkt |
| 2–5 bekannte Werte | Segmentierte Auswahl oder Optionsfeldgruppe, alle sichtbar | Auswahlfeld, das die Optionen versteckt |
| 6–15 bekannte Werte | Auswahlfeld | Textfeld |
| Mehr als 15 Werte | Auswahlfeld mit Suche und Tastaturnavigation | Textfeld, auch nicht „mit Autovervollständigung" |
| Mehrfachauswahl | Chips mit Vervollständigung, entfernbar | Kommagetrennte Liste im Textfeld |
| Abhängige Auswahl | Kaskade: die zweite Liste entsteht aus der ersten | Zwei freie Felder, die zueinander passen müssen |
| Felder oder Pfade einer fremden Antwort | Quelle abfragen, tatsächlich vorhandene Felder anbieten | Pfad eintippen und beim Speichern zurückweisen |
| Datum | Datumswähler **plus** maskiertes Feld (TT.MM.JJJJ) | Freitext, Datum in drei Feldern |
| Uhrzeit, Dauer, Intervall | Wähler mit sinnvoller Schrittweite und Einheit | Textfeld mit „z. B. 300" |
| Zeitzone | Liste aus der Laufzeit (IANA), mit aktueller Verschiebung | Textfeld, feste Auswahl von Hand gepflegt |
| Land, Sprache, Währung | Liste mit Name und Kennzeichen, nach Name suchbar | Textfeld, Codeeingabe |
| Telefonnummer | Länderwahl plus maskiertes Feld, Speicherung in E.164 | Ein Feld für alles |
| Zahl, Betrag, Menge | Zahlenfeld mit Einheit, Schrittweite, Grenzen, Tausendertrennung, tabellarischen Ziffern | Textfeld, Einheit nur im Hilfetext |
| Anteil, Schwelle | Schieber und Zahlenfeld gekoppelt, beide zeigen denselben Wert | Schieber allein (nicht genau), Zahlenfeld allein (nicht anschaulich) |
| Farbe | Farbwähler mit den Tokens des Systems als Voreinstellung, Kontrastwert sichtbar | Hex-Eingabe ohne Prüfung |
| Datei | Ablagefläche mit Typ- und Größenprüfung, Vorschau, Nachbearbeitung | Dateifeld ohne Rückmeldung |
| Reihenfolge | Ziehbare Liste mit Tastaturalternative | Zahlenfeld „Position" |
| Kennwort | Feld mit Sichtbarkeitsschalter und Stärkeanzeige | Zweites Feld „wiederholen" bei vorhandenem Sichtbarkeitsschalter |
| E-Mail-Adresse | Textfeld mit Formatprüfung und Tippfehlerhinweis bei bekannten Anbietern | Zweites Feld „wiederholen" |
| Adresse einer Ressource | Textfeld mit vorangestelltem Schema und Erreichbarkeitstest | Textfeld ohne Test |
| Langer Freitext | Textbereich mit Zeichenzähler und Vorschau, wenn Auszeichnung erlaubt ist | Einzeiliges Feld |
| Suche | Suchfeld mit Sofortfilterung und Löschknopf | Suchfeld, das erst auf Eingabetaste reagiert |

## Eingabemasken

- Die Maske führt beim Tippen: sie setzt Trennzeichen selbst, lässt nur
  gültige Zeichen zu und zeigt das Zielformat als Platzhalter.
- Die Maske ist **Führung, keine Prüfung**. Der gültige Wert wird
  zusätzlich geprüft, und zwar serverseitig (Skill `neo-sicherheit`).
- Einfügen aus der Zwischenablage muss funktionieren: die Maske
  normalisiert das Eingefügte, statt es abzulehnen. Eine Telefonnummer
  mit Leerzeichen und Klammern ist der Normalfall, nicht der Angriff.
- Die Maske zerstört nie, was schon dasteht. Wer in der Mitte tippt,
  verliert nicht das Ende.
- Formate mit regionaler Bedeutung (Datum, Dezimaltrennzeichen,
  Tausendertrennung) folgen der eingestellten Sprache, nicht der Technik.

## Wann geprüft und wann gemeldet wird

- **Während des Tippens:** Zeichenfilter, Länge, Format, Verfügbarkeit
  einer Kennung. Sichtbar als ruhiger Hinweis, nicht als roter Alarm
  beim ersten Zeichen.
- **Beim Verlassen des Feldes:** die vollständige Feldprüfung.
- **Beim Absenden:** Zusammenhänge zwischen Feldern. Der Fokus springt
  in das erste fehlerhafte Feld, die Meldung steht am Feld, und eine
  Zusammenfassung nennt die Anzahl.
- Ein Feld, das noch nie berührt wurde, ist nicht fehlerhaft, sondern
  leer. Formulare begrüßen niemanden mit Rot.
- Der Absenden-Knopf wird nicht deaktiviert, solange der Grund nicht
  sichtbar ist. Ein toter Knopf ohne Erklärung ist ein Rätsel.

## Voreinstellungen

- Jedes Feld, dessen Wert sich vernünftig herleiten lässt, kommt gefüllt:
  aus dem Kontext, aus der letzten Eingabe, aus der Voreinstellung des
  Mandanten. Ein Formular, das mit sinnvollen Werten startet, ist die
  bessere Anleitung.
- Eine Voreinstellung ist als solche erkennbar und änderbar. Sie ist nie
  eine stille Entscheidung mit Folgen (Kosten, Sichtbarkeit, Löschung).
- Pflichtfelder sind gekennzeichnet, nicht die optionalen. Sind fast alle
  Felder Pflicht, wird stattdessen „optional" gekennzeichnet.

## Dateien und Nachbearbeitung

Ein Upload endet nicht beim Hochladen. Was danach kommt, entscheidet
darüber, ob das Ergebnis brauchbar ist:

- Typ, Größe und Inhalt vor der Übernahme prüfen und das Ergebnis
  benennen — auch, was entfernt wurde.
- Vorschau in der Umgebung, in der die Datei später steht.
- Zuschnitt und Platzierung im Browser, mit fester Bühne, damit das
  Ergebnis überall gleich hoch steht.
- **Nachträglich einstellbar machen, was einstellbar ist.** Bei einer
  Vektorgrafik stehen die Farben im Klartext: sie werden ausgelesen,
  einzeln angezeigt und einzeln änderbar gemacht — Verlaufsstopps
  eingeschlossen. Für den Dunkelmodus wird eine eigene Fassung
  angeboten; was gegen dunklen Grund schon trägt, bleibt unverändert.
  In einem bestehenden Projekt umgesetzt und dort als Entscheidungsakte
  „Logo und SVG" festgehalten.
- Wo die Rechnung nicht reicht, eine zweite Datei zulassen — gespeichert
  nur, wenn sie sich unterscheidet.

## Gefährliche Eingaben

- Destruktives und Unumkehrbares verlangt eine Bestätigung, die die Folge
  benennt. Bei großer Tragweite: den Namen des Objekts abtippen lassen.
- Massenaktionen zeigen vorher die Anzahl und eine Liste des Betroffenen.
- Was rückgängig gemacht werden kann, bekommt „Rückgängig" statt eines
  Dialogs. Das ist die freundlichere und die sicherere Lösung.
