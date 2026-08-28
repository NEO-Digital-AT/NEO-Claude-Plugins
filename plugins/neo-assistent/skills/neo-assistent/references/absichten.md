# Absichten

Lesekonvention siehe `SKILL.md`.

Eine **Absicht** ist das, was jemand erreichen will — nicht das, was er
schreibt. Sie ist der Ersatz für die Schlüsselwort-Verzweigung und der
Grund, warum ein Assistent mehrsprachig funktioniert, ohne dass jemand
Wortlisten pflegt.

## Der Katalog

Die Liste der Absichten ist **geschlossen**. Sie steht an einer Stelle,
sie ist versioniert, und die Einordnung darf nichts zurückgeben, was
nicht darin steht.

```markdown
## auftrag_suchen

Zweck        Einen bestehenden Auftrag finden, um ihn anzusehen oder
             weiterzuverarbeiten.
Nicht dafür  Einen neuen Auftrag anlegen (auftrag_anlegen). Einen
             gefundenen Auftrag ändern (auftrag_aendern).
Werkzeuge    auftrag_suchen, auftrag_lesen
Braucht      mindestens ein Merkmal: Nachname, Auftragsnummer oder Termin
Fehlt etwas  nachfragen, nicht raten
Schreibend   nein
```

Je Absicht gehören dazu:

- **Ein Zweck in einem Satz.** Wer zwei Sätze braucht, hat zwei Absichten.
- **Eine Abgrenzung.** Wogegen ist sie am leichtesten zu verwechseln?
  Diese Zeile ist die wirksamste im ganzen Katalog.
- **Die erlaubten Werkzeuge.** Nur diese sieht die zweite Stufe.
- **Die Mindestangaben.** Was fehlt, wird erfragt.
- **Schreibend ja oder nein.** Steuert Bestätigung und Prüfschwelle.

## Zuschnitt

- **Nach Ziel schneiden, nicht nach Bildschirm.** Was der Benutzer
  erreichen will, nicht wo er gerade ist.
- **Eine Absicht, eine Aufgabe.** „Auftrag verwalten" ist keine Absicht,
  sondern ein Menüpunkt.
- **Lesen und Schreiben trennen.** `auftrag_suchen` und
  `auftrag_stornieren` sind zwei Absichten, auch wenn sie im selben
  Gespräch vorkommen. Sie haben verschiedene Rechte, verschiedene
  Prüfschwellen und verschiedene Vorbedingungen.
- **Nicht zu fein.** Wer 40 Absichten hat, verlagert das Problem nur:
  die Einordnung wird dann selbst unzuverlässig. Als Orientierung: eher
  8 bis 15; darüber prüfen, ob sich Absichten mit gleichen Werkzeugen
  und gleicher Abgrenzung zusammenlegen lassen.
- **Neu geschnitten wird nur mit Messung.** Ein geänderter Zuschnitt ist
  eine Änderung mit Auswirkung auf alle Goldfälle.

## Die drei Pflichtabsichten

Jeder Katalog hat diese drei, unabhängig vom Fach:

| Absicht | Wofür | Verhalten |
| --- | --- | --- |
| `unklar` | Die Anfrage passt auf mehrere Absichten oder auf keine sicher | **Kein Werkzeug.** Genau eine Rückfrage, die die Alternativen nennt |
| `ausserhalb` | Die Anfrage liegt außerhalb der Zuständigkeit | **Kein Werkzeug.** Sagen, was der Assistent kann, und den nächsten Schritt nennen |
| `plauderei` | Gruß, Dank, Höflichkeit | **Kein Werkzeug.** Kurz antworten, nicht ausweichen |

**`unklar` ist die wichtigste Absicht des Katalogs.** Ohne sie rät die
Einordnung, und ein geratener Werkzeugaufruf ist schlimmer als eine
Rückfrage. Ein Assistent, der nie nachfragt, ist nicht sicher — er ist
nur schneller falsch.

## Mehrdeutigkeit

- **Im Zweifel `unklar`.** Die Einordnung entscheidet sich nicht für den
  ähnlichsten Wert, sondern für die Rückfrage.
- **Eine Rückfrage, nicht drei.** Sie nennt die zwei bis drei möglichen
  Absichten in der Sprache des Benutzers und fragt nach genau der einen
  fehlenden Angabe.
- **Nach der Antwort neu einordnen**, nicht die erste Vermutung
  fortführen.
- Wo die Anwendung die Auswahl kennt (eine geöffnete Zeile, ein
  markierter Datensatz), steht sie im Zustand und die Rückfrage entfällt.
  Das ist der beste Weg, Mehrdeutigkeit loszuwerden: sie gar nicht erst
  entstehen lassen (Skill `neo-design`).

## Was die Einordnung zurückgibt

Streng, über strukturierte Ausgabe erzwungen:

```json
{
  "intent": "auftrag_suchen",
  "language": "de",
  "sicher": true
}
```

- `absicht` — aus der geschlossenen Liste. Kommt etwas anderes zurück,
  gilt `unklar`, und der Fall wird protokolliert (Skill `neo-ki`).
- `sprache` — die Antwortsprache, einmal bestimmt (`sprachen.md`).
- `sicher` — falsch heißt: wie `unklar` behandeln. Ein Modell, das seine
  Unsicherheit melden darf, rät seltener.

Die Einordnung bekommt **kein Werkzeug**. Sie soll einordnen, nicht
handeln — und was sie nicht kann, kann sie nicht falsch tun.

## Absicht und Verlauf

- Die Absicht wird je **Benutzerbeitrag** neu bestimmt, nicht einmal je
  Gespräch. Menschen wechseln das Thema mitten im Satz.
- Der bisherige Verlauf geht in die Einordnung mit ein, sonst wird aus
  „Ja." nichts Sinnvolles.
- **Ein Themenwechsel setzt den Zustand nicht zurück**, aber er beendet
  eine offene Bestätigung. Eine Bestätigung gilt genau für die Handlung,
  zu der sie gegeben wurde — nie für die nächste.
