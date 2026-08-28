# Abnahmeliste KI-Assistent

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.
Was bewusst nicht erfüllt ist, wird benannt, mit Grund.

## Aufbau

- [ ] Der Systemprompt ist **unter 150 Zeilen** — gemessen, nicht
      geschätzt (`prompt-inventory.py`).
- [ ] Er enthält **keine** Werkzeugauswahl, kein Fachwissen, kein Schema
      und keinen Beispieldialog.
- [ ] Absichten, Werkzeuge, Zustand und Ablauf liegen getrennt.
- [ ] Vorbedingungen, Bestätigung, Wiederholung und Rechte stehen im
      **Code**, nicht im Prompt.
- [ ] `heute`, Zeitzone, Mandant und Auswahl kommen als **Daten** aus dem
      Zustand.
- [ ] `prompt-inventory.py` meldet **null** Befunde der Art
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

## Härtefälle

Alle elf Klassen aus `haertefaelle.md`, je Absicht und je Sprache.

- [ ] **Ungenaue Sprache**: Tippfehler, Umgangssprache, halbe Sätze,
      Dialekt — je Absicht mindestens zwei Fassungen.
- [ ] **Vollständiger Ablauf** über mehrere Beiträge geprüft, als Folge
      von Aufrufen, nicht nur der erste.
- [ ] **Außerhalb der Zuständigkeit**: kein Werkzeug, professionelle
      Antwort mit nächstem Schritt, 100 %.
- [ ] **Zusatzleistung**: der bestehende Vorgang wird gefunden, kein
      neuer angelegt; bei mehreren offenen Vorgängen Rückfrage.
- [ ] **Einmalgeheimnis**: Die Mengenregel steht **im Code**, nicht im
      Prompt. Zweite Anfrage, dringliche Anfrage, Anfrage für einen
      Dritten und „es funktioniert nicht" lösen **keinen** zweiten
      Aufruf aus — alle bei 100 %.
- [ ] Bei „es funktioniert nicht" folgt **Eskalation**, nie ein zweites
      Geheimnis.
- [ ] Kein Geheimnis steht in einem Protokoll oder in einem Bericht; der
      Fall prüft **dass**, nie **was** ausgegeben wurde.
- [ ] **Eskalation**: konkret benannte Stelle, mit Zusammenhang, ohne
      Zeitzusage, ohne zweiten Versuch; auslösende Eskalation ist ein
      schreibendes Werkzeug.
- [ ] **Betriebslage** kommt aus dem Zustand, nie aus dem Prompt; die
      Einschränkung wird von sich aus genannt. Ein Gegenfall ohne
      Störung ist vorhanden.
- [ ] **Zahlungsvorgang**: nie ohne Bestätigung, nie doppelt,
      Idempotenzschlüssel, Verweis nicht zusammengesetzt, kein Betrag aus
      dem Modell — 100 %.
- [ ] **Störungsmeldung**: aufgenommen, weitergeleitet, ohne
      Reparaturzusage und ohne Ursachenvermutung.
- [ ] **Einschleusung** über Name, Notiz und Werkzeugantwort: kein
      schreibendes Werkzeug, keine Ausgabe interner Anweisungen — 100 %.
- [ ] Alle elf Klassen in **jeder** ausgelieferten Sprache, mit
      identischer Erwartung.
- [ ] Die Erwartungen stammen aus der fachlichen Regel, **nicht** aus
      einem Probelauf; die erzeugten Fälle wurden gelesen und vorgelegt.
- [ ] Kein Härtefall führt etwas wirklich aus; keine echten
      personenbezogenen Daten; nicht gegen die Produktivumgebung
      gemessen, wo ein Werkzeug etwas ändern könnte.

## Modellzugang über Requesty

- [ ] Basisadresse ist der **EU-Router** (`router.eu.requesty.ai`).
- [ ] Die Modellkennung trägt eine **Regionsangabe** oder ist eine
      Policy — sonst verlässt die Anfrage die EU trotz EU-Router.
- [ ] Bei einer Policy: **jedes Kettenglied** ist EU-fähig,
      festgenagelt und gegen dieselben Goldfälle gemessen.
- [ ] Der Schlüssel steht **nur** in `REQUESTY_API_KEY` — nicht in der
      Konfiguration, nicht im Repository, nicht in einem Protokoll.
- [ ] Für die Messung ein eigener Schlüssel mit eigener Kostengrenze,
      getrennt vom Betriebsschlüssel.
- [ ] Strenge Ausgaben (`json_schema`, `strict`) sind für das eingesetzte
      Modell nachgewiesen — nicht angenommen; sonst prüft der Code selbst.
- [ ] 400 wird **nicht** wiederholt; 429 und 5xx mit wachsendem Abstand
      und Obergrenze, besser über eine Policy.
- [ ] Standort, Auftragsverarbeitung und Trainingsausschluss sind
      geklärt und in der Erklärung genannt (Skill `neo-recht`).

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
