# Datenschutzerklärung und Consent

## Die Datenschutzerklärung

Sie beantwortet für **jede** Verarbeitung: wer, was, wozu, auf welcher
Grundlage, wie lange, an wen, wohin — und welche Rechte der Betroffene
hat.

| Abschnitt | Inhalt |
| --- | --- |
| Verantwortlicher | Name, Anschrift, Kontakt; Datenschutzbeauftragter, falls bestellt |
| Verarbeitungen | je Zweck: welche Daten, Rechtsgrundlage, Speicherdauer, Empfänger |
| Server-Protokolle | IP, Zeitpunkt, angeforderte Ressource, Zweck, Dauer |
| Kontaktaufnahme | Formular, E-Mail, Telefon — was gespeichert wird und wie lange |
| Cookies und ähnliche Techniken | vollständige Auflistung, siehe unten |
| Externe Dienste | je Dienst: Anbieter, Sitz, Zweck, Daten, Drittland, Link auf dessen Erklärung |
| Newsletter | Anmeldeverfahren, Nachweis, Abmeldung |
| Bewerbungen, Kundenkonten, Zahlungen | soweit vorhanden |
| Betroffenenrechte | Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch, Datenübertragbarkeit, Widerruf |
| Beschwerderecht | Österreichische Datenschutzbehörde, mit Anschrift |
| Stand | Datum der letzten Änderung |

Sprache: verständlich, nicht juristisch verklausuliert. Fachbegriffe beim
ersten Auftreten erklären.

## Cookie-Auflistung

Für **jedes** Cookie und jede vergleichbare Speicherung:

| Spalte | Beispiel |
| --- | --- |
| Name | `neo_consent` |
| Anbieter | eigene Domain |
| Zweck | speichert die Einwilligungsentscheidung |
| Kategorie | notwendig |
| Laufzeit | 6 Monate |
| Art | Cookie, lokaler Speicher, Sitzungsspeicher |

- **Die Liste stammt aus dem Consent-Werkzeug**, nicht aus dem Gedächtnis.
  Wo das Werkzeug die Daten pflegt, wird die Seite daraus erzeugt oder
  eingebunden; zwei getrennt gepflegte Listen laufen auseinander.
- Die Liste wird gegen die Wirklichkeit geprüft: Seite in einem frischen
  Profil aufrufen, ablehnen, Speicher ansehen — es darf nur stehen, was
  als notwendig gelistet ist.

## Consent — die Regeln

1. **Nichts von Dritten vor der Einwilligung.** Keine Schrift, keine
   Karte, kein Video, kein Zählpixel, kein Chat, kein eingebetteter
   Rahmen, keine Vorverbindung.
2. **Eingebettete Rahmen sind Drittzugriffe.** Bis zur Einwilligung steht
   dort eine Vorschau aus dem eigenen Haus: eigenes Standbild, Titel, ein
   Satz, was beim Klick geladen wird, und ein Knopf. Erst der Klick lädt.
3. **Gleichwertigkeit.** „Ablehnen" auf derselben Ebene, in derselben
   Größe, mit derselben Auffälligkeit wie „Akzeptieren". Kein grauer
   Textlink gegen einen farbigen Knopf.
4. **Keine Vorauswahl.** Nur notwendige Kategorien sind aktiv; alles
   andere ist aus, bis jemand es einschaltet.
5. **Nur echte Kategorien.** Eine Kategorie ohne eingesetzten Dienst
   entfällt.
6. **Granular.** Wer nur eine Kategorie will, bekommt nur eine.
7. **Widerruf jederzeit**, über einen festen Punkt in der Fußzeile, so
   einfach wie die Erteilung. Nach dem Widerruf werden die gesetzten
   Daten entfernt.
8. **Nachweisbar.** Zeitpunkt, Fassung des Textes und Umfang der
   Einwilligung werden festgehalten — ohne mehr Daten zu speichern als
   nötig.
9. **Drittland benennen.** Geht etwas in die USA oder anderswohin,
   steht das im Dialog, nicht nur in der Erklärung.
10. **Kein Zwang.** Kein Sperren der Seite, kein Weiterscrollen als
    Zustimmung, kein wiederholtes Nachfragen nach einer Ablehnung.
11. **Der Dialog ist barrierefrei:** Tastatur, Fokusfalle, Escape,
    Kontrast, Vorlesegerät — er ist das erste Bedienelement der Seite
    (Skill `neo-design`).

## Prüfung mit dem Netzwerkmitschnitt

Der einzige belastbare Nachweis:

1. Frisches Browserprofil, Entwicklerwerkzeuge, Netzwerkanzeige öffnen.
2. Seite aufrufen, **nichts** anklicken.
3. Alle Anfragen nach Ziel-Host sortieren.
4. **Jeder Host außer der eigenen Domain ist ein Befund** — Schriften,
   Karten, Videos, Analyse, Ersatzverweise eingeschlossen.
5. Speicheransicht prüfen: nur als notwendig gelistete Einträge.
6. Ablehnen, neu laden, wiederholen. Dann annehmen und prüfen, ob genau
   die erlaubten Hosts dazukommen — nicht mehr.

Das Ergebnis wird als Liste der Hosts berichtet, nicht als „geprüft".

## Externe Dienste: was vorliegen muss

Vor dem Einbau eines Fremddienstes:

- Anbieter mit vollständigem Namen und Sitz
- Zweck und übertragene Daten
- Rechtsgrundlage und Speicherdauer
- Drittlandübermittlung und deren Grundlage
- Link auf die Datenschutzerklärung des Anbieters
- Auftragsverarbeitungsvertrag, wo nötig
- Kategorie im Consent-Werkzeug

Fehlt eines davon, wird der Dienst nicht eingebaut, sondern der fehlende
Punkt beschafft oder ein anderer Dienst vorgeschlagen.

## Schriften

Selbst ausliefern, von der eigenen Domain, mit eigener Vorladung. Nie von
einem fremden Dienst. Ausweichlösung nach Abstimmung: **bunny.net**.

Eine Schrift, die von einem fremden Host geladen wird, überträgt die
IP-Adresse jedes Besuchers — vor jeder Einwilligung, auf jeder Seite.
Das ist kein Randfall, sondern der häufigste Befund überhaupt.
