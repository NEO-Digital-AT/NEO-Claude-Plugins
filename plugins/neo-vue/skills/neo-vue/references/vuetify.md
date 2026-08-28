# Vuetify

Lesekonvention siehe `SKILL.md`.

> **Vor dem Schreiben lesen:** <https://vuetifyjs.com/llms.txt>.
> Geprüft 2026-08.

Vuetify ist die Wahl, wo eine dichte Arbeitsoberfläche mit vielen
Bedienelementen entsteht — Tabellen, Formulare, Dialoge, Datenlisten.
**Eine Bibliothek je Projekt**: Vuetify **oder** Nuxt UI.

## Hinter den Wrappern

- **Keine `v-`-Komponente in einer View.** Views rufen `Neo*`-Wrapper
  (Skill `neo-komponenten`). Der Wächter-Test hält das maschinell.
- Der Wrapper **verengt**: Er gibt nicht alle Props durch, sondern die,
  die im Projekt vorgesehen sind. Eine durchgereichte Prop, die niemand
  gewollt hat, ist die nächste Abweichung vom Designsystem.
- **Ein Bibliothekswechsel darf keine View anfassen.** Wenn er es müsste,
  ist der Wrapper zu dünn.

## Theme statt Überschreiben

- **Das Theme kommt aus der Vuetify-Konfiguration**, gespeist aus den
  Tokens des Projekts — hell und dunkel.
- **Kein `!important`**, kein Überschreiben von Bibliotheksklassen in
  einer View, kein `::v-deep` als Standardwerkzeug. Wer eine Komponente
  biegen muss, hat die falsche gewählt oder das Theme nicht gepflegt.
- **Dichte, Abstände und Radien kommen aus der Skala**, nicht aus
  Einzelwerten an der Komponente.
- Wo das Designsystem etwas verlangt, das die Bibliothek nicht kann, ist
  das eine **Rückfrage** (Skill `neo-design`,
  `references/claude-design.md`) — keine Eigenkonstruktion.

## Was trotz Bibliothek geprüft wird

Eine ausgereifte Bibliothek nimmt viel ab und **nicht alles**:

- **Kontraste werden gerechnet**, auch für Bibliotheksfarben — besonders
  in Hover- und Deaktiviert-Zuständen (`kontrast.py`, Skill `neo-design`).
- **Bedienziele**: Symbolknöpfe in Tabellenzeilen sind der häufigste
  Verstoß gegen 44 × 44 px auf schmalen Geräten.
- **Tabellen** füllen die Inhaltsbreite und folgen auf schmalen Geräten
  der Rangfolge — Spalten weglassen, Zeile zu Karte, erst dann scrollen
  (Skill `neo-design`, `references/responsiv.md`).
- **Dialoge** füllen auf schmalen Geräten die Fläche und schließen mit
  einem Knopf, nicht nur mit einem Klick daneben.
- **Fokusreihenfolge und Fokusfalle** in Dialogen und Menüs.
- **Textpassung**: Bibliothekskomponenten mit fester Höhe schneiden bei
  langen Beschriftungen ab (Skill `neo-design`,
  `references/textpassung.md`).

## Größe

- **Nur laden, was verwendet wird.** Ein vollständiger Import aller
  Komponenten und Symbole ist der häufigste Grund für ein zu großes
  Bündel.
- **Symbole gezielt einbinden**, nicht den ganzen Satz.
- Die Bündelgröße wird gemessen und berichtet.

## Formulare

- Die Regeln aus Skill `neo-design`, `references/eingaben.md` gelten
  unverändert: **was nicht eingegeben werden kann, kann nicht falsch
  sein.** Auswahl vor Freitext, Masken, Prüfung beim Tippen.
- **Serverseitige Prüfung ist die Autorität**, die Oberfläche ist Komfort
  (Skill `neo-sicherheit`).
- Fehlermeldungen nennen Ursache und nächsten Schritt, nicht nur „ungültig".
