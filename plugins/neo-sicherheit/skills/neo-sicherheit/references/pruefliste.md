# Abnahmeliste Sicherheit

Vor jeder Fertigmeldung durchgehen, die eine der folgenden Flächen
berührt: Endpoint, Authentifizierung, Daten, Datei, Webhook, Container,
Abhängigkeit, Release.

Jeden Punkt mit dem **Ergebnis** berichten, nicht mit „erledigt".
**Nicht Geprüftes gilt als nicht erfüllt.** Was bewusst nicht erfüllt
ist, wird benannt, mit Grund, Freigabe und Datum.

## Identität und Autorisierung

- [ ] Mandanten- und Nutzerkontext kommt ausschließlich aus
      authentifizierten Ansprüchen — keine Stelle liest ihn aus Body,
      Query, Route oder Kopfzeile.
- [ ] Jeder neue oder geänderte Endpoint hat eine ausdrückliche,
      feingliedrige Berechtigungsregel.
- [ ] Die Prüfung liegt im Dienst, nicht nur im Controller.
- [ ] Objektbezogene Prüfung vorhanden: gehört **dieses** Objekt dem
      Aufrufer?
- [ ] Fremdes Objekt antwortet mit `404`, nicht mit `403`.
- [ ] Für jede neue mandantenbezogene Tabelle existiert ein Test, der
      die Trennung belegt.
- [ ] Re-Authentifizierung vor Destruktivem und Hochprivilegiertem.

## Secrets und Protokolle

- [ ] Kein Secret im Diff, im Verlauf, in der Konfiguration, im Abbild.
- [ ] Rotation ohne Codeänderung möglich.
- [ ] `.env.example` vollständig, ohne echte Werte.
- [ ] Fehlender Pflichtwert führt zu einem klaren Fehler, nicht zu einem
      stillen Standardwert.
- [ ] Protokolle enthalten keine personenbezogenen Daten, Secrets,
      Tokens oder Zahlungsdaten — **im Protokoll nachgesehen**, nicht
      im Code vermutet.
- [ ] Korrelationskennung geht durch alle Schichten und in jede
      Fehlerantwort.
- [ ] Auditpflichtige Vorgänge werden erfasst und sind unveränderlich.

## Daten

- [ ] Keine hochsensiblen Daten persistiert — über alle Ausgabekanäle
      geprüft (Liste in `daten.md`), mit echten Testwerten.
- [ ] Nur sichere Kennzeichen gespeichert.
- [ ] Übertragung verschlüsselt, ruhende Daten wo vorgesehen.
- [ ] Schlüssel liegt nicht neben den Daten.
- [ ] Hochgeladene Dateien an den ersten Bytes geprüft, begrenzt,
      gereinigt; Entferntes wird benannt.
- [ ] Exporte tragen dieselben Berechtigungen wie die Ansicht.

## Härtung

- [ ] Keine Tokens in local- oder sessionStorage.
- [ ] Keine ungeprüfte HTML-Senke; CSRF-Schutz vorhanden.
- [ ] Sicherheitskopfzeilen an der **ausgelieferten** Antwort geprüft,
      nicht in der Konfiguration gelesen.
- [ ] CSP scharf geschaltet, nicht im Berichtsmodus vergessen.
- [ ] Container läuft nicht als `root`, Abbild festgenagelt, keine
      Secrets in Build-Schichten.
- [ ] Nur veröffentlicht, was von außen erreichbar sein muss.
- [ ] Zeitüberschreitungen überall gesetzt.
- [ ] Ratenbegrenzung nach dem authentifizierten Aufrufer.

## Lieferkette und Release

- [ ] Installation reproduzierbar, Audit gelaufen, Ergebnis berichtet.
- [ ] Keine Schwachstelle ab mittlerem Schweregrad ohne befristete,
      dokumentierte Risikoakzeptanz.
- [ ] Alle CI-Tore grün, keines übersprungen.
- [ ] Evidenzpaket vollständig, soweit die Pipeline es hergibt.
- [ ] `SECURITY.md` vorhanden und aktuell.

## Bei riskanten Umbauten

- [ ] Geprüfte Sicherung vorhanden.
- [ ] Entscheidungsakte geschrieben und freigegeben.
- [ ] Inaktive Auslieferung, dann Schattenbetrieb, dann Umschalten in
      Scheiben.
- [ ] Parität mit Zahlen über einen benannten Zeitraum belegt.
- [ ] Rückweg festgelegt und geprobt.

## Abschluss

- „Geprüft: <n> von <m> Punkten, <k> nicht anwendbar."
- „Sicherheitsfreigabe vertretbar: ja/nein" mit Begründung. Ein offener
  Blocker heißt nein.
