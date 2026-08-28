# Geräte, Peripherie, Betriebsarten

Lesekonvention siehe `SKILL.md`.

Mobile Anwendungen im Betrieb laufen selten auf einem blanken Telefon:
sie stehen in einer Halterung, hängen an einem Drucker, einem Scanner,
einer Waage, einer Geldlade. Diese Umgebung ist **Teil der Anwendung**,
nicht Zubehör.

## Vollbild und Kiosk

- **Ein Betriebsgerät zeigt die Anwendung, nicht das Betriebssystem.**
  Status- und Navigationsleiste bleiben verborgen, wo das Gerät es
  zulässt; die dafür nötige Einstellung wird **belegt** (Hersteller-Doku
  oder System-API), nicht vermutet.
- **Kein Ausstieg aus Versehen.** Wischgesten dürfen den Vorgang nicht
  verlieren; was der Benutzer angefangen hat, überlebt einen
  Fensterwechsel.
- **Feste Bühne statt Umbruch**, wo das Gerät genau eine Auflösung hat:
  einmal maßstäblich skalieren ist ehrlicher als ein Layout, das auf
  keinem Gerät stimmt.

## Fremdgeräte, die wie eine Tastatur sprechen

Scanner, Schlüsselleser und Kartenleser melden sich oft als Tastatur.

- **Ein Zuhörer an einer Stelle**, nicht je Bildschirm einer.
- **Die Eingabe endet mit Enter** — bis dahin wird gesammelt; einzelne
  Zeichen sind keine Eingabe.
- **Ein Scan ist kein Tippen**: er zählt nie als Fehlversuch, löst keine
  Sperre aus und stiehlt keinem Feld den Fokus.
- **Unbekannte Codes werden still verworfen**, nicht als Fehler gemeldet
  — ein fremder Strichcode ist Alltag.

## Ausgabegeräte

- **Drucker, Lade, Display sind Dienste hinter einer Schnittstelle**,
  mit einer Attrappe für Entwicklung und Tests. Die Fachlogik kennt kein
  Gerät.
- **Was gedruckt wird, ist vorher sichtbar**: dieselbe Darstellung am
  Bildschirm wie auf dem Zettel — dann stimmt beides oder keins.
- **Ein Gerätefehler blockiert den Vorgang nicht.** Papierende ist ein
  Zustand, kein Absturz; der Vorgang bleibt gültig und wird nachgedruckt.

## Kamera, Biometrie, Berechtigungen

- **Jede Berechtigung zum Zeitpunkt des Bedarfs**, mit einem Satz, warum.
- **Ablehnung ist ein vorgesehener Weg**: es gibt immer einen zweiten
  (tippen statt scannen, PIN statt Fingerabdruck).
- **Biometrie bleibt auf dem Gerät.** Merkmale werden nie übertragen,
  nie gespeichert, nie protokolliert (Skill `neo-sicherheit`).

## Offline und Rückkehr

- **Offline ist der Normalfall**, nicht die Ausnahme: der Betrieb läuft
  weiter, wenn die Leitung fehlt.
- **Ausgehende Aufträge in eine Warteschlange**, die den Neustart
  überlebt, idempotent verarbeitet wird und nie doppelt bucht.
- **Der Zustand ist sichtbar** — eine stille Anwendung, die seit Stunden
  nichts überträgt, ist ein Ausfall ohne Meldung.

## Prüfen

- Am **echten Gerät**, nicht nur im Emulator: Halterung, Peripherie,
  Vollbild, Systemschrift.
- Jedes Fremdgerät **abgesteckt** geprüft: Scanner weg, Drucker aus,
  Netz weg — die Anwendung sagt, was ist, und verliert nichts.
- Berechtigungen **abgelehnt** durchgespielt.
