# Aufbau einer Erweiterung

Abgeleitet aus den vier ausgelieferten Erweiterungen
(`NEO-Digital-AT/NEO-Contao-Websitecheck`, `…-Brevo`, `…-SuperAgent`,
`…-LLMS`). Wer eine neue anlegt, öffnet zuerst die passendste davon und
übernimmt deren Aufbau.

## Namen

| Was | Regel | Beispiel |
| --- | --- | --- |
| Repository | `NEO-Contao-<Name>` | `NEO-Contao-Websitecheck` |
| Composer-Paket | `neo-digital/contao-<name>-bundle` | `neo-digital/contao-websitecheck-bundle` |
| Namensraum | `Neo\<Name>Bundle` | `Neo\WebsitecheckBundle` |
| Bundle-Klasse | `src/Neo<Name>Bundle.php` | `NeoWebsitecheckBundle` |
| Tabellen | `tl_neo_<name>`, Einstellungen `tl_neo_<name>_settings` | `tl_neo_websitecheck_settings` |
| Übersetzungsdomain | `neo_<name>` | `neo_websitecheck` |
| CSS-Präfix | kurz, eigen | `--nwc-*`, `.nwc__…` |
| Backend-Menü | Gruppe `neo` | „NEO › Website-Check-Einstellungen" |

Skill `neo-contao` verwendet dieselben Namen.

## Ordner

```
NEO-Contao-<Name>/
  composer.json          type contao-bundle, Lizenz proprietary, PSR-4, Manager-Plugin
  README.md              erst Englisch, dann Deutsch (doku.md)
  CHANGELOG.md
  LICENSE                eigene Lizenz, erst Deutsch, dann Englisch
  .gitattributes         export-ignore für alles, was nicht ausgeliefert wird (veroeffentlichen.md)
  config/
    services.yaml        autowire + autoconfigure; Dienste mit Argumenten explizit
    routes.yaml          nur, wo die Erweiterung eigene Endpunkte hat
  contao/
    config/config.php    Backend-Module (BE_MOD), sonst Dienste-Tags
    dca/                 tl_neo_*.php
    languages/<11>/      Backend-Texte, elf Sprachen (sprachen.md)
    templates/           Twig, neutral, überschreibbar
  translations/          <domain>.<11>.yaml, Texte für Besucher, PDF, Mail
  public/                ausgelieferte Assets (JS, CSS, Icons), neutral
  src/
    Neo<Name>Bundle.php
    ContaoManager/Plugin.php
    DependencyInjection/ Configuration.php (nur Technisches + Rückfallwerte)
    Backend/             DCA-Callbacks, Backend-Operationen (Vorschau, Verbindung prüfen)
    Controller/          ContentElement/, FrontendModule/, Api/
    Migration/           AbstractMigration, defensiv, wiederholbar
    Security/SecretCipher.php   Verschlüsselung der Schlüssel
    Settings.php         ein Objekt, das Backend vor Konfiguration liest
  docs/                  en/ und de/ (doku.md)
  dev/                   lokaler Prüfstand (Docker), wird NICHT gespiegelt und nicht ausgeliefert
```

`composer.json`, Pflichtangaben wie in den bestehenden Paketen:
`"type": "contao-bundle"`, `"license": "proprietary"`, `"description"` ohne
Herstellerbezug, `"require"` mit `^`-Bereichen (`"contao/core-bundle":
"^5.3"`), `"autoload": {"psr-4": {"Neo\\<Name>Bundle\\": "src/"}}`,
`"extra": {"contao-manager-plugin": "Neo\\<Name>Bundle\\ContaoManager\\Plugin"}`.
`contao/manager-plugin` steht unter `"require-dev"` (`^2.0`) mit
`"conflict": {"contao/manager-plugin": "<2.0 || >=3.0"}`, nicht unter
`"require"` (Contao-Doku, Manager Plugin). Keine `version`; `homepage` und
`support` zeigen auf das öffentliche Repository (`veroeffentlichen.md`).
Ausgelieferte Dateien liegen in `public/` im Wurzelordner, nicht in
`Resources/public/`.
`authors` darf den Hersteller nennen, ohne Personennamen.

