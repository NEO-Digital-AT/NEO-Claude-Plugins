# Abnahmeliste Komponenten

Vor jeder Fertigmeldung durchgehen, die eine View oder eine Komponente
berührt. Jeden Punkt mit dem **Ergebnis** berichten, nicht mit
„erledigt". **Nicht Geprüftes gilt als nicht erfüllt.**

## Die Kernregel

- [ ] Keine View enthält ein gestaltendes HTML-Element.
- [ ] Keine View enthält ein `class`- oder `style`-Attribut.
- [ ] Keine View enthält ein Farbliteral.
- [ ] Keine View enthält eine Maßzahl mit Einheit außerhalb einer
      Token-Referenz.
- [ ] Keine View importiert aus dem Designframework.
- [ ] **Der Wächter-Test läuft und ist grün.** Existiert keiner, ist das
      selbst ein Befund.
- [ ] Die Ausnahmeliste des Wächters ist nicht gewachsen. Jeder neue
      Eintrag hat Grund und Freigabe.

## Die Komponente

- [ ] Name nach `{Präfix}{Bereich}{Element}{Ausprägung}`, im passenden
      Ordner.
- [ ] Baut auf der Original-Komponente des Frameworks auf; eigenes
      Styling nur, wo begründet.
- [ ] Farbe, Größe, Radius, Abstand ausschließlich aus Tokens.
- [ ] Hell- und Dunkelfassung gebaut und **angesehen**.
- [ ] Standardgröße gesetzt, Skala über `size` erreichbar.
- [ ] **Alle Zustände gebaut:** Ruhe, Hover, Fokus, Gedrückt, Aktiv,
      Deaktiviert, Fehler, Ladend.
- [ ] Hover verschiebt um eine Stufe; der Text nähert sich nicht der
      Fläche an.
- [ ] Deaktiviert ist erkennbar und sagt warum.
- [ ] Kontrast für **jeden** Zustand gerechnet, Zahlen berichtet
      (Skill `neo-design`).
- [ ] Zugänglicher Name, Rolle, Tastaturbedienung, Zielgröße ≥ 24 px.
- [ ] Sichtbare Texte aus der Sprachdatei, **in der Komponente**.
- [ ] Kein Framework-Typ in der Signatur.
- [ ] Kein Durchreichen unbekannter Attribute.
- [ ] Höchstens sechs Eigenschaften, sonst begründet.
- [ ] Ohne die Anwendung darstellbar.

## Grenzen eingehalten

- [ ] Liste oder Tabelle ab 10 Zeilen mit Suche.
- [ ] Tabelle ab 25 Zeilen mit Seitennavigation oder Nachladen.
- [ ] Auswahlfeld ab 10 Einträgen mit Suche im Feld.
- [ ] Leer-Zustand vorhanden, getrennt nach „nichts angelegt" und
      „Filter ohne Treffer".
- [ ] Vorgang über 10 Sekunden mit Fortschritt und Auskunft.

## Interaktion

- [ ] Destruktives bestätigt die Folge und nennt das Objekt.
- [ ] Fehlerfarbe nur für Zerstörendes verwendet.
- [ ] Jede Aktion endet in einer sichtbaren Rückmeldung.
- [ ] Zustand trägt Farbe **und** Symbol **und** Wort.

## Bestand und Wechsel

- [ ] Keine bestehende Bibliothek ohne Freigabe umgeschrieben.
- [ ] Kein Duplikat einer bestehenden Komponente angelegt.
- [ ] Ein vorhandenes Muster wurde übernommen, keine lokale Variante
      erfunden.

## Tests und Doku

- [ ] **Jedes Bedienelement hat einen Oberflächen-Funktionstest**, der
      die Bedienung auslöst und das beobachtbare Ergebnis prüft.
- [ ] Der deaktivierte Zustand löst nachweislich nichts aus.
- [ ] Die Komponente steht im Katalog bzw. Klickprototyp des Projekts.
- [ ] Der Komponenten-Grundsatz steht als Entscheidungsakte und als
      Abschnitt in der Regeldatei des Projekts, mit Verweis auf den
      Wächter (Skill `neo-doku`).

## Abschluss

- „Geprüft: <n> von <m> Punkten, <k> nicht anwendbar."
- „Ausnahmeliste des Wächters: <vorher> → <nachher>."
- „Abnahmefähig: ja/nein" mit Begründung.
