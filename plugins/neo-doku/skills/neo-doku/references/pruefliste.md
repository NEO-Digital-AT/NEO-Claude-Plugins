# Abnahmeliste Dokumentation

Vor jeder Fertigmeldung durchgehen, die Verhalten, Oberfläche,
Schnittstelle, Konfiguration oder Architektur ändert. Jeden Punkt mit
dem **Ergebnis** berichten. **Nicht Geprüftes gilt als nicht erfüllt.**

## Aktualität

- [ ] Die Doku beschreibt den **IST-Zustand**. Kein Zielzustand als
      Gegenwart, keine Beschreibung von Entferntem.
- [ ] Die Doku ist im **selben Commit** nachgezogen, nicht im nächsten.
- [ ] Die ganze Kette geprüft: Entwicklerdoku, Anwenderdoku,
      Inhaltsverzeichnisse, Screenshots, Änderungsprotokoll,
      Regeldatei für Agenten.
- [ ] Offene Punkte sind ehrlich benannt.
- [ ] `stand:` im Kopf jeder geänderten Datei nachgezogen.

## Struktur

- [ ] Ablage nach `docs/[frontend|backend]/<sprache>/…`.
- [ ] Jeder berührte Ordner hat eine `README.md` als
      Inhaltsverzeichnis, und die neue Datei steht darin.
- [ ] Dateinamen sind Slugs: klein, mit Bindestrich, ohne Umlaute.
- [ ] Bilder liegen in `bilder/` neben ihrer Doku.
- [ ] Bei mehreren Sprachen: gleiche Dateinamen in allen Sprachbäumen,
      Fehlendes im Verzeichnis benannt.
- [ ] Geplantes liegt unter `/plan`, nicht unter `/docs`. Beide
      widersprechen sich nicht.

## Zielgruppen

- [ ] Anwenderdoku enthält **keine** Implementierungsdetails,
      Komponentennamen, Endpoints, Tabellen oder Konfigurationsschlüssel.
- [ ] Entwicklerdoku erklärt das **WARUM**, nicht das Was.
- [ ] Bedienelemente sind **wörtlich** benannt, wie sie in der
      Oberfläche stehen.

## Bedienung

- [ ] Je Ablauf: Ziel, Voraussetzungen, nummerierte Schritte, Ergebnis,
      häufige Fehler.
- [ ] Der Abschnitt „Was diese Funktion nicht tut" ist vorhanden.
- [ ] Screenshots vorhanden, markiert, **im Repository eingecheckt**.
- [ ] Jeder Screenshot hat einen Alternativtext, der den Inhalt und die
      Markierungen beschreibt.
- [ ] Keine Aussage steht **nur** im Bild.
- [ ] Kein Screenshot zeigt echte Daten, echte Adressen oder Tokens.
- [ ] Geänderte Oberfläche heißt: betroffene Screenshots **neu erzeugt**.

## Entscheidungen

- [ ] Tragende Entscheidung hat eine Entscheidungsakte — **vor** der
      Umsetzung geschrieben.
- [ ] Die Akte nennt verworfene Möglichkeiten mit Grund.
- [ ] Der Status ist gepflegt; keine angenommene Akte widerspricht dem
      Code.
- [ ] `docs/adr/README.md` listet sie.

## Agentenlesbarkeit

- [ ] Kopfdaten vorhanden und gefüllt.
- [ ] Ein Thema je Datei, eine H1, Hierarchie ohne Sprünge.
- [ ] Keine Verweise wie „siehe oben" über Dateigrenzen.
- [ ] Keine mehrdeutigen Pronomen.
- [ ] Parameter, Felder, Fehlercodes als **Tabelle**.
- [ ] Exakte Zeichenketten in Anführung.
- [ ] Die fünf Punkte, die Agenten am häufigsten fehlen, sind
      beantwortet (Wortlaut, Vorgabe, vollständige Werteliste,
      Fehlerfall, Abgrenzung).

## Sprache

- [ ] Kein verbotenes Adjektiv, kein Meta-Satz, kein Füllwort.
- [ ] Zahlen statt Adjektive, Bedingungen statt Andeutungen.
- [ ] Aktiv, kurze Sätze, Infinitiv-Imperativ.
- [ ] **Echte Umlaute** in jedem deutschen Text.
- [ ] Keine Emojis.
- [ ] Gedankenstrich einheitlich, nie als Doppel-Bindestrich.
- [ ] Ein Begriff je Sache, projektweit.
- [ ] Jede Behauptung mit Fundstelle.

## Bei einem Doku-System

- [ ] Navigation und Sidebar mitgepflegt.
- [ ] Interne Linkform des Systems verwendet.
- [ ] **Der Build der Doku läuft durch.**

## Abschluss

- „Geprüft: <n> von <m> Punkten, <k> nicht anwendbar."
- „Geänderte Doku-Dateien: <n>, neu erzeugte Screenshots: <n>."
- „Doku auf dem Stand des Codes: ja/nein" mit Begründung.
