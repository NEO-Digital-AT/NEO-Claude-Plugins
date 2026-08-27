# Abnahmeliste KI-Assistent

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.
Was bewusst nicht erfüllt ist, wird benannt, mit Grund.

## Aufbau

- [ ] Der Systemprompt ist **unter 150 Zeilen** — gemessen, nicht
      geschätzt (`promptinventar.py`).
- [ ] Er enthält **keine** Werkzeugauswahl, kein Fachwissen, kein Schema
      und keinen Beispieldialog.
- [ ] Absichten, Werkzeuge, Zustand und Ablauf liegen getrennt.
- [ ] Vorbedingungen, Bestätigung, Wiederholung und Rechte stehen im
      **Code**, nicht im Prompt.
- [ ] `heute`, Zeitzone, Mandant und Auswahl kommen als **Daten** aus dem
      Zustand.
- [ ] `promptinventar.py` meldet **null** Befunde der Art
      Schlüsselwort-Verzweigung.

## Absichten

- [ ] Die Liste ist **geschlossen**, versioniert und an einer Stelle.
- [ ] Je Absicht: Zweck in einem Satz, Abgrenzung, erlaubte Werkzeuge,
      Mindestangaben, schreibend ja/nein.
- [ ] Die drei Pflichtabsichten `unklar`, `ausserhalb` und `plauderei`
      sind vorhanden und lösen **kein** Werkzeug aus.
- [ ] Die Einordnung liefert strukturiert `{absicht, sprache, sicher}`
      und hat **keinen** Werkzeugzugriff.
- [ ] Ein Wert außerhalb der Liste führt zu `unklar`, nicht zum
      ähnlichsten Wert — und wird protokolliert.
- [ ] Die Absicht wird je Benutzerbeitrag neu bestimmt.

## Werkzeuge

- [ ] Ein Werkzeug, eine Aufgabe. Kein Sammelwerkzeug mit `typ`.
- [ ] Jede Beschreibung nennt **dafür**, **nicht dafür** (mit dem Namen
      des ähnlichsten Werkzeugs) und **vorher**.
- [ ] Schema streng: `additionalProperties: false`, Pflichtfelder,
      `enum` statt Freitext, `pattern` und Formate gesetzt.
- [ ] Je Feld eine Beschreibung mit Beispielwert.
- [ ] Kein Argument für etwas, das aus dem Zustand kommt.
- [ ] Kennungen stammen aus Ergebnis oder Zustand; vor jedem schreibenden
      Werkzeug mit Kennung steht ein Suchschritt.
- [ ] Positivliste je Absicht wird **im Code** durchgesetzt.
- [ ] Schemafehler geht mit Begründung zurück ans Modell, höchstens
      zweimal, dann Abbruch mit Klartext.
- [ ] Schreibende Werkzeuge: Bestätigung mit Gegenstand und Folge,
      Idempotenzschlüssel, Rechte des angemeldeten Nutzers.
- [ ] Eine Bestätigung gilt nur für die Handlung, zu der sie gegeben
      wurde.
- [ ] Ergebnisse sind auf die nötigen Felder reduziert, Trefferzahl
      begrenzt und die Begrenzung genannt.
- [ ] Fehler des Fachdienstes sind übersetzt, nicht durchgereicht.
- [ ] Werkzeuge eines fremden MCP-Servers sind ausgewählt und umhüllt,
      nicht unbesehen durchgereicht; die Serverfassung ist festgenagelt.

## Sprachen

- [ ] Arbeitssprache und Antwortsprache sind getrennt.
- [ ] Absichtsnamen, Werkzeugnamen, Aufzählungswerte, Kennungen und
      Formate werden **nie** übersetzt — durch `enum` erzwungen.
- [ ] Die Antwortsprache wird **einmal** bestimmt, nicht je Satz.
- [ ] Keine Beispieldialoge — oder je Sprache eigene, gleich aufgebaut.
- [ ] **Eine neue Sprache dazuzuschalten hat keine Prompt-Zeile
      geändert.** Nachgewiesen, nicht behauptet.
- [ ] Der KI-Hinweis nach Artikel 50 ist in **jeder** ausgelieferten
      Sprache vorhanden (Skill `neo-ki`).

## Messung

- [ ] Je Absicht mindestens drei Fälle: klar, mehrdeutig, ohne Werkzeug.
- [ ] Je Sprache derselbe Satz Fälle, mit **identischer** Erwartung.
- [ ] Fälle für Einschleusung, Datumsrechnung, Umlaute, leeres Ergebnis,
      zu großes Ergebnis, Bestätigung nach Themenwechsel.
- [ ] Je Vorbedingung ein Fall, der das schreibende Werkzeug **verbietet**.
- [ ] Goldlauf mit **fünf** Läufen je Fall vor der Freigabe, **zehn** bei
      Umbau oder Modellwechsel.
- [ ] Schreibende Werkzeuge, Verweigerung und Zuständigkeitsgrenze bei
      **100 %**; alles Übrige mindestens **95 %**.
- [ ] Der Adapter fährt denselben Weg wie die Anwendung und führt keine
      schreibenden Werkzeuge wirklich aus.
- [ ] Der Goldlauf läuft in der CI bei jeder Änderung an Prompt,
      Katalog, Werkzeug, Schema, Adapter oder Modell — und wöchentlich
      ohne Änderung.
- [ ] Kein Goldfall wurde an das Verhalten angepasst; Änderungen an
      Fällen tragen einen Vermerk mit Grund.
- [ ] Zahlen **vorher und nachher** sind berichtet, je Sprache und je
      Absicht — nicht nur der Mittelwert.

## Modell

- [ ] Feste Fassung, kein „latest", kein gleitender Alias.
- [ ] Modellname und Fassung stehen in der Konfiguration, nicht im Code.
- [ ] Die Fassung steht in jedem Goldfall-Bericht.
- [ ] Je Stufe ein Modell; die Einordnung läuft nicht auf dem stärksten.
- [ ] Ein Modellwechsel wurde allein gemessen, ohne begleitende Änderung,
      und als Entscheidungsakte festgehalten.
- [ ] Kein Modellwechsel als Ersatz für einen Umbau.

## Betrieb und Recht

- [ ] Der Assistent gibt sich als Maschine zu erkennen, sichtbar und in
      jeder Sprache (Skill `neo-ki`).
- [ ] Zeitüberschreitung, Längengrenze, Rate Limit und Kostengrenze sind
      gesetzt (Skill `neo-ki`).
- [ ] Keine Eingaben und Ausgaben im Klartext protokolliert; Kennung,
      Modell, Dauer, Verbrauch und Ergebnisart genügen.
- [ ] Fremder Text aus Datensätzen ist Daten, nie Anweisung — mit
      Goldfall belegt.
- [ ] Ist die KI-Fähigkeit abgeschaltet, startet die Anwendung und meldet
      die Funktion als nicht verfügbar.
- [ ] Der Anwender kann eine falsche Antwort melden, und jemand liest die
      Meldung.

## Änderung und Doku

- [ ] Eine Änderung je Commit, mit Messung davor und danach.
- [ ] Kein Umbauschritt wurde nachgebessert, statt ihn zurückzunehmen.
- [ ] Absichtskatalog, Werkzeuge, Schemata und Adapter sind dokumentiert
      (Skill `neo-doku`).
- [ ] Tragende Entscheidungen liegen als Entscheidungsakte vor.
- [ ] Ein zweiter Assistent teilt das Skelett; nichts wurde kopiert.
