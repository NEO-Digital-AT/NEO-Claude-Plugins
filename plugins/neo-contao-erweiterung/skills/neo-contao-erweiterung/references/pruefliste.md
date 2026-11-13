# Abnahme einer Erweiterung

Vor jeder Fertigmeldung durchgehen und die Ergebnisse mit Zahlen nennen.
Nicht Geprüftes gilt als nicht erfüllt.

## Automatisch

- [ ] `bundle-check.py <bundle> --forbid …` mit den Namen des Inhabers,
      der Firma, der Domain und betroffener Kunden: **0 Befunde** in allen
      sechs Gruppen (Neutralität, Backend-Sprachen, Frontend-Texte, Paket,
      README, Doku). Jeder Name als eigenes `--forbid` oder kommagetrennt.
      In Basic dazu `--allow public/credit.js --allow
      src/License/LicenseService.php --allow src/License/Store.php` (die
      Ausnahmen der Regel).
- [ ] Store-Link vorhanden: `LICENSE`, Abschnitt „License“/„Lizenz“ der
      README und die Lizenzstellen der Doku verlinken
      `https://store.neo-digital.at/extensions/<name>`; die Adresse
      antwortet mit 200 (`curl -sL -o /dev/null -w "%{http_code}"`).
- [ ] `php -l` über alle PHP-Dateien, Syntaxprüfung der YAML-Dateien.
- [ ] Im Prüfprojekt: `contao:migrate` läuft durch, ein zweiter Lauf meldet
      nichts mehr.
- [ ] Vor dem Veröffentlichen: `release-bundle.py` ohne Befund
      (`veroeffentlichen.md`); die ZIP lässt sich in einer frischen
      Contao-Installation installieren, Abhängigkeiten kommen von Packagist.

## Von Hand

- [ ] Standard-CSS, PDF- und Mail-Vorlage ohne Hausfarben, Hausschrift,
      Logo; alle Farben als CSS-Variablen.
- [ ] Bilder und Screenshots im Paket zeigen keine echte Website, keinen
      echten Namen.
- [ ] Keine Einstellung sieht wirksam aus, die es nicht ist: Felder, die
      von einer anderen Einstellung, einem Schlüssel oder der Lizenzstufe
      abhängen, sind gesperrt oder ausgeblendet, der Grund steht am Feld.
- [ ] Jede Einstellung, die ein Kunde braucht, ist im Backend pflegbar;
      Schlüssel verschlüsselt, mit Sonderzeichen (`=`, `+`, `/`, `&`)
      gespeichert und wieder gelesen — Wert unverändert.
- [ ] „Verbindung prüfen" zeigt für jeden Dienst den richtigen Status.
- [ ] Bei kostenpflichtigen Aufrufen: Obergrenze greift (Test mit Grenze 1),
      Headless-Browser wird abgewiesen, fehlender Schlüssel führt zu einer
      offenen Ablehnung.
- [ ] Aktualisierung über eine bestehende Installation: keine Daten weg,
      kein Feld leer, das vorher gefüllt war.
- [ ] README kurz, erst Englisch, dann Deutsch: Installation und Link auf
      die Doku in beiden Teilen.
- [ ] `docs/en/` und `docs/de/` mit den Pflichtseiten (Installation,
      Einrichtung, Rechte, Bedienung, Datenschutz, Fehlersuche), gleiche
      Dateinamen, Screenshots je Sprache; neue Funktionen, Rechte und
      bekannte Fehler eingetragen.
- [ ] Durchgang nach der Doku: Gruppe nach `permissions.md` angelegt, jeder
      Ablauf aus der Bedienungsanleitung mit diesem Benutzer gelungen.
- [ ] CHANGELOG-Eintrag für die Fassung.
- [ ] Spiegel im Projekt aktualisiert (`rsync`), Paketname im Projekt
      stimmt mit `composer.json` der Erweiterung überein.

## Tests

- [ ] PHPUnit (oder Pest) ist eingerichtet: `phpunit.xml.dist`, das Testwerkzeug in
      `require-dev`, Tests unter `tests/` (Erich 12.11.2026: „jedes Modul sollte Unit-Tests
      haben, das ist heutiger Standard“).
- [ ] Getestet ist die Logik, auf die es ankommt: Verschlüsselung, Signaturen, Filter,
      Entscheidungen (Lizenzstufen, Einwilligung, gesperrte Felder), Aufbau und Auswertung
      fremder Antworten, Migrationen. Reine Contao-Verdrahtung braucht keinen eigenen Test.
- [ ] Gegenprobe: eine getestete Stelle absichtlich verändert, der Test schlägt an.
- [ ] Die Tests laufen in der CI auf allen freigegebenen PHP-Fassungen.
- [ ] `bundle-check.py` prüft das Vorhandensein (Gruppe „tests“), nicht die Qualität.
