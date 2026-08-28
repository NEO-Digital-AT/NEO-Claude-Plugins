---
name: neo-vue
description: >
  NEO-Regeln für Vue 3, Nuxt, Nuxt UI, Vuetify und Pinia. Diesen Skill
  laden, sobald eine Vue- oder Nuxt-Anwendung entsteht oder geändert
  wird: Komponente, Seite, Layout, Composable, Store, Plugin,
  Middleware, Serverroute, Datenabruf. Ebenso bei Fragen zu script setup,
  Props und Emits, Reaktivität, ref gegen reactive, computed, watch,
  Slots, Teleport und Suspense, zu Rendern auf dem Server, Hydration und
  Auslieferung, zu Nuxt-UI- oder Vuetify-Komponenten, Themes und Tokens,
  zu TypeScript in Vue und zu Tests mit Vitest oder Playwright. Ebenso
  bei der Frage, wie eine dieser Bibliotheken aktuell etwas macht — dann
  wird ihre llms.txt gelesen, nicht erinnert.
metadata:
  herkunft: NEO Digital — Vorgaben Erich Nigg, Stand 2026-08
---

# Vue, Nuxt, Nuxt UI, Vuetify

Lesekonvention siehe `README.md` des Regel-Repositorys.

Schichten und Benennung: Skill `neo-code`. Der Komponenten-Grundsatz —
Views rufen nur Wrapper der Produktfamilie — steht im Skill
`neo-komponenten` und gilt hier **ohne Abzug**.

## Der Satz vorweg

> **Die API wird nachgeschlagen, nicht erinnert.**

Alle vier Bibliotheken liefern ihre Dokumentation maschinenlesbar. **Vor
dem Schreiben von Code gegen eine davon wird sie gelesen:**

| Bibliothek | Quelle |
| --- | --- |
| Vue | <https://vuejs.org/llms.txt>, ausführlich `llms-full.txt` |
| Nuxt | <https://nuxt.com/llms.txt> |
| Nuxt UI | <https://ui.nuxt.com/llms.txt>, ausführlich `llms-full.txt` |
| Vuetify | <https://vuetifyjs.com/llms.txt> |

Geprüft 2026-08. **Eine erinnerte Prop-Signatur ist eine Vermutung** —
und der häufigste Grund, warum eine Komponente „fast" funktioniert.

## 1. Eine Art, eine Komponente zu schreiben

- **`<script setup lang="ts">`**, überall. Keine Options-API in neuem
  Code, keine gemischten Stile im selben Projekt.
- **Props und Emits typisiert**, über die Typdeklaration, nicht über
  Laufzeit-Objekte. Pflichtangaben und Standardwerte gehören dazu.
- **Ein Zweck je Komponente.** Wer sie nicht in einem Satz beschreiben
  kann, hat zwei.
- **Kein `any`.** Ein `any` in einer Prop ist eine Schnittstelle ohne
  Vertrag.
- **Keine Fachlogik im Template**, keine Abfrage, keine Berechnung, die
  in ein `computed` oder ein Composable gehört.

## 2. Reaktivität ohne Überraschung

- **`ref` als Standard**, `reactive` nur mit Grund. `reactive` verliert
  seine Reaktivität beim Destrukturieren — das ist die häufigste stille
  Fehlerquelle.
- **`computed` statt `watch`**, wo ein abgeleiteter Wert gemeint ist. Ein
  `watch`, der nur zuweist, ist ein `computed` im Versteck.
- **`watch` nur für Nebenwirkungen**, mit klarer Quelle, nicht auf ein
  ganzes Objekt tief.
- **`shallowRef` für große, ganz ersetzte Daten.**
- **Aufräumen ist Pflicht**: jeder Zuhörer, jedes Intervall, jede
  Beobachtung wird beendet.

## 3. Composables sind die Fachschicht des Frontends

- **Was mehr als eine Komponente braucht, ist ein Composable**, kein
  kopierter Block.
- Namen beginnen mit `use`, geben `readonly`-Werte nach außen und ändern
  nichts, was ihnen nicht gehört.
