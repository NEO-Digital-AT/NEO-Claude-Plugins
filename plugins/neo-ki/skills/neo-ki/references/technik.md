# KI technisch einbauen

## Die Abstraktion

- **Ein Dienst, eine Schnittstelle.** Der Fachcode ruft die eigene
  Abstraktion, nie das SDK eines Anbieters. Ein Anbieterwechsel darf
  keine Fachlogik anfassen (Skill `neo-code`).
- **Modell aus der Konfiguration**, mit einem Standardmodell als Rückfall
  und der Möglichkeit, es je Ablauf zu übersteuern. Kein Modellname im
  Code, keine Modellwahl in einer View.
- Routing, Residenz und Rückfall auf einen zweiten Anbieter gehören in
  die Konfiguration bzw. in den vorgeschalteten Dienst — nicht in
  Verzweigungen im Fachcode.
- **Ist die Fähigkeit abgeschaltet, startet die Anwendung trotzdem.** Die
  betroffenen Abläufe behandeln sie als nicht verfügbar und sagen das:
  eine Meldung, kein Absturz, kein stiller Rückfall auf etwas anderes.
  Bei einem Assistenten gehen die Nachrichten dann an das Team; der
  Server schreibt dem Kunden nichts (Skill `neo-assistent`).

## Fremder Text ist Daten, nie Anweisung

Der häufigste Angriff auf eine KI-Funktion braucht keine Lücke im Code —
er steht im Inhalt.

- Inhalte aus E-Mails, Webseiten, Dateien, Formularfeldern oder
  API-Antworten werden als **Daten** übergeben, klar abgegrenzt, nie
  als Teil der Aufgabenstellung.
- Die Aufgabenstellung liegt serverseitig und ist nicht von außen
  veränderbar.
- **Was das Modell zurückgibt, darf keine Rechte auslösen.** Ein
  Werkzeugaufruf wird gegen eine feste Liste geprüft, mit den Rechten
  des angemeldeten Nutzers ausgeführt und nie mit denen des Dienstes.
- Ausgaben, die weiterverarbeitet werden, werden gegen ein Schema
  geprüft. Freier Text aus einem Modell ist nie ein Datensatz.
- Verweise und Adressen aus einer Ausgabe werden nie ungeprüft
  aufgerufen. Bei einem Assistenten prüft das Werkzeug, das sie aufruft;
  welche Links das Modell schreibt, regeln Skill und Einstellungen.

## Ausgaben prüfen

Gilt für Ausgaben, die Code weiterverarbeitet — Datensatz,
Klassifizierung, Extraktion. **Die Antwort eines Assistenten an den
Kunden wird nie geprüft, gefiltert oder umgeschrieben**; seine Grenzen
halten die Werkzeuge (Skill `neo-assistent`).

- **Gestalt vor Inhalt:** erst prüfen, ob die Antwort die erwartete Form
  hat, dann verwenden.
- Bei Antworten mit Quellen: die Quelle muss existieren und den Inhalt
  tragen. Ein erfundener Verweis ist der klassische Fehler.
- Bei Klassifizierung: nur Werte aus der bekannten Menge annehmen;
  alles andere ist „unbekannt", nicht der nächstähnliche Wert.
- **Keine Zustandsänderung ohne Prüfung.** Löschen, Buchen, Senden,
  Bezahlen laufen nie direkt aus einer Modellausgabe. Bei einem
  Assistenten laufen sie über Werkzeuge, und das Werkzeug prüft Mandant,
  Rechte, Eigentum und die vorbereitete Handlung — nicht ein zweites
  Modell (Skill `neo-assistent`, `references/werkzeuge.md`).
- Ein Weg für Rückmeldungen des Anwenders auf eine falsche Antwort, und
  jemand, der sie liest.

## Grenzen und Kosten

- **Zeitüberschreitung gesetzt**, überall. Ein Modellaufruf ohne Frist
  hängt irgendwann für immer.
- Obergrenze für Ein- und Ausgabelänge, damit ein langer Eingang keine
  Kostenexplosion auslöst.
- Rate Limiting je Nutzer und je Mandant, nicht nur global (Skill
  `neo-api`).
- Wiederholung mit wachsendem Abstand und Obergrenze — nur bei Fehlern,
  die sich wiederholen lassen.
- Kosten sind sichtbar: je Ablauf zählen, was verbraucht wurde, und eine
  Grenze, ab der abgeschaltet statt weitergezahlt wird. Eine laufende
  Anfrage an einen Assistenten endet dabei nie still (Skill
  `neo-assistent`).
- Ein Zwischenspeicher für gleiche Anfragen, wo die Antwort nicht
  personenbezogen ist.

## Protokollierung

- **Keine Eingaben und Ausgaben im Klartext protokollieren**, solange
  darin personenbezogene Daten stehen können — und das können sie fast
  immer.
- Protokolliert werden Kennungen, Zeitpunkt, Modell, Dauer, Verbrauch,
  Ergebnisart und Fehler. Das reicht für den Betrieb.
- Wo Inhalte für die Verbesserung gebraucht werden, braucht es eine
  Einwilligung und eine Frist (Skill `neo-recht`).
- Die Korrelationskennung der Anfrage geht mit, damit sich eine Beschwerde
  zurückverfolgen lässt (Skill `neo-code`).

## Tests

- Der Anbieter wird in Tests **gefälscht**. Kein Test ruft ein echtes
  Modell — er wäre langsam, teuer und nicht reproduzierbar.
- Getestet wird das Verhalten drumherum: Abstraktion, Prüfung der
  Ausgabe, Fehlerfall, Zeitüberschreitung, abgeschaltete Fähigkeit,
  Grenzen.
- Die Qualität der Antworten zeigt nur ein Lauf mit dem echten Modell in
  der Testumgebung, mit Testdaten. **Kein Prüfskript und keine
  Fallsammlung bewertet Antworten automatisch.** Ruft die KI-Funktion
  **Werkzeuge** auf, gelten die Belegarten des Skills `neo-assistent`,
  `references/abnahme.md`: Tests der Werkzeuggrenzen und der Lauf im
  Staging.
- **Ein Modellwechsel ist eine Änderung mit Auswirkung** und wird wie
  eine solche behandelt: vorlegen, vergleichen, freigeben (Skill
  `neo-grundregeln`).
