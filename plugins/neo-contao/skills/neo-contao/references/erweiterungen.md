# Erweiterungen: auswählen, vorschlagen, selbst bauen

## Rangfolge

1. **Contao-Bordmittel** (`references/bordmittel.md`).
2. **MetaModels** oder **Contao Catalog** für eigene Datenstrukturen.
3. **Fremde Erweiterung** aus der offiziellen Liste.
4. **Eigene Erweiterung** — nur, wenn es keine marktreife gibt, und nur
   nach Freigabe.

Ein Schritt wird nur übersprungen, wenn er belegbar nicht trägt. „Ich
baue das schnell selbst" ist kein Beleg.

## Fremde Erweiterungen

Suchen: <https://extensions.contao.org/> und die Contao-Dokumentation.
Fremde Erweiterungen sind **ausdrücklich erwünscht** — sie sparen
Wartung, nicht nur Zeit.

Jede Kandidatin wird geprüft, bevor sie vorgeschlagen wird:

| Kriterium | Was geprüft wird |
| --- | --- |
| Freigabe | Ist sie für die eingesetzte Contao-Version freigegeben? |
| Pflege | Letzte Veröffentlichung, offene Fehler, Reaktionszeit |
| Verbreitung | Installationszahlen, wer sie einsetzt |
| Lizenz | Frei nutzbar? **Kostenpflichtige möglichst meiden** — wo nur eine kostenpflichtige passt: nachfragen, nicht entscheiden |
| Abhängigkeiten | Was zieht sie mit? Konflikte mit vorhandenen Paketen? |
| Sicherheit | Bekannte Schwachstellen, Umgang mit Eingaben, Rechte |
| Datenhaltung | Eigene Tabellen? Migration beim Entfernen möglich? |
| Redaktionstauglichkeit | Sind die Felder für Redakteure brauchbar, oder ist es ein Freitextfeld-Baukasten? |

**Der Vorschlag an den Projektinhaber** enthält je Kandidatin: Name und
Quelle, was sie löst, die acht Kriterien oben, Risiken, Aufwand — und
eine begründete Empfehlung. Mindestens zwei Kandidatinnen, wo es zwei
gibt. Die Entscheidung fällt der Projektinhaber (Skill
`neo-grundregeln`).

## Wenn sich eine Erweiterung nicht installieren lässt

Dann ist sie für diese Contao-Version wahrscheinlich nicht freigegeben.
Zulässige Wege:

- Eine andere Erweiterung suchen.
- Eine Eigenentwicklung vorschlagen.
- Beim Anbieter nach einer freigegebenen Fassung fragen.

**Nicht zulässig:** Versionsbeschränkungen aushebeln, den Kern anpassen,
die Erweiterung patchen, Dateien in `vendor/` ändern. Der Kern und fremde
Erweiterungen bleiben unangetastet — jede Änderung dort ist beim nächsten
Update weg und beim übernächsten ein Fehler, den niemand findet.

## MetaModels oder Catalog oder eigenes Bundle

| Fall | Weg |
| --- | --- |
| Strukturierte Inhalte, die Redakteure pflegen (Referenzen, Team, Produkte, Standorte) | **MetaModels** oder **Contao Catalog** — Felder, Listen und Filter ohne Code |
| Dieselben Inhalte, aber mit eigener Fachlogik oder Anbindung an ein Fremdsystem | eigenes Bundle |
| Ein neues Inhaltselement mit besonderem Verhalten | eigenes Bundle |
| Eine Anbindung an eine API | eigenes Bundle |
| Eine einmalige Sonderausgabe für genau eine Seite | meist ein Bordmittel plus Feld, kein Bundle |

## Eigene Erweiterungen

- **Eigenes Repository je Erweiterung.** Name:
  **`Contao-<NameDerErweiterung>-by-NEO`**, ohne Leerzeichen, z. B.
  `Contao-BrevoNewsletter-by-NEO`.
- Composer-Paket `neo/<name>-bundle`, Tabellen `tl_neo_*`.
- **Keine Projekt-Spezifika.** Alles, was ein anderes Projekt anders
  braucht, ist ein Einstellungsfeld: Routen statt fester Adressen,
  Auswahl statt eingebauter Firmenregel, Vorlage statt eingebautem Text.
  Nur so ist die Erweiterung später für den Contao-Store tauglich.
- Feldtypen nach `references/bordmittel.md`. Eine eigene Erweiterung mit
  kommagetrennten Textfeldern ist der Fehler, den sie beheben sollte.
- Rechte mitliefern: Backend-Module registrieren, Tabellen den Modulen
  zuordnen, Feldrechte bedenken.
- Migrationen mitliefern, auch für das Entfernen.
- Vollständige Dokumentation über mehrere Seiten. **Englisch ist Pflicht
  und Leitsprache**, Deutsch optional daneben (Skill `neo-doku`). Ohne
  englische Doku ist die Erweiterung nicht fertig.
- Übersetzungen der Oberfläche mindestens Englisch und Deutsch.

## Vorhandene NEO-Bundles

In `NEO-Digital-AT/website` liegen drei Bundles, die noch **nicht** in
eigenen Repositories stehen. Sie dürfen weiterverwendet werden:

| Paket | Ordner | Zweck |
| --- | --- | --- |
| `neo/super-agent-bundle` | `bundles/super-agent-bundle` | KI-Chat |
| `neo/brevo-newsletter-bundle` | `bundles/brevo-newsletter-bundle` | Anbindung an Brevo |
| `neo/llms-bundle` | `bundles/llms-bundle` | `llms.txt` und `llms-full.txt` |

Eingebunden sind sie dort als Pfad-Repositories mit Symlink. Wird eines
in ein eigenes Repository herausgelöst, gilt die Namensregel oben, und
die Einbindung wechselt von Pfad auf VCS oder Paketquelle. Der Umzug ist
eine eigene, angekündigte Änderung — nicht nebenbei.

Vor dem Bau einer neuen Erweiterung wird zuerst geprüft, ob eines dieser
Bundles die Aufgabe bereits löst.
