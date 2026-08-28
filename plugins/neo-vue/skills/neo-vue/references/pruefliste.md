# Abnahmeliste Vue und Nuxt

Vor jeder Fertigmeldung durchgehen. Jeden Punkt mit dem **Ergebnis**
berichten, nicht mit „erledigt". Nicht Geprüftes gilt als nicht erfüllt.

## Quelle

- [ ] Die verwendeten Komponenten und APIs wurden aus der `llms.txt` der
      jeweiligen Bibliothek **nachgeschlagen**, nicht erinnert.
- [ ] Keine Prop, kein Ereignis und kein Slot aus dem Gedächtnis.

## Komponenten

- [ ] `<script setup lang="ts">` überall; keine Options-API in neuem Code.
- [ ] Props und Emits **typisiert**, mit Pflichtangaben und Standardwerten.
- [ ] Kein `any` in einer öffentlichen Schnittstelle.
- [ ] Ein Zweck je Komponente, in einem Satz beschreibbar.
- [ ] Keine Fachlogik, keine Abfrage und keine Berechnung im Template.
- [ ] **Die View verwendet ausschließlich `Neo*`-Wrapper** — kein
      `v-`-Element, keine Nuxt-UI-Komponente direkt; der Wächter-Test
      läuft grün (Skill `neo-komponenten`).

## Reaktivität

- [ ] `ref` als Standard; jedes `reactive` ist begründet.
- [ ] `computed` statt `watch`, wo ein abgeleiteter Wert gemeint ist.
- [ ] Kein tiefes `watch` auf ein ganzes Objekt ohne Grund.
- [ ] Jeder Zuhörer, jedes Intervall und jede Beobachtung wird beendet.

## Nuxt

- [ ] **Keine Geheimnisse im geteilten Code** — was dort steht, landet im
      Bündel, auch hinter einer Serverprüfung.
- [ ] Alles, was einen Schlüssel braucht, läuft über eine Serverroute.
- [ ] Laufzeitkonfiguration getrennt in öffentlich und privat.
- [ ] Datenabruf über die vorgesehenen Wege, mit Schlüssel; kein nacktes
      `fetch` in einer Komponente.
- [ ] Jeder Abruf hat einen **Fehlerzustand** und einen **Ladezustand**
      in der Ansicht.
- [ ] Rendermodus je Route bewusst gewählt und begründet.
- [ ] **Keine Hydration-Warnung** — sie ist ein Fehler, keine Meldung.
- [ ] Kein `window`-Zugriff ohne Prüfung.

## UI-Bibliothek

- [ ] **Genau eine** UI-Bibliothek im Projekt — Nuxt UI oder Vuetify.
- [ ] Theme aus Tokens, hell und dunkel; **kein `!important`**, kein
      Überschreiben von Bibliotheksklassen in einer View.
- [ ] Keine lokale Variante einer Bibliothekskomponente.
- [ ] Wo das Designsystem etwas verlangt, das die Bibliothek nicht kann,
      wurde **rückgefragt**, nicht selbst gebaut.
- [ ] Nur geladen, was verwendet wird; Symbole gezielt eingebunden.
- [ ] **Bündelgröße gemessen und berichtet.**

## Aussehen und Größen

- [ ] Umsetzung nach Claude Design mit Inventar und Messung je Element;
      **eigene Gestaltungsentscheidungen: 0** (Skill `neo-design`).
- [ ] Acht Prüfbreiten ohne Befund: kein Überlauf, nichts ragt hinaus,
      Tabellen füllen, keine Löcher, Bedienziele groß genug, kein Text
      abgeschnitten.
- [ ] Kontraste **gerechnet**, auch für Bibliotheksfarben und
      Hover-Zustände.
- [ ] Farben, Abstände, Radien und Schriftmaße aus Tokens — auch in
      Scoped Styles.

## Tests

- [ ] Komponententests prüfen **Verhalten**, nicht Aufbau.
- [ ] Stabile Marken (`data-test`) statt Auswahl über Beschriftung.
- [ ] Oberflächendurchlauf: jedes Bedienelement an **jeder** Stelle
      (Skill `neo-grundregeln`, `references/durchlauf.md`).
- [ ] Rauchtest je Route: lädt, rendert, keine Konsolenfehler.
- [ ] Wächter-Test grün.
