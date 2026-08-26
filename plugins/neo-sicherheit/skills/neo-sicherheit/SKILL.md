---
name: neo-sicherheit
description: >
  NEO-Sicherheitsregeln (EU-CRA-orientiert). Diesen Skill laden bei:
  neuen oder geänderten Endpoints, Authentifizierung/Autorisierung,
  Secrets und Tokens, Logging, Datenbank- und Migrationsarbeit,
  Datei-Import/-Export, Webhooks, Zahlungs- oder anderen hochsensiblen
  Daten, Container-/Deployment-Änderungen, Abhängigkeits-Updates,
  Releases sowie riskanten Umbauten bestehender Systeme
  (Schatten-/Paritätsbetrieb).
metadata:
  herkunft: NEO Digital — destilliert aus den LeoFlex-Sicherheitsregelwerken (CRA-Baseline), Stand 2026-08
---

# NEO-Sicherheitsregeln

Baseline-Referenzen: EU Cyber Resilience Act (CRA), OWASP ASVS, OWASP
Top 10, CWE Top 25, Least Privilege, Zero Trust für privilegierte
Operationen. Ehrlichkeitsregel: „CRA-konform" nie behaupten — ohne
Produktklassifizierung, Risikoanalyse, technisches Doku-Paket,
SBOM-Automatisierung und Release-Evidenz ist es nur eine an CRA
orientierte Engineering-Baseline.

Bei Konflikt zwischen Geschwindigkeit und Produktionssicherheit gewinnt
immer die Produktionssicherheit.

## Security by Design

- Sicherheit ist nie nachträglich: jede Methode, jeden Endpoint und jede
  Datenbankoperation von Anfang an mit Sicherheitsblick bauen.
- Nutzer- und Mandantenkontext kommt ausschließlich aus authentifizierten
  Claims — nie aus Body- oder Query-Parametern. Durchsetzung liegt in
  den Services, nicht nur in Controllern oder im Frontend;
  Frontend-Guards sind Bedienkomfort, das Backend ist die einzige
  Autorität für Berechtigungen.
- Jeder Endpoint bekommt eine explizite, granulare Berechtigungs-Policy —
  kein nacktes „authentifiziert". Geschützte Operationen dokumentieren
  Auth-Modus und benötigte Rechte in der API-Beschreibung.
- Requests nie direkt an Entities binden (Mass-Assignment-Schutz über
  DTOs); ungültige Payloads nie still akzeptieren.
- Webhook-Signaturen fail-closed prüfen. Idempotenz bei allem, was
  wiederholt eintreffen kann. Rate Limiting global und nicht umgehbar.
- Re-Authentifizierung vor destruktiven oder hochprivilegierten Aktionen.
  Dauerhafte Tokens und Onboarding-/Consent-Flüsse nur für Admin-Rollen.
- **Verbotene Abkürzungen:** keine Localhost-Bypässe für geschütztes
  Verhalten, keine Fallbacks, die Sicherheit außerhalb der Entwicklung
  schwächen, funktionierende Auth-Flows nie neu erfinden, Scope-Checks
  und Mandantentrennung nie aufweichen. Verstecken ist kein Schutz:
  versteckte Endpoints oder ausgeblendete Navigation ersetzen nie
  serverseitige Autorisierung. Eine WAF ist nur zusätzliche Verteidigung.

## Secrets und Logging

- Secrets nie im Code, nie in committeter Konfiguration, nie in Images:
  nur Umgebungs-Konfiguration oder ein Verschlüsselungsdienst. Rotation
  muss ohne Codeänderung möglich sein.
- Logs enthalten nie personenbezogene Daten, Secrets, Tokens, Passwörter
  oder Zahlungsdaten. Strukturierte Sicherheits-Logs; Audit-Logs sind aus
  Anwendungssicht unveränderlich.
- Jeder Request erhält eine Korrelations-Kennung: sie geht an den
  Aufrufer zurück, steht in jeder Fehlerantwort und ist in den Logs
  suchbar.

