---
name: neo-angular
description: >
  NEO-Regeln für Angular, Angular Material und Material Design 3. Diesen
  Skill laden, sobald eine Angular-Anwendung entsteht oder geändert wird:
  Komponente, Direktive, Pipe, Dienst, Guard, Resolver, Interceptor,
  Route, Formular, Modul. Ebenso bei Fragen zu Standalone-Komponenten,
  Signals und Change Detection, zu RxJS und wann es nicht gebraucht
  wird, zu reaktiven Formularen, HTTP und Fehlerbehandlung, zu Angular
  Material, Theming und Material-Design-3-Tokens, zu Tests mit
  Karma/Jest und Playwright. Ebenso bei der Frage, wie Angular aktuell
  etwas macht — dann wird die llms.txt gelesen, nicht erinnert.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# Angular, Angular Material, Material Design 3

Lesekonvention siehe `README.md` des Regel-Repositorys.

Schichten und Benennung: Skill `neo-code`. Der Komponenten-Grundsatz
steht im Skill `neo-komponenten` und gilt hier **ohne Abzug**.

## Der Satz vorweg

> **Die API wird nachgeschlagen, nicht erinnert.**

**Angular:** <https://angular.dev/llms.txt> (geprüft 2026-08).

**Für Angular Material gibt es derzeit keine `llms.txt`** — dort wird die
offizielle Dokumentation **der eingesetzten Fassung** gelesen. Angular
bewegt sich schnell; eine erinnerte Signatur stammt oft aus einer Fassung,
die es im Projekt nicht gibt (Skill `neo-grundregeln`, Belegpflicht).

## 1. Der moderne Weg, ohne Mischbetrieb

- **Standalone**, keine `NgModule` in neuem Code.
- **`inject()` statt Konstruktor-Einspritzung** in neuem Code — eine
  Schreibweise im Projekt, nicht zwei.
- **Die eingebaute Ablaufsteuerung im Template** statt der alten
  Direktiven.
- **Kein Mischbetrieb.** Zwei Schreibweisen nebeneinander sind teurer als
  eine Umstellung; was umgestellt wird, wird ganz umgestellt und
  vorgelegt (Skill `neo-grundregeln`).

## 2. Signals als Standard, RxJS wo es hingehört

- **Signals für Zustand** einer Komponente und für abgeleitete Werte.
- **RxJS für Ströme**: HTTP, Ereignisse, alles über die Zeit. Nicht als
  Zustandsspeicher.
- **`OnPush` überall.** Eine Komponente ohne `OnPush` ist eine
  Entscheidung mit Begründung.
- **Kein manuelles Abonnieren im Template-Code**, wo die Sprache es
  abnimmt; wo doch abonniert wird, wird **beendet** — jedes Abonnement,
  ohne Ausnahme.
- **Keine Logik in einem Getter, der im Template steht.** Er läuft öfter,
  als jemand denkt.

## 3. Formulare

- **Reaktive Formulare**, typisiert. Keine templategetriebenen Formulare
  in neuem Code.
- **Prüfregeln als eigene Funktionen**, wiederverwendbar und getestet.
- **Fehlermeldungen nennen Ursache und nächsten Schritt** (Skill
  `neo-design`, `references/oberflaechentexte.md`).
- Es gilt Skill `neo-design`, `references/eingaben.md`: **was nicht
  eingegeben werden kann, kann nicht falsch sein.**
- **Serverseitige Prüfung ist die Autorität**, das Formular ist Komfort
  (Skill `neo-sicherheit`).

## 4. Angular Material und Material Design 3

- **Material-Komponenten nie direkt in einer View**, sondern hinter den
  `Neo*`-Wrappern (Skill `neo-komponenten`). Der Wächter-Test hält das
  maschinell.
- **Das Theme kommt aus Tokens**, über die vorgesehenen
  Theming-Werkzeuge — nicht aus überschriebenem CSS, nie aus
  `::ng-deep`. `::ng-deep` ist abgekündigt und in NEO-Projekten
  **verboten**; wer eine Komponente biegen muss, hat die falsche gewählt
  oder das Theme nicht gepflegt.
- **Material Design 3 ist ein System, kein Farbtopf.** Farbrollen,
  Typografie- und Formstufen werden übernommen — nicht einzelne Werte
  herausgepickt.
- **Wo das Designsystem von Material abweicht, gewinnt das
  Designsystem** — und die Abweichung ist eine **Rückfrage**, keine
  Eigenkonstruktion (Skill `neo-design`, `references/claude-design.md`).
- **Barrierefreiheit wird geprüft, nicht angenommen**: Kontraste
  gerechnet, Bedienziele gemessen, Fokusreihenfolge durchgegangen.

Theming, Dichte, typische Fallstricke: `references/material.md`.

## 5. Struktur

- **Fachbereiche statt technischer Ordner.** Nicht `components/`,
  `services/`, `pipes/` — sondern je Fachbereich alles beieinander
  (Skill `neo-code`).
- **Faules Laden je Route.** Was der Start nicht braucht, kommt später.
- **Dienste sind zustandsarm**; Zustand liegt an einer Stelle, nicht in
  drei Diensten gleichzeitig.
- **Interceptoren für Querschnitt** — Anmeldung, Korrelationskennung,
  Fehlerübersetzung —, nicht in jedem Aufruf wiederholt.

## 6. Aussehen und Größen

Es gilt der Skill `neo-design` vollständig: Umsetzung nach Claude Design
mit Inventar und Messung, Barrierefreiheit nach WCAG 2.2 AA, acht
Prüfbreiten ohne Überlauf, ohne Löcher, ohne abgeschnittenen Text.

## 7. Tests

Es gilt Skill `neo-grundregeln`, `references/tests.md`. Zusätzlich:

- **Komponententests prüfen Verhalten**, nicht Aufbau.
- **Harness-Werkzeuge statt DOM-Gefummel**, wo Angular Material sie
  anbietet — sie überleben eine Fassungsänderung.
- **Ende-zu-Ende mit dem Oberflächendurchlauf** über jedes Bedienelement
  an jeder Stelle (Skill `neo-grundregeln`, `references/durchlauf.md`).
- Stabile Marken (`data-test`) statt Auswahl über Beschriftung.

## 8. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.

Zugehörige Skills: `neo-komponenten` (Wrapper, Wächter), `neo-design`
(Gestaltung, Größen, Barrierefreiheit), `neo-code` (Schichten),
`neo-api` (Verträge), `neo-grundregeln` (Belegpflicht, Tests).
