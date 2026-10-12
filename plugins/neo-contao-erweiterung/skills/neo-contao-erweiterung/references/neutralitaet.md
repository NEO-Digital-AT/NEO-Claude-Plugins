# Neutralität

Eine Erweiterung wird an fremde Agenturen verkauft. Sie darf weder den
Hersteller noch ein Kundenprojekt verraten. Diese Datei sagt, was das im
Einzelnen heißt.

## Was nicht vorkommen darf

| Was | Wo es typischerweise durchrutscht |
| --- | --- |
| Name des Inhabers oder eines Mitarbeiters | Hilfstext „z. B. …", Beispiel in der Doku, Kommentar „Befund von …", Knopftext „An … weiterleiten" |
| Firmenname, Domain, Adresse, Telefonnummer | README „Built by …", `composer.json` `homepage`, Beispielkonfiguration, Absender in Testmails |
| Stadt oder Region des Herstellers | Beispiel „Zahnarzt in …", Testdaten |
| Kundennamen, Kundenprodukte, Kundendomains | Kommentare aus dem Projekt, aus dem die Erweiterung stammt; Testdaten; Screenshots |
| Hausfarben, Hausschriften, Hausklassen, Logo | Standard-CSS, PDF- und Mail-Vorlage, Vorschaubilder |
| Projektdatum und Projektbezug | „ergänzt am … für …", „Ansage vom …" |

**Erlaubt** sind: der Name der Erweiterung selbst (er darf die Marke
tragen), das Backend-Menü der Erweiterung, `authors` in `composer.json`
und der Rechteinhaber in `LICENSE`. Sonst nichts.

## Neutrale Beispielwerte

Beispiele werden mitübersetzt und bleiben in jeder Sprache erfunden.

| Sprache | Person | Vorname (für Knöpfe) | Ort |
| --- | --- | --- | --- |
| de | Max Mustermann | Max | Musterstadt |
| en | John Smith | John | Springfield |
| fr | Jean Dupont | Jean | — |
| nl | Jan Jansen | Jan | — |
| it | Mario Rossi | Mario | — |
| pl | Jan Kowalski | Jan | — |
| cs | Jan Novák | Jan | — |
| hu | Kovács János | János | — |
| sl | Janez Novak | Janez | — |
| hr | Ivan Horvat | Ivan | — |
| es | Juan Pérez | Juan | — |

- **E-Mail-Adressen** nur mit den reservierten Domains `example.com`,
  `example.org`, `example.net` (RFC 2606). `name@company.com` sieht
  harmlos aus, ist aber eine echte Domain. Der lokale Teil darf übersetzt
  sein: `jmeno@example.com`.
- **Websites:** `https://example.com`.
- **Telefon:** keine Nummer, oder eine offensichtlich erfundene ohne
  echte Vorwahl.
- **Logos und Porträts** in Beispielen: Platzhalterpfade wie
  `files/theme/logo.svg`, `files/theme/portrait.jpg`.

## Neutrales Design

- Web-Komponente: schlichtes Grunddesign, **alle** Farben, Abstände,
  Radien und Schriften als CSS-Variablen mit eigenem Präfix (z. B.
  `--nwc-*`). Keine Inline-Stile aus der Konfiguration — sie schlagen das
  Theme-CSS des Kunden.
- PDF und E-Mail: neutrale Vorlage, Markenfarben und Logo kommen aus den
  Backend-Einstellungen bzw. der Konfiguration des Kunden.
- Die Gestaltung für ein bestimmtes Projekt (Hausfarben, eigenes
  PDF-Layout) entsteht **in der Website dieses Projekts** — Template-
  Überschreibung unter `templates/`, CSS-Variablen im Theme, Werte in der
  Datenbank. Nie im Paket.

## Prüfen

```
python3 plugins/neo-contao-erweiterung/scripts/bundle-check.py <bundle> \
  --forbid "<Vorname>" --forbid "<Nachname>" --forbid "<Firma>" --forbid "<domain.tld>"
```

- Begriffe werden als ganze Wörter gesucht: „Erich" trifft nicht
  „Bericht".
- Zusätzlich meldet das Werkzeug jede E-Mail-Adresse außerhalb der
  Beispiel-Domains und Zahlenfolgen, die wie eine Telefonnummer aussehen.
- `LICENSE` und `authors` in `composer.json` werden übersprungen.
- Ergebnis muss **null Befunde** sein. Ein Befund wird behoben, nicht
  weggeschaltet.

Was das Werkzeug nicht sieht, wird von Hand geprüft: Bilder und
Screenshots im Paket (zeigen sie eine echte Website, einen echten Namen?),
Standardfarben in CSS und Vorlagen.
