# Barrierefreiheitserklärung und das Barrierefreiheits-Werkzeug

## Zwei Regime, ein Dokument

| Regime | Wen es trifft | Was verlangt wird |
| --- | --- | --- |
| **WZG** | öffentliche Stellen | Eine förmliche Erklärung zur Barrierefreiheit nach dem EU-Muster, samt Feedback-Weg und Durchsetzungsverfahren |
| **BaFG** | Produkte und Dienste am Markt | Informationen darüber, wie der Dienst die Anforderungen erfüllt — mit den Ausnahmen und ihrer Begründung |

Die Form unterscheidet sich, der Inhalt überschneidet sich weitgehend.
NEO baut in beiden Fällen dieselbe Seite und passt Wortlaut und Umfang
an. Welches Regime gilt, wird beim Kunden erfragt, nicht angenommen.

## Inhalt

| Abschnitt | Was hineingehört |
| --- | --- |
| Geltungsbereich | Für welche Website, Anwendung oder welchen Dienst die Erklärung gilt |
| Stand der Vereinbarkeit | vollständig, teilweise oder nicht vereinbar — mit dem angewandten Maßstab (EN 301 549 bzw. WCAG 2.2 AA) |
| Nicht barrierefreie Inhalte | **einzeln aufgezählt**, je Punkt der Grund: technisch nicht möglich, unverhältnismäßige Belastung, Inhalt außerhalb des Anwendungsbereichs — dazu, was stattdessen angeboten wird |
| Erstellung der Erklärung | Datum, Verfahren: Selbstbewertung oder Prüfung durch Dritte, mit Nennung der Stelle |
| Letzte Überprüfung | Datum; die Erklärung wird bei jeder wesentlichen Änderung nachgezogen |
| Feedback und Kontakt | Ein Weg, um Barrieren zu melden und barrierefreie Fassungen anzufordern, mit Reaktionsfrist |
| Durchsetzungsverfahren | Wohin sich jemand wenden kann, wenn die Rückmeldung ausbleibt |

**Die Ausnahmen werden ehrlich benannt.** Eine Erklärung, die
„vollständig vereinbar" behauptet, während der Kontrast an drei Stellen
nicht passt, ist schlechter als eine, die die drei Stellen nennt und ein
Datum für die Behebung angibt.

Die Erklärung wird aus der tatsächlichen Prüfung gespeist — der Liste
aus `neo-design`, `references/pruefliste.md`. Wer nicht geprüft hat,
kann sie nicht schreiben.

## Das Barrierefreiheits-Werkzeug

Zusätzlich zur barrierefreien Seite bekommt jede Website ein
Bedienwerkzeug mit den üblichen Einstellungen:

- Kontrast erhöhen bzw. umstellen
- Schriftgröße ändern
- Graustufen- bzw. Schwarzweiß-Darstellung
- Links sichtbar markieren
- Vorlesen
- Bewegung abschalten
- Zeilen- und Wortabstand vergrößern
- Lesehilfe (Zeilenlineal, Fokusmaske)

Es ist **weder gesetzlich vorgeschrieben noch von den Fachstellen
empfohlen** — es ist ein Zusatz für Menschen, die es bequem finden.

### Die Regeln dazu

1. **Es ist ein Bonus, kein Ersatz.** Die Seite selbst muss barrierefrei
   sein. Ein Werkzeug, das eine unzugängliche Seite überdeckt, macht sie
   nicht zugänglich.
2. **Nie damit werben, es stelle Konformität her.** Solche Behauptungen
   sind der Grund, warum Überlagerungswerkzeuge in Fachkreisen einen
   schlechten Ruf haben. In der Barrierefreiheitserklärung wird das
   Werkzeug höchstens erwähnt, nie als Nachweis geführt.
3. **Das Werkzeug ist selbst barrierefrei:** per Tastatur erreichbar und
   bedienbar, mit Namen für Vorlesegeräte, ausreichendem Kontrast und
   einer Zielgröße von mindestens 24 px.
4. **Es bricht die Seite nicht.** Jede Einstellung wird in allen
   Ansichten geprüft — vergrößerte Schrift darf kein Layout zerlegen und
   kein horizontales Scrollen erzeugen.
5. **Es lädt nichts von Dritten.** Kein fremdes Skript, keine fremde
   Stimme, kein Zählpixel. Die Einstellungen bleiben im Browser des
   Besuchers.
6. **Die Auswahl bleibt erhalten** über Seitenwechsel hinweg, und sie
   lässt sich zurücksetzen.
7. Die Vorlesefunktion nutzt die Sprachausgabe des Browsers oder eine
   selbst betriebene Lösung — nicht einen Dienst, der den Seitentext
   nach außen schickt.

Umgesetzt in `NEO-Digital-AT/website` als `theme/js/a11y.js` und
`theme/scss/_a11y.scss`. Aufbau übernehmen, Gestaltung an die jeweilige
Marke anpassen.
