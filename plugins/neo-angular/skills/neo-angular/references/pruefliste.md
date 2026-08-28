# Abnahmeliste Angular

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Quelle

- [ ] Angular-APIs aus <https://angular.dev/llms.txt> nachgeschlagen.
- [ ] Angular Material aus der Doku **der eingesetzten Fassung** — keine
      Mixin- oder Theme-Signatur aus dem Gedächtnis.

## Aufbau

- [ ] Standalone; keine `NgModule` in neuem Code.
- [ ] `inject()` durchgängig; **kein Mischbetrieb** zweier Schreibweisen.
- [ ] Eingebaute Ablaufsteuerung im Template statt der alten Direktiven.
- [ ] Fachbereiche statt technischer Ordner.
- [ ] Faules Laden je Route; der Start lädt nur, was er braucht.
- [ ] Querschnitt in Interceptoren, nicht in jedem Aufruf.

## Reaktivität

- [ ] Signals für Zustand, RxJS für Ströme — nicht umgekehrt.
- [ ] **`OnPush` überall**; jede Ausnahme begründet.
- [ ] **Jedes Abonnement wird beendet.**
- [ ] Keine Logik in einem Getter, der im Template steht.

## Formulare

- [ ] Reaktive Formulare, **typisiert**; keine templategetriebenen in
      neuem Code.
- [ ] Prüfregeln als eigene, getestete Funktionen.
- [ ] Auswahl vor Freitext, Masken, Prüfung beim Tippen (Skill
      `neo-design`, `references/eingaben.md`).
- [ ] Serverseitige Prüfung vorhanden — das Formular ist Komfort.

## Material

- [ ] **Keine `mat-`-Komponente in einer View**; Wächter-Test grün.
- [ ] Theme aus Tokens, hell und dunkel, an einer Stelle.
- [ ] **Kein `::ng-deep`, kein `!important`**, kein Überschreiben von
      Material-Klassen.
- [ ] Dichte über die vorgesehene Einstellung, nicht je Komponente.
- [ ] Material Design 3 als **System** übernommen: Farbrollen,
      Typografiestufen, Formstufen, Höhenstufen, Zustandsdeckschichten.
- [ ] Abweichungen vom Designsystem **rückgefragt**, nicht selbst
      entschieden.
- [ ] Symbole selbst ausgeliefert, nur der benötigte Satz, jedes mit
      Namen.

## Aussehen und Größen

- [ ] Umsetzung nach Claude Design mit Inventar und Messung je Element;
      **eigene Gestaltungsentscheidungen: 0**.
- [ ] Kontraste **gerechnet**, auch für Theme-Farben und Hover-Zustände.
- [ ] Acht Prüfbreiten ohne Befund; Textpassung in der längsten Sprache.
- [ ] Dialoge: Fokus hinein, gefangen, zurück; Escape schließt.
- [ ] `prefers-reduced-motion` beachtet.

## Tests

- [ ] Komponententests prüfen **Verhalten**, nicht Aufbau.
- [ ] Harness-Werkzeuge statt DOM-Gefummel, wo vorhanden.
- [ ] Stabile Marken (`data-test`) statt Auswahl über Beschriftung.
- [ ] Oberflächendurchlauf über jedes Bedienelement an **jeder** Stelle.
- [ ] Rauchtest je Route: lädt, rendert, keine Konsolenfehler.
- [ ] Bündelgröße gemessen und berichtet.
