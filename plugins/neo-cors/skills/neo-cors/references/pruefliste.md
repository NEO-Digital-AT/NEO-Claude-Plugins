# Abnahmeliste Herkunftsgrenzen

Vor jeder Fertigmeldung, in der etwas über eine Herkunftsgrenze geladen
wird. Jeden Punkt mit dem **Ergebnis** berichten, nicht mit „erledigt".
Nicht Gemessenes gilt als nicht erfüllt.

## Bestandsaufnahme

- [ ] **Jede Quelle außerhalb der eigenen Herkunft ist aufgezählt** —
      API, Medienspeicher, CDN, Schriften, Karten, Module, Texturen.
- [ ] Je Umgebung steht die **Herkunft der Oberfläche** und die Liste
      ihrer Quellen in der Regeldatei des Projekts.
- [ ] Für jede Quelle ist entschieden, welcher Weg gilt: gleiche
      Herkunft, benannte Freigabe oder Freigabe an der Quelle selbst.
- [ ] Wo keiner der drei Wege geht, **wurde gefragt**, nicht
      improvisiert.

## Im Browser

- [ ] Für jede Quelle ist beantwortet: Wird sie nur angezeigt, oder wird
      ihr Inhalt **ausgewertet**?
- [ ] Alles, was in eine Zeichenfläche, nach WebGL, nach three.js oder
      in den Audiographen geht, lädt mit `crossorigin` — **gesetzt vor
      `src`**.
- [ ] `crossorigin` steht an **einer** Stelle, in der Komponente, nicht
      in jeder View.
- [ ] Fremde Schriften: Freigabe an der Schriftdatei geprüft, oder die
      Schrift wird selbst ausgeliefert. **Ein stummer Rückfall ist kein
      Ergebnis.**
- [ ] Fremde Modulskripte und Quelltextkarten: Freigabe vorhanden.
- [ ] Kein Worker-Skript von fremder Herkunft.
- [ ] Anmeldedaten: **beide Hälften** geprüft — Freigabe mit benannter
      Herkunft und `Allow-Credentials`, und ein Cookie, das
      herkunftsübergreifend mitreisen darf.

## An der Quelle, gemessen

`cors-check.py`, je Quelle und **je Umgebung**:

- [ ] **Null Blocker** für jede Quelle, mit der Herkunft, unter der die
      Oberfläche dort läuft.
- [ ] Die Vorabfrage wird mit **2xx** beantwortet und läuft **nicht**
      durch die Anmeldeprüfung.
- [ ] Die Vorabfrage nennt **jede** Methode und **jede** Kopfzeile, die
      die echte Anfrage verwendet.
- [ ] Freigabe gespiegelt **und `Vary: Origin` gesetzt** — oder eine
      feste Herkunft ohne Spiegelung.
- [ ] Die Herkunft wird gegen eine **geprüfte Liste** aus der
      Konfiguration freigegeben, nicht ungeprüft zurückgeschrieben.
      `null` steht nicht in der Liste.
- [ ] Jede Antwortkopfzeile, die der Code liest, steht in
      `Access-Control-Expose-Headers` — Dateiname, Ort, Gesamtzahl,
      Prüfmarke, Bereichsangaben.
- [ ] **Auch Fehlerantworten tragen die Freigabe** — 401, 403, 422, 500
      und die Ratenbegrenzung.
- [ ] Nur **eine** Stelle setzt die Kopfzeilen; keine doppelte Freigabe
      aus Anwendung und Proxy.
- [ ] Keine Freigabe steht im Code; alle Herkünfte kommen aus der
      Konfiguration.

## Im Quelltext, gemessen

`cors-scan.py`:

- [ ] **Null Befunde.** Keine abgeschaltete Browsersicherheit, kein
      öffentlicher Weiterleitungsdienst, kein `*` neben Anmeldedaten,
      kein fremdes Worker-Skript, kein `file://`.
- [ ] Jeder Punkt aus der Gruppe **„nachsehen"** wurde angesehen und das
      Ergebnis berichtet — angesehen heißt nicht behoben, aber es heißt
      auch nicht übergangen.

## Prüfstand, Entwicklung und CI

- [ ] Der Prüfstand lädt über einen **Server**, nicht über `file://`.
- [ ] Der Browser läuft **mit** Sicherheitsprüfung, auch im Prüfstand.
- [ ] Keine Browsererweiterung, kein Weiterleitungsdienst, kein `*`
      „vorläufig".
- [ ] Wo die Entwicklung über einen Proxy läuft: **das ist keine
      CORS-Prüfung.** Gemessen wurde zusätzlich in der Umgebung, in der
      die Herkünfte echt sind.
- [ ] Abgefangene Anfragen im Test sind als solche benannt; die
      Freigabe wurde getrennt davon gegen die echte Quelle gemessen.
- [ ] Die Messung läuft als **Tor in der CI**, je Umgebung und je
      Quelle.

## Berichtet wird

- [ ] Je Quelle eine Zeile: Adresse, Herkunft, Blocker, Warnungen.
- [ ] Ein leeres Bild, eine fehlende Schrift, ein schwarzer
      Aufnahmeausschnitt oder ein stummer Ton wurde **zuerst auf CORS
      geprüft**, bevor er als Mangel der Anwendung gemeldet wurde.