## Hochsensible Daten

Karten-, Gesundheits- und Ausweisdaten nie persistieren — nicht in
Tabellen, Roh-Payloads, Queues, Job-Details, Logs, Fehlerantworten oder
Exporten. Klardaten existieren nur transient im Speicher für genau einen
Aufruf. Verarbeitung nur in isolierten Pfaden (kein öffentlicher Ingress,
nur Allowlist-Egress). Vor Freigabe eines solchen Pfads:
Redaktionstests über alle Ausgabekanäle.

## Frontend- und Container-Härtung

- Frontend: keine Tokens in local-/sessionStorage (HttpOnly-Cookies),
  CSP, HSTS, nosniff, restriktive Referrer- und Permissions-Policy,
  CSRF-Schutz für zustandsändernde Requests, keine ungeprüften
  HTML-Injection-Senken (v-html, innerHTML, eval, dynamische Scripts).
- Ruhende Daten verschlüsseln, wo die Plattform es vorsieht (z. B.
  SQLCipher/Keystore auf Geräten).
- Container: non-root, minimales Image, keine unnötigen Capabilities,
  no-new-privileges, möglichst read-only Dateisystem, Healthcheck,
  Builds aus Lockfiles, Basis-Images gepinnt.

## Lieferkette

- Reproduzierbare Installationen aus Lockfiles; Abhängigkeits-Audit als
  Release-Gate. Keine bekannten mittleren oder höheren Schwachstellen
  ohne explizite, dokumentierte Risikoakzeptanz.
- Updates klein, nachvollziehbar und getestet. SBOM erzeugen, wo die
  Pipeline es vorsieht.

## Riskante Umbauten: Schatten-/Paritätsbetrieb

Für Umbauten an tragenden, produktiven Teilen gilt das Paritätsmuster:

1. Neue Komponente zuerst inaktiv (dormant) ausliefern; Datenmodell und
   Invarianten validieren.
2. Schatten- oder Brückenbetrieb: die neue Komponente läuft parallel zum
   Bestand mit, ihre Ergebnisse werden verglichen, nicht verwendet.
3. Umschalten erst nach nachgewiesener Parität — Scheibe für Scheibe,
   nie alles auf einmal.
4. Querschnitts-Refactorings nie auf einem unfertigen Feature-Branch,
   sondern von einem stabilen, getesteten Stand aus.

## Meldungen und Release-Evidenz

- Für jede glaubwürdige Schwachstellenmeldung einen internen Eintrag
  anlegen. Der Eintrag enthält: Eingang, betroffene Komponente und
  Versionen, Auswirkung und Ausnutzbarkeit, Folgen für Kundendaten und
  Mandantentrennung, Verantwortlichen, Patch- und Offenlegungszeitplan,
  Entscheidung über Meldepflichten. Sofort eskalieren bei aktiver
  Ausnutzung, Credential-Kompromittierung, Zahlungsdaten oder
  Mandanten-Datenabfluss.
- Je Release ein Evidenzpaket, soweit die Pipeline es hergibt:
  Quell-Revision und Image-Digest, Scan-Ergebnisse, SBOM,
  Testergebnisse, Build- und Start-Logs, Migrations- und
  Rollback-Notizen, bekannte Schwachstellen mit Risikoakzeptanz.
- CI-Gates verbindlich: Lint, Tests, Produktions-Build, Security-Scan,
  Dependency-Check.
- **Die Meldung nach außen ist geregelt, nicht improvisiert.** Welche
  Dokumente der CRA verlangt und welche Fristen gelten — Meldepflicht
  nach Artikel 14 ab 11.09.2026, Frühwarnung 24 Stunden, ausführliche
  Meldung 72 Stunden, Abschlussbericht 14 Tage bzw. 1 Monat — steht im
  Skill `neo-recht`, `references/cra-dokumentation.md`. Dieser Skill
  regelt, wie gebaut wird; jener, was dokumentiert und gemeldet wird.
