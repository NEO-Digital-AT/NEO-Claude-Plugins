# API-Betrieb

## Migrationen

- **Nur EF-Core-Migrationen.** Kein `EnsureCreated()`, kein Abgleich von
  Hand, kein Einspielen eines Abzugs über den Bestand.
- Automatische Anwendung beim Start darf eingeschaltet sein. Sie ist
  **nie** die Erlaubnis, Mandantendaten neu anzulegen oder zu löschen.
- Eine Migration wird vor dem Ausrollen gegen eine Kopie des Bestands
  gefahren, nicht erst in der Produktion.
- Vorwärts und rückwärts durchdenken: was passiert bei einem Rückbau,
  was mit bereits erfassten Daten.

## Webhooks

Eingang nach dem **Store-First-Modell**, in dieser Reihenfolge:

1. Signatur prüfen, wo konfiguriert — fail-closed.
2. Eintrag samt Idempotenzschlüssel speichern.
3. Auftrag für die Hintergrundverarbeitung einreihen.
4. Erfolg antworten.

Die Fachlogik läuft danach. Mehrfachzustellung wird über
`(Anbieter, externe Ereigniskennung)` entdoppelt.

- In geteilten Aufstellungen speichert die API die Zeile, eigene
  Arbeiter-Container holen sich die Aufträge aus der Datenbank.
- Die Warteschlange ist abfragbar, mit Filtern nach Objekt, Modulgruppe
  und Ereignisart — sonst ist eine Störung nicht nachvollziehbar.
- Laufzeitangaben werden **nach** der Verarbeitung in die Zeile
  zurückgeschrieben, damit man später sieht, was tatsächlich lief.

## Hintergrundarbeit

- Jeder Auftrag trägt Mandant, Objekt, Modul, Anbieter, Art, Priorität,
  Wiederholungszähler und Fehlerkontext. Ohne das ist er nicht
  diagnostizierbar.
- **Arbeiter scheitern geschlossen**, wenn der Kontext mehrdeutig ist —
  sie raten nicht.
- Lange Vorgänge laufen nie im Anfrage-Thread. Kundenauslösung,
  Webhook-Auslösung und geplanter Lauf reihen **dieselbe** Maschine ein.
- Aufrufe an fremde Anbieter beachten deren Drosselung, je Anbieter, je
  Mandant, je Objekt.
- Ist die Verarbeitung nach Ausführungsziel getrennt (etwa ein
  besonders abgeschotteter Arbeiter für Zahlungsdaten), führt ein
  Standardarbeiter dessen Aufträge **nie** aus.
- Die Kundenansicht zeigt fachliche Warnungen und Zusammenfassungen; die
  Verwaltung zeigt Aufträge, Wiederholungen, Fehlerablage und Diagnose.

## Rate Limiting

- Konfigurierbar, mit getrennten Grenzen: externe Aufrufer, angemeldete
  Oberflächensitzungen (großzügiger), Testkonten (strenger).
- **Der Begrenzer läuft nach der Authentifizierung.** Die Aufteilung
  kommt aus den Ansprüchen des Aufrufers, nie aus Query- oder
  Routenwerten — sonst umgeht man ihn durch Weglassen.
- Ein optionaler interner Umgehungskopf wird in konstanter Zeit
  verglichen und **nie** protokolliert.
- Gesundheitsendpoints sind ausgenommen.

## CORS und Cookies

Vollständig aus der Konfiguration, nichts davon im Code:

- Basisadresse der Oberfläche
- erlaubte Herkünfte
- Cookie-Name, -Domäne, SameSite, Sicherheitsrichtlinie, Lebensdauer

Jede Browser-Herkunft, die Sitzungsendpoints aufruft, steht in der Liste
der erlaubten Herkünfte — auch die Verwaltungsoberfläche, wenn sie direkt
mit der API spricht.

## Statusendpunkt für externe Überwachung

Ein eigener Endpunkt für die Betriebs-Statusseite, getrennt von der
Kundenfläche:

