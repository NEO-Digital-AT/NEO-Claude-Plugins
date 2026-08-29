# Zielgruppe und Sprachstufe

Lesekonvention siehe `SKILL.md`.

> **Für wen ist dieser Satz? Die Antwort steht im Projekt, nicht im
> Bauchgefühl des Agenten.**

Derselbe Satz ist an einer Stelle richtig und an der anderen ein Fehler.
„Die Synchronisierung mit dem Server ist fehlgeschlagen" hilft einem
Administrator und lässt einen Kellner mitten im Service ratlos stehen.
Ohne eine festgelegte Stufe entscheidet das jedes Mal jemand neu — und
jedes Mal anders.

## Die Stufe hängt am Bereich, nicht am Projekt

Das ist der Punkt, an dem die meisten Festlegungen scheitern. Ein
Kassensystem hat **beide** Enden in derselben Anwendung:

| Bereich | Wer bedient es | Stufe |
| --- | --- | --- |
| Kassenoberfläche, Bonieren, Bezahlen | Kassier, Kellner, Gastronom | 1 |
| Einstellungen, Registrierkasse hinterlegen, Steuersätze | Betreiber, Buchhaltung | 2 |
| Verwaltung, Protokolle, Schnittstellen, API-Doku | Administrator, Entwickler | 3 |

**Ein Projekt bekommt deshalb keine Stufe, sondern eine Tabelle.** Sie
steht in der `CLAUDE.md` (Kernregel 4).

## Die drei Stufen

### Stufe 1 — ohne Vorkenntnisse

Wer hier liest, kennt den Beruf, nicht das System. Kassier, Kellner,
Gastronom, Endkunde, Patient, Mieter.

- **Keine Technik.** Kein Server, kein Synchronisieren, kein Datensatz,
  kein Cache, kein Token, kein Endpunkt, kein Timeout, kein Status 500.
- **Keine Abkürzungen**, auch keine gängigen: nicht API, nicht PDF-ID,
  nicht ID.
- **Die Sprache des Berufs, nicht die des Systems.** Ein Beleg ist ein
  Beleg, kein Datensatz. Ein Tisch ist ein Tisch, kein Objekt.
- **Fehlermeldungen sagen, was zu tun ist**, nicht, was das System nicht
  konnte: „Der Bon wurde nicht gedruckt. Bitte prüfen Sie, ob der Drucker
  eingeschaltet ist." Eine Kennung darf als **Zusatz für den Support**
  danebenstehen, klein und benannt — nie als einzige Auskunft.
- **Keine Wahl, die niemand treffen kann.** Wer nicht weiß, was ein
  Format ist, soll es nicht auswählen müssen.

### Stufe 2 — kundig

Wer hier liest, kennt die Sache, nicht die Technik. Betreiber,
Filialleiter, Buchhaltung, Redakteur, Disponent.

- **Fachbegriffe der Sache: ja.** Registrierkasse, Steuersatz, Beleg,
  Kassenidentifikationsnummer, Sammelbeleg.
- **Technik nur, wo sie unvermeidbar ist** — und dort **einmal, an Ort
  und Stelle erklärt**, nicht in einem Handbuch, das niemand aufschlägt.
- **Keine Fehlercodes ohne Satz daneben.**
- Der Maßstab: Der Leser trifft eine fachliche Entscheidung und braucht
  dafür genau die Information, die sie trägt — nicht mehr.

### Stufe 3 — technisch

Administratoren, Entwickler, Betrieb, API-Nutzer, Backend-Oberflächen.

- **Fachausdrücke ohne Erklärung.** Statuscode, Warteschlange, Migration,
  Zertifikat.
- Trotzdem gilt Skill `neo-doku`: trocken, ohne Marketingsprache, ohne
  Füllwörter.
- **Technisch heißt nicht ungenau.** Ein Fehlercode ohne Ursache und
  ohne nächsten Schritt ist auch hier eine schlechte Meldung.

## Regeln über alle Stufen

- **Im Zweifel die niedrigere Stufe.** Wer Stufe 2 versteht, versteht
  Stufe 1 auch. Umgekehrt nicht.
- **Eine Stufe wird nicht kurz verlassen.** Ein technischer Satz in einem
  Bereich der Stufe 1 ist ein Fehler, auch wenn er stimmt und auch wenn
  er hilfreich gemeint war.
- **Die Dokumentation folgt der Stufe des Bereichs, den sie beschreibt** —
  nicht der Stufe dessen, der sie schreibt (Skill `neo-doku`).
- **Die Stufe ändert den Wortlaut, nicht die Wahrheit.** Einfacher heißt
  nicht ungenauer: Was zugesagt wird, muss stimmen (Kernregel 2).
- **Fehlt die Stufe für einen Bereich, wird gefragt** — und bis zur
  Antwort gilt die niedrigste.

## Die Wortliste

**Ein Begriff je Sache, im ganzen Projekt.** Nicht „Auftrag", „Bestellung"
und „Order" für dasselbe. Deshalb führt jedes Projekt eine kurze
Wortliste, eingecheckt neben der `CLAUDE.md`:

```markdown
| Sache | Wir sagen | Wir sagen nicht |
| --- | --- | --- |
| Der gedruckte Kassenbeleg | Bon | Beleg, Rechnung, Quittung |
| Der Vorgang am Tisch | Bestellung | Order, Auftrag |
| Das Gerät an der Theke | Kassa | POS, Terminal, Client |
```

- **Sie entsteht mit dem Projekt**, nicht wenn die Verwirrung schon da
  ist.
- **Sie gilt für Oberfläche, Dokumentation und Hilfetexte gleichermaßen.**
- **Neue Begriffe kommen nicht beim Bauen dazu**, sondern über eine
  Rückfrage (Kernregel 2).
- Englische Bezeichner im Code bleiben davon unberührt: Das System
  spricht englisch, der Mensch deutsch (Kernregel 16).

## Eintrag in der CLAUDE.md

```markdown
## Zielgruppen und Sprachstufen

| Bereich | Wer bedient es | Stufe |
| --- | --- | --- |
| Kassenoberfläche | Kassier, Kellner | 1 — ohne Vorkenntnisse |
| Einstellungen | Betreiber | 2 — kundig |
| Verwaltung, API | Administrator | 3 — technisch |

Wortliste: `docs/wortliste.md`
```

## Abnahme

- [ ] Für **jeden** Bereich mit sichtbaren Texten ist eine Stufe
      festgelegt; es gibt keinen Bereich ohne Eintrag.
- [ ] Die Texte des Bereichs halten seine Stufe ein — geprüft am
      fertigen Bildschirm, nicht an der Absicht.
- [ ] Fehlermeldungen der Stufe 1 nennen die nächste Handlung; eine
      Kennung steht höchstens als benannter Zusatz daneben.
- [ ] Die Wortliste ist eingecheckt und wurde eingehalten.
- [ ] Kein Begriff ist beim Bauen neu erfunden worden (Kernregel 2).
- [ ] Die Dokumentation eines Bereichs hat dieselbe Stufe wie der
      Bereich.
