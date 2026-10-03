# Abnahmeliste KI-Assistent

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Bauweise

- [ ] Der Assistent besteht aus Modell, Werkzeugen und Skills — sonst
      nichts.
- [ ] Kein Router, kein Klassifizierer, keine Wortliste vor dem Modell.
- [ ] Keine Fachagenten, keine Übergabe zwischen Modellen.
- [ ] Kein Prüfagent, kein Antwortprüfer, kein Endredakteur.
- [ ] Keine fachliche Regel im Code; im Code nur Mandant, Rechte,
      Eigentum, gültige Angaben, Doppelausführung.
- [ ] Kein Text vom Server an den Kunden; jede Antwort schreibt das
      Modell, die Anwendung hängt nur KI-Hinweis und Signatur an.
- [ ] Die KI schaltet sich nie still ab: Die Übergabe trägt die Nachricht
      des Modells an den Kunden als Pflichtangabe; kein Code gibt ein
      Gespräch ab.
- [ ] Keine fachliche Folgekette; Hintergrundarbeit führt nur zu Ende, was
      das Modell ausgelöst hat.
- [ ] Kein Laufzeitprompt im Code; kein Kommentar und kein Test beschreibt
      eine stillgelegte Bauweise.

## Kontext und Schleife

- [ ] Kern, alle Aufgaben-Skills und alle Werkzeugdefinitionen stehen ab
      dem ersten Aufruf im Kontext — gemessen.
- [ ] Einstellungen, Zustand und Gespräch kommen als eigene Abschnitte.
- [ ] Neue Nachrichten gehen in den laufenden Lauf ein; je Gespräch läuft
      genau ein Lauf.
- [ ] Die Grenzen der Schleife stehen in der Konfiguration und enden nie
      mit einer Absage oder einer stillen Abschaltung.
- [ ] Ein voller Kontext wird komprimiert — älterer Verlauf und ältere
      Werkzeugergebnisse ins Gedächtnis —, die Arbeit läuft weiter.
- [ ] Eine abgeschnittene Modellantwort führt keine Werkzeugaufrufe aus.
- [ ] Zugestellt wird nur die fertige Antwort, mit KI-Hinweis und
      Signatur aus der Anwendung.

## Zugriff

- [ ] Die Art des Assistenten ist festgelegt und dokumentiert.
- [ ] Die Werkzeuge passen zur Art; keine Kundenassistenz hat ein
      prozesskritisches Werkzeug.
- [ ] Der Mandant kommt aus Anmeldung oder Kanal; jedes Werkzeug arbeitet
      mit dessen Zugangsdaten; jede Kennung wird gegen ihn geprüft.
- [ ] Die Mandantentrennung ist mit einem Test nachgewiesen.
- [ ] Bei Kundendaten: Nachweis mit zwei bis drei Merkmalen vor jeder
      Auskunft zu einem bestehenden Vorgang, Abgleich im Werkzeug, Sperre
      nach Fehlversuchen.
- [ ] Die Abrechnung zwischen Plattform und Mandant erreicht nur die
      Plattformassistenz.
- [ ] Geheimnisse erreichen das Modell nur als Platzhalter.
- [ ] Schalter wirken im Werkzeug; Anweisungen des Betreibers wirken beim
      Modell, mit Vorrang vor dem Standard im Skill.

## Werkzeuge

- [ ] Eine Freigabeliste je Assistent; Werkzeuge außerhalb werden nicht
      ausgeführt.
- [ ] Die Definitionen kommen vom Server; jeder Vertrag ist gegen die
      Dokumentation und einen echten Aufruf belegt.
- [ ] Fehler gehen als Tatsache an das Modell; kein schreibender Aufruf
      wird verdeckt wiederholt.
- [ ] Schreiben mit Folgen läuft über Vorbereiten und Ausführen; das Token
      bleibt intern.
- [ ] Jeder Schreibvorgang ist vor dem Aufruf vermerkt und idempotent; ein
      ungewisses Ergebnis wird geklärt.
- [ ] Kein Werkzeug gibt einen fertigen Satz für den Kunden zurück.
- [ ] Das Modell kann seine Werkzeuge selbstständig nutzen; eine
      freigegebene Website ist frei durchsuchbar, nicht nur über `llms.txt`.

## Skills

- [ ] Ein Paket aus Kern, Aufgaben-Skills und Manifest, versioniert im
      Repository, in die Anwendung eingebettet, beim Start geprüft.
- [ ] Jede Regel steht genau einmal und nicht zugleich im Code.
- [ ] Englisch, im Befehlston; keine Beschreibung ist eine Wortliste.
- [ ] Skills nur für komplexe Abläufe mit Folgen, je in der Form Zweck,
      Werkzeuge, Schritte, Nie, Übergabe, unter der Längengrenze des
      Projekts.
- [ ] Der Kern verbietet das Erfinden: Genannt wird nur, was ein Werkzeug,
      das Wissen oder das Gespräch belegt.
- [ ] Kein Skill wird aus Kundennachricht, Webseite, Anhang oder
      beschreibbarer Einstellung geladen.
- [ ] Jede Änderung hat die Fassung im Manifest gehoben.

## Modell

- [ ] Basisadresse ist der Requesty-EU-Router; die Modellkennung trägt
      eine Regionsangabe.
- [ ] Der Schlüssel steht nur in der Umgebung.
- [ ] Feste Fassung, Denktiefe und Zeitgrenze stehen in der Konfiguration.
- [ ] Angefragtes und geliefertes Modell sind je Lauf festgehalten.

## Belege

- [ ] Belegart 1: Tests der Werkzeuggrenzen für Mandant, Nachweis,
      Schalter, Freigabeliste, Doppelausführung, neue Nachrichten,
      Zustellung, Übergabe und Paket — grün.
- [ ] Belegart 2: Lauf im Staging mit Testdaten für jeden betroffenen
      Ablauf, in jeder ausgelieferten Sprache — bewertet an der Wirkung im
      Fachsystem.
- [ ] Keine Prüfskripte um das Modell.
- [ ] Keine echten Kundendaten, keine echten Zahlungen.
- [ ] Die zwei Belegarten sind in der Fertigmeldung getrennt berichtet.