- **Kein Autorisierungs-Attribut, kein Swagger-Eintrag**, und nur
  gemappt, wenn das Geheimnis konfiguriert ist. Ohne den Wert existiert
  die Route nicht — ein vergessener Konfigurationseintrag kann keine
  Diagnosefläche veröffentlichen.
- Das Geheimnis reist im **Kopf**, nie in der Query: Query-Zeichenketten
  landen in Zugriffs- und WAF-Protokollen. Verglichen wird in konstanter
  Zeit. Falsches Geheimnis: `401` mit leerem Rumpf — der Aufrufer erfährt
  nicht einmal, ob eine geratene Komponente existiert.
- **Ein authentifizierter Aufrufer bekommt immer 200**, die Aussage steht
  in der Nutzlast. So bleibt eine gemeldete Störung von einem
  unerreichbaren Endpunkt unterscheidbar.
- Die API antwortet für die Komponenten mit, die von außen nicht
  erreichbar sind: Datenbank selbst prüfen, Arbeiter über das interne
  Netz abfragen.
- Wo eine Komponente netzwerkseitig getrennt ist, kommt ihr Zustand aus
  einer **Herzschlagzeile** in der Datenbank statt aus einer Abfrage.
  Kein Eintrag oder ein zu alter Schlag ist eine Störung; dazwischen eine
  Warnung.
- **Die Bewertung entsteht dort, wo die Fakten liegen** — jeder Container
  schreibt sein fertiges Urteil, nicht seine Rohwerte.
- Fremde Anbieter dürfen als Komponenten gespiegelt werden, aber
  ausdrücklich als extern gekennzeichnet: **eine Störung beim Anbieter
  ist keine Störung des eigenen Produkts** und verschiebt das
  Gesamturteil nicht. Eine unerreichbare Anbieterseite ergibt eine
  Warnung, nie eine Störung.
- Kennzahlen (Laufzeit, Speicher, Prozessor, Antwortzeiten) nur auf
  ausdrückliche Anforderung, und sie beeinflussen das Urteil **nie**:
  ein .NET-Prozess hält seinen Speicher nahe an der Grenze, das ist
  Normalbetrieb und kein Fehler.
- Meldungen sind kuratierte Sätze, nie roher Ausnahmetext.

## Wiederkehrende Protokollfunde

Wo es kein Protokollarchiv gibt, wird im erzeugenden Prozess gezählt:

- Gezählt wird gegen eine Signatur aus Quelle, **Meldungsvorlage** und
  Ausnahmetyp — **nicht** gegen die gerenderte Meldung. Die trägt Werte
  und damit möglicherweise personenbezogene Daten; die Vorlage ist eine
  statische Entwicklerzeichenkette und darf veröffentlicht werden.
- Eine Signatur über der Schwelle im gleitenden Fenster wird gemeldet und
  verschwindet von selbst, wenn sie aufhört. Nichts wird von Hand
  quittiert.
- Funde aus sicherheitsnahen Bereichen (Authentifizierung,
  Autorisierung, Signaturprüfung, Rate Limiting) werden eigens
  gekennzeichnet.
- Die Anzahl verfolgter Signaturen ist gedeckelt, damit ein Protokollsturm
  keinen etablierten Fund verdrängt und keinen Speicher frisst.
- **Überwachung darf sich nie selbst krank melden.** Fehler beim Abfragen
  fremder Statusseiten werden niedrig protokolliert, sonst sammeln sie
  sich im eigenen Fundzähler.

## Konfiguration

- Alles, was sich je Umgebung unterscheidet, ist Konfiguration: Adressen,
  Herkünfte, Zeitüberschreitungen, Intervalle, Schalter, Grenzen.
- **Fail-closed:** fehlt ein Pflichtwert, startet die Anwendung nicht oder
  die betroffene Funktion meldet einen klaren Konfigurationsfehler. Sie
  fällt nie stillschweigend auf einen unsicheren oder falschen
  Standardwert zurück.
- Ein fehlender optionaler Wert lässt die Anwendung starten und schaltet
  die betroffene Funktion ab — mit Meldung, nicht stumm.
- Zugangsdaten stehen nie in Verträgen, nie in Protokollen, nie in
  Beispielen (Skill `neo-sicherheit`).
