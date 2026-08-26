# Querschnitt — stackübergreifend

Diese Punkte hängen an keinem Framework und verursachen die teuersten
Fehler, weil sie erst spät auffallen und dann Daten betreffen.

## Zeit und Zeitzonen

- **Gespeichert wird in UTC.** Immer. Eine lokale Zeit in der Datenbank
  ist beim nächsten Serverumzug falsch.
- Zeitzonen als **IANA-Kennung** (`Europe/Vienna`), nie als Verschiebung.
  Eine Verschiebung ist zweimal im Jahr falsch.
- Umgerechnet wird erst bei der Anzeige, in der Zone des Anwenders bzw.
  des Objekts.
- **Ein Datum ohne Zeit ist etwas anderes als ein Zeitpunkt.** Ein
  Geburtstag, ein Anreisetag und ein Rechnungsdatum haben keine Uhrzeit
  und dürfen keine bekommen — sonst wandern sie über die Zeitzone.
- Dauern in Sekunden oder als Dauertyp, nie als Zeitpunktdifferenz aus
  zwei lokalen Zeiten.
- Die aktuelle Zeit kommt aus einer **einspritzbaren Quelle**, nicht aus
  einem statischen Aufruf — sonst ist das Verhalten nicht testbar.
- Anzeige in Österreich: `TT.MM.JJJJ` und 24 Stunden.

## Geld und Zahlen

- **Nie Gleitkomma für Geld.** Dezimaltyp oder kleinste Einheit als
  ganze Zahl. `0.1 + 0.2` ist auch in der Buchhaltung nicht `0.3`.
- **Die Währung wird immer mitgeführt.** Ein Betrag ohne Währung ist
  keine Zahl, sondern eine Falle.
- **Einmal gerundet, am Ende**, mit festgelegter Regel. Zwischenrundungen
  summieren sich zu Differenzen, die niemand mehr erklären kann.
- Steuersätze und Umrechnungskurse werden mit dem Vorgang gespeichert,
  nicht bei jeder Anzeige neu geholt — sonst ändert sich eine alte
  Rechnung rückwirkend.
- Prozentwerte eindeutig: `0.19` oder `19` — einmal festlegen, im Namen
  sichtbar machen.
- In der Oberfläche tabellarische Ziffern und die Formatierung der
  eingestellten Sprache (Skill `neo-design`).

## Kennungen

- Keine sprechenden Kennungen, aus denen sich etwas ableiten lässt.
- Keine Kennung aus Nutzereingabe übernehmen und als vertrauenswürdig
  behandeln.
- Nach außen sichtbare Kennungen sind nicht ratbar und nicht
  hochzählbar — sonst kann man eine Datenbank abgrasen.
- Der Mandantenkontext kommt **ausschließlich** aus den authentifizierten
  Ansprüchen, nie aus einem Parameter (Skill `neo-sicherheit`).

## Nullwerte und Vorgaben

- Nullbarkeit ist ausdrücklich, wo der Stack es kann.
- **Kein magischer Ersatzwert**: kein `0`, kein leerer Text, kein
  `0001-01-01` für „unbekannt". Unbekannt ist unbekannt.
- Eine Vorgabe wird gesetzt, weil sie fachlich richtig ist — nicht, um
  einen Nullwert loszuwerden.

## Fehlerbehandlung

- Ausnahmen für Ausnahmen. Erwartbare Fachfälle sind Ergebnisse.
- Nie leer fangen. Wer fängt, behandelt oder wirft weiter — mit Kontext
  und ohne den Stapel zu verlieren.
- Ein Fehler wird an genau einer Stelle in eine Antwort übersetzt, nicht
  in jedem Controller neu (Skill `neo-api`).
- **Ein stiller Rückfall ist schlimmer als ein Absturz.** Wer bei einem
  Fehler heimlich etwas anderes tut, erzeugt falsche Daten statt einer
  Meldung.

## Protokollierung

- Strukturiert, mit Vorlage und benannten Werten — nicht als
  zusammengeklebte Zeichenkette. Nur so lässt sich später zählen und
  filtern.
- **Eine Korrelationskennung** je Anfrage, durch alle Schichten und in
  die Antwort. Ohne sie ist eine Supportanfrage nicht auflösbar.
- **Nie personenbezogene Daten, Secrets, Tokens, Kennwörter oder
  Zahlungsdaten** ins Protokoll (Skill `neo-sicherheit`).
- Ebenen bewusst: `Debug` für Entwicklung, `Information` für
  Geschäftsereignisse, `Warning` für Auffälliges mit Weiterlauf, `Error`
  für Abbruch. Alles auf `Information` heißt: nichts ist auffindbar.

## Konfiguration

- Alles, was sich je Umgebung unterscheidet, ist Konfiguration.
- **Fail-closed:** fehlt ein Pflichtwert, startet die Anwendung nicht oder
  meldet einen klaren Konfigurationsfehler. Kein stiller Rückfall auf
  einen unsicheren Standard.
- Werte werden beim Start geprüft, nicht beim ersten Aufruf im laufenden
  Betrieb.
- Eine Beispieldatei (`.env.example`) im Repo hält jeden Schlüssel fest,
  mit Bedeutung und ohne echten Wert.

## Nebenläufigkeit

- Kein blockierendes Warten auf asynchrone Arbeit.
- Geteilter veränderlicher Zustand braucht eine ausdrückliche Absicherung
  — oder es gibt ihn nicht.
- Alles, was mehrfach eintreffen kann, ist **idempotent**: Webhooks,
  Wiederholungen, Aufträge, Zahlungen.
- Ein Hintergrundauftrag ist wiederholbar, ohne Schaden anzurichten.
- Sperren so kurz wie möglich; nie über einen Netzaufruf hinweg halten.

## Grenzen zu fremden Systemen

- Ein fremdes Modell wird an der Grenze in das eigene übersetzt. Kein
  fremder Typ wandert bis in die Fachlogik.
- Zeitüberschreitungen sind gesetzt — überall. Ein Aufruf ohne Frist
  hängt irgendwann für immer.
- Wiederholung mit wachsendem Abstand und Obergrenze, nur bei Fehlern,
  die sich wiederholen lassen.
- Ein Ausfall des Fremdsystems ist ein vorgesehener Zustand, kein
  Sonderfall: er wird behandelt, angezeigt und protokolliert.
