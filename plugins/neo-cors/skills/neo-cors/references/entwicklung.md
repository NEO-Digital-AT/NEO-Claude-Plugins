# Entwicklung, Vorschau, Prüfstand und CI

Lesekonvention siehe `SKILL.md`. Kopfzeilen: `server.md`. Medien im
Browser: `browser.md`.

> **Der erste Reflex ist nicht „CORS öffnen", sondern „gleiche Herkunft
> herstellen".**

## In der Entwicklung: der Proxy des Entwicklungsservers

Oberfläche auf `http://localhost:5173`, API auf `http://localhost:8080`
— zwei Herkünfte, also CORS. **Der übliche Weg ist, diese Grenze gar
nicht entstehen zu lassen:** Der Entwicklungsserver reicht `/api` an die
API weiter, die Oberfläche ruft einen Pfad auf statt eine zweite
Adresse, und damit gibt es nichts freizugeben.

| Rahmenwerk | Wo der Proxy eingetragen wird |
| --- | --- |
| Vite | `server.proxy` in der Vite-Konfiguration |
| Nuxt | `nitro.devProxy` bzw. eine Weiterleitungsregel in `routeRules` |
| Angular CLI | `proxy.conf.json`, verknüpft in der Serve-Konfiguration |
| ASP.NET Core mit SPA | der Entwicklungs-Proxy des SPA-Hosts |
| Contao, klassisches PHP | in der Regel schon dieselbe Herkunft — sonst ein Reverse-Proxy davor |

```js
// Vite: /api bleibt ein Pfad der eigenen Herkunft
export default {
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true }
    }
  }
}
```

`changeOrigin` setzt den Hostnamen der weitergeleiteten Anfrage auf den
des Ziels — nötig, sobald das Ziel nach dem Hostnamen unterscheidet
(virtuelle Hosts, TLS-Namen).

> **Und die Kehrseite, die genau deshalb übersehen wird:** Wer in der
> Entwicklung über einen Proxy arbeitet, prüft CORS dort **nie**. Der
> erste Kontakt kommt dann in der Abnahme- oder Produktivumgebung, wo
> die Herkünfte echt sind. Deshalb steht die Messung aus Abschnitt 7 des
> Skills **je Umgebung** an, nicht einmal auf dem Entwicklungsrechner.

## Die Herkünfte je Umgebung stehen aufgeschrieben

In der Regeldatei des Projekts, eine Zeile je Umgebung. Ohne diese Liste
kann niemand die Freigabe konfigurieren und niemand sie messen:

| Umgebung | Herkunft der Oberfläche | Quellen, die sie über die Grenze lädt |
| --- | --- | --- |
| Entwicklung | `http://localhost:5173` | API über Proxy, Medien von … |
| Abnahme | `https://test.example.at` | `https://api-test.example.at`, `https://medien.example.at` |
| Produktion | `https://app.example.at` | `https://api.example.at`, `https://medien.example.at` |

Was hier nicht steht, ist nicht freigegeben. Eine Verwaltungsoberfläche,
eine zweite Domäne für Kunden, eine Vorschauumgebung — jede kommt in die
Liste, oder sie fällt beim ersten Aufruf um.

## Prüfstand und Vorschau

- **Über einen Server laden, nie über `file://`.** Eine Seite aus dem
  Dateisystem hat die Herkunft `null`; Modulskripte, Schriften, geholte
  Daten und jede Freigabe scheitern daran. Das gilt auch für eine
  einzelne Artboard-Datei, die nur kurz angesehen werden soll.
- **Die Vorschau läuft über die Programmierschnittstelle des Werkzeugs
  im selben Prozess**, nicht als Kindprozess — aus einem anderen Grund,
  mit demselben Ergebnis: ein Prüfstand, der sich beherrscht (Skill
  `neo-design`, `references/pruefstand.md`).
- **Feste Testdaten kommen aus der eigenen Herkunft.** Ein Prüfstand,
  der Bilder von einer fremden Adresse zieht, misst deren Verfügbarkeit
  mit.
- **Ein leeres Bild, eine fehlende Schrift, ein schwarzer
  Aufnahmeausschnitt oder ein stummer Ton sind im Prüfstand zuerst
  CORS-verdächtig**, bevor sie als Mangel der Anwendung gemeldet werden.
  Ein Befund, der nur im Prüfstand auftritt, ist ein Befund über den
  Prüfstand.

### Abgefangene Anfragen beweisen nichts über CORS

Ein Test, der Anfragen im Browser abfängt und selbst beantwortet
(`route`, `intercept` und Verwandte), umgeht die Herkunftsprüfung
vollständig — das ist für einen Oberflächentest richtig und für eine
CORS-Aussage wertlos. **Beides wird getrennt gehalten:** Die Oberfläche
wird gegen abgefangene Antworten geprüft, die Freigabe gegen die echte
Quelle, mit dem Werkzeug.

## In der CI

`cors-check.py` liefert einen Rückgabewert ungleich null, sobald ein
Blocker vorliegt, und taugt damit als Tor:

```
python3 scripts/cors-check.py https://api.example.at/v1/auftraege \
        --origin https://app.example.at --method POST \
        --header authorization --header content-type --credentials
```

Geprüft wird **je Umgebung** und **je Quelle** aus der Tabelle oben:
API, Medienspeicher, CDN, Schriftenquelle. Eine Quelle, die niemand
misst, ist eine Quelle, die beim nächsten Umzug ausfällt.

## Was in der Entwicklung nie gemacht wird

- Den Browser **ohne Sicherheitsprüfung** starten. Was so läuft, läuft
  nicht — und ein Prüfstand, der so startet, misst eine Anwendung, die
  es nicht gibt.
- Eine **Browsererweiterung**, die Kopfzeilen nachträglich einfügt. Sie
  steht auf keinem anderen Rechner und in keiner CI.
- Ein **öffentlicher Weiterleitungsdienst** als Zwischenstation.
- **`*` „vorläufig"** in einer Umgebung, die irgendwann produktiv wird.
- Die Herkunft im Code statt in der Konfiguration — dann braucht jede
  Umgebung einen eigenen Bau (Skill `neo-api`).
