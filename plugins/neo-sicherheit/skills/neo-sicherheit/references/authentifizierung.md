# Identität, Autorisierung, Mandantentrennung

Lesekonvention siehe `SKILL.md`: **Nie/immer/muss** ist ein Blocker,
**Ausnahme** braucht eine dokumentierte Freigabe mit Grund und Datum.

## Woher der Kontext kommt

**Nutzer- und Mandantenkontext kommt ausschließlich aus
authentifizierten Ansprüchen.** Nie aus Body, Query, Route, Kopfzeile
oder Cookie-Inhalt, den der Aufrufer setzen kann.

| Falsch | Warum es bricht |
| --- | --- |
| `GET /rechnungen?mandant=42` | Der Aufrufer wählt seinen Mandanten selbst |
| `POST /nutzer` mit `rolle` im Body | Rechteausweitung in einem Feld |
| Mandant aus einem Unterdomänen-Namen ohne Abgleich | Wer die Adresse tippt, wechselt den Mandanten |
| Mandant aus einem Kopfzeilenwert eines Vermittlers | Eine falsch konfigurierte Zwischenschicht hebt die Trennung auf |

Folge bei Verstoß: **Blocker.** Der Endpoint geht nicht live, auch nicht
„nur für interne Nutzung".

## Autorisierung

- **Jeder Endpoint deklariert seine Berechtigung ausdrücklich und
  feingliedrig.** „Authentifiziert" ist keine Berechtigung.
- **Deny-by-default:** eine globale Rückfallregel verlangt auf jedem
  Endpoint einen authentifizierten Aufrufer. Absichtlich anonyme
  Endpoints tragen die Freigabe ausdrücklich (Skill `neo-api`).
- **Durchsetzung im Dienst, nicht im Controller.** Ein Controller, der
  prüft, und ein Dienst, der es nicht tut, ist eine Lücke, sobald ein
  zweiter Aufrufer dazukommt — ein Hintergrundauftrag, ein Kommando, ein
  Test.
- **Das Frontend ist keine Autorität.** Ausgeblendete Knöpfe und
  gefilterte Menüs sind Bedienkomfort. Jede Prüfung existiert
  serverseitig noch einmal.
- **Objektbezogene Prüfung, nicht nur typbezogen.** „Darf Rechnungen
  lesen" reicht nicht — es muss geprüft werden, ob **diese** Rechnung dem
  Mandanten des Aufrufers gehört. Fehlende Objektprüfung ist der
  häufigste Fund in Sicherheitsprüfungen.
- Ein Objekt, das dem Aufrufer nicht gehört, antwortet wie ein nicht
  vorhandenes: **`404`, nicht `403`** — sonst verrät die Antwort seine
  Existenz.

## Mandantentrennung

- Jede mandantenbezogene Tabelle trägt die Mandantenkennung, jede Abfrage
  filtert darauf (Skill `neo-code`, `references/datenmodell.md`).
- Wo das ORM es hergibt, erzwingt ein globaler Filter die Trennung als
  **zweite** Linie. Er ersetzt die erste nicht.
- **Für jede neue mandantenbezogene Tabelle entsteht ein Test**, der
  belegt, dass Mandant A die Daten von Mandant B nicht sieht. Ohne
  diesen Test gilt die Tabelle als ungeprüft.
- Eindeutigkeiten gelten je Mandant, nicht global.
- Ein Abfluss über die Mandantengrenze ist ein **sofortiger
  Eskalationsfall**, kein Fehlerbericht.

## Sessions und Tokens

| Regel | Folge bei Verstoß |
| --- | --- |
| **Nie** ein Token im local- oder sessionStorage | Blocker. Ein XSS liest es aus. HttpOnly-Cookie, `Secure`, `SameSite` |
| Sitzungscookies mit `HttpOnly`, `Secure`, passendem `SameSite` | Blocker |
| Sitzung bei Rechte- oder Kennwortänderung **ungültig** | Blocker. Ein entzogenes Recht muss sofort wirken |
| Abmelden macht die Sitzung serverseitig ungültig | Blocker. Ein nur clientseitig gelöschtes Cookie ist keine Abmeldung |
| Tokens tragen feingliedrige Lese- und Schreibrechte | Ein pauschales Recht ist höchstens Altbestand mit Ablaufdatum |
| Dauerhafte Tokens nur für ausdrücklich dafür vorgesehene Rollen | Blocker |
| Token-Lebensdauer begrenzt, Erneuerung vorgesehen | Sollte |

- **Zugangsdaten werden nie im Klartext gespeichert** — nur als
  Hash mit einem für Kennwörter vorgesehenen Verfahren und
  projektweit festgelegten Parametern.
- Beim Anmelden wird nicht verraten, ob eine Kennung existiert. Dieselbe
  Meldung, dieselbe Antwortzeit.
- **Anmeldeversuche werden begrenzt** — je Konto und je Herkunft, nicht
  nur global.

## Re-Authentifizierung

Vor diesen Aktionen wird erneut authentifiziert, auch in einer laufenden
Sitzung:

- Löschen eines Kontos, eines Mandanten oder eines Datenbestands
- Ändern von Kennwort, zweitem Faktor, Wiederherstellungswegen
- Ändern von Zahlungs- oder Auszahlungsdaten
- Anlegen oder Ausgeben eines dauerhaften Tokens
- Übernahme einer fremden Identität durch die Verwaltung

Folge bei Verstoß: **Blocker.**

## Identitätsübernahme durch die Verwaltung

Wo eine Verwaltung im Namen eines Nutzers handeln kann:

- **Nie stillschweigend.** Der Vorgang wird protokolliert, mit
  Handelndem, Ziel, Zeitraum und Grund.
- Die Übernahme ist zeitlich begrenzt und endet automatisch.
- Der betroffene Nutzer wird informiert, sofern nicht ein benannter Grund
  dagegensteht.
- **Nie** darf über eine Übernahme etwas möglich sein, das die
  Verwaltung nicht ohnehin darf.

## Verbotene Abkürzungen

Keine davon hat einen Freigabeweg:

- Localhost-, Entwicklungs- oder Kopfzeilen-Bypass für geschütztes
  Verhalten.
- Ein Rückfall, der Sicherheit außerhalb der Entwicklung schwächt.
- Ein Scope-Check, der bei fehlendem Scope durchlässt.
- Eine Signaturprüfung, die bei fehlender Signatur durchlässt.
- Ein `if (umgebung === 'test')` im ausgelieferten Code.
- Verstecken statt Autorisieren.
