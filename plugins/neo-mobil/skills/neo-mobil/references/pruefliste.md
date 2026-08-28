# Abnahmeliste mobile Anwendung

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Quelle

- [ ] APIs aus <https://docs.flutter.dev/llms.txt> und aus der Doku der
      **eingesetzten** Paketfassungen nachgeschlagen, nicht erinnert.

## Aufbau

- [ ] Ein Widget, ein Zweck; keine `build`-Methode über 60 Zeilen.
- [ ] Widgets statt Hilfsmethoden, die Widgets zurückgeben.
- [ ] `const`, wo möglich.
- [ ] Keine Fachlogik in `build`.
- [ ] **Eine** Zustandsverwaltung im Projekt, als Entscheidungsakte
      festgehalten.
- [ ] **Jede Ressource freigegeben**: Controller, Zuhörer, Ströme,
      Zeitgeber.

## Aussehen

- [ ] Umsetzung nach Claude Design mit Inventar und Messung je Element;
      **eigene Gestaltungsentscheidungen: 0**.
- [ ] Material 3 als **System** übernommen; Theme aus Tokens, hell und
      dunkel, an einer Stelle.
- [ ] Keine Farbe, kein Maß, kein Radius im Widget-Code.
- [ ] Material-Widgets hinter den Wrappern der Produktfamilie.
- [ ] Abweichungen vom Designsystem **rückgefragt**, nicht entschieden.

## Größen

- [ ] **Kein Überlauf** — kein `RenderFlex overflowed`, in keinem Zustand.
- [ ] Nichts ragt hinaus, auch nicht bei größter Systemschrift.
- [ ] Keine Löcher beim Umbrechen auf Tablet und Querformat.
- [ ] Bedienziele mindestens 44 × 44 px, mit Abstand dazwischen.
- [ ] Kein abgeschnittener Text, kein zu schmaler Bereich.
- [ ] Sichere Bereiche beachtet: Kerbe, Statusleiste, Gestenleiste,
      Tastatur.
- [ ] Geprüft auf **Telefon hoch und quer, Tablet hoch und quer**, bei
      kleinster und größter Systemschrift, hell und dunkel.

## Barrierefreiheit

- [ ] Jedes Bedienelement hat einen Namen für Vorlesegeräte.
- [ ] Kontraste **gerechnet** und als Zahl berichtet.
- [ ] Bei 200 % Systemschrift bricht nichts.
- [ ] Bewegung reduzierbar, wo das System es verlangt.
- [ ] Mit dem **Vorlesegerät des Systems** durchgegangen, nicht nur mit
      dem Prüfwerkzeug.

## Betrieb

- [ ] **Keine Geheimnisse im Paket** — auch nicht obfuskiert.
- [ ] Berechtigungen sparsam, jede begründet und zum Zeitpunkt des
      Bedarfs erklärt; Ablehnung ist ein vorgesehener Zustand.
- [ ] Offline-Verhalten festgelegt und geprüft.
- [ ] Kein Datenverlust beim Beenden durch das System.
- [ ] Jedes Paket vorgelegt: Zweck, Alternative, Pflegezustand, Lizenz,
      Plattformabdeckung.
- [ ] Signierung und Veröffentlichung dokumentiert und reproduzierbar;
      Schlüssel nicht im Repository.

## Lokale Daten

- [ ] Gerätestellungen, Bewegungsdaten und Stammdaten getrennt; ein
      abgeschlossener Vorgang trägt **Kopien**, keine Verweise.
- [ ] Jede Schemaänderung mit erhöhter Version **und** Migrationsschritt.
- [ ] **Migrationstest** je Schritt: alte Fassung roh angelegt, geöffnet,
      Altdaten unversehrt, neue Spalte benutzbar.
- [ ] Neustart-Simulation geprüft: laufende Nummern laufen fort.
- [ ] Aufzeichnungen, die lückenlos sein müssen: **nur anhängen**, kein
      Änderungs- oder Löschweg vorhanden; Korrektur als Gegenbuchung.
- [ ] Geschrieben, **bevor** die Oberfläche aufräumt; Leser nach jedem
      Anhängen aufgefrischt.
- [ ] Ein Durchlauf **ohne Netz** gemacht.

## Geräte und Peripherie

- [ ] Vollbild/Kiosk am echten Gerät geprüft; die dafür nötige
      Einstellung ist **belegt**, nicht vermutet.
- [ ] Fremdgeräte, die wie eine Tastatur sprechen: EIN Zuhörer, Eingabe
      endet mit Enter, Scan zählt nie als Fehlversuch, unbekannte Codes
      still verworfen.
- [ ] Ausgabegeräte hinter einer Schnittstelle mit Attrappe; ein
      Gerätefehler blockiert keinen Vorgang.
- [ ] Jedes Fremdgerät **abgesteckt** geprüft (Scanner, Drucker, Netz).
- [ ] Jede Berechtigung **abgelehnt** durchgespielt; zweiter Weg
      vorhanden.
- [ ] Biometrische Merkmale bleiben auf dem Gerät.

## Tests

- [ ] Widget-Test je Bedienelement, der das **beobachtbare Ergebnis**
      prüft.
- [ ] Integrationstests für die Abläufe, mit Oberflächendurchlauf über
      jedes Bedienelement an **jeder** Stelle.
- [ ] **Auf beiden Plattformen** geprüft, nicht nur auf der des
      Entwicklers.
- [ ] Goldene Aufnahmen nur dort, wo der Inhalt stabil ist.
