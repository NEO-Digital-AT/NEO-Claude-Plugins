---
name: neo-sicherheit
description: >
  NEO-Sicherheitsregeln (EU-CRA-orientiert). Diesen Skill laden bei:
  neuen oder geänderten Endpoints, Authentifizierung und Autorisierung,
  Sessions, Tokens und Scopes, Secrets, Logging und Audit,
  Mandantentrennung, Datenbank- und Migrationsarbeit,
  Datei-Import und -Export, Webhooks, Zahlungs-, Gesundheits- oder
  Ausweisdaten, Frontend- und Container-Härtung, Sicherheitskopfzeilen,
  Abhängigkeits-Updates und Lieferkette, Releases, Schwachstellenmeldungen
  sowie riskanten Umbauten bestehender Systeme (Schatten- und
  Paritätsbetrieb).
metadata:
  herkunft: NEO Digital — destilliert aus den LeoFlex-Sicherheitsregelwerken (CRA-Baseline), Stand 2026-08
---

# NEO-Sicherheitsregeln

Grundlagen: EU Cyber Resilience Act (CRA), OWASP ASVS, OWASP Top 10,
CWE Top 25, Least Privilege, Zero Trust für privilegierte Operationen.

**Bei Konflikt zwischen Geschwindigkeit und Produktionssicherheit gewinnt
immer die Produktionssicherheit.** Ohne Ausnahme, ohne Termindruck-Rabatt.

## Wie diese Regeln zu lesen sind

| Wort | Bedeutung |
| --- | --- |
| **Nie**, **immer**, **muss** | Verbindlich. Ein Verstoß ist ein **Blocker**: die Arbeit gilt als nicht fertig, ein Merge wird zurückgewiesen, ein Release findet nicht statt. |
| **Ausnahme** | Nur mit ausdrücklicher, dokumentierter Freigabe des Projektinhabers — vermerkt an der betroffenen Stelle im Code **und** in der Sicherheitsdoku, mit Grund und Datum. **Ohne diesen Vermerk gibt es keine Ausnahme**, auch wenn sie mündlich erteilt wurde. |
| **Sollte** | Begründet abweichbar. Die Abweichung wird gemeldet, nicht stillschweigend genommen. |

Diese Konvention gilt in allen Referenzdateien dieses Skills.

## Ehrlichkeitsregel

**„CRA-konform", „sicher" oder „gehärtet" wird nie behauptet.** Ohne
Produktklassifizierung, Risikoanalyse, technisches Dokumentationspaket,
SBOM-Automatisierung und Release-Evidenz ist es eine an CRA orientierte
Engineering-Baseline — mehr nicht. Wer mehr behauptet, macht eine
Zusage, die niemand einlösen kann.

Welche Dokumente der CRA verlangt und welche Meldefristen gelten:
Skill `neo-recht`, `references/cra-dokumentation.md`. **Dieser Skill
regelt, wie gebaut wird; jener, was dokumentiert und gemeldet wird.**

## Die zehn harten Verbote

Sie gelten überall, ohne Ausnahme und ohne Freigabeweg. Wer eines davon
findet, behebt es sofort und meldet es unverzüglich (Kernregel 25).

1. **Nie** ein Secret im Code, in committeter Konfiguration oder in einem
   Abbild.
2. **Nie** personenbezogene Daten, Secrets, Tokens, Kennwörter oder
   Zahlungsdaten in einem Protokoll.
3. **Nie** Mandanten- oder Nutzerkontext aus Body, Query oder Route —
   ausschließlich aus authentifizierten Ansprüchen.
4. **Nie** einen Endpoint ohne ausdrückliche, feingliedrige
   Berechtigungsregel. „Authentifiziert" allein ist keine.
5. **Nie** einen Localhost-, Entwicklungs- oder Kopfzeilen-Bypass für
   geschütztes Verhalten.
6. **Nie** eine Anfrage direkt an eine Entität binden.
7. **Nie** eine Webhook-Signatur überspringen oder fail-open prüfen.
8. **Nie** Karten-, Gesundheits- oder Ausweisdaten dauerhaft speichern.
9. **Nie** ein Token im local- oder sessionStorage.
10. **Nie** Verstecken als Schutz ausgeben: ein unverlinkter Endpoint,
    eine ausgeblendete Navigation oder eine geratene Adresse ersetzen
    keine serverseitige Autorisierung. Eine WAF ist zusätzliche
    Verteidigung, nie die erste.

## Security by Design

Sicherheit ist nie nachträglich. Jede Methode, jeder Endpoint und jede
Datenbankoperation entsteht von Anfang an mit Sicherheitsblick.

- **Das Backend ist die einzige Autorität für Berechtigungen.**
  Durchsetzung liegt in den Diensten, nicht nur in Controllern und nicht
  im Frontend. Frontend-Prüfungen sind Bedienkomfort.
- **Deny-by-default:** was seine Autorisierung nicht ausdrücklich
  deklariert, ist geschlossen (Skill `neo-api`).
- **Idempotenz** bei allem, was wiederholt eintreffen kann.
- **Re-Authentifizierung** vor destruktiven und hochprivilegierten
  Aktionen.
- **Funktionierende Auth-Flüsse werden nie neu erfunden.** Wer einen
  bestehenden Anmeldeweg umbaut, legt vorher einen Plan vor.

## Die Bereiche

| Bereich | Referenz |
| --- | --- |
| Identität, Autorisierung, Sessions, Tokens, Mandantentrennung | `references/authentifizierung.md` |
| Secrets, Rotation, Protokollierung, Audit, Korrelationskennung | `references/secrets-und-logging.md` |
| Hochsensible Daten, Verschlüsselung, Export, Redaktionstests | `references/daten.md` |
| Frontend, Sicherheitskopfzeilen, Container, Netz | `references/haertung.md` |
| Abhängigkeiten, SBOM, CI-Tore, Release-Evidenz, Schwachstellenmeldungen, riskante Umbauten | `references/lieferkette-und-release.md` |
| Abnahme vor jeder Fertigmeldung | `references/pruefliste.md` |

## Eskalation

- Eine **harte Sicherheitslücke** wird sofort behoben und unverzüglich
  gemeldet — sie ist die einzige Änderung, die ohne vorherige Freigabe
  beginnen darf (Kernregel 1).
- Sofort eskaliert wird bei: aktiver Ausnutzung, kompromittierten
  Zugangsdaten, betroffenen Zahlungsdaten, Abfluss über die
  Mandantengrenze.
- **Ein Verdacht wird gemeldet, nicht erst der Beweis.** Wer wartet, bis
  er sicher ist, meldet zu spät.
- Meldewege nach außen und deren Fristen: Skill `neo-recht`.

Zugehörige Skills: `neo-api` (Endpoints, Autorisierung, Rate Limiting),
`neo-recht` (CRA-Dokumente, Meldefristen, Datenschutz), `neo-betrieb`
(Sicherung, Notfall), `neo-code` (Codeaufbau), `neo-deployment`
(Zweigschutz, Ausrollung), `neo-grundregeln` (Prozess, Freigabe).