- **Keine Framework-Aufrufe im Fachcode eines Composables**, wo eine
  Abstraktion möglich ist (Skill `neo-code`).
- **Ein Store ist kein Ablageplatz.** Pinia für Zustand, den mehrere
  Bereiche teilen — nicht für alles.

## 4. Nuxt: der Rahmen bestimmt den Ort

- **Datenabruf über die dafür vorgesehenen Wege**, nicht mit einem
  nackten `fetch` in einer Komponente. Schlüssel setzen, damit nicht
  doppelt geladen wird.
- **Server bleibt Server.** Geheimnisse, Schlüssel und direkte
  Datenbankzugriffe liegen in Serverrouten, nie im geteilten Code.
  Was im Browser landet, wird angenommen als öffentlich.
- **Laufzeitkonfiguration** statt eingebauter Werte; öffentlich und
  privat getrennt.
- **Rendermodus je Route bewusst gewählt** und begründet — daran hängen
  Ladezeit und Auffindbarkeit (Skill `neo-design`, `references/messwerte.md`).
- **Kein Zugriff auf `window` ohne Prüfung**; Hydration-Warnungen sind
  Fehler, keine Meldungen.

## 5. Nuxt UI und Vuetify: gewählt, nicht gemischt

**Eine Bibliothek je Projekt.** Nuxt UI **oder** Vuetify — beide
zusammen ergeben zwei Themes, zwei Umbruchsysteme und zwei
Bedienlogiken im selben Fenster.

- **Die Bibliothek wird nicht direkt in Views verwendet**, sondern hinter
  den `Neo*`-Wrappern (Skill `neo-komponenten`). Ein Bibliothekswechsel
  darf keine View anfassen.
- **Das Theme kommt aus Tokens**, nicht aus überschriebenem CSS. Wer eine
  Bibliothekskomponente per `!important` biegt, hat den falschen Weg
  gewählt.
- **Keine lokale Variante** einer Bibliothekskomponente in einer View.
- **Zugänglichkeit wird geprüft, nicht angenommen.** Auch eine gute
  Bibliothek liefert Kontraste, die nicht reichen, und Bedienziele, die
  zu klein sind (Skill `neo-design`).

Einzelheiten und Fallstricke: `references/nuxt.md`, `references/vuetify.md`.

## 6. Aussehen und Größen

Es gilt der Skill `neo-design` vollständig: Gestaltung nach Claude
Design, Barrierefreiheit nach WCAG 2.2 AA, acht Prüfbreiten ohne
Überlauf, ohne Löcher, ohne abgeschnittenen Text.

**Scoped Styles sind kein Freibrief.** Farben, Abstände, Radien und
Schriftmaße kommen aus Tokens, auch in einer Komponente.

## 7. Tests

Es gilt Skill `neo-grundregeln`, `references/tests.md`. Zusätzlich:

- **Komponententests mit Vitest** für Verhalten, nicht für Aufbau: was
  der Anwender sieht und auslöst, nicht welche interne Methode lief.
- **Ende-zu-Ende für Abläufe**, mit dem Oberflächendurchlauf über
  **jedes** Bedienelement an **jeder** Stelle (Skill `neo-grundregeln`,
  `references/durchlauf.md`).
- **Der Wächter-Test** hält den Komponenten-Grundsatz maschinell (Skill
  `neo-komponenten`).
- Stabile Marken (`data-test`) statt Auswahl über Beschriftung oder
  Klasse.

## 8. Abnahme

Vor jeder Fertigmeldung `references/pruefliste.md` durchgehen und das
Ergebnis mit Zahlen berichten. Nicht Geprüftes gilt als nicht erfüllt.

Zugehörige Skills: `neo-komponenten` (Wrapper, Katalog, Wächter),
`neo-design` (Gestaltung, Größen, Barrierefreiheit), `neo-code`
(Schichten, Benennung), `neo-api` (Verträge), `neo-grundregeln`
(Belegpflicht, Tests, Durchlauf).
