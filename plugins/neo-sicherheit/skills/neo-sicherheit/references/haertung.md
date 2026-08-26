# Härtung: Frontend, Kopfzeilen, Container, Netz

Lesekonvention siehe `SKILL.md`.

## Frontend

| Regel | Folge bei Verstoß |
| --- | --- |
| **Nie** Tokens in local- oder sessionStorage — HttpOnly-Cookies | Blocker |
| **Nie** eine ungeprüfte HTML-Senke: `v-html`, `innerHTML`, `eval`, dynamisch erzeugte Skripte, `dangerouslySetInnerHTML` | Blocker. Ausnahme nur mit Reinigung über eine Positivliste, dokumentiert |
| CSRF-Schutz für jede zustandsändernde Anfrage | Blocker |
| Fremder Text wird nie als Auszeichnung eingesetzt | Blocker |
| Keine Zugangsdaten oder Schlüssel im ausgelieferten Bündel | Blocker |
| Eine Adresse aus fremder Hand wird nie ungeprüft verlinkt oder aufgerufen | Blocker |
| Externe Verweise mit `rel="noopener noreferrer"` | Muss |
| Keine Klartext-E-Mail-Adresse im ausgelieferten HTML | Muss (Skill `neo-recht`) |

## Sicherheitskopfzeilen

Jede ausgelieferte Antwort trägt sie. Fehlt eine, ist das ein Befund,
kein Feinschliff.

| Kopfzeile | Zweck |
| --- | --- |
| `Content-Security-Policy` | Die wichtigste. Ohne `unsafe-inline` für Skripte; wo Inline nötig ist, über Einmalkennungen |
| `Strict-Transport-Security` | Erzwingt HTTPS für die Domäne |
| `X-Content-Type-Options: nosniff` | Verhindert Ratespiele des Browsers über den Inhaltstyp |
| `Referrer-Policy` | Restriktiv, damit Adressen nicht nach außen wandern |
| `Permissions-Policy` | Schaltet ab, was die Seite nicht braucht: Kamera, Mikrofon, Standort |
| `X-Frame-Options` bzw. `frame-ancestors` | Gegen Einbettung in fremde Seiten |
| `Cache-Control` bei geschützten Antworten | `no-store`, damit nichts in einem Zwischenspeicher landet |

- Die Richtlinie wird **gegen die tatsächliche Seite geprüft**, nicht
  gegen eine Vorlage. Eine CSP, die im Berichtsmodus läuft und nie
  scharf geschaltet wird, ist keine.
- Wo eine Datei aus fremder Hand ausgeliefert wird, trägt **die Antwort**
  eine eigene, engere Richtlinie.

## Container

| Regel | Folge bei Verstoß |
| --- | --- |
| Nicht als `root` laufen | Blocker |
| Minimales Basisabbild, auf eine Fassung festgenagelt | Muss |
| `no-new-privileges`, unnötige Fähigkeiten entfernt | Muss |
| Dateisystem so weit wie möglich nur lesbar | Sollte |
| Aufbau aus Sperrdateien, reproduzierbar | Muss |
| Gesundheitsprüfung vorhanden | Muss |
| Keine Secrets in Build-Argumenten oder Zwischenschichten | Blocker |
| Keine Entwicklungswerkzeuge im Produktionsabbild | Muss |

**Konsolenbefehle nie als `root` ausführen** — oder danach die
Dateirechte richtigstellen. Sonst gehören erzeugte Dateien dem falschen
Benutzer und die Anwendung kann nicht mehr schreiben (belegt an NEO
Uptime und am Contao-Standardprompt).

## Netz

- **Nur veröffentlichen, was von außen erreichbar sein muss.**
  Datenbanken, Warteschlangen und Arbeiter veröffentlichen keinen Port.
- Interne Dienste erreichen einander über das interne Netz, nicht über
  die öffentliche Adresse.
- Wo ein Pfad besonders abgeschottet ist, gilt eine **Positivliste für
  ausgehende Verbindungen**.
- Verwaltungsoberflächen laufen auf einem eigenen Zugang und nicht unter
  dem erwartbaren Standardpfad.
- **Zeitüberschreitungen sind überall gesetzt.** Ein Aufruf ohne Frist
  hängt irgendwann für immer und wird zum Ausfall.

## Ratenbegrenzung

- Global, nicht umgehbar, **nach der Authentifizierung** — die
  Aufteilung kommt aus den Ansprüchen des Aufrufers, nie aus Query- oder
  Routenwerten (Skill `neo-api`).
- Getrennte Grenzen für externe Aufrufer, angemeldete
  Oberflächensitzungen und Testkonten.
- Anmeldeversuche werden gesondert begrenzt, je Konto und je Herkunft.
- Gesundheitsendpoints sind ausgenommen.
