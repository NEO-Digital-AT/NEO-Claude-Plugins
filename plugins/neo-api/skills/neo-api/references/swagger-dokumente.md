# Swagger-Dokumente schneiden

## Der Schnitt

Ein Dokument je Fachbereich, je Modul und je Sichtbarkeitsstufe. Der
Auswähler in der Oberfläche ist damit zugleich das Inhaltsverzeichnis der
Schnittstelle.

| Dokument | Inhalt | Sichtbar |
| --- | --- | --- |
| `Authentication` | Anmeldung, Token, Abmeldung | immer |
| `<Fachbereich> V1` | stabile Kundenfläche eines Bereichs | immer |
| `<Fachbereich> NSFW` | Vorschaufläche desselben Bereichs | immer, als instabil gekennzeichnet |
| `Module <Name> V1` / `NSFW` | Laufzeitfläche **eines** Moduls | immer |
| `Modules V1` / `NSFW` | nur der Modulkern: Katalog, Buchung, Gutschein, Zuordnungen, Kündigung, Abrechnungsstand | immer |
| `Administration` | Verwaltungsrouten `/admin/...` | nur mit Konfigurationsschalter |
| `Development` | Entwicklerendpoints | nur in der Entwicklung |
| `Frontend` | Bootstrap-Routen der eigenen Oberfläche | **nicht** in der Kundenansicht; nur intern und nur mit Schalter |
| `Webhooks` | eingehende Ereignisse | immer |

## Regeln

1. **Ein neues Modul bekommt eigene Dokumente**, stabil und Vorschau.
   Das gemeinsame Modul-Dokument wächst nicht mit — es trägt nur den
   Kern, der für alle Module gilt.
2. **Verwaltung und Entwicklung hängen an einem Schalter.** Ohne ihn
   existiert die Adresse nicht. Ein vergessener Konfigurationswert darf
   keine Diagnosefläche veröffentlichen.
3. **Ist ein Verwaltungsdokument freigeschaltet, muss es stimmen.** Ein
   veröffentlichtes Dokument, das nicht zu den Routen passt, ist
   schlimmer als keines.
4. **Die Bootstrap-Fläche der eigenen Oberfläche ist keine Kundenfläche.**
   Sie steht nicht in der öffentlichen Auswahl und wird nie als
   Integrationsweg beschrieben.
5. **Tags gruppieren nach Sachgebiet.** Verwaltungsrouten bekommen eigene
   Tags (`AdminAccounts`, `AdminModules`, `AdminProperties`, …), damit
   sich das Dokument navigieren lässt.
6. **Die Anzeigeoberfläche ist abschaltbar.** Sie wird vor der
   Autorisierung ausgeliefert und braucht deshalb ihren eigenen Schalter.

## Wiederverwendbare Verträge

Was mehr als einmal vorkommt, existiert einmal:

- Adresse
- Firma, einschließlich Abteilung
- Rechnungskontakt
- die Fehlerhülle

Ein zweites Adressschema in einem zweiten Bereich ist ein Befund, kein
Feature. Wo ein Feld fehlt, wächst das gemeinsame Schema — mit Prüfung
der Auswirkung auf alle Nutzer.

## Was ins Dokument gehört

- Jede Antwort, die vorkommen kann — auch `400`, `401`, `403`, `404`,
  `409`, `422`, `429`.
- Beispiele mit **echten, plausiblen** Werten. Nie mit Produktivdaten,
  nie mit Kartendaten, nie mit Klartext-Adressen.
- Bei geschützten Operationen: Modus und benötigte Rechte.
- Bei Vorschauflächen: ein sichtbarer Hinweis, dass sie brechen dürfen.

## Prüfung

- Das Dokument wird bei jeder Änderung neu erzeugt und der Unterschied
  angesehen. Ein unbeabsichtigter Vertragsbruch fällt nur dort auf.
- Wo möglich, prüft ein Test, dass jede Route in genau einem Dokument
  steht und keines verwaist ist.
- Ein Endpoint ohne Eintrag im Dokument gilt als nicht vorhanden.
