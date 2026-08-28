# Messwerte: PageSpeed Insights und Lighthouse

## Die Zielwerte

| Kategorie | Ziel | Untergrenze | Bemerkung |
| --- | --- | --- | --- |
| Leistung | 100 | **95** | Feldwerte zählen mehr als Laborwerte |
| Barrierefreiheit | 100 | **95** | Der Wert ist ein Teilcheck, kein Nachweis — siehe unten |
| Best Practices | **100** | 100 | Keine Ausrede: hier gibt es nichts, was nicht machbar wäre |
| SEO | **100** | 100 | Ebenso |
| Agentisches Browsen | **3/3** | 3/3 | Drei Prüfungen, alle drei bestehen |

**Gemessen wird mobil.** Der Mobilwert ist der Maßstab; Desktop läuft
nebenher mit. Eine Seite, die auf dem Schreibtisch 100 hat und auf dem
Telefon 74, ist nicht schnell.

Werte unterhalb der Untergrenze sind ein Befund, kein Merkposten. Wer
sie nicht erreicht, benennt die Ursache, den Aufwand und den Vorschlag —
und der Projektinhaber entscheidet, ob es dabei bleibt.

## Barrierefreiheit: 100 ist kein Nachweis

Der Lighthouse-Wert prüft automatisch, was sich automatisch prüfen lässt
— das ist ein Bruchteil der WCAG-Kriterien. Eine Seite mit 100 kann
unbedienbar sein.

Deshalb gilt unverändert: **WCAG 2.2 AA ist hart**, gerechnete
Kontraste, Tastaturweg, Vorlesegerät, Graustufen — die Prüfung in
`barrierefreiheit.md`. Der Lighthouse-Wert ist ein zusätzliches Tor, das
zeigt, ob die einfachen Dinge stimmen. Er ersetzt die Prüfung nicht, und
„Lighthouse sagt 100" ist keine Antwort auf einen gemeldeten Mangel.

## Agentisches Browsen — die drei Prüfungen

Seit Mai 2026 eine eigene Lighthouse-Kategorie. Sie liefert keine Zahl
von 0 bis 100, sondern ein Verhältnis. Die drei Standardprüfungen:

| Prüfung | Was sie will | Wie sie erfüllt wird |
| --- | --- | --- |
| Sauberer Accessibility-Tree | Bedienelemente haben Namen, Rollen und gültige Verschachtelung; nichts Bedienbares ist vor dem Baum versteckt | Fällt ab, wenn `barrierefreiheit.md` eingehalten wird: jedes Symbol mit Namen, Beschriftungen verknüpft, Überschriften ohne Sprünge, keine bedienbaren Elemente hinter `aria-hidden` |
| Stabiles Layout | Nichts verschiebt sich, während die Seite steht — ein Agent soll den richtigen Knopf treffen | Maße an Bildern und eingebetteten Rahmen, Platz für nachgeladene Inhalte reservieren, Schriften ohne Umsprung laden, Bewegung nur über `transform` und `opacity` (`webseiten.md`) |
| Gültige `llms.txt` | Eine `llms.txt` an der Domain-Wurzel, die dem Format entspricht | **Bei Webseiten Pflicht**, aus der Datenbank erzeugt, nicht von Hand gepflegt, dazu `llms-full.txt` (Skill `neo-contao`). Bei Web-Anwendungen und APIs nicht verlangt — dort ist OpenAPI der Vertrag (Skill `neo-api`) |

Die Kategorie ist eine Diagnose, kein Ranking-Faktor. Sie fordert nichts,
was diese Regeln nicht ohnehin verlangen — deshalb ist 3/3 die
Untergrenze, nicht das Ziel.

## Feld und Labor

- **Feldwerte** stammen aus echten Aufrufen und brauchen genug Verkehr.
  Sie sind das, was Nutzer erleben.
- **Laborwerte** kommen aus einem simulierten Lauf. Sie sind
  reproduzierbar und deshalb der Maßstab beim Bauen.
- Widersprechen sich beide, gewinnt das Feld. Eine Seite mit Laborwert 99
  und schlechten Feldwerten hat ein Problem, das der Labortest nicht
  sieht — meist Serverantwortzeit, Drittanbieter oder Netz.

## Was die Werte kostet

| Kategorie | Häufigste Ursache | Abhilfe |
| --- | --- | --- |
| Leistung | Bilder in falscher Größe oder falschem Format | Bildgrößen des CMS, moderne Formate, Maße im Markup |
| Leistung | Blockierendes CSS und JavaScript im Kopf | Nur ausliefern, was die Seite braucht; minifizieren; JavaScript nachrangig laden |
| Leistung | Schriften | Selbst ausliefern, vorladen, Anzeige ohne Umsprung |
| Leistung | Drittanbieter vor der Einwilligung | Nichts lädt vor der Einwilligung — das ist zugleich Pflicht (Skill `neo-recht`) |
| Layoutstabilität | Bilder und Rahmen ohne Maße, nachgeladene Banner | Maße setzen, Platz reservieren |
| Reaktionszeit | Lange JavaScript-Aufgaben beim ersten Tippen oder Klicken | Arbeit aufteilen, Effekte nach dem ersten Farbanstrich starten |
| Best Practices | Fehler in der Konsole, veraltete Schnittstellen, unsicheres Laden | Konsole muss leer sein; alles über HTTPS; Inhaltsrichtlinie setzen |
| SEO | Fehlender oder zu langer Titel, fehlende Beschreibung, fehlendes Canonical | Aus Feldern im CMS, nicht aus dem Template |
| SEO | Seiten auf `noindex`, die in der Sitemap stehen | Sitemap und Indexierungsangabe müssen zusammenpassen |

## Wann gemessen wird

- **Vor der Fertigmeldung**, auf der ausgelieferten Adresse, mobil, für
  **jede** Seitenvorlage — nicht nur für die Startseite. Eine Startseite
  mit 100 und eine Detailseite mit 68 ist ein Befund.
- **Nach jedem Ausrollen**, damit ein Rückschritt auffällt, solange man
  noch weiß, woher er kommt.
- Wo das Projekt es hergibt, als Tor in der Pipeline mit festen
  Schwellen (Skill `neo-deployment`).

**Berichtet werden Zahlen**, je Seite und je Kategorie, dazu die drei
Kernwerte für Ladezeit, Reaktion und Layoutstabilität. „Sieht schnell
aus" ist kein Messwert.
