# Secrets, Protokollierung, Audit

Lesekonvention siehe `SKILL.md`.

## Secrets

**Nie im Code, nie in committeter Konfiguration, nie in einem Abbild.**
Kein Freigabeweg. Ein Secret, das einmal im Verlauf steht, gilt als
kompromittiert und wird gewechselt — es reicht nicht, den Commit zu
entfernen.

| Wo Secrets liegen | Wo sie nie liegen |
| --- | --- |
| Umgebungskonfiguration des Betriebs | Quellcode |
| Verschlüsselungsdienst oder Tresor | committete `.env`, `appsettings.json`, `config.php` |
| Umgebungs-Secrets der Ausrollung (Skill `neo-deployment`) | Repository-Secrets, die jeder Zweig sieht |
| — | Abbilder, Build-Argumente, Zwischenschichten |
| — | Protokolle, Fehlermeldungen, Beispiele in der API-Beschreibung |
| — | Konfigurationsdateien eines MCP-Servers |

- **Rotation muss ohne Codeänderung möglich sein.** Ein Secret, dessen
  Wechsel ein Deployment erzwingt, wird nicht gewechselt.
- `.env.example` führt jeden Schlüssel mit Bedeutung, **ohne echten
  Wert**.
- Ein Secret wird beim Start geprüft: fehlt ein Pflichtwert, startet die
  Anwendung nicht oder meldet einen klaren Konfigurationsfehler. **Nie
  ein stiller Rückfall auf einen Standardwert.**
- Ein Vergleich von Geheimnissen läuft in **konstanter Zeit**.
- Ein konfiguriertes Geheimnis wird **nie protokolliert**, auch nicht
  gekürzt, auch nicht beim Start.

## Was nie in ein Protokoll gehört

Kein Freigabeweg:

- Personenbezogene Daten: Namen, Adressen, E-Mail, Telefon, Geburtsdatum
- Zugangsdaten, Tokens, Sitzungskennungen, Wiederherstellungscodes
- Zahlungsdaten in jeder Form
- Gesundheits- und Ausweisdaten
- Vollständige Anfrage- oder Antwortkörper aus Fachaufrufen
- Eingaben und Ausgaben eines Sprachmodells im Klartext (Skill `neo-ki`)

**Protokolliert wird gegen die Meldungsvorlage, nicht gegen die
gerenderte Meldung.** Die Vorlage ist eine statische
Entwicklerzeichenkette und darf veröffentlicht werden; die gerenderte
Meldung trägt Werte und damit möglicherweise personenbezogene Daten.

## Was ins Protokoll gehört

- Zeitpunkt, Ebene, Quelle, Meldungsvorlage, benannte Werte
- **Korrelationskennung** je Anfrage
- Fachliche Kennungen, sofern nicht personenbeziehbar
- Sicherheitsereignisse: Anmeldung, Fehlversuch, Rechteänderung,
  Signaturfehler, Ratenbegrenzung, Autorisierungsablehnung

Ebenen bewusst wählen: `Debug` für Entwicklung, `Information` für
Geschäftsereignisse, `Warning` für Auffälliges mit Weiterlauf, `Error`
für Abbruch. **Alles auf `Information` heißt: nichts ist auffindbar.**

## Korrelationskennung

- **Jede Anfrage erhält eine.** Sie geht durch alle Schichten, in jede
  Protokollzeile, in jede Fehlerantwort und zurück an den Aufrufer
  (Skill `neo-api`, Fehlerhülle).
- Sie ist nicht ratbar und trägt keine Bedeutung.
- Ohne sie ist eine Supportanfrage nicht auflösbar. Folge bei Fehlen:
  **Blocker** für jeden Endpoint, der Fehler nach außen meldet.

## Audit

- **Audit-Einträge sind aus Anwendungssicht unveränderlich.** Kein
  Ändern, kein Löschen, kein Überschreiben aus dem Fachcode.
- Ein Audit-Eintrag hält fest: wer, was, an welchem Objekt, wann, von wo,
  mit welchem Ergebnis.
- Auditpflichtig sind mindestens: Anmeldung und Abmeldung,
  Rechteänderungen, Identitätsübernahme, Löschungen, Änderungen an
  Zahlungs- und Stammdaten, Ausgabe und Entzug von Tokens, Zugriff auf
  hochsensible Daten.
- **Die Aufbewahrung des Audits folgt dem Löschkonzept** (Skill
  `neo-recht`) — ein Audit ist kein Freibrief, personenbezogene Daten
  unbegrenzt zu halten.

## Fehlermeldungen nach außen

- **Nie** ein Stacktrace, ein interner Pfad, ein Datenbankfehler, ein
  Bibliotheksname oder eine Versionsnummer.
- Die Meldung ist für Menschen, der Code für Maschinen, die
  Korrelationskennung für den Support (Skill `neo-api`).
- Eine Fehlermeldung verrät nie, ob ein Objekt existiert, wenn der
  Aufrufer es nicht sehen darf.
