# Lieferkette, Release, riskante Umbauten

Lesekonvention siehe `SKILL.md`.

## Abhängigkeiten

| Regel | Folge bei Verstoß |
| --- | --- |
| Installation reproduzierbar aus Sperrdateien | Blocker |
| Abhängigkeits-Audit als Release-Tor | Blocker |
| **Keine bekannte Schwachstelle ab mittlerem Schweregrad** ohne dokumentierte, befristete Risikoakzeptanz | Blocker |
| Neue Abhängigkeit nur mit Freigabe (Skill `neo-grundregeln`) | Blocker |
| Updates klein, nachvollziehbar, getestet | Muss |
| SBOM erzeugen, wo die Pipeline es hergibt | Muss |

**Eine Risikoakzeptanz ist ein Dokument, kein Gedanke.** Sie nennt die
Schwachstelle, warum sie hier nicht ausnutzbar ist, wer entschieden hat,
und ein Datum, an dem erneut geprüft wird. Ohne Datum ist sie ungültig.

Vor der Aufnahme einer neuen Abhängigkeit wird geprüft: Herkunft,
Pflegezustand, letzte Veröffentlichung, offene Sicherheitsmeldungen,
Lizenz, mitgezogene Abhängigkeiten, Umfang der Rechte. Das Ergebnis geht
in die Entscheidungsakte (Skill `neo-doku`).

## CI-Tore

Verbindlich, in dieser Reihenfolge, jedes ein Blocker:

1. Abhängigkeiten installieren
2. Lint und statische Analyse
3. Tests
4. Produktions-Build
5. Sicherheits-Scan
6. Abhängigkeits-Prüfung

**Kein Tor wird übersprungen, um ein Deployment zu erzwingen.**
`continue-on-error` an einem dieser Schritte ist ohne Freigabe verboten
(Skill `neo-deployment`).

## Release-Evidenz

Je Release ein Paket, soweit die Pipeline es hergibt:

- Quell-Revision und Abbild-Prüfsumme
- Ergebnisse der Sicherheits-Scans
- SBOM
- Testergebnisse mit Zahlen
- Build- und Startprotokolle
- Migrations- und Rückbaunotizen
- Bekannte Schwachstellen mit Risikoakzeptanz und Frist

**Ohne Evidenzpaket ist ein Release nicht nachweisbar** — und ohne
Nachweis ist die CRA-Dokumentation eine Behauptung (Skill `neo-recht`).

## Schwachstellenmeldungen

Für **jede** glaubwürdige Meldung entsteht sofort ein interner Eintrag:

| Feld | Inhalt |
| --- | --- |
| Eingang | Wann, von wem, über welchen Weg |
| Betroffen | Komponente und Versionen |
| Auswirkung | Was ein Angreifer erreicht, wie leicht |
| Datenfolgen | Kundendaten, Mandantentrennung, Zahlungsdaten |
| Verantwortlicher | Ein Name, keine Gruppe |
| Zeitplan | Patch, Auslieferung, Offenlegung |
| Meldepflicht | Entscheidung mit Begründung (Skill `neo-recht`) |

**Sofort eskaliert wird bei:** aktiver Ausnutzung, kompromittierten
Zugangsdaten, betroffenen Zahlungsdaten, Abfluss über die
Mandantengrenze. Ein Verdacht wird gemeldet, nicht erst der Beweis.

`SECURITY.md` im Wurzelverzeichnis nennt den Meldeweg, die
Erreichbarkeit und die Reaktionszeit — sonst meldet niemand.

## Riskante Umbauten: Schatten- und Paritätsbetrieb

Für Umbauten an tragenden, produktiven Teilen. **Kein Umbau am
Bestand ohne dieses Muster**, wenn Daten, Geld oder Zugriffsrechte
betroffen sind.

1. **Inaktiv ausliefern.** Die neue Komponente geht mit, tut aber
   nichts. Datenmodell und Invarianten werden am echten Bestand
   validiert, ohne Wirkung.
2. **Schatten- oder Brückenbetrieb.** Die neue Komponente läuft parallel
   zum Bestand mit, ihre Ergebnisse werden **verglichen, nicht
   verwendet**. Abweichungen werden gezählt und untersucht.
3. **Umschalten erst nach nachgewiesener Parität** — Scheibe für
   Scheibe, nie alles auf einmal. „Nachgewiesen" heißt: Zahlen über
   einen benannten Zeitraum, nicht ein Stichtag ohne Abweichung.
4. **Der Rückweg steht vorher fest** und ist geprobt. Ein Umbau ohne
   Rückweg wird nicht begonnen.
5. **Querschnitts-Refactorings nie auf einem unfertigen Feature-Zweig**,
   sondern von einem stabilen, getesteten Stand aus.

Vor dem Umbau eine geprüfte Sicherung (Skill `neo-betrieb`) und eine
Entscheidungsakte (Skill `neo-doku`).

## Was der Agent nie tut

- Ein CI-Tor abschalten, überspringen oder als nicht erforderlich
  markieren.
- Eine Risikoakzeptanz ohne Freigabe eintragen.
- Eine Abhängigkeit aufnehmen, weil sie das Problem löst, ohne die
  Prüfung oben.
- Eine Schwachstellenmeldung selbst nach außen melden — das entscheidet
  und verantwortet der Projektinhaber.
- Ein Release freigeben.
