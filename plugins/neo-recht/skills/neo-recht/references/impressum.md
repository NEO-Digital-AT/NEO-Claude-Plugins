# Impressum und Offenlegung (Österreich)

Zwei Regelwerke greifen nebeneinander, dazu das Unternehmensrecht. Erfüllt
wird alles auf einer Seite, klar gegliedert.

Verstöße sind nicht folgenlos: nach ECG bis 3.000 Euro, nach § 25
MedienG bis 20.000 Euro.

## Nach § 5 ECG — für jede geschäftliche Website

| Angabe | Anmerkung |
| --- | --- |
| Name oder Firma | wie im Firmenbuch bzw. Gewerberegister |
| Geografische Anschrift der Niederlassung | Postfach genügt nicht |
| Elektronische Kontaktadresse | E-Mail für rasche Kontaktaufnahme; dazu üblicherweise Telefon |
| Firmenbuchnummer und Firmenbuchgericht | wenn eingetragen |
| UID-Nummer | wenn vorhanden |
| Kammer, Berufsverband | z. B. Wirtschaftskammer, Fachgruppe |
| Anwendbare berufsrechtliche Vorschriften und Zugang dazu | z. B. Gewerbeordnung, mit Link auf die Fassung im RIS |
| Berufsbezeichnung und Mitgliedstaat der Verleihung | bei reglementierten Berufen |
| Aufsichtsbehörde | bei bewilligungspflichtiger Tätigkeit, z. B. Bezirkshauptmannschaft/Magistrat |

## Nach §§ 24 und 25 MedienG — Offenlegung

- **Kleine Website** (nicht auf Meinungsbildung angelegt): Name oder
  Firma, Sitz oder Wohnort, Unternehmensgegenstand des Medieninhabers.
- **Größere Website** (Blog, Nachrichten, meinungsbildende Inhalte):
  zusätzlich Beteiligungsverhältnisse, Geschäftsführung bzw.
  vertretungsbefugte Organe, Aufsichtsrat, und die **grundlegende
  Richtung** („Blattlinie").
- Die Einordnung trifft nicht der Agent. Sie wird beim Kunden bzw.
  dessen Rechtsbeistand erfragt und im Projekt festgehalten.

## Nach § 14 UGB — bei eingetragenen Unternehmen

Firma, Rechtsform, Sitz, Firmenbuchnummer und Firmenbuchgericht gehören
auch auf die Website, nicht nur auf Geschäftsbriefe.

## Was zusätzlich ins Impressum gehört

- **Rechtevorbehalt / Urheberrecht.** Inhalte, Texte, Bilder, Grafiken
  und Aufbau sind geschützt; Verwendung nur mit Zustimmung.
- **Haftung für Inhalte.** Erstellung mit Sorgfalt, keine Gewähr für
  Richtigkeit, Vollständigkeit und Aktualität.
- **Haftung für Links.** Fremde Inhalte werden nicht überwacht; bei
  Kenntnis einer Rechtsverletzung wird der Link entfernt. Verantwortlich
  für verlinkte Seiten bleibt deren Betreiber.
- **Bildrechte.** Herkunft jeder verwendeten Grafik: eigenes Material,
  Bildagentur mit Lizenznummer, Urheber mit Nennungspflicht, freie
  Lizenz mit Bedingung. Wer eine Nennung verlangt, wird genannt — beim
  Bild oder gesammelt im Impressum.
- Bei Online-Handel zusätzlich die Angaben aus dem Verbraucherrecht
  (Widerrufsbelehrung, AGB, Zahlungs- und Versandbedingungen) — auf
  eigenen Seiten, nicht im Impressum vermischt.

## Was nicht mehr hineingehört

**Der Hinweis auf die EU-Plattform zur Online-Streitbeilegung entfällt.**
Die Plattform wurde am **20.07.2025** eingestellt; die Verordnung (EU)
2024/3228 hat die ODR-Verordnung aufgehoben. Der Link ist aus Impressum,
AGB und E-Mail-Signaturen zu **entfernen** — ein Verweis auf eine
abgeschaltete Plattform ist irreführend.

Ältere Vorlagen tragen ihn noch. Bei jeder Bestandsseite prüfen.

## Umsetzung

- Alle Angaben kommen aus **Feldern**, nicht aus dem Template (Skill
  `neo-contao`). Eine Adressänderung darf keine Codeänderung sein.
- Die Seite ist aus jeder Seite über die Fußzeile erreichbar, ohne
  Einwilligung, ohne `noindex`.
- **Keine E-Mail-Adresse lesbar im ausgelieferten HTML** — das gilt für
  jede Adresse auf jeder Seite, eigene wie fremde, nicht nur im Impressum
  (Erich 21.11.2026: „meine regel gilt für alle mailadressen!“). Im
  Quelltext steht die Adresse **so gut verschlüsselt, wie es geht**; in der
  Ansicht sieht der Besucher sie ganz normal („email muss so gut es geht
  verschlüsselt sein, aber ein seitenbesucher soll sie im klartext
  sehen“). Nicht lesbar heißt auch:
  - **keine Ersatzform** wie „name(at)domain“ oder „name [at] domain“ —
    Bots lesen sie genauso („das bringt null. das erkennen die bots
    dennoch“);
  - **keine HTML-Zeichencodes** (`&#97;&#x67;…&#64;…`): Contaos Filter
    `encode_email`, den jedes Rich-Text-Element benutzt, schreibt Adressen
    so; der Browser zeigt sie lesbar, Bots entschlüsseln sie in einem
    Schritt. Die Verschleierung muss diese Form erkennen;
  - **kein bloßes Base64**, auch nicht umgedreht: Sammler entschlüsseln
    Base64 von sich aus. Der Wert wird mit einem Schlüssel verknüpft, der
    bei jedem Aufruf neu entsteht und nur im Skript steht.
- Ganz verhindern lässt es sich nicht: Ein Bot, der Seiten wie ein Browser
  ausführt, sieht, was der Besucher sieht. Die Verschlüsselung hält alle ab,
  die nur den Quelltext lesen.
- Umsetzung: Ein Listener am Ende der Antwort ersetzt `mailto:`-Links und
  sichtbare Adressen durch Elemente mit verschlüsseltem Wert (XOR mit dem
  Schlüssel des Aufrufs, dann Base64) und leerem Inhalt; ein kleines
  Skript vor `</head>` setzt die Adresse ein, sobald der Browser das
  Element liest — vor dem ersten Bild, ohne Layout-Sprung. Ohne
  JavaScript bleibt die Stelle leer, ein Mail-Link führt zum
  Kontaktformular. Vorlage: `EmailObfuscationListener` in
  `NEO-Digital-AT/website`.
- Nie eine Adresse in strukturierten Daten — diese Blöcke werden von der
  Verschleierung übersprungen.
- In jeder ausgelieferten Sprache vorhanden. Die Pflichtangaben ändern
  sich dabei nicht, nur die Sprache der erklärenden Sätze.
