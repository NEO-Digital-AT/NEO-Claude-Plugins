# Abnahme einer Erweiterung

Vor jeder Fertigmeldung durchgehen und die Ergebnisse mit Zahlen nennen.
Nicht Geprüftes gilt als nicht erfüllt.

## Automatisch

- [ ] `bundle-check.py <bundle> --forbid …` mit den Namen des Inhabers,
      der Firma, der Domain und betroffener Kunden: **0 Befunde** in allen
      sechs Gruppen (Neutralität, Backend-Sprachen, Frontend-Texte, Paket,
      README, Doku). Jeder Name als eigenes `--forbid` oder kommagetrennt.
      In Basic dazu `--allow public/credit.js --allow
      src/License/LicenseService.php` (die beiden Ausnahmen der Regel).
- [ ] `php -l` über alle PHP-Dateien, Syntaxprüfung der YAML-Dateien.
- [ ] Im Prüfprojekt: `contao:migrate` läuft durch, ein zweiter Lauf meldet
      nichts mehr.

## Von Hand

- [ ] Standard-CSS, PDF- und Mail-Vorlage ohne Hausfarben, Hausschrift,
      Logo; alle Farben als CSS-Variablen.
- [ ] Bilder und Screenshots im Paket zeigen keine echte Website, keinen
      echten Namen.
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