## Einstellungen

Das Muster aus der Website-Check-Erweiterung:

- **Eine Einstellungstabelle mit genau einem Datensatz**
  (`tl_neo_<name>_settings`): `notCreatable`, `notDeletable`, die Liste
  wird übersprungen, das Modul öffnet die Maske direkt.
- **`Settings.php`** liest jeden Wert zuerst aus dem Datensatz, dann aus
  `config.yaml`. Leeres Feld = Rückfall, nicht „aus".
- **Schlüssel** (`*_api_key`): `inputType text` mit `hideInput`,
  `decodeEntities`, `doNotCopy`; `load_callback` zeigt eine Maske,
  `save_callback` verschlüsselt mit `SecretCipher` (libsodium, Schlüssel aus
  dem App-Secret) und behält den alten Wert, wenn das Feld leer oder
  unverändert ist. Beim Lesen `html_entity_decode`, damit früher kodiert
  gespeicherte Schlüssel weiter funktionieren.
- **Übernahme-Migration**: füllt leere Backend-Felder einmalig aus der
  Konfiguration. Nie etwas überschreiben, was im Backend steht.
- **Auswahl vom Fremdsystem**: `onload_callback` macht aus dem Textfeld
  eine Auswahl, sobald ein Schlüssel bekannt ist; der gespeicherte Wert
  bleibt immer in der Liste; Ergebnis eine Stunde zwischengespeichert.
- **Statuszeile** über den Schlüsselfeldern: woher jeder Wert gerade kommt
  (Backend, Konfiguration, fehlt).
- **Abhängige Felder**: `submitOnChange` am auslösenden Feld, ein
  `onload_callback` sperrt die abhängigen (`eval.disabled`, Wert bleibt
  gespeichert) oder blendet sie aus und ersetzt ihre Hilfe durch den Grund
  (als Warnung, mit Link zur Stelle, an der man es ändert). Fehlender
  Schlüssel, andere Einstellung, Lizenzstufe: gleiche Behandlung. Die
  Ausgabe im Frontend folgt derselben Bedingung.
- **„Verbindung prüfen"** als Backend-Operation (`key=test_api`): ruft
  jeden Dienst vom Server aus auf, zeigt Status, Dauer und Antwort, dazu
  Länge, Anfang und Ende des Schlüssels — nie den Schlüssel selbst — und
  die Fehler der letzten Vorgänge.
- **Kostenschutz**, wenn Aufrufe Geld kosten: Obergrenze je Stunde und Tag
  für alle Besucher zusammen, Grenze je Besucher, unsichtbares ALTCHA plus
  Honeypot, offensichtliche Skripte (leerer User-Agent, Headless-Browser,
  curl, python) abweisen. Fehlt ein nötiger Schlüssel: offen ablehnen.
- **Abrufe fremder Adressen**, die ein Besucher eingibt, gehen über einen
  Client, der private Netze sperrt (`NoPrivateNetworkHttpClient`).

## Rechte

Backend-Module in `contao/config/config.php` registrieren, jede Tabelle
dem Modul zuordnen. In der README steht, welche Module und Tabellen eine
Redakteursgruppe braucht.

## Spiegel im Projekt

Ein Projekt bindet die Erweiterung als Pfad-Repository ein:

```
rsync -a --delete --exclude .git --exclude dev --exclude vendor \
  --exclude composer.lock <repo>/ bundles/<ordner>/
```

Geändert wird **nur im eigenen Repository**, dann gespiegelt. Der
Paketname im `require` des Projekts ist der aus `composer.json` der
Erweiterung — nach einer Umbenennung beide anpassen, sonst bricht der
Build mit `composer update`.

## Prüfstand

`dev/` enthält einen Docker-Prüfstand (Contao, Datenbank, Mailpit), der
die Erweiterung mit Beispieldaten startet. Der Prüfstand nutzt dieselben
neutralen Beispielwerte wie die Doku.
